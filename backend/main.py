from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from backend.users.router import router as users_router
from backend.database.configuration import Base, engine
from backend.config import API_ENDPOINT


Base.metadata.create_all(bind=engine)

app = FastAPI(
    docs_url=f"{API_ENDPOINT}/docs",
    redoc_url=f"{API_ENDPOINT}/redocs",
    title="Users login-registration API",
    description="API for an application with a user login and registration system.",
    version="1.0",
    openapi_url=f"{API_ENDPOINT}/openapi.json"
)

origins = [
    "http://localhost:8000",
    "http://localhost:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(users_router, prefix=API_ENDPOINT)


if __name__ == "__main__":
    uvicorn.run("backend.main:app",host="localhost", port=8000, reload=True)
