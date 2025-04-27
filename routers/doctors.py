from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud, database
from auth import get_current_user, admin_required  # Import admin_required
from models import User  # Import the User model

router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.DoctorOut)
def create_doctor(
    doctor: schemas.DoctorCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(admin_required)  # Admin-only access
):
    return crud.create_doctor(db, doctor)

@router.get("/", response_model=list[schemas.DoctorOut])
def list_doctors(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # Accessible to all authenticated users
):
    return crud.get_doctors(db, skip, limit)

@router.get("/{doctor_id}", response_model=schemas.DoctorOut)
def get_doctor(
    doctor_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(admin_required)  # Accessible to all authenticated users
):
    doctor = crud.get_doctor(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@router.put("/{doctor_id}", response_model=schemas.DoctorOut)
def update_doctor(
    doctor_id: int, 
    doctor: schemas.DoctorCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(admin_required)  # Admin-only access
):
    db_doctor = crud.update_doctor(db, doctor_id, doctor)
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return db_doctor

@router.delete("/{doctor_id}")
def delete_doctor(
    doctor_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(admin_required)  # Admin-only access
):
    db_doctor = crud.delete_doctor(db, doctor_id)
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return {"detail": "Doctor deleted"}

@router.put("/link_user/{doctor_id}", response_model=schemas.DoctorOut)
def link_doctor_user(
    doctor_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    doctor = crud.get_doctor(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if doctor.user_id is not None:
        raise HTTPException(status_code=400, detail="Doctor already linked to a user.")

    doctor.user_id = user_id
    db.commit()
    db.refresh(doctor)
    return doctor
