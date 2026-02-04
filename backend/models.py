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

    class Settings:
        name = "users"

class Complaint(Document):
    student_id: str # References User ID string
    category: str
    description: str
    is_anonymous: bool = False
    status: str = "Pending"
    admin_remark: Optional[str] = None
    incident_date: Optional[datetime] = None
    attachment: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "complaints"
