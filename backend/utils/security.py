from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_hashed_string(plain_string: str, hashed_string: str) -> bool:
    """
    Verifies a plain string against a string hashed by a cryptographic context.

        Parameters:
            plain_string (str): A plain string to be verified.
            hashed_string (str): A hashed string to compare against.

        Returns:
            bool: True if the string match, False otherwise.
    """
    return pwd_context.verify(plain_string, hashed_string)

def get_hashed_string(string: str) -> str:
    """
   Hashes a string using the configured cryptographic context.

       Parameters:
           string (str): The string to be hashed.

       Returns:
           str: The hashed string.
    """
    return pwd_context.hash(string)
