from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base

from routers import patients, doctors, appointments,auth


app = FastAPI()
app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(appointments.router)
app.include_router(auth.router)

# CORS setup to allow Bolt.new frontend to access backend
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

