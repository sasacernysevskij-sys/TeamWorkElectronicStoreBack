from flask import Blueprint, request, jsonify
from services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)
auth_service = AuthService()

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    result, status_code = auth_service.register(
        email=data.get("email"),
        password=data.get("password"),
        name=data.get("name"),
        surname=data.get("surname"),
        phone=data.get("phone", "")
    )
    return jsonify(result), status_code

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    result, status_code = auth_service.login(
        email=data.get("email"),
        password=data.get("password")
    )
    return jsonify(result), status_code