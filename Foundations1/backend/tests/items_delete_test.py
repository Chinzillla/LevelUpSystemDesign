def test_delete_item_successfully(client, auth_headers):
    response = client.delete("/items/delete",
        json={"name": "Study caching"},
        headers=auth_headers
    )

    data = response.get_json()

    assert response.status_code == 200
    assert data["message"] == "Item deleted"
    assert data["id"]
    assert data["name"] == "Study caching"

# def test_delete_item_invalid_token(client):

# def test_delete_item_missing_token(client):

# def test_delete_item_requires_name(client, auth_headers):

# def test_delete_item_incorrect_data_type(client, auth_headers):

# def test_delete_item_not_json(client, auth_headers):