from flask import Blueprint, jsonify, request
import sqlite3
from db import get_connection
from helper.auth import get_bearer_token
from helper.items import validate_item

items_bp = Blueprint('items', __name__, url_prefix='/items')

@items_bp.route('/create', methods=['POST'])
def create_item():
    data = request.get_json() or {}
    session_token = get_bearer_token(request.headers.get("Authorization"))

    if session_token is None:
        return jsonify({"error": "Authentication required"}), 401

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT user_id FROM sessions WHERE session_token = ?",
            (session_token,)
        )

        session = cursor.fetchone()

        if session is None:
            return jsonify({"error": "Invalid session"}), 401

        item_data, error = validate_item(data)

        if error:
            message, status_code = error
            return jsonify({"error": message}), status_code

        user_id = session["user_id"]

        cursor.execute(
            """
            INSERT INTO items (user_id, name, created_at) 
            VALUES (?, ?, datetime('now'))
            """,
            (user_id, item_data["name"])
        )
        connection.commit()
        item_id = cursor.lastrowid

        cursor.execute(
            "SELECT created_at FROM items WHERE id = ?",
            (item_id,)
        )

        created_at = cursor.fetchone()["created_at"]

        return jsonify({
            "message": "Item created",
            "id": item_id,
            "name": item_data["name"],
            "completed": False,
            "created_at": created_at
            }), 201

    finally:
        connection.close()

@items_bp.route('/list', methods=['GET'])
def list_items():
    session_token = get_bearer_token(request.headers.get("Authorization"))

    if session_token is None:
        return jsonify({"error": "Authentication required"}), 401
    
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT user_id FROM sessions WHERE session_token = ?",
            (session_token,)
        )

        session = cursor.fetchone()
        if session is None:
            return jsonify({"error": "Invalid session"}), 401
        
        user_id = session["user_id"]

        cursor.execute(
            "SELECT id, name, completed, created_at FROM items WHERE user_id = ?",
            (user_id,)
        )

        items = [
            {
                "id": row["id"],
                "name": row["name"],
                "completed": row["completed"],
                "created_at": row["created_at"]
            }
            for row in cursor.fetchall()
        ]

        return jsonify({
            "message": "Successfully retrieved items list",
            "items": items
        }), 200

    finally:
        connection.close()

@items_bp.route('/update', methods=['PUT'])
def update_item():
    data = request.get_json() or {}
    session_token = get_bearer_token(request.headers.get("Authorization"))

    if session_token is None:
        return jsonify({"error": "Authentication required"}), 401

    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT user_id FROM sessions WHERE session_token = ?",
            (session_token,)
        )
        session = cursor.fetchone()
        if session is None:
            return jsonify({"error": "Invalid session"}), 401

        user_id = session["user_id"]

        name = data.get("name")
        new_name = data.get("new_name")
        completed = data.get("completed")

        if not name:
            return jsonify({"error": "Item name is required"}), 400

        updates = []
        params = []
        if new_name is not None:
            updates.append("name = ?")
            params.append(new_name.strip())
        if completed is not None:
            updates.append("completed = ?")
            params.append(1 if completed else 0)

        if not updates:
            return jsonify({"error": "No update fields provided"}), 400

        params.extend([user_id, name])

        cursor.execute(
            f"UPDATE items SET {', '.join(updates)} WHERE user_id = ? AND name = ?",
            tuple(params)
        )

        if cursor.rowcount == 0:
            return jsonify({"error": "Item not found"}), 404

        connection.commit()

        cursor.execute(
            "SELECT name, completed FROM items WHERE user_id = ? AND name = ?",
            (user_id, new_name if new_name else name)
        )
        updated = cursor.fetchone()
        return jsonify({
            "message": "Item updated",
            "name": updated["name"],
            "completed": bool(updated["completed"])
        }), 200

    finally:
        connection.close()

@items_bp.route('/delete', methods=['DELETE'])
def delete_item():
    data = request.get_json() or {}
    session_token = get_bearer_token(request.headers.get("Authorization"))

    if session_token is None:
        return jsonify({"error": "Authentication required"}), 401
    
    item_data, error = validate_item(data)

    if error:
        message, status_code = error
        return jsonify({"error": message}), status_code

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT user_id FROM sessions WHERE session_token = ?",
            (session_token,)
        )

        session = cursor.fetchone()

        if session is None:
            return jsonify({"error": "Invalid session"}), 401
        
        user_id = session["user_id"]

        cursor.execute(
            "DELETE FROM items WHERE user_id = ? AND name = ?",
            (user_id, item_data["name"],)
        )

        if cursor.rowcount == 0:
            return jsonify({"error": "Item not found"}), 404

        connection.commit()
    
        return jsonify({
            "message": "Item deleted",
            "name": item_data["name"]
        }), 200
    finally:
        connection.close()
    
