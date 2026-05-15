from flask import Blueprint, request, jsonify
from db import get_connection

messages_bp = Blueprint('messages', __name__, url_prefix='/messages')

@messages_bp.route('/', methods=['GET'])
def get_messages():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM messages")
    messages = cursor.fetchall()
    connection.close()

    return jsonify([dict(message) for message in messages])

@messages_bp.route('/', methods=['POST'])
def create_message():
    data = request.get_json() or {}
    name = data.get('name')
    message = data.get('message')

    if not name or not message:
        return jsonify({'error': 'Name and message are required'}), 400

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO messages (name, message) VALUES (?, ?)", (name, message))
    connection.commit()
    message_id = cursor.lastrowid
    connection.close()

    return jsonify({
        'id': message_id,
        'name': name,
        'message': message
    }), 201

@messages_bp.route('/<int:message_id>/', methods=['PATCH'])
def update_message(message_id):
    data = request.get_json() or {}
    name = data.get('name')
    message = data.get('message')

    if not name or not message:
        return jsonify({'error': 'Name and message are required'}), 400

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE messages SET name = ?, message = ? WHERE id = ?",
        (name, message, message_id)
    )
    connection.commit()
    updated_count = cursor.rowcount
    connection.close()

    if updated_count == 0:
        return jsonify({'error': 'Message not found'}), 404

    return jsonify({
        'id': message_id,
        'name': name,
        'message': message
    }), 200

@messages_bp.route('/<int:message_id>/', methods=['DELETE'])
def delete_message(message_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM messages WHERE id = ?", (message_id,))
    connection.commit()
    deleted_count = cursor.rowcount
    connection.close()

    if deleted_count == 0:
        return jsonify({'error': 'Message not found'}), 404

    return jsonify({'message': 'Message deleted'}), 200