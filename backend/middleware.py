from flask import request, jsonify
import json

from errors import json_error
from tokens import check_token

# Closure to ensure that there is a JSON request body and that it contains
# the desired properties, passed in the *args.
# Sets the field "parsed_body" on the request if successful.
def check_body_data(*args):
    def check_body_inner(func):
        def verify(request):
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
            return func(request)

        return verify
    return check_body_inner


# Closure to check the Authorization header. Sets the field "user_id" on the request
# if successful.
def check_token_header(func):
    def verify(request):

        auth_header = request.headers.get("Authorization")
        if auth_header == None:
            return json_error({"error": "No token set."}, 401)

        token = auth_header.replace("Bearer ", "")

        try:
            valid, user_id = check_token(token)
        except:
            return json_error({"error": "Invalid token."}, 401)

        if not valid:
            return json_error({"error": "Invalid token."}, 401)

        # the token was valid!
        try:
            from prisma import Prisma
            prisma = Prisma()
            user = prisma.user.find_first(where={ 
                "id": int(user_id)
            })

            if user == None:
                raise Exception("could not find user")
        except:
            return json_error({"error": "Invalid token"}, 401)

        request.user = user
        return func(request)

    return verify