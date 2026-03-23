from fastapi.testclient import TestClient
import pytest

from src.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_remove_participant_success(client):
    """Test successful removal of a participant."""
    email = "michael@mergington.edu"
    activity = "Chess Club"

    response = client.delete(f"/activities/{activity}/participants?email={email}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity}"}

    # Verify participant was removed
    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity]["participants"]


def test_remove_nonexistent_participant_returns_404(client):
    """Test that removing a nonexistent participant returns 404."""
    email = "nonexistent@mergington.edu"
    activity = "Chess Club"

    response = client.delete(f"/activities/{activity}/participants?email={email}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found"}


def test_remove_from_nonexistent_activity_returns_404(client):
    """Test that removing from a nonexistent activity returns 404."""
    email = "test@mergington.edu"
    activity = "Nonexistent Activity"

    response = client.delete(f"/activities/{activity}/participants?email={email}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}