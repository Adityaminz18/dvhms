from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud, database
from auth import get_current_user, admin_required  # Import access control dependencies
from models import User  # Import the User model

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.AppointmentOut)
def create_appointment(
    appointment: schemas.AppointmentCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # Only patients can create appointments
):
    if current_user.role != "patient":
        raise HTTPException(status_code=403, detail="Only patients can create appointments.")
    return crud.create_appointment(db, appointment)

@router.get("/", response_model=list[schemas.AppointmentOut])
def list_appointments(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # Any logged-in user can access
):
    return crud.get_appointments(db, skip, limit)

@router.get("/{appointment_id}", response_model=schemas.AppointmentOut)
def get_appointment(
    appointment_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # Any logged-in user can access
):
    appt = crud.get_appointment(db, appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt

@router.put("/{appointment_id}", response_model=schemas.AppointmentOut)
def update_appointment(
    appointment_id: int, 
    appointment: schemas.AppointmentCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(admin_required)  # Only admins can update appointments
):
    appt = crud.update_appointment(db, appointment_id, appointment)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt

@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(admin_required)  # Only admins can delete appointments
):
    appt = crud.delete_appointment(db, appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"detail": "Appointment deleted"}