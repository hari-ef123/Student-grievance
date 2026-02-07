from beanie import Document, Indexed
from datetime import datetime
from typing import Optional
from pydantic import Field
import enum

class UserRole(str, enum.Enum):
    student = "student"
    admin = "admin"

class ComplaintStatus(str, enum.Enum):
    pending = "Pending"
    in_progress = "In Progress"
    resolved = "Resolved"

class User(Document):
    name: str
    email: Indexed(str, unique=True)
    hashed_password: str
    role: str = "student"
    # Profile Fields
    register_number: Optional[str] = None
    department: Optional[str] = None
    year: Optional[str] = None
    phone: Optional[str] = None

    class Settings:
        name = "user"

class Complaint(Document):
    student_id: str 
    title: Optional[str] = "Grievance" # Added title
    category: str
    description: str
    is_anonymous: bool = False
    status: str = "Pending"
    admin_remark: Optional[str] = None
    incident_date: Optional[datetime] = None
    attachment: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "complaint"

class Notification(Document):
    user_id: str
    message: str
    is_read: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "notification"

class Feedback(Document):
    complaint_id: str
    rating: int # 1 to 5
    feedback_text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "feedback"

class SupportMessage(Document):
    user_id: str
    message: str
    reply: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "support_message"
