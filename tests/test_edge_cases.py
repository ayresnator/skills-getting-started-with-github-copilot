from fastapi.testclient import TestClient
import pytest

from src.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_multiple_signups_and_removals(client):
    """Test multiple signups and removals in sequence."""
    activity = "Programming Class"
    emails = ["test1@mergington.edu", "test2@mergington.edu", "test3@mergington.edu"]

    # Sign up all
    for email in emails:
        response = client.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 200

    # Verify all added
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity]["participants"]
    for email in emails:
        assert email in participants

    # Remove all
    for email in emails:
        response = client.delete(f"/activities/{activity}/participants?email={email}")
        assert response.status_code == 200

    # Verify all removed
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity]["participants"]
    for email in emails:
        assert email not in participants


def test_email_case_sensitivity(client):
    """Test that email case sensitivity is handled correctly."""
    email1 = "test@mergington.edu"
    email2 = "TEST@mergington.edu"
    activity = "Gym Class"

    # Sign up with lowercase
    response = client.post(f"/activities/{activity}/signup?email={email1}")
    assert response.status_code == 200

    # Try to sign up with uppercase (should be treated as different)
    response = client.post(f"/activities/{activity}/signup?email={email2}")
    assert response.status_code == 200  # Assuming no case sensitivity check

    # Verify both are in participants
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity]["participants"]
    assert email1 in participants
    assert email2 in participants


def test_empty_email_handling(client):
    """Test handling of empty email."""
    activity = "Chess Club"

    response = client.post(f"/activities/{activity}/signup?email=")

    # This might pass or fail depending on implementation, but should not crash
    assert response.status_code in [200, 400, 422]  # 422 for validation error


def test_activity_name_with_spaces(client):
    """Test activity names with spaces are handled correctly."""
    email = "test@mergington.edu"
    activity = "Programming Class"  # Has space

    response = client.post(f"/activities/{activity}/signup?email={email}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}

    # Verify
    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity]["participants"]