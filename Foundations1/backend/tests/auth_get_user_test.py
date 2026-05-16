def test_me_rejects_missing_token(client):
    response = client.get("/auth/me")

    assert response.status_code == 401
    assert response.get_json() == {
        "error": "Authentication required"
    }

def test_me_rejects_invalid_token(client):
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer fake-token"}
    )

    assert response.status_code == 401
    assert response.get_json() == {
        "error": "Invalid session"
    }

def test_me_returns_logged_in_user(client, mock_user):
    login_response = client.post("/auth/login", json={
        "email": mock_user["email"],
        "password": mock_user["password"]
    })

    token = login_response.get_json()["session_token"]

    me_response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    data = me_response.get_json()

    assert me_response.status_code == 200
    assert data["email"] == mock_user["email"]