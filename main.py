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

# 👇 Then, read ENV
ENV = os.getenv("ENV", "development")  # default to development if missing

# 👇 THEN, create app based on ENV
if ENV == "production":
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
else:
    app = FastAPI(
        title="Hospital Management System API",
        version="3.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )

# Include routers with /api prefix
app.include_router(users.router, prefix="/api")
app.include_router(doctors.router, prefix="/api")
app.include_router(patients.router, prefix="/api")
app.include_router(appointments.router, prefix="/api")
app.include_router(auth.router, prefix="/api")

# Enable CORS (allow all origins for now)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change this to specific frontend domains!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Function to create default admin if it doesn't exist
def create_default_admin():
    db: Session = SessionLocal()
    try:
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
    finally:
        db.close()

# Create admin on app startup
create_default_admin()

# Root endpoint
@app.get("/")
def root():
    return {"message": "🏥 Hospital Management System API is running 🚀"}
