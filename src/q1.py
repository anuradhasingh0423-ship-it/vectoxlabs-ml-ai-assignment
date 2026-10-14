
from collections import Counter

documents = [
    {"id": "D101", "quality": 0.92, "time": 101},
    {"id": "D102", "quality": 0.43, "time": 102},
    {"id": "D103", "quality": 0.81, "time": 103},
    {"id": "D101", "quality": 0.92, "time": 104},
    {"id": "D104", "quality": 0.28, "time": 105},
    {"id": "D105", "quality": 0.74, "time": 105},
    {"id": "D102", "quality": 0.92, "time": 106}
]


def process_documents(documents):
    # Keep the latest record for each document ID
    unique_documents = {}

    for document in documents:
        doc_id = document["id"]

        if (
            doc_id not in unique_documents
            or document["time"] > unique_documents[doc_id]["time"]
        ):
            unique_documents[doc_id] = document

    # Classify each unique document
    category_counts = Counter()
    results = []

    for document in unique_documents.values():
        quality = document["quality"]

        if quality >= 0.80:
            category = "ACCEPT"
        elif quality >= 0.50:
            category = "REVIEW"
        else:
            category = "RETAKE"

        category_counts[category] += 1

        results.append({
            "id": document["id"],
            "quality": quality,
            "time": document["time"],
            "category": category
        })

    average_quality = (
        sum(doc["quality"] for doc in results) / len(results)
        if results else 0.0
    )

    return {
        "unique_documents": results,
        "average_quality": average_quality,
        "category_counts": {
            category: category_counts[category]
            for category in ["ACCEPT", "REVIEW", "RETAKE"]
        }
    }


if __name__ == "__main__":
    output = process_documents(documents)

    print("Unique Documents:")
    for document in output["unique_documents"]:
        print(document)

    print(f"\nAverage Quality: {output['average_quality']:.3f}")
    print("Category Counts:", output["category_counts"])
