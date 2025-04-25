from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud, database
from auth import get_current_user, admin_required  # Import admin_required
from models import User  # Import the User model

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.PatientOut)
def create_patient(
    patient: schemas.PatientCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(admin_required)  # Admin-only access
):
    return crud.create_patient(db, patient)

@router.get("/", response_model=list[schemas.PatientOut])
def list_patients(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # Accessible to all authenticated users
):
    return crud.get_patients(db, skip, limit)

@router.get("/{patient_id}", response_model=schemas.PatientOut)
def get_patient(
    patient_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # Accessible to all authenticated users
):
    patient = crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.put("/{patient_id}", response_model=schemas.PatientOut)
def update_patient(
    patient_id: int, 
    patient: schemas.PatientCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(admin_required)  # Admin-only access
):
    db_patient = crud.update_patient(db, patient_id, patient)
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient

@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(admin_required)  # Admin-only access
):
    db_patient = crud.delete_patient(db, patient_id)
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"detail": "Patient deleted"}