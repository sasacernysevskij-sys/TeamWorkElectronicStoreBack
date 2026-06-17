from functools import wraps
from flask import request, jsonify
from utils.jwt_utils import decode_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"error": "Токен отсутствует"}), 401

        user_id = decode_token(token)
        if not user_id:
            return jsonify({"error": "Токен недействителен или истёк"}), 401

        return f(user_id, *args, **kwargs)
    return decorated