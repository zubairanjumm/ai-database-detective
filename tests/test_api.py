from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_investigate_endpoint():
    response = client.post(
        "/investigate",
        json={
            "question": "What is the total revenue for each order status?"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["question"] == (
        "What is the total revenue for each order status?"
    )

    assert "DATABASE INVESTIGATION REPORT" in data["report"]
    assert "3130.0" in data["report"]