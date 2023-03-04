from flask import jsonify

def json_error(data, status_code):
    res = jsonify(data)
    res.status_code = status_code
    return res