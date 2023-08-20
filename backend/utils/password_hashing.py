from passlib.context import CryptContext
from pydantic import SecretStr


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: SecretStr, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

        Parameters:
            plain_password (SecretStr): The plain password to be verified.
            hashed_password (str): The hashed password to compare against.

        Returns:
            bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(
        plain_password.get_secret_value(), hashed_password
    )

def get_password_hash(password: SecretStr) -> str:
    """
   Hash a password using the configured cryptographic context.

       Parameters:
           password (SecretStr): The password to be hashed.

       Returns:
           str: The hashed password.
    """
    return pwd_context.hash(password.get_secret_value())
