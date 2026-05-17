def test_health_route(client):
    response = client.get("/health/")

    assert response.status_code == 200
    assert response.get_json() == {"Health": "I am healthy, Thanks for asking!"}

def test_local_frontend_origin_is_allowed(client):
    response = client.get("/health/", headers={
        "Origin": "http://127.0.0.1:5500"
    })

    assert response.status_code == 200
    assert response.headers["Access-Control-Allow-Origin"] == "http://127.0.0.1:5500"
