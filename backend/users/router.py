from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.users import services
from backend.users.exceptions import EmailAlreadyRegistered
from .schemas import UserIn, UserOut
from ..dependencies import get_db
from ..utils import responses


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post(
    "/",
    summary="Create user",
    description=
    """
    <h1>Creates a new user with the provided information:</h1>
    
    email: User's unregistered email address.
    password: User's password that must meet the following criteria:
        - eight characters,
        - one uppercase letter,
        - one lowercase letter,
        - one number
    """,
    response_model=UserOut,
    responses={
        status.HTTP_201_CREATED: {
            "description": "User created successfully",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Invalid email address or password",
        },
        EmailAlreadyRegistered.STATUS_CODE: {
            "description": "Already registered email address",
            **responses.build_example_response(EmailAlreadyRegistered.DETAIL)
        },
    },
    response_description="User created successfully",
    status_code=status.HTTP_201_CREATED
)
async def create_user(user: UserIn, db: Session = Depends(get_db)):
    """
    Creates a new user and adds it to the database if the email is not already registered.

        Parameters:
            user (UserIn): Input data for creating the user.
            db (Session): Database session. Defaults to Depends(get_db).

        Raises:
            EmailAlreadyRegistered: If the email is already registered.

        Returns:
            UserOut: Information about the created user.
    """
    db_user = services.get_user_by_email(db, user.email)
    if db_user:
        raise EmailAlreadyRegistered()

    return services.create_user(db, user)
