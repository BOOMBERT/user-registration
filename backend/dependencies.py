from typing import Generator
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from os import getenv
from jose import jwt, JWTError

from backend.users.services import get_user_by_id
from backend.config import API_ENDPOINT
from backend.database.configuration import SessionLocal
from backend.authentication.exceptions import InvalidCredentials
from backend.users.schemas import UserInDB


def get_db() -> Generator[SessionLocal, None, None]:
    """
    Database session to communicate with the database.

        Returns:
            Generator[SessionLocal, None, None]: A generator yielding a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_bearer = OAuth2PasswordBearer(tokenUrl=f"{API_ENDPOINT}/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_bearer)) -> UserInDB:
    """
    Get the currently authenticated user based on the provided JWT token.

        Parameters:
            db (Session): The database session.
            token (str): JWT token obtained from the authentication header.

        Raises:
            InvalidCredentials:
                If the provided token is invalid, lacks a valid user ID, or
                if the user with the extracted ID is not found in the database.

        Returns:
            user (UserInDB): The Information of the current user from database.
    """
    try:
        payload = jwt.decode(token, getenv("SECRET_KEY"), algorithms=[getenv("ALGORITHM")])
        user_id = payload.get("sub")
        if user_id is None:
            raise InvalidCredentials

    except JWTError:
        raise InvalidCredentials

    user = get_user_by_id(db, int(user_id))

    if user is None:
        raise InvalidCredentials
    return user
