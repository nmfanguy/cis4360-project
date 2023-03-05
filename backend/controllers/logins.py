from flask import jsonify
from prisma import Base64
from middleware import *
from db import prisma
from cryptography.fernet import Fernet
from cipher import gen_fernet_key

@check_token_header
def get_all(request):
    user = request.user
    all_services = [{"service": login.service, "id": login.id} for login in user.logins]
    return jsonify({ "logins": all_services }) 

@check_body_data("accountPassword", "username", "password", "service")
@check_token_header
def create_login(request):
    fernet_key, salt = gen_fernet_key(request.parsed_body["accountPassword"])
    cipher = Fernet(fernet_key)

    encrypted_username = cipher.encrypt(bytes(request.parsed_body["username"], encoding="utf8"))
    encrypted_password = cipher.encrypt(bytes(request.parsed_body["password"], encoding="utf8"))

    prisma.login.create(data={
        'userId': request.user.id,
        'username': Base64.encode(encrypted_username),
        'password': Base64.encode(encrypted_password),
        'service': request.parsed_body["service"],
        "salt": Base64.encode(salt),
    })

    return jsonify({"message": "success"})

@check_body_data("accountPassword")
@check_token_header
def get_single(request, id):
    user = request.user
    matching_service = list(filter(lambda l: l.id == id, user.logins))

    if len(matching_service) != 1:
        return json_error({"error": "could not find that login"}, 404)

    matching_service = matching_service[0]

    salt = Base64.decode(matching_service.salt)
    fernet_key, _salt = gen_fernet_key(request.parsed_body["accountPassword"], salt)
    cipher = Fernet(fernet_key)

    raw_username = Base64.decode(matching_service.username)
    raw_password = Base64.decode(matching_service.password)

    decrypted_username = str(cipher.decrypt(raw_username), encoding="utf8")
    decrypted_password = str(cipher.decrypt(raw_password), encoding="utf8")
    
    return jsonify({"login": {
            "service": matching_service.service,
            "id": matching_service.id,
            "username": decrypted_username,
            "password": decrypted_password,
        }
    })

@check_token_header
def delete_login(request, id):
    user = request.user

    matching_service = list(filter(lambda l: l.id == id, user.logins))

    if len(matching_service) != 1:
        return json_error({"error": "could not find that login"}, 404)

    matching_service = matching_service[0]

    try:
        prisma.login.delete(where={"id": id})
    except Exception as e:
        return json_error({"error": str(e)}, 500)
    
    return jsonify({"message": "success"})
