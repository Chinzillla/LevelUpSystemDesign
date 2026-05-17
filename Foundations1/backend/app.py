from flask import Flask
from flask_cors import CORS

# DB init
from db import init_db

# API Routes
from routes.health import health_bp
from routes.auth import auth_bp
from routes.items import items_bp

# Helpers
from helper.app import register_routes

app = Flask(__name__)
CORS(app, origins=[
    "http://127.0.0.1:5500",
    "http://localhost:5500",
])

init_db()

register_routes(app, health_bp, auth_bp, items_bp)

if __name__ == '__main__':
    app.run()
