import importlib
import sys
from pathlib import Path

import pytest


BACKEND_DIR = Path(__file__).resolve().parents[1]


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE", str(tmp_path / "test.db"))

    if str(BACKEND_DIR) not in sys.path:
        sys.path.insert(0, str(BACKEND_DIR))

    for module_name in ["app", "db", "routes", "routes.messages"]:
        sys.modules.pop(module_name, None)

    app_module = importlib.import_module("app")
    app_module.app.config.update(TESTING=True)

    with app_module.app.test_client() as test_client:
        yield test_client


def test_message_crud_flow(client):
    response = client.get("/messages/")
    assert response.status_code == 200
    assert response.get_json() == []

    response = client.post("/messages/", json={"name": "Ada", "message": "Hello"})
    assert response.status_code == 201

    created_message = response.get_json()
    assert created_message["id"]
    assert created_message["name"] == "Ada"
    assert created_message["message"] == "Hello"

    response = client.get("/messages/")
    assert response.status_code == 200
    assert response.get_json() == [created_message]

    response = client.patch(
        f"/messages/{created_message['id']}/",
        json={"name": "Ada Lovelace", "message": "Updated"},
    )
    assert response.status_code == 200

    updated_message = response.get_json()
    assert updated_message == {
        "id": created_message["id"],
        "name": "Ada Lovelace",
        "message": "Updated",
    }

    response = client.get("/messages/")
    assert response.status_code == 200
    assert response.get_json() == [updated_message]

    response = client.delete(f"/messages/{created_message['id']}/")
    assert response.status_code == 200
    assert response.get_json() == {"message": "Message deleted"}

    response = client.get("/messages/")
    assert response.status_code == 200
    assert response.get_json() == []


def test_message_validation_and_missing_records(client):
    response = client.post("/messages/", json={"name": "", "message": "Missing name"})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Name and message are required"}

    response = client.patch("/messages/999/", json={"name": "Nobody", "message": "Missing"})
    assert response.status_code == 404
    assert response.get_json() == {"error": "Message not found"}

    response = client.delete("/messages/999/")
    assert response.status_code == 404
    assert response.get_json() == {"error": "Message not found"}