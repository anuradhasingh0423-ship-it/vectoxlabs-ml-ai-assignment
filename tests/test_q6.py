
import pytest

from src.q6_knowledge_base import KnowledgeBaseChatbot


@pytest.fixture
def chatbot():
    documents = [
        {
            "project": "Alpha",
            "document": "alpha.txt",
            "text": "Project Alpha uses Python for backend development.",
        },
        {
            "project": "Beta",
            "document": "beta.txt",
            "text": "Project Beta uses Java for backend development.",
        },
        {
            "project": "Alpha",
            "document": "database.txt",
            "text": "Project Alpha stores information in PostgreSQL.",
        },
    ]
    return KnowledgeBaseChatbot(
        documents, similarity_threshold=0.10
    )


import pytest


def test_relevant_answer_has_citation(chatbot):
    result = chatbot.answer(
        "Which language does Alpha use?",
        "user1",
        ["Alpha"],
    )

    assert result["status"] == "answered"
    assert result["citations"]
    assert all(
        citation["project"] == "Alpha"
        for citation in result["citations"]
    )


def test_unauthorized_project_is_not_retrieved(chatbot):
    result = chatbot.answer(
        "Which language does Beta use?",
        "user1",
        ["Alpha"],
    )

    assert result["status"] == "insufficient_information"
    assert result["citations"] == []
    assert "Java" not in result["answer"]


def test_authorized_project_can_be_retrieved(chatbot):
    result = chatbot.answer(
        "Which language does Beta use?",
        "user1",
        ["Beta"],
    )

    assert result["status"] == "answered"
    assert "Java" in result["answer"]


def test_missing_information_is_flagged(chatbot):
    result = chatbot.answer(
        "What is the project's office address?",
        "user1",
        ["Alpha"],
    )

    assert result["status"] == "insufficient_information"
    assert result["citations"] == []


def test_history_is_separated_by_user(chatbot):
    chatbot.answer("Which language does Alpha use?", "user1", ["Alpha"])
    chatbot.answer("Which language does Beta use?", "user2", ["Beta"])

    assert len(chatbot.get_history("user1")) == 1
    assert len(chatbot.get_history("user2")) == 1
    assert "Java" not in chatbot.get_history("user1")[0]["answer"]


def test_empty_question_is_handled(chatbot):
    result = chatbot.answer("   ", "user1", ["Alpha"])

    assert result["status"] == "empty_question"


def test_no_documents_is_handled():
    chatbot = KnowledgeBaseChatbot([])

    result = chatbot.answer("Any question?", "user1", ["Alpha"])

    assert result["status"] == "no_documents"
