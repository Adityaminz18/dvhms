from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud, database
from auth import get_current_user, admin_required  # Import admin_required
from models import User, Patient  # Import the User and Patient models

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
    current_user: User = Depends(get_current_user)  # Admin-only access
):
    return crud.get_patients(db, skip, limit)

@router.get("/me", response_model=schemas.PatientOut)
def get_my_patient(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Only normal login required, not admin
):
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    if not current_user.id:
        raise HTTPException(status_code=400, detail="Invalid user ID in current_user.")
    
    if not patient:
        raise HTTPException(status_code=404, detail="No patient profile found for current user.")
    
    return patient

@router.get("/all", response_model=list[schemas.PatientOut])
def get_all_patients(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)  # Admin-only access
):
    return crud.get_all_patients(db)

@router.get("/{patient_id}", response_model=schemas.PatientOut)
def get_patient(
    patient_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # Admin-only access
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

@router.put("/link_user/{patient_id}", response_model=schemas.PatientOut)
def link_patient_user(
    patient_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    patient = crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    if patient.user_id is not None:
        raise HTTPException(status_code=400, detail="Patient already linked to a user.")

    patient.user_id = user_id
    db.commit()
    db.refresh(patient)
    return patient


