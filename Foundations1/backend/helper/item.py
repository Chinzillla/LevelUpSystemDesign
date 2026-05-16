def validate_item(data):
    if not isinstance(data, dict):
        return None, ("Request body must be a JSON object", 400)
    
    item_name = data.get("name")

    if not item_name:
        return None, ("Item name is required", 400)

    if not isinstance(item_name, str):
        return None, ("Valid item name format is required", 400)
    
    return {"name": item_name}, None