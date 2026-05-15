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