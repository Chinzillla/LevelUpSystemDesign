from flask import Blueprint, jsonify, request
import sqlite3
from db import get_connection

item_bp = Blueprint('items', __name__, url_prefix='/items')

@item_bp.route('/create', methods=[''])

@item_bp.route('/list', methods=[''])

@item_bp.route('/update', methods=[''])

@item_bp.route('/delete', methods=[''])
