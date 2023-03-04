from flask import Flask, jsonify, Response
from prisma import Prisma
import bcrypt
import jwt

app = Flask(__name__)

@app.route("/api/ping", methods=["GET"])
def ping():
    return "pong"

@app.route("/api/register", methods=["POST"])
def register():
    return "registering you..."

@app.route("/api/login", methods=["POST"])
def login():
    return "logging you in..."

if __name__ == "__main__":
    app.run(port=8888, debug=True)
