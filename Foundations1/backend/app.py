from flask import Flask
from flask_cors import CORS

# DB init
from db import init_db

# API Routes
from routes.health import health_bp
from routes.auth import auth_bp

# Helpers
from helper.app import register_routes

app = Flask(__name__)
CORS(app, origins=["http://"])

init_db()

register_routes(app, health_bp, auth_bp)

if __name__ == '__main__':
    app.run()
