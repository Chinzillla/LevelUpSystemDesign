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
    data = request.get_json()
    name = data.get('name')
    message = data.get('message')

    if not name or not message:
        return jsonify({'error': 'Name and message are required'}), 400

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO messages (name, message) VALUES (?, ?)", (name, message))
    connection.commit()
    connection.close()

    return jsonify({'message': 'Message created successfully'}), 201

@messages_bp.route('/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM messages WHERE id = ?", (message_id,))
    connection.commit()
    connection.close()

    return jsonify({'message': 'Message deleted'}), 200