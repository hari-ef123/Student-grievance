from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# --- User Schemas ---
class UserBase(BaseModel):
    email: str
    name: str
    role: str = "student"
    register_number: Optional[str] = None
    department: Optional[str] = None
    year: Optional[str] = None
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: str 

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    register_number: Optional[str] = None
    department: Optional[str] = None
    year: Optional[str] = None
    phone: Optional[str] = None

# --- Complaint Schemas ---
class ComplaintBase(BaseModel):
    title: Optional[str] = "Grievance"
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
    id: str 
    student_id: str
    student_name: Optional[str] = None
    status: str
    admin_remark: Optional[str] = None
    incident_date: Optional[datetime] = None
    attachment: Optional[str] = None
    created_at: datetime

# --- Notification Schemas ---
class NotificationResponse(BaseModel):
    id: str
    message: str
    is_read: bool
    created_at: datetime

# --- Feedback Schemas ---
class FeedbackCreate(BaseModel):
    complaint_id: str
    rating: int
    feedback_text: str

class FeedbackResponse(FeedbackCreate):
    id: str
    created_at: datetime

# --- Support Schemas ---
class SupportMessageCreate(BaseModel):
    message: str

class SupportMessageUpdate(BaseModel):
    reply: str

class SupportMessageResponse(BaseModel):
    id: str
    user_id: str
    message: str
    reply: Optional[str] = None
    created_at: datetime

# --- Analytics Schemas ---
class AnalyticsResponse(BaseModel):
    total: int
    pending: int
    resolved: int
    pending_percent: float
    resolved_percent: float
    monthly_data: List[dict] # {month: "Jan", count: 10}

# --- Auth Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    email: str
    password: str
    role: str
