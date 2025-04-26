import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import patients, doctors, appointments, auth, users
from dotenv import load_dotenv

load_dotenv() 
# Read the environment variable
ENV = os.getenv("ENV", "development")

# Configure FastAPI app based on the environment
if ENV == "production":
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)  # Disable docs in production
else:
    app = FastAPI()  # Default to development with docs enabled

# Include routers
app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(appointments.router)
app.include_router(auth.router)
app.include_router(users.router)

# CORS setup to allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, use exact frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Hospital Management System API is running 🚀"}

