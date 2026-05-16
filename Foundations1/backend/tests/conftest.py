import importlib
import sys
import pytest
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

@pytest.fixture()
def client(tmp_path, monkeypatch):
    test_database = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_NAME", str(test_database))
    monkeypatch.setenv("SALT", "4az")

    for module_name in ["app", "db", "routes.auth", "routes.health", "routes.items"]:
        sys.modules.pop(module_name, None)

    app_module = importlib.import_module("app")
    app_module.app.config.update(TESTING=True)

    with app_module.app.test_client() as test_client:
        yield test_client

@pytest.fixture()
def mock_user(client):
    email = "test@example.com"
    password = "hellothere!"

    response = client.post("/auth/register", json ={
        "email": email,
        "password": password
    })

    assert response.status_code == 201

    return {
        "email": email,
        "password": password
    }

@pytest.fixture()
def auth_headers(client, mock_user):
    login_response = client.post("/auth/login", json={
        "email": mock_user["email"],
        "password": mock_user["password"]
    })

    token = login_response.get_json()["session_token"]

    return {
        "Authorization": f"Bearer {token}"
    }

@pytest.fixture()
def create_item(client, auth_headers):
    def _create_item(name="name"):
        response = client.post("/items/create",
            json={"name": name},
            headers=auth_headers
        )

        data = response.get_json()

        return {
            "name": data["name"],
            "bearer_token": auth_headers
        }

    return _create_item