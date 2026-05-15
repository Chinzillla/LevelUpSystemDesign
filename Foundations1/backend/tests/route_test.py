def test_register_route_exists(client):
    response = client.post("/auth/register", json = {
        "email": "abcd@example.com",
        "password": "hellowhyareyouhere?"
    })

    assert response.status_code == 201

def test_emptydata_register_route(client):
    no_email_response = client.post("/auth/register", json = {
        "email": "",
        "password" : ""
    })

    no_password_response = client.post("/auth/register", json = {
        "email": "test@gmail.com",
        "password": ""
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