from src.q1 import process_documents

def test_duplicate_ids_keep_latest_record():
    docs = [
        {"id": "D1", "quality": 0.30, "time": 1},
        {"id": "D1", "quality": 0.90, "time": 2},
    ]

    result = process_documents(docs)

    assert len(result["unique_documents"]) == 1
    assert result["unique_documents"][0]["quality"] == 0.90


def test_quality_categories():
    docs = [
        {"id": "D1", "quality": 0.80, "time": 1},
        {"id": "D2", "quality": 0.50, "time": 2},
        {"id": "D3", "quality": 0.49, "time": 3},
    ]

    result = process_documents(docs)

    assert result["category_counts"] == {
        "ACCEPT": 1,
        "REVIEW": 1,
        "RETAKE": 1,
    }


def test_empty_input():
    result = process_documents([])

    assert result["unique_documents"] == []
    assert result["average_quality"] == 0.0


def test_equal_timestamps_keep_first_record():
    docs = [
        {"id": "D1", "quality": 0.70, "time": 5},
        {"id": "D1", "quality": 0.90, "time": 5},
    ]

    result = process_documents(docs)

    assert result["unique_documents"][0]["quality"] == 0.70
