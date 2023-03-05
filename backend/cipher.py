import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def gen_fernet_key(raw_password):
    password = bytes(raw_password, encoding="utf8")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b"",
        iterations=480000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password))
