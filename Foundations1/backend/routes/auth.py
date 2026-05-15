import sqlite3
from flask import Blueprint, jsonify, request
from db import get_connection
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()
SALT = os.environ.get("SALT")

if not SALT:
    raise RuntimeError("SALT environment variable must be set")

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json() or {}

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    email = data.get("email")
    password = data.get("password")

    if not is_valid_email(email):
        return jsonify({"error": "Valid email format is required"}), 400

    email = email.strip()

    password_error = validate_password(password)
    if password_error:
        return jsonify({"error": password_error}), 400
    
    hashed_password = hash_password(password)

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, hashed_password)
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

@auth_bp.route("/login", methods=['POST'])
def login_user():
    data = request.get_json() or {}

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    email = data.get("email")
    password = data.get("password")

    if not is_valid_email(email):
        return jsonify({"error": "Valid email format is required"}), 400

    email = email.strip()

    password_error = validate_password(password)
    if password_error:
        return jsonify({"error": password_error}), 400
    
    hashed_password = hash_password(password)

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT password FROM users WHERE email = ?",
            (email,)
        )
        user = cursor.fetchone()
        if user is None:
            return jsonify({"error": "Invalid email or password"}), 401

        stored_password_hash = user["password"]
        if hash_password(password) != stored_password_hash:
            return jsonify({"error": "Invalid email or password"}), 401
        
        return jsonify({
            "message": "Login successful",
            "email": email
        }), 200

    except sqlite3.IntegrityError:
        return jsonify({
            "error": "Email already exists"
        }), 409

    finally:
        connection.close()

#Helpers
def is_valid_email(email):
    """
    Basic validatation for registration email.

    Returns:
        Boolean
    """
    if not isinstance(email, str):
        return False

    if not email:
        return False

    email = email.strip()
    email_parts = email.split("@")

    if len(email_parts) != 2:
        return False

    local_part, domain_part = email_parts

    if not local_part or not domain_part:
        return False

    if "." not in domain_part:
        return False

    return True

def validate_password(password):
    """
    Basic validatation for registration password.

    Returns:
        str | None: An error message when invalid, otherwise None.
    """
    if not isinstance(password, str):
        return "Valid Password is required"

    if not password:
        return "Valid Password is required"

    if len(password) < 8:
        return "Password must be at least 8 characters"

    if len(password) > 128:
        return "Password must be 128 characters or fewer"

    if any(ord(char) < 32 or ord(char) > 126 for char in password):
        return "Password contains invalid characters"

    return None

def hash_password(password):
    salted_password = password + SALT
    hashed = hashlib.sha256(salted_password.encode())
    return hashed.hexdigest()