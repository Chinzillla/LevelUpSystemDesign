from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app, origins=["http://127.0.0.1:5500"])

@app.route('/')
def hello_world():
    return jsonify({
        'message': 'Hello, World!'
    })

if __name__ == '__main__':
    app.run()
