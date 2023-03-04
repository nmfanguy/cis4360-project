import bcrypt
from prisma import Base64

from tokens import gen_token
from errors import json_error
from middleware import *
from db import prisma

@check_body_data("username", "password")
def handle_register(request):
    existing_users = prisma.user.find_first(
        where={
            "username": request.parsed_body["username"],
        }
    )

    if existing_users != None:
        return json_error({"error": "username is taken"}, 400)
    
    encoded_pw = bytes(request.parsed_body["password"], encoding="utf8")
    hashed_pw = bcrypt.hashpw(encoded_pw, bcrypt.gensalt())

    new_user = prisma.user.create(data={
        "username": request.parsed_body["username"],
        "password": Base64.encode(hashed_pw)
    })

    token = gen_token(new_user.id)

    return jsonify({
        "token": token
    })

@check_body_data("username", "password")
def handle_login(request):
    user = prisma.user.find_first(
        where={
            "username": request.parsed_body["username"],
        }
    )

    if user == None:
        return json_error({"error": "username not found"}, 400)
    
    encoded_pw = bytes(request.parsed_body["password"], encoding="utf8")
    bytes_db_pw = Base64.decode(user.password)
    if not bcrypt.checkpw(encoded_pw, bytes_db_pw):
        return json_error({"error": "incorrect password"}, 400)

    token = gen_token(user.id)

    return jsonify({
        "token": token
    })
