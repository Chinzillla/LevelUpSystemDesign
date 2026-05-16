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

    data = response_login.get_json()

    assert response_login.status_code == 200
    assert data["message"] == "Login successful"
    assert data["email"] == mock_user["email"]
    assert "session_token" in data

def test_login_creates_session_record(client, mock_user):
    response_login = client.post("/auth/login", json={
        "email": mock_user["email"],
        "password": mock_user["password"]
    })

    data = response_login.get_json()

    from db import get_connection

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT sessions.session_token, users.email
        FROM sessions
        JOIN users ON users.id = sessions.user_id
        WHERE sessions.session_token = ?
        """,
        (data["session_token"],)
    )

    session = cursor.fetchone()
    connection.close()

    assert session is not None
    assert session["session_token"] == data["session_token"]
    assert session["email"] == mock_user["email"]