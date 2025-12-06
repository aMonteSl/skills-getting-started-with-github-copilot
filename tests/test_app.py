from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Expect some known activity from the seed data
    assert "Chess Club" in data


def test_signup_and_reflect():
    activity = "Chess Club"
    email = "test_add_user@example.com"

    # Ensure email not present initially
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    body = resp.json()
    assert "Signed up" in body.get("message", "")

    # Verify via GET that participant appears
    resp2 = client.get("/activities")
    assert resp2.status_code == 200
    data = resp2.json()
    assert email in data[activity]["participants"]

    # Clean up
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)


def test_remove_participant_endpoint():
    activity = "Programming Class"
    email = "test_remove_user@example.com"

    # Ensure participant exists (add directly)
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)

    # Delete via endpoint
    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 200
    body = resp.json()
    assert "Removed" in body.get("message", "")

    # Verify removal
    resp2 = client.get("/activities")
    data = resp2.json()
    assert email not in data[activity]["participants"]
