from pydantic import BaseModel, EmailStr, field_validator, Field
import re


class UserBase(BaseModel):
    """
    Base class for user data.

        Parameters:
            email (EmailStr): The user's email address.
    """
    email: EmailStr = Field(..., examples=["user@example.com"])


class UserIn(UserBase):
    """
    Class representing user input data.

        Parameters:
            email (EmailStr): The user's email address (inherited from UserBase).
            password (str): The user's password.
    """
    password: str = Field(..., max_length=32, examples=["Userexamplepassword123"])

    @field_validator("password")
    def password_validator(cls, value: str) -> str | ValueError:
        """
        Validate the password format.

            Parameters:
                value (str): The password to validate.

            Raises:
                ValueError: If the password does not meet the specified requirements:
                    - At least eight characters
                    - One uppercase letter
                    - One lowercase letter
                    - One number

            Returns:
                value (str): The validated password.
        """
        PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d!@#?$%^&*]{8,}$"

        if not re.match(PASSWORD_REGEX, value):
            raise ValueError(
                "The password must consist of at least eight characters, "
                "one uppercase letter, one lowercase letter and one number"
            )

        return value


class UserOut(UserBase):
    """
    Class representing user output data.

        Parameters:
            email (EmailStr): The user's email address (inherited from UserBase).
            id (int): The user's unique identifier.
    """
    id: int = Field(..., examples=[1])


class UserInDB(UserBase):
    """
    Class representing user data stored in the database.

        Parameters:
            email (EmailStr): The user's email address (inherited from UserBase).
            id (int): The user's unique identifier.
            hashed_password (str): Hashed user password.
    """
    id: int = Field(..., examples=[1])
    hashed_password: str = Field(..., examples=["Userexamplehashedpassword123"])
