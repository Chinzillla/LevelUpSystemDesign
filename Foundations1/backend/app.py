from flask import Flask
from flask_cors import CORS

# API Routes
from routes.health import health_bp

app = Flask(__name__)
CORS(app, origins=["http://"])

app.register_blueprint(health_bp)

if __name__ == '__main__':
    app.run()
