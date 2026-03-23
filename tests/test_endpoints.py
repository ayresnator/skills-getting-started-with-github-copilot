from fastapi.testclient import TestClient
import pytest

from src.app import app


def test_get_root_redirects_to_static(client):
    """Test that GET / redirects to static files."""
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Mergington High School" in response.text


def test_get_activities_returns_200(client):
    """Test that GET /activities returns 200 and activity data."""
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]