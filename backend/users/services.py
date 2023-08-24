from sqlalchemy.orm import Session
from pydantic import EmailStr

from .. import models
from .schemas import UserIn, UserInDB, UserOut
from ..utils.security import get_password_hash


def get_user_by_email(db: Session, email: EmailStr) -> UserInDB | None:
    """
    Retrieve a user by their email address.

        Parameters:
            db (Session): The database session.
            email (EmailStr): The email address of the user to retrieve.

        Returns:
            UserInDB | None: The retrieved user if found, otherwise None.
        """
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> UserInDB | None:
    """
    Retrieve a user by their identifier.

    Parameters:
        db (Session): The database session.
        user_id (int): The identifier of the user to retrieve.

    Returns:
        UserInDB | None: The retrieved user if found, otherwise None.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: UserIn) -> UserOut:
    """
    Create a new user.

        Parameters:
            db (Session): The database session.
            user (UserIn): User input data including email and password.

        Returns:
            UserOut: The created user.
    """
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
