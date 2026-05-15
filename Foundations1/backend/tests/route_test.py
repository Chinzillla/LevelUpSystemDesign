from app import app

def test_register_route_exists():
    client = app.test_client()

    response = client.post("/auth/register", json = {
        "email": "abcd@example.com",
        "password": "urmum"
    })

    assert response.status_code == 201