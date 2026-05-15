import sqlite3
from flask import Blueprint, jsonify, request
from db import get_connection

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json() or {}

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    email = data.get("email").strip()
    password = data.get("password")

    if not is_valid_email(email):
        return jsonify({"error": "Valid email format is required"}), 400

    if not password:
        return jsonify({"error": "Valid Password is required"}), 400
    
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


#Helper
def is_valid_email(email):
    if not isinstance(email, str):
        return False

    email = email.strip()

    if not email:
        return False

    email_parts = email.split("@")

    if len(email_parts) != 2:
        return False

    local_part, domain_part = email_parts

    if not local_part or not domain_part:
        return False

    if "." not in domain_part:
        return False

    return True