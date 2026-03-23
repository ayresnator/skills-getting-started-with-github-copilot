import pytest
from fastapi.testclient import TestClient
from copy import deepcopy

from src.app import app, activities


@pytest.fixture
def client():
    """Arrange: Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Arrange: Reset activities to original state before each test."""
    original_activities = deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_activities)