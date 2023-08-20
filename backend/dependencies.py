from typing import Generator

from backend.database.configuration import SessionLocal


def get_db() -> Generator[SessionLocal, None, None]:
    """
    Get a database session for the current request.

        Returns:
            Generator[SessionLocal, None, None]: A generator yielding a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
