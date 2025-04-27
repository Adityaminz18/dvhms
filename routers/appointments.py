from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud, database
from auth import get_current_user, admin_required
from models import User

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

# Role based checker
def roles_required(allowed_roles: list):
    def checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Not authorized")
        return current_user
    return checker

@router.post("/", response_model=schemas.AppointmentOut)
def create_appointment(
    appointment: schemas.AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(roles_required(["admin", "doctor", "patient"]))
):
    if current_user.role == "patient":
        # Set correct patient_id
        patient = crud.get_patient_by_user_id(db=db, user_id=current_user.id)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient record not found.")
        appointment.patient_id = patient.id  # Force correct patient_id

    if current_user.role == "doctor":
        # Set correct doctor_id
        doctor = crud.get_doctor_by_user_id(db=db, user_id=current_user.id)
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor record not found.")
        appointment.doctor_id = doctor.id  # Force correct doctor_id

    return crud.create_appointment(db, appointment)


@router.get("/", response_model=list[schemas.AppointmentOut])
def list_appointments(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(roles_required(["admin", "doctor", "patient"]))
):
    if current_user.role == "admin":
        return crud.get_appointments(db=db, skip=skip, limit=limit)

    elif current_user.role == "patient":
        patient = crud.get_patient_by_user_id(db=db, user_id=current_user.id)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not linked to profile.")
        return crud.get_appointments_by_patient_id(db=db, patient_id=patient.id)

    elif current_user.role == "doctor":
        doctor = crud.get_doctor_by_user_id(db=db, user_id=current_user.id)
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not linked to profile.")
        return crud.get_appointments_by_doctor_id(db=db, doctor_id=doctor.id)

@router.get("/{appointment_id}", response_model=schemas.AppointmentOut)
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(roles_required(["admin", "doctor", "patient"]))
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
    current_user: User = Depends(roles_required(["admin", "doctor", "patient"]))
):
    appt = crud.update_appointment(db, appointment_id, appointment)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt

@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    appt = crud.delete_appointment(db, appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"detail": "Appointment deleted"}
