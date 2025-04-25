from sqlalchemy.orm import Session
import models, schemas

# ---------------------- PATIENT ----------------------

def create_patient(db: Session, patient: schemas.PatientCreate):
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_patient(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()

def get_patients(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Patient).offset(skip).limit(limit).all()

def update_patient(db: Session, patient_id: int, updated_data: schemas.PatientCreate):
    db_patient = get_patient(db, patient_id)
    if db_patient:
        for key, value in updated_data.dict().items():
            setattr(db_patient, key, value)
        db.commit()
        db.refresh(db_patient)
    return db_patient

def delete_patient(db: Session, patient_id: int):
    db_patient = get_patient(db, patient_id)
    if db_patient:
        db.delete(db_patient)
        db.commit()
    return db_patient


# ---------------------- DOCTOR ----------------------

def create_doctor(db: Session, doctor: schemas.DoctorCreate):
    db_doctor = models.Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

def get_doctor(db: Session, doctor_id: int):
    return db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()

def get_doctors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Doctor).offset(skip).limit(limit).all()

def update_doctor(db: Session, doctor_id: int, updated_data: schemas.DoctorCreate):
    db_doctor = get_doctor(db, doctor_id)
    if db_doctor:
        for key, value in updated_data.dict().items():
            setattr(db_doctor, key, value)
        db.commit()
        db.refresh(db_doctor)
    return db_doctor

def delete_doctor(db: Session, doctor_id: int):
    db_doctor = get_doctor(db, doctor_id)
    if db_doctor:
        db.delete(db_doctor)
        db.commit()
    return db_doctor

# ------------------ APPOINTMENTS ------------------

def create_appointment(db: Session, appointment: schemas.AppointmentCreate):
    db_appointment = models.Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def get_appointment(db: Session, appointment_id: int):
    return db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()

def get_appointments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Appointment).offset(skip).limit(limit).all()

def update_appointment(db: Session, appointment_id: int, updated: schemas.AppointmentCreate):
    db_appointment = get_appointment(db, appointment_id)
    if db_appointment:
        for key, value in updated.dict().items():
            setattr(db_appointment, key, value)
        db.commit()
        db.refresh(db_appointment)
    return db_appointment

def delete_appointment(db: Session, appointment_id: int):
    db_appointment = get_appointment(db, appointment_id)
    if db_appointment:
        db.delete(db_appointment)
        db.commit()
    return db_appointment
# This code defines CRUD operations for managing patients, doctors, and appointments in a hospital management system.