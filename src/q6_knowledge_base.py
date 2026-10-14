
import re
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class KnowledgeBaseChatbot:
    def __init__(self, documents, similarity_threshold=0.12):
        """
        Initialize the knowledge base.

        Each document must contain:
        {
            "project": "ProjectA",
            "document": "requirements.txt",
            "text": "The project uses Python."
        }
        """
        self.documents = documents
        self.similarity_threshold = similarity_threshold
        self.history = {}
        self.vectorizer = None
        self.document_vectors = None

        if documents:
            texts = [
                self._clean_text(doc["text"])
                for doc in documents
            ]

            # Handle empty documents or documents containing only
            # stop words, which can produce an empty vocabulary.
            try:
                self.vectorizer = TfidfVectorizer(
                    stop_words="english"
                )
                self.document_vectors = (
                    self.vectorizer.fit_transform(texts)
                )
            except ValueError:
                self.vectorizer = None
                self.document_vectors = None

    @staticmethod
    def _clean_text(text):
        return re.sub(r"\s+", " ", str(text)).strip()

    @staticmethod
    def _meaningful_terms(text):
        """Extract words useful for basic relevance checking."""
        stop_words = {
            "what", "is", "the", "a", "an", "does", "do",
            "which", "how", "why", "about", "tell", "me",
            "more", "please", "can", "could", "would",
            "project", "its", "their", "this", "that",
            "of", "in", "on", "for", "to", "and", "or",
            "use", "uses", "using", "tell", "show",
            "give", "find", "there", "any",
        }

        terms = set(re.findall(r"\b\w+\b", text.lower()))
        return terms - stop_words

    def _authorized_indices(self, allowed_projects):
        return [
            index
            for index, doc in enumerate(self.documents)
            if doc["project"] in allowed_projects
        ]

    def _record_history(self, user_id, question, answer):
        self.history.setdefault(user_id, []).append({
            "question": question,
            "answer": answer,
        })

    def answer(self, question, user_id, allowed_projects):
        """
        Retrieve relevant excerpts from authorized documents.

        Returns:
            {
                "answer": str,
                "citations": list,
                "status": str
            }
        """
        question = self._clean_text(question)
        allowed_projects = set(allowed_projects)

        if not question:
            return self._response(
                "Please enter a question.",
                [],
                "empty_question",
            )

        if not self.documents:
            return self._response(
                "I don't have any documents to answer this question.",
                [],
                "no_documents",
            )

        indices = self._authorized_indices(allowed_projects)

        if not indices:
            answer_text = (
                "I don't have authorized project documents "
                "to answer this question."
            )
            self._record_history(user_id, question, answer_text)

            return self._response(
                answer_text,
                [],
                "no_authorized_documents",
            )

        # Support simple follow-ups using the user's previous question.
        history = self.history.get(user_id, [])
        retrieval_question = question

        follow_up_prefixes = (
            "what about",
            "and ",
            "why",
            "how about",
            "tell me more",
            "what is its",
            "what are its",
        )

        if (
            history
            and question.lower().startswith(follow_up_prefixes)
        ):
            retrieval_question = (
                history[-1]["question"] + " " + question
            )

        # A vectorizer may be unavailable if all documents contain
        # only empty text or stop words.
        if self.vectorizer is None:
            answer_text = (
                "I couldn't find sufficient information in the "
                "authorized documents to answer this question."
            )
            self._record_history(user_id, question, answer_text)

            return self._response(
                answer_text,
                [],
                "insufficient_information",
            )

        try:
            query_vector = self.vectorizer.transform(
                [retrieval_question]
            )

            # Compare only against authorized documents.
            authorized_vectors = self.document_vectors[indices]

            scores = cosine_similarity(
                query_vector,
                authorized_vectors,
            )[0]

        except ValueError:
            return self._response(
                "I couldn't process this question. Please try rephrasing it.",
                [],
                "retrieval_error",
            )

        ranked = sorted(
            zip(indices, scores),
            key=lambda item: item[1],
            reverse=True,
        )

        if not ranked:
            return self._response(
                "No authorized documents were found.",
                [],
                "no_authorized_documents",
            )

        best_index, best_score = ranked[0]

        # Require both sufficient similarity and meaningful term overlap.
        query_terms = self._meaningful_terms(retrieval_question)

        authorized_text = " ".join(
            self.documents[index]["text"].lower()
            for index in indices
        )

        document_terms = set(
            re.findall(r"\b\w+\b", authorized_text)
        )

        matched_terms = query_terms & document_terms

        if (
            best_score < self.similarity_threshold
            or not matched_terms
        ):
            answer_text = (
                "I couldn't find sufficient information in the "
                "authorized documents to answer this question."
            )

            citations = []
            status = "insufficient_information"

        else:
            # Return the original source text rather than inventing
            # a generated answer unsupported by the documents.
            selected = [
                (index, score)
                for index, score in ranked[:3]
                if score >= self.similarity_threshold
            ]

            excerpts = []
            citations = []

            for index, score in selected:
                doc = self.documents[index]

                excerpts.append(doc["text"])

                citations.append({
                    "project": doc["project"],
                    "document": doc["document"],
                    "similarity": round(float(score), 3),
                })

            answer_text = "\n\n".join(excerpts)
            status = "answered"

        self._record_history(
            user_id,
            question,
            answer_text,
        )

        return self._response(
            answer_text,
            citations,
            status,
        )

    @staticmethod
    def _response(answer, citations, status):
        return {
            "answer": answer,
            "citations": citations,
            "status": status,
        }

    def get_history(self, user_id):
        """Return conversation history for one user."""
        return list(self.history.get(user_id, []))


def load_text_documents(folder):
    """
    Load .txt and .md files organized as:

        folder/
            ProjectA/
                requirements.txt
                overview.md
            ProjectB/
                notes.txt

    Each top-level project folder is treated as a project namespace.
    """
    folder = Path(folder)
    documents = []

    if not folder.exists() or not folder.is_dir():
        return documents

    for project_folder in folder.iterdir():
        if not project_folder.is_dir():
            continue

        for path in project_folder.rglob("*"):
            if path.suffix.lower() not in {".txt", ".md"}:
                continue

            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue

            if text.strip():
                documents.append({
                    "project": project_folder.name,
                    "document": str(path.relative_to(folder)),
                    "text": text.strip(),
                })

    return documents


if __name__ == "__main__":
    sample_documents = [
        {
            "project": "SwasthyaSetu",
            "document": "requirements.txt",
            "text": (
                "SwasthyaSetu is a healthcare support project. "
                "Its backend exposes APIs for the application."
            ),
        },
        {
            "project": "VotingSystem",
            "document": "overview.txt",
            "text": (
                "The voting system uses Python, OpenCV, "
                "and face recognition to identify registered voters."
            ),
        },
    ]

    chatbot = KnowledgeBaseChatbot(sample_documents)

    response = chatbot.answer(
        "Which technology does the voting system use?",
        user_id="demo_user",
        allowed_projects=["VotingSystem"],
    )

    print("Answer:", response["answer"])
    print("Citations:", response["citations"])
    print("Status:", response["status"])
