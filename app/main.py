from flask import Flask, jsonify
from app.config import Config


app = Flask(__name__)
app.config.from_object(Config)


@app.route("/")
def health():
    return jsonify({"status": "ok", "env": app.config["ENV"]}), 200


@app.route("/hello")
def hello():
    return jsonify({"message": "Hello from CI/CD pipeline"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
