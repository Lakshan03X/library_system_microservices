from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from routes import router

load_dotenv()

app = FastAPI(
    title="Reservation Service",
    description="Microservice for managing book reservations in the library system",
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
    return {"message": "Reservation Service", "status": "running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}