from app import app

def test_health_route():
    # Create a mock client
    client = app.test_client()

    response = client.get("/health/")

    assert response.status_code == 200
    assert response.get_json() == {"Health": "I am healthy, Thanks for asking!"}