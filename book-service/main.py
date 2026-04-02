from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routes import router
from db import DB_MODE, connection_error

load_dotenv()

app = FastAPI(
    title="Book Service",
    description="Microservice for managing books in the library system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Book Service", "status": "running", "db_mode": DB_MODE}


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "db_mode": DB_MODE,
        "db_error": connection_error
    }