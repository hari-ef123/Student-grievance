from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# --- User Schemas ---
class UserBase(BaseModel):
    email: str
    name: str
    role: str = "student"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: str # MongoDB ID is a string (ObjectId)

# --- Complaint Schemas ---
class ComplaintBase(BaseModel):
    category: str
    description: str
    is_anonymous: bool = False
    incident_date: Optional[datetime] = None

class ComplaintCreate(ComplaintBase):
    pass

class ComplaintUpdate(BaseModel):
    status: str
    admin_remark: Optional[str] = None

class ComplaintResponse(ComplaintBase):
    id: str # MongoDB ID is a string (ObjectId)
    student_id: str
    student_name: Optional[str] = None
    status: str
    admin_remark: Optional[str] = None
    incident_date: Optional[datetime] = None
    attachment: Optional[str] = None
    created_at: datetime

# --- Auth Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    email: str
    password: str
    role: str
