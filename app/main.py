from flask import Flask, jsonify
import os


app = Flask(__name__)


ENV = os.getenv("APP_ENV", "dev")


@app.route("/")
def health():
    return jsonify({"status": "ok", "env": ENV}), 200


@app.route("/hello")
def hello():
    return jsonify({"message": "Hello from CI/CD pipeline"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
