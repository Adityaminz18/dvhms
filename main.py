import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
from routers import patients, doctors, appointments, auth, users
from dotenv import load_dotenv
import models
from auth import hash_password

load_dotenv()

ENV = os.getenv("ENV")

if ENV == "production":
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
else:
    app = FastAPI()

# Include routers
app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(appointments.router)
app.include_router(users.router)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

# 🚀 Create default admin user if not exists
def create_default_admin():
    db: Session = SessionLocal()
    admin_username = "admin"
    admin_password = "admin"
    
    existing_admin = db.query(models.User).filter(models.User.username == admin_username).first()
    
    if not existing_admin:
        hashed_pw = hash_password(admin_password)
        admin_user = models.User(
            username=admin_username,
            password_hash=hashed_pw,
            role="admin"
        )
        db.add(admin_user)
        db.commit()
        print("✅ Default admin user created: admin/admin")
    else:
        print("✅ Admin user already exists.")
    
    db.close()

create_default_admin()  # Call it when app starts!

@app.get("/")
def root():
    return {"message": "Hospital Management System API is running 🚀"}
