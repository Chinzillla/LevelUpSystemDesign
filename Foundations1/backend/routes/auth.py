import sqlite3
from flask import Blueprint, jsonify, request
from db import get_connection

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "error": "Email and password are required"
        }), 400
    
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, password)
        )

        connection.commit()
        user_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        return jsonify({
            "error": "Email already exists"
        }), 409
    finally:
        connection.close()

    return jsonify({
        "message": "You are registered!",
        "id": user_id,
        "email": email
    }), 201