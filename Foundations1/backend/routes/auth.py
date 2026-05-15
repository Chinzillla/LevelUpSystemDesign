from flask import Blueprint, jsonify, request

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

    return jsonify({
        "message": "You are registered!",
        "id": "1",
        "email": email
    }), 201