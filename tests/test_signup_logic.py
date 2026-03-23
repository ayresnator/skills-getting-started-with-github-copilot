from fastapi.testclient import TestClient
import pytest

from src.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_signup_new_participant(client):
    """Test successful signup of a new participant."""
    email = "newstudent@mergington.edu"
    activity = "Chess Club"

    response = client.post(f"/activities/{activity}/signup?email={email}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}

    # Verify participant was added
    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity]["participants"]


def test_signup_duplicate_participant_returns_400(client):
    """Test that signing up a duplicate participant returns 400."""
    email = "michael@mergington.edu"  # Already in Chess Club
    activity = "Chess Club"

    response = client.post(f"/activities/{activity}/signup?email={email}")

    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up"}


def test_signup_activity_full_returns_400(client):
    """Test that signing up for a full activity returns 400."""
    activity = "Chess Club"
    # Fill the activity
    for i in range(10):  # Chess Club has max 12, already has 2, so add 10 more
        email = f"test{i}@mergington.edu"
        client.post(f"/activities/{activity}/signup?email={email}")

    # Try to add one more
    response = client.post(f"/activities/{activity}/signup?email=overflow@mergington.edu")

    assert response.status_code == 400
    assert response.json() == {"detail": "Activity is full"}


def test_signup_nonexistent_activity_returns_404(client):
    """Test that signing up for a nonexistent activity returns 404."""
    email = "test@mergington.edu"
    activity = "Nonexistent Activity"

    response = client.post(f"/activities/{activity}/signup?email={email}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}