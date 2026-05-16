import sqlite3
from flask import Blueprint, jsonify, request
from db import get_connection
import secrets
from helper.auth import is_valid_email, validate_password, hash_password, get_bearer_token

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

        user_id = cursor.lastrowid
        connection.commit()

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

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT id, password FROM users WHERE email = ?",
            (email,)
        )
        user = cursor.fetchone()
        if user is None:
            return jsonify({"error": "Invalid email or password"}), 401

        stored_password_hash = user["password"]
        if hash_password(password) != stored_password_hash:
            return jsonify({"error": "Invalid email or password"}), 401
        
        session_token = secrets.token_urlsafe(32)
        
        cursor.execute(
            "INSERT INTO sessions (session_token, user_id, created_at) VALUES (?, ?, datetime('now'))" ,
            (session_token, user["id"])
        )

        connection.commit()

        return jsonify({
            "message": "Login successful",
            "email": email,
            "session_token": session_token
        }), 200

    except sqlite3.IntegrityError:
        return jsonify({
            "error": "Email already exists"
        }), 409

    finally:
        connection.close()

@auth_bp.route("/me", methods=['GET'])
def get_current_user():
    session_token = get_bearer_token(request.headers.get("Authorization"))

    if session_token is None:
        return jsonify({"error": "Authentication required"}), 401

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT users.id, users.email
            FROM sessions
            JOIN users ON users.id = sessions.user_id
            WHERE sessions.session_token = ?
            """,
            (session_token,)
        )

        user = cursor.fetchone()

        if user is None:
            return jsonify({"error": "Invalid session"}), 401

        return jsonify({
            "id": user["id"],
            "email": user["email"]
        }), 200

    finally:
        connection.close()

@auth_bp.route("/logout", methods=['POST'])
def logout_user():
    session_token = get_bearer_token(request.headers.get("Authorization"))

    if session_token is None:
        return jsonify({"error": "Authentication required"}), 401

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM sessions
            WHERE session_token = ?
            """,
            (session_token,)
        )

        if cursor.rowcount == 0:
            return jsonify({"error": "Invalid session"}), 401

        connection.commit()
        
        return jsonify({"message": "Logout successful"}), 200
    
    finally:
        connection.close()