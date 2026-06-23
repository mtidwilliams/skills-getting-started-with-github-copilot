from copy import deepcopy
from urllib.parse import quote

import pytest
from fastapi.testclient import TestClient

import src.app as app_module
from src.app import app


@pytest.fixture(autouse=True)
def reset_activities_state():
    original_activities = deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(original_activities)


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def _activity_action_path(activity_name: str, action: str) -> str:
    encoded_activity_name = quote(activity_name, safe="")
    return f"/activities/{encoded_activity_name}/{action}"


@pytest.fixture
def signup_request(client):
    def _signup(activity_name: str, email: str):
        return client.post(
            _activity_action_path(activity_name, "signup"),
            params={"email": email},
        )

    return _signup


@pytest.fixture
def remove_request(client):
    def _remove(activity_name: str, email: str):
        return client.delete(
            _activity_action_path(activity_name, "remove"),
            params={"email": email},
        )

    return _remove
