def test_delete_item_successfully(client, auth_headers):
    response = client.delete("/items/delete",
        json={"name": "pencil"},
        headers=auth_headers
    )

    data = response.get_json()

    assert response.status_code == 200
    assert data["message"] == "Item deleted"
    assert data["id"]
    assert data["name"] == "pencil"

def test_delete_item_missing_token(client):
    response = client.delete("/items/delete",
        json={"name": "Book"},
    )

    assert response.status_code == 401
    assert response.get_json() == {
        "error": "Authentication required"
    }

def test_delete_item_not_json(client, auth_headers):
    response = client.delete("/items/delete",
        json="test",
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Request body must be a JSON object"
    }

def test_delete_item_incorrect_data_type(client, auth_headers):
    response = client.delete("/items/delete",
        json={"name": 10},
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Valid item name format is required"
    }

def test_delete_item_requires_name(client, auth_headers):
    response = client.delete("/items/delete",
        json={"name": "  "},
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Item name is required"
    }

# def test_delete_item_invalid_token(client):


