from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud, database

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
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    return crud.create_appointment(db, appointment)

@router.get("/", response_model=list[schemas.AppointmentOut])
def list_appointments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_appointments(db, skip, limit)

@router.get("/{appointment_id}", response_model=schemas.AppointmentOut)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appt = crud.get_appointment(db, appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt

@router.put("/{appointment_id}", response_model=schemas.AppointmentOut)
def update_appointment(appointment_id: int, appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    appt = crud.update_appointment(db, appointment_id, appointment)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt

@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appt = crud.delete_appointment(db, appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"detail": "Appointment deleted"}
# This code defines a FastAPI router for managing appointments in a hospital management system.
# It includes endpoints for creating, listing, retrieving, updating, and deleting appointment records.