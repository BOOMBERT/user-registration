from fastapi import FastAPI

from backend.users import router as users_router
from backend.database.configuration import Base, engine


Base.metadata.create_all(bind=engine)

API_ENDPOINT = "/api/v1"

app = FastAPI(
    docs_url=f"{API_ENDPOINT}/docs",
    redoc_url=f"{API_ENDPOINT}/redocs",
    title="User registration API",
    description="API for applications with user registration.",
    version="1.0",
    openapi_url=f"{API_ENDPOINT}/openapi.json"
)

app.include_router(users_router.router, prefix=API_ENDPOINT)
