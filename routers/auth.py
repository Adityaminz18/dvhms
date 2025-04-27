from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from auth import hash_password, verify_password, create_access_token,admin_required
import models, schemas, database
from models import User
from schemas import UserLogin


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", response_model=schemas.UserOut)
def signup(
    user: schemas.UserCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(admin_required)  # Only Admin can access
):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_pw = hash_password(user.password)
    new_user = models.User(username=user.username, password_hash=hashed_pw, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
async def login(
    request: Request,
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(None)
):
    if request.headers.get('Content-Type', '').startswith('application/json'):
        # Handle JSON login
        body = await request.json()
        username = body.get('username')
        password = body.get('password')
    else:
        # Handle form-data login
        form = await request.form()
        username = form.get('username')
        password = form.get('password')

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password required.")

    user = db.query(models.User).filter(models.User.username == username).first()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
        "role": user.role
    }