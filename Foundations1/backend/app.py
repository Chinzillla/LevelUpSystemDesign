from flask import Flask
from flask_cors import CORS

# API Routes
app.register_blueprint(health_bp)

app = Flask(__name__)
CORS(app, origins=["http://"])

if __name__ == '__main__':
    app.run()
