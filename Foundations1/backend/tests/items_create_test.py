def test_create_item_rejects_missing_token(client):
    response = client.post("/items/create", json={
        "name": "Study caching"
    })

    assert response.status_code == 401
    assert response.get_json() == {
        "error": "Authentication required"
    }

def test_create_item_returns_created_item(client, auth_headers):
    response = client.post(
        "/items/create",
        json={"name": "Study caching"},
        headers=auth_headers
    )

    data = response.get_json()

    assert response.status_code == 201
    assert data["message"] == "Item created"
    assert data["id"]
    assert data["name"] == "Study caching"
    assert data["completed"] is False

def test_create_item_rejects_invalid_token(client):
    response = client.post(
        "/items/create",
        json={"name": "Study caching"},
        headers={"Authorization": "Bearer fake-token"}
    )

    assert response.status_code == 401
    assert response.get_json() == {
        "error": "Invalid session"
    }

def test_create_item_requires_name(client, auth_headers):
    response = client.post(
        "/items/create",
        json={},
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Item name is required"
    }

def test_create_item_rejects_non_object_json(client, auth_headers):
    response = client.post(
        "/items/create",
        json=["Study caching"],
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Request body must be a JSON object"
    }