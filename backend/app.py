from flask import Flask, jsonify, Response, request
from dotenv import load_dotenv

load_dotenv()

import controllers.auth
from db import prisma

app = Flask(__name__)

@app.route("/api/ping", methods=["GET"])
def ping():
    return "pong"

@app.route("/api/register", methods=["POST"])
def register():
    return controllers.auth.handle_register(request)

@app.route("/api/login", methods=["POST"])
def login():
    return controllers.auth.handle_login(request)

if __name__ == "__main__":
    app.run(port=8888, debug=True)
    prisma.disconnect()
