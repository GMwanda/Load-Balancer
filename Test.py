from flask import Flask
import os

app = Flask(__name__)


@app.route('/home', methods=['GET'])
def home():
    server_id = os.environ.get('SERVER_ID', 'Unknown')
    return f"Hello from Server: {server_id}"


@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return 'Hello', 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
