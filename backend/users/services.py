from sqlalchemy.orm import Session
from pydantic import EmailStr

from .. import models
from .schemas import UserIn, UserInDB, UserOut
from ..utils.security import get_hashed_string


def get_user_by_email(db: Session, email: EmailStr) -> UserInDB | None:
    """
    Retrieves a user by his email address.

        Parameters:
            db (Session): A database session.
            email (EmailStr): An email address of the user to retrieve.

        Returns:
            UserInDB | None: The retrieved user if found, otherwise None.
        """
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> UserInDB | None:
    """
    Retrieves a user by his identifier.

    Parameters:
        db (Session): A database session.
        user_id (int): An identifier of the user to retrieve.

    Returns:
        UserInDB | None: The retrieved user if found, otherwise None.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: UserIn) -> UserOut:
    """
    Creates a new user.

        Parameters:
            db (Session): A database session.
            user (UserIn): User input data including email and password.

        Returns:
            UserOut: Main information about the created user.
    """
    hashed_password = get_hashed_string(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def hash_and_save_refresh_token_in_db(db: Session, user_id: int, refresh_token: str) -> UserOut:
    """
    Saves a hashed user refresh token in the database.

        Parameters:
            db (Session): A database session.
            user_id (int): An identifier of the user whose refresh token we want to save in the database.
            refresh_token (str): User refresh token that we want to save in the database.

        Returns:
            UserOut: Main information about the user whose refresh token we have saved in the database.
    """
    db_user = get_user_by_id(db, user_id)
    db_user.hashed_refresh_token = get_hashed_string(refresh_token)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
