from pydantic import BaseModel
from typing import Optional
from datetime import date, time

# User
class UserBase(BaseModel):
    username: str
    role: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    class Config:
        orm_mode = True

# Patient
class PatientBase(BaseModel):
    name: str
    age: int
    gender: str
    address: str
    phone: str

class PatientCreate(PatientBase):
    pass  # No user_id from frontend — backend will add automatically

class PatientOut(PatientBase):
    id: int
    user_id: Optional[int]  # 🆕 Return user_id
    class Config:
        orm_mode = True

# Doctor:

class DoctorBase(BaseModel):
    name: str
    specialization: str
    phone: str

class DoctorCreate(DoctorBase):
    pass

class DoctorOut(DoctorBase):
    id: int
    user_id: Optional[int]  # 🆕 Return user_id
    class Config:
        orm_mode = True

# Appointment
class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    date: date
    time: time
    status: str

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentOut(AppointmentBase):
    id: int
    class Config:
        orm_mode = True

# Auth-related schemas already added before (UserCreate, UserOut)
# If not, here's a recap:

class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    username: str
    password: str
