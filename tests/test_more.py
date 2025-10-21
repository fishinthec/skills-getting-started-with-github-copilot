from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_signup_unknown_activity():
    resp = client.post("/activities/NoSuchActivity/signup?email=someone@example.com")
    assert resp.status_code == 404


def test_added_activities_present():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    expected = [
        "Soccer Club",
        "Swimming Team",
        "Art Club",
        "Theater Workshop",
        "Math Olympiad",
        "Science Bowl",
    ]
    for name in expected:
        assert name in data
