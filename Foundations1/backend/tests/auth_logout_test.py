def test_logout_deletes_session(client, mock_user):
    login_response = client.post("/auth/login", json={
        "email": mock_user["email"],
        "password": mock_user["password"]
    })

    token = login_response.get_json()["session_token"]

    logout_response = client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )

    me_response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert logout_response.status_code == 200
    assert logout_response.get_json() == {
        "message": "Logout successful"
    }

    assert me_response.status_code == 401
    assert me_response.get_json() == {
        "error": "Invalid session"
    }

def test_logout_rejects_missing_token(client):
    response = client.post("/auth/logout")

    assert response.status_code == 401
    assert response.get_json() == {
        "error": "Authentication required"
    }


def test_logout_rejects_invalid_token(client):
    response = client.post(
        "/auth/logout",
        headers={"Authorization": "Bearer fake-token"}
    )

    assert response.status_code == 401
    assert response.get_json() == {
        "error": "Invalid session"
    }