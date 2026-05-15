import pytest
from app import app

@pytest.fixture()
def client():
    app.config.update(TESTING=True)

    with app.test_client() as test_client:
        yield test_client

def test_register_route_exists(client):
    response = client.post("/auth/register", json = {
        "email": "abcd@example.com",
        "password": "hellowhyareyouhere?"
    })

    assert response.status_code == 201

def test_emptydata_register_route(client):
    response = client.post("/auth/register", json = {
        "email": "",
        "password" : ""
    })

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Email and password are required"
    }

def test_register_returns_user(client):
    response = client.post("/auth/register", json={
        "email": "noob@example.com",
        "password": "dontstealmypasswordpls"
    })

    data = response.get_json()
    assert data["id"]
    assert data["email"] == "noob@example.com"

# def test_register_existing_user(client):
#     response = cl