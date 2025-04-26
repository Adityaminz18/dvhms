from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database
from auth import admin_required
from models import User

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.UserOut])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)  # Only Admin can access
):
    users = db.query(models.User).all()
    return users
