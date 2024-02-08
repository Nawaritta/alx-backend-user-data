#!/usr/bin/env python3
"""This module contains hash_password function"""

import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """validates that the provided password matches the hashed password."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
