from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
from datetime import datetime
import os
import traceback

from . import models, schemas, database, auth

from bson import ObjectId

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for Demo/File usage
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await database.init_db([models.User, models.Complaint])

# --- Auth Routes ---
@app.post("/api/auth/register", response_model=schemas.UserResponse)
async def register(user: schemas.UserCreate):
    db_user = await models.User.find_one(models.User.email == user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = auth.get_password_hash(user.password)
    new_user = models.User(name=user.name, email=user.email, hashed_password=hashed_pw, role=user.role)
    await new_user.insert()
    
    # Return response - Beanie models have 'id' which maps to '_id'
    return schemas.UserResponse(
        id=str(new_user.id),
        name=new_user.name,
        email=new_user.email,
        role=new_user.role
    )

@app.post("/api/auth/login")
async def login(request: schemas.LoginRequest):
    user = await models.User.find_one(models.User.email == request.email)
    if not user or not auth.verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if user.role != request.role:
        raise HTTPException(status_code=403, detail=f"Access Denied: You are not registered as a {request.role}")

    access_token = auth.create_access_token(data={"sub": user.email, "role": user.role, "user_id": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer", "role": user.role, "name": user.name}

# --- Complaint Routes ---
@app.post("/api/complaints", response_model=schemas.ComplaintResponse)
async def create_complaint(
    category: str = Form(...),
    description: str = Form(...),
    is_anonymous: bool = Form(False),
    incident_date: Optional[str] = Form(None),
    attachment: Optional[UploadFile] = File(None),
    token: str = Depends(auth.oauth2_scheme)
):
    try:
        payload = auth.decode_token(token)
        if not payload:
             raise HTTPException(status_code=401, detail="Invalid token")
        
        user_id = payload.get("user_id")
        
        attachment_path = None
        if attachment and attachment.filename:
            # Create uploads directory if it doesn't exist
            os.makedirs("uploads", exist_ok=True)
            # Create a unique filename
            safe_filename = attachment.filename.replace(" ", "_")
            filename = f"{int(datetime.utcnow().timestamp())}_{safe_filename}"
            attachment_path = f"uploads/{filename}"
            content = await attachment.read()
            if content:
                with open(attachment_path, "wb") as f:
                    f.write(content)
            else:
                attachment_path = None

        # Handle incident_date string to datetime
        dt_incident = None
        if incident_date and incident_date != "null" and incident_date != "":
            try:
                # Try parsing browser date (YYYY-MM-DD) or ISO
                if 'T' in incident_date:
                    dt_incident = datetime.fromisoformat(incident_date.replace('Z', '+00:00'))
                else:
                    dt_incident = datetime.strptime(incident_date, "%Y-%m-%d")
            except Exception as e:
                 print(f"Date parsing error: {e}")
                 dt_incident = None

        new_complaint = models.Complaint(
            student_id=user_id,
            category=category,
            description=description,
            is_anonymous=is_anonymous,
            incident_date=dt_incident,
            attachment=attachment_path
        )
        await new_complaint.insert()
        
        return schemas.ComplaintResponse(
            id=str(new_complaint.id),
            student_id=new_complaint.student_id,
            category=new_complaint.category,
            description=new_complaint.description,
            is_anonymous=new_complaint.is_anonymous,
            status=new_complaint.status,
            admin_remark=new_complaint.admin_remark,
            incident_date=new_complaint.incident_date,
            attachment=new_complaint.attachment,
            created_at=new_complaint.created_at
        )
    except Exception as e:
        print("Error in create_complaint:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/complaints/my", response_model=List[schemas.ComplaintResponse])
async def get_my_complaints(token: str = Depends(auth.oauth2_scheme)):
    payload = auth.decode_token(token)
    if not payload:
         raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("user_id")
    complaints = await models.Complaint.find(models.Complaint.student_id == user_id).to_list()
    
    # Map to schema
    return [
        schemas.ComplaintResponse(
            id=str(c.id),
            student_id=c.student_id,
            category=c.category,
            description=c.description,
            is_anonymous=c.is_anonymous,
            status=c.status,
            admin_remark=c.admin_remark,
            incident_date=c.incident_date,
            attachment=c.attachment,
            created_at=c.created_at
        ) for c in complaints
    ]

@app.get("/api/admin/complaints", response_model=List[schemas.ComplaintResponse])
async def get_all_complaints(token: str = Depends(auth.oauth2_scheme)):
    payload = auth.decode_token(token)
    if not payload or payload.get("role") != "admin":
         raise HTTPException(status_code=403, detail="Admin access required")
    
    complaints = await models.Complaint.all().to_list()
    
    # optimize: fetch all relevant users in one go
    student_ids = list(set([c.student_id for c in complaints]))
    # Beanie finds by ID if we pass iterables to the id query? 
    # Or we can just find all users since the scale is small for this project
    users = await models.User.find({"_id": {"$in": [ObjectId(uid) for uid in student_ids]}}).to_list()
    
    user_map = {str(u.id): u.name for u in users}

    return [
        schemas.ComplaintResponse(
            id=str(c.id),
            student_id=c.student_id,
            student_name=user_map.get(c.student_id, "Unknown"),
            category=c.category,
            description=c.description,
            is_anonymous=c.is_anonymous,
            status=c.status,
            admin_remark=c.admin_remark,
            incident_date=c.incident_date,
            attachment=c.attachment,
            created_at=c.created_at
        ) for c in complaints
    ]

@app.put("/api/admin/complaints/{id}")
async def update_complaint_status(id: str, update: schemas.ComplaintUpdate, token: str = Depends(auth.oauth2_scheme)):
    payload = auth.decode_token(token)
    if not payload or payload.get("role") != "admin":
         raise HTTPException(status_code=403, detail="Admin access required")
    
    complaint = await models.Complaint.get(id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    complaint.status = update.status
    if update.admin_remark:
        complaint.admin_remark = update.admin_remark
    
    await complaint.save()
    return {"message": "Status updated successfully"}

@app.get("/")
async def read_root():
    return FileResponse("index.html")

# Serve multiple HTML files
@app.get("/{filename}.html")
async def read_html(filename: str):
    file_path = f"{filename}.html"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="Page not found")

# Serve static assets
app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/js", StaticFiles(directory="js"), name="js")
if not os.path.exists("uploads"):
    os.makedirs("uploads")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
