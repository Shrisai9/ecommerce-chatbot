# backend/routes/auth_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from models.user import User
from database import db

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/auth")


# ──────────────── REGISTER ────────────────
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify(msg="Username and password required"), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify(msg="Username already exists"), 400

    user = User(username=data["username"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    return jsonify(msg="User registered successfully"), 201


# ──────────────── LOGIN ────────────────
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify(msg="Username and password required"), 400

    user = User.query.filter_by(username=data["username"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify(msg="Invalid credentials"), 401

    # 🔑 FIX: convert user.id to string
    access_token = create_access_token(identity=str(user.id))

    return jsonify(token=access_token, user=user.to_dict()), 200


# ──────────────── CURRENT USER ────────────────
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    uid = get_jwt_identity()
    user = User.query.get_or_404(uid)
    return jsonify(user=user.to_dict())
