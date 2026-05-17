def test_list_items_successfully(client,  create_item):
    item_data = create_item(["book", "pen", "pencil"])
    auth_header = item_data[0]["bearer_token"]

    response = client.get("/items/list", 
            headers=auth_header
        )
    
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Successfully retrieved items list"
    assert len(data["items"]) == 3

    expected_names = [item["name"] for item in item_data]
    returned_names = [item["name"] for item in data["items"]]
    assert returned_names == expected_names

    for item in data["items"]:
        assert isinstance(item["created_at"], str)

def test_list_item_invalid_session(client):
    response = client.get("/items/list", 
        headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response.status_code == 401
    assert response.get_json() == {
        "error": "Invalid session"
        }

def test_list_item_no_auth(client):
    response = client.get("/items/list")
    assert response.status_code == 401
    assert response.get_json() == {
        "error": "Authentication required"
        }
