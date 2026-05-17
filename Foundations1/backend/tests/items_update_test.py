def test_update_item_successfully(client, create_item):
    item = create_item(["book"])
    auth_header = item[0]["bearer_token"]
    response = client.put("/items/update",
        json={"name": "book", "new_name": "notebook", "completed": True},
        headers=auth_header
    )

    data = response.get_json()
    
    assert response.status_code == 200
    assert data["message"] == "Item updated"
    assert data["name"] == "notebook"
    assert data["completed"] is True

def test_update_item_not_found(client, create_item):
    item = create_item("book")
    auth_header = item[0]["bearer_token"]

    response = client.put("/items/update",
        json={"name": "doesnotexist", "new_name": "something"},
        headers=auth_header
    )
    assert response.status_code == 404
    assert response.get_json() == {"error": "Item not found"}

def test_update_item_no_auth(client):
    response = client.put("/items/update",
        json={"name": "book", "new_name": "notebook"}
    )
    assert response.status_code == 401
    assert response.get_json() == {"error": "Authentication required"}

def test_update_item_invalid_token(client):
    response = client.put("/items/update",
        json={"name": "book", "new_name": "notebook"},
        headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response.status_code == 401
    assert response.get_json() == {"error": "Invalid session"}

def test_update_item_invalid_data(client, create_item):
    item = create_item("book")
    auth_header = item[0]["bearer_token"]

    response = client.put("/items/update",
        json={"new_name": "notebook"},
        headers=auth_header
    )
    assert response.status_code == 400
    assert "error" in response.get_json()