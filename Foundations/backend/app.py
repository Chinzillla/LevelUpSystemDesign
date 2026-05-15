from flask import Flask
from flask_cors import CORS
from db import init_db
from routes.messages import messages_bp

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5500"])

init_db()

app.register_blueprint(messages_bp)

if __name__ == '__main__':
    app.run()
