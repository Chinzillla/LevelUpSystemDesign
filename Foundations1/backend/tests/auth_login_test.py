import pytest

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

def test_login_rejects_nonexistent_email(client):
    response = client.post("/auth/login", json = {
        "email": "iamnotindb@gmail.com",
        "password": "thisispassword"
    })

    assert response.status_code == 401
    assert response.get_json() == {
        "error": "Invalid email or password"
    }

def test_login_rejects_wrong_password(client, mock_user):
    response_login = client.post("/auth/login", json = {
        "email": mock_user["email"],
        "password":"wrong_password"
    })

    assert response_login.status_code == 401
    assert response_login.get_json() == {
        "error": "Invalid email or password"
    }

def test_login_correct_password(client, mock_user):
    response_login = client.post("/auth/login", json = {
        "email": mock_user["email"],
        "password": mock_user["password"]
    })

    assert response_login.status_code == 200
    assert response_login.get_json() == {
            "message": "Login successful",
            "email": mock_user["email"]
    }