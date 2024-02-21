#!/usr/bin/env python3
"""This module contains flask app"""

from flask import Flask, jsonify, request, abort
from auth import Auth
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def home() -> str:
    """home page"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """return a JSON payload if the user exists"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """user login"""
    email = request.form.get("email")
    password = request.form.get("password")

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response

    return abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """user logout"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is not None:
        AUTH.destroy_session(user.id)
        return redirect('/')
    abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """user logout"""
    try:
        session_id = request.cookies.get('session_id')
        user = AUTH.get_user_from_session_id(session_id)
        if user is None:
            abort(403)
        response = jsonify({"email": user.email})
        return response, 200

    except Exception:
        abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """rest password"""
    email = request.form.get("email")
    try:
        new_token = AUTH.get_reset_password_token(email)
    except Exception:
        abort(403)
    response = jsonify({"email": email, "reset_token": new_token})
    return response, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
