from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_signup_unknown_activity_returns_404():
    r = client.post("/activities/NoSuchActivity/signup?email=x@y.com")
    assert r.status_code == 404


def test_activities_added_present():
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    for expected in ["Soccer Team", "Track and Field", "Art Club", "Drama Club", "Science Club", "Debate Team"]:
        assert expected in data
