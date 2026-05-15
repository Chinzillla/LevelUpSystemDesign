from flask import Blueprint, jsonify, request

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")

    return jsonify({
        "message": "You are registered!",
        "email": email
    }), 201