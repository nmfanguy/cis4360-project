import base64

def gen_fernet_key(raw_password):
    bytes_pw = bytes(raw_password, encoding="utf8")
    idx = 0
    out_pw = []

    while len(out_pw) < 32:
        out_pw.append(bytes_pw[idx])
        idx = (idx + 1) % len(bytes_pw)

    return base64.encodebytes(bytes(out_pw))
