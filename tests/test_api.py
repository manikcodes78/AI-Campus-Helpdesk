
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_get_faqs():
    response = client.get("/faqs/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_tickets():
    response = client.get("/tickets/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)



def test_search_faqs():
    response = client.get(
        "/faqs/search",
        params={"keyword": "library"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)



def test_search_tickets():
    response = client.get(
        "/tickets/search",
        params={"keyword": "library"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_dashboard_stats():
    response = client.get("/dashboard/stats")

    assert response.status_code == 200

    data = response.json()

    assert "total_faqs" in data
    assert "total_tickets" in data
    assert "open_tickets" in data
    assert "resolved_tickets" in data



def test_search_faqs_rejects_short_keyword():
    response = client.get(
        "/faqs/search",
        params={"keyword": "a"}
    )

    assert response.status_code == 422
