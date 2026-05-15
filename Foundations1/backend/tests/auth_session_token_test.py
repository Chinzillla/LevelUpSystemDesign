import pytest

@pytest.fixture()
def mock_user(client):
    email = "test@example.com"
    password = "hellothere!"

    response_reg = client.post("/auth/register", json ={
        "email": email,
        "password": password
    })

    assert response_reg.status_code == 201

    response_login = client.post("/auth/login", json = {
        "email" : email,
        "password": password
    })

    assert response_login.status_code == 200

    return {
        "email": email,
        "password": password
    }
