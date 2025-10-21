from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Check a known activity exists
    assert "Chess Club" in data


def test_signup_success_and_duplicate_and_capacity():
    activity_name = "Test Capacity Club"
    # create a temporary activity for testing
    activities[activity_name] = {
        "description": "Temp activity",
        "schedule": "Now",
        "max_participants": 2,
        "participants": []
    }

    # successful signup
    resp = client.post(f"/activities/{activity_name}/signup?email=test1@example.com")
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # duplicate signup (case/whitespace insensitive)
    resp = client.post(f"/activities/{activity_name}/signup?email= Test1@Example.com ")
    assert resp.status_code == 400
    assert resp.json().get("detail") == "Student is already signed up"

    # second unique signup
    resp = client.post(f"/activities/{activity_name}/signup?email=test2@example.com")
    assert resp.status_code == 200

    # capacity reached
    resp = client.post(f"/activities/{activity_name}/signup?email=test3@example.com")
    assert resp.status_code == 400
    assert resp.json().get("detail") == "Activity is full"

    # cleanup
    del activities[activity_name]


def test_unregister_participant():
    activity_name = "Unregister Club"
    activities[activity_name] = {
        "description": "Temp activity",
        "schedule": "Now",
        "max_participants": 5,
        "participants": ["a@b.com", "c@d.com"]
    }

    # successful unregister
    resp = client.delete(f"/activities/{activity_name}/participants?email=a@b.com")
    assert resp.status_code == 200
    assert "Unregistered" in resp.json().get("message", "")
    assert "a@b.com" not in activities[activity_name]["participants"]

    # unregister non-existent
    resp = client.delete(f"/activities/{activity_name}/participants?email=notfound@example.com")
    assert resp.status_code == 404

    # cleanup
    del activities[activity_name]
