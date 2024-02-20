#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User
from typing import Dict, Union


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """saves the user to the database"""
        new_user = User(email=email, hashed_password=hashed_password)
        DBSession = self._session
        DBSession.add(new_user)
        DBSession.commit()
        return new_user

    def find_user_by(self, **kwa: Union[str, int]) -> User:
        """returns the first row found in the users table as filtered
        by the method's input arguments"""

        DBSession = self._session
        try:
            user = DBSession.query(User).filter_by(**kwa).first()
            if user is None:
                raise NoResultFound
            return user
        except NoResultFound:
            raise
        except InvalidRequestError:
            raise

    def update_user(self, user_id: int, **kwa: Union[str, int]) -> None:
        """updates a user"""

        DBSession = self._session
        user_to_update = self.find_user_by(id=user_id)
        for key, value in kwa.items():
            if not hasattr(user_to_update, key):
                raise ValueError
            setattr(user_to_update, key, value)

        DBSession.commit()
