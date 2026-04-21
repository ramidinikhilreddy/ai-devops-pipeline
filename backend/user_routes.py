from flask import Blueprint, jsonify, request

from backend.services.user_service import register_user

user_bp = Blueprint("user_bp", __name__)


@user_bp.route("/register", methods=["POST"])
def register():
    """
    Handle user registration requests.
    """
    data = request.get_json(silent=True) or {}
    result = register_user(data)
    return jsonify(result["body"]), result["status"]