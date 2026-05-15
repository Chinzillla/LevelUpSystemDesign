def test_health_route(client):
    response = client.get("/health/")

    assert response.status_code == 200
    assert response.get_json() == {"Health": "I am healthy, Thanks for asking!"}