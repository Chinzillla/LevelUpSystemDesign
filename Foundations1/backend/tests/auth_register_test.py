def test_register_route_exists(client):
    response = client.post("/auth/register", json = {
        "email": "abcd@example.com",
        "password": "hellowhyareyouhere?"
    })

    assert response.status_code == 201

def test_missing_data_register_route(client):
    no_email_response = client.post("/auth/register", json = {
        "password" : "213142131"
    })

    no_password_response = client.post("/auth/register", json = {
        "email": "test@gmail.com",
    })

    assert no_email_response.status_code == 400
    assert no_email_response.get_json() == {
        "error": "Valid email format is required"
    }
    
    assert no_password_response.status_code == 400
    assert no_password_response.get_json() == {
        "error": "Valid Password is required"
    }

def test_register_returns_user(client):
    response = client.post("/auth/register", json={
        "email": "noob@example.com",
        "password": "dontstealmypasswordpls"
    })

    data = response.get_json()
    assert data["id"]
    assert data["email"] == "noob@example.com"

def test_register_existing_user(client):
    first_response = client.post("/auth/register", json={
        "email": "noob1@example.com",
        "password": "dontstealmypasswordpls"
    })

    second_response = client.post("/auth/register", json={
        "email": "noob1@example.com",
        "password": "dontstealmypasswordpls"
    })

    assert first_response.status_code == 201
    assert second_response.status_code == 409

def test_register_incorrect_email(client):
    response = client.post("/auth/register", json={
        "email": "notanemail",
        "password": "dontstealmypasswordpls"
    })

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Valid email format is required"
    }

def test_register_requires_email_when_whitespace(client):
    response = client.post("/auth/register", json={
        "email": "   ",
        "password": "password123"
    })

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Valid email format is required"
    }

def test_register_rejects_email_with_only_at_symbol(client):
    response = client.post("/auth/register", json={
        "email": "@",
        "password": "password123"
    })

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Valid email format is required"
    }

def test_register_rejects_non_object_json(client):
    response = client.post("/auth/register", json=["email", "password"])

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Request body must be a JSON object"
    }

def test_register_rejects_non_string_password(client):
    response = client.post("/auth/register", json={
        "email": "numberpassword@example.com",
        "password": 12345678
    })

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Valid Password is required"
    }


def test_register_rejects_short_password(client):
    response = client.post("/auth/register", json={
        "email": "shortpassword@example.com",
        "password": "short"
    })

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Password must be at least 8 characters"
    }


def test_register_rejects_password_longer_than_128_characters(client):
    response = client.post("/auth/register", json={
        "email": "longpassword@example.com",
        "password": "a" * 129
    })

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Password must be 128 characters or fewer"
    }


def test_register_accepts_password_with_128_characters(client):
    response = client.post("/auth/register", json={
        "email": "maxpassword@example.com",
        "password": "a" * 128
    })

    assert response.status_code == 201


def test_register_rejects_password_with_non_ascii_character(client):
    response = client.post("/auth/register", json={
        "email": "unicodepassword@example.com",
        "password": "passwordé123"
    })

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Password contains invalid characters"
    }


def test_register_accepts_password_with_printable_special_characters(client):
    response = client.post("/auth/register", json={
        "email": "specialpassword@example.com",
        "password": "Pass word!123#$"
    })

    assert response.status_code == 201

def test_register_does_not_store_plain_text_password(client):
    plain_password = "password123"

    response = client.post("/auth/register", json={
        "email": "hashed@example.com",
        "password": plain_password
    })

    assert response.status_code == 201

    from db import get_connection

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE email = ?",
        ("hashed@example.com",)
    )

    user = cursor.fetchone()
    connection.close()

    assert user is not None
    assert user["password"] != plain_password