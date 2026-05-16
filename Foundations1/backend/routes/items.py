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

        return jsonify({
            "message": "Item created",
            "id": item_id,
            "name": item_data["name"],
            "completed": False
            }), 201

    finally:
        connection.close()

# @items_bp.route('/list', methods=[''])

# @items_bp.route('/update', methods=[''])

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
    
