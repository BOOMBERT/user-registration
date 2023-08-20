from pydantic import BaseModel, EmailStr, SecretStr, field_validator, Field
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
            password (SecretStr): The user's password.
    """
    password: SecretStr = Field(..., max_length=32, examples=["Userexamplepassword123"])

    @field_validator("password")
    def password_validator(cls, value: SecretStr) -> SecretStr | ValueError:
        """
        Validate the password format.

            Parameters:
                value (SecretStr): The password to validate.

            Raises:
                ValueError: If the password does not meet the specified requirements:
                    - At least eight characters
                    - One uppercase letter
                    - One lowercase letter
                    - One number

            Returns:
                value (SecretStr): The validated password.
        """
        PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d!@#?$%^&*]{8,}$"

        if not re.match(PASSWORD_REGEX, value.get_secret_value()):
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
    """
    pass


class UserInDB(UserBase):
    """
    Class representing user data stored in the database.

        Parameters:
            email (EmailStr): The user's email address (inherited from UserBase).
            hashed_password (SecretStr): Hashed user password.
    """
    hashed_password: SecretStr = Field(..., examples=["Userexamplehashedpassword123"])
