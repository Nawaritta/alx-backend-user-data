#!/usr/bin/env python3
""" Authentication module """

import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User
import uuid
from typing import Union


def _hash_password(password: str) -> bytes:
    """ takes in a password string arguments and returns bytes """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """ Returns a string representation of a new UUID."""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """constructor"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ register user """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """ Try locating the user by email """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'),
                              user.hashed_password)

    def create_session(self, email: str) -> str:
        """returns the session ID as a string"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """returns the corresponding User or None."""
        if session_id is not None:
            user = self._db.find_user_by(session_id=session_id)
            if user is not None:
                return user
        return None

    def destroy_session(self, user_id: int) -> None:
        """updates the corresponding user's session ID to None."""
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """takes an email string argument and returns a string."""

        if email is not None:
            user = self._db.find_user_by(email=email)
            if user is None:
                raise ValueError()
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)

            return new_token

    def update_password(self, reset_token: str, password: str) -> None:
        """ updates the password """
        user = self._db.find_user_by(reset_token=reset_token)
        if user is None:
            raise ValueError()
        hashed_password = _hash_password(password)
        self._db.update_user(user.id, reset_token=None)
        self._db.update_user(user.id, hashed_password=hashed_password)
