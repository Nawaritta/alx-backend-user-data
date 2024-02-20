#!/usr/bin/env python3
""" Authentication module """

import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """ takes in a password string arguments and returns bytes """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


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

    def _generate_uuid() -> str:
        """ Returns a string representation of a new UUID."""
        return str(uuid.uuid4())
