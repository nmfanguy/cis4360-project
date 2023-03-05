from flask import request, jsonify
import json

from errors import json_error
from tokens import check_token
from db import prisma

# Closure to ensure that there is a JSON request body and that it contains
# the desired properties, passed in the *args.
# Sets the field "parsed_body" on the request if successful.
def check_body_data(*args):
    def check_body_inner(func):
        def verify(*args2):
            try:
                # try to parse the message body
                body = request.get_json()

                # and check every property exists
                for property in args:
                    if property not in body:
                        return json_error({
                                "error"f"Invalid Form: missing '{property}'"
                            }, 400)

            except json.JSONDecodeError:
                return json_error({"error": "Could not decode form."}, 400)

            # finally, return the result of the function
            request.parsed_body = body
            return func(*args2)

        return verify
    return check_body_inner


# Closure to check the Authorization header. Sets the field "user_id" on the request
# if successful.
def check_token_header(func):
    def verify(*args):
        auth_header = request.headers.get("Authorization")
        if auth_header == None:
            return json_error({"error": "No token set."}, 401)

        token = auth_header.replace("Bearer ", "")

        try:
            valid, user_id = check_token(token)
        except:
            return json_error({"error": "Invalid token."}, 401)

        if not valid:
            print(f"check token ({token}) was false")
            return json_error({"error": "Invalid token."}, 401)

        # the token was valid!
        try:
            user = prisma.user.find_first(where={ 
                "id": int(user_id)
            }, include={
                "logins": True,
            })

            if user == None:
                raise Exception("could not find user")
        except Exception as e:
            print(f"error: {e}")
            return json_error({"error": "Invalid token"}, 401)

        request.user = user
        return func(*args)

    return verify