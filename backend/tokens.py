import jwt
import datetime
import os

SECRET = os.environ.get("JWT_SECRET")

def gen_token(user_id):
    """Create a new token that encodes the User ID and expires in 30 days."""
    if SECRET == None:
        raise Exception("JWT_SECRET environment variable not set. Create a .env file and define the variable there.")

    return jwt.encode(
        {
            "id" : user_id,
            "exp" : datetime.datetime.utcnow() + datetime.timedelta(days=30) 
        }, 
        SECRET, 
        algorithm = "HS256"
    )

def check_token(token):
    """Check if the token is valid, returning (valid, user_id)."""
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return (True, payload["id"])
    except:
        return (False, None)