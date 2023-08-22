from fastapi import FastAPI

from backend.users.router import router as users_router
from backend.authentication.router import router as auth_router
from backend.database.configuration import Base, engine
from backend.config import API_ENDPOINT


Base.metadata.create_all(bind=engine)

app = FastAPI(
    docs_url=f"{API_ENDPOINT}/docs",
    redoc_url=f"{API_ENDPOINT}/redocs",
    title="User login-registration API",
    description="API for an application with a user login and registration system.",
    version="1.0",
    openapi_url=f"{API_ENDPOINT}/openapi.json"
)

app.include_router(users_router, prefix=API_ENDPOINT)
app.include_router(auth_router, prefix=API_ENDPOINT)
