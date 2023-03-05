from flask import Flask, jsonify, Response, request
from dotenv import load_dotenv

load_dotenv()

import controllers.auth
import controllers.logins
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

@app.route("/api/logins", methods=["GET", "POST"])
def all_logins_route():
    if request.method == "GET":
        return controllers.logins.get_all(request)
    elif request.method == "POST":
        return controllers.logins.create_login(request)

@app.route("/api/logins/<int:id>", methods=["DELETE", "POST"])
def single_login_route(id):
    if request.method == "POST":
        return controllers.logins.get_single(request, id)
    elif request.method == "DELETE":
        return controllers.logins.delete_login(request, id)

if __name__ == "__main__":
    app.run(port=8888, debug=True)
    prisma.disconnect()
