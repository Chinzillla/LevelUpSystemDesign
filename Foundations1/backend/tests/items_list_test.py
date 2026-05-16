# user doesnt exist
def test_get_all_items_successfully(client,  create_item):
    item_data = create_item(["book", "pen", "pencil"])
    auth_header = item_data[0]["bearer_token"]

    response = client.get("/items/list", 
            headers=auth_header
        )
    
    response.status_code == 200
    response.get_json == {
        "messsage": "Successfully retrieved items list"
    }

# invalid session

# Authorization required

# Invalid request
