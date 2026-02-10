from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
from datetime import datetime
import os
import traceback

import models, schemas, database, auth

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

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    print(f"Global Exception: {exc}")
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal Server Error: {str(exc)}"},
    )

@app.on_event("startup")
async def startup_event():
    # Ensure uploads directory exists
    os.makedirs("uploads", exist_ok=True)
    
    await database.init_db([
        models.User, 
        models.Complaint, 
        models.Notification, 
        models.Feedback, 
        models.SupportMessage
    ])

# Mount Uploads for Static Access
if not os.path.exists("uploads"):
    os.makedirs("uploads")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# --- Auth & Profile Routes ---
@app.post("/api/auth/register", response_model=schemas.UserResponse)
async def register(user: schemas.UserCreate):
    db_user = await models.User.find_one(models.User.email == user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = auth.get_password_hash(user.password)
    new_user = models.User(
        name=user.name, 
        email=user.email, 
        hashed_password=hashed_pw, 
        role=user.role,
        register_number=user.register_number,
        department=user.department,
        year=user.year,
        phone=user.phone
    )
    await new_user.insert()
    
    return schemas.UserResponse(
        id=str(new_user.id),
        name=new_user.name,
        email=new_user.email,
        role=new_user.role,
        register_number=new_user.register_number,
        department=new_user.department,
        year=new_user.year,
        phone=new_user.phone
    )

@app.get("/api/profile", response_model=schemas.UserResponse)
async def get_profile(token: str = Depends(auth.oauth2_scheme)):
    payload = auth.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = await models.User.get(payload.get("user_id"))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/api/profile", response_model=schemas.UserResponse)
async def update_profile(update: schemas.ProfileUpdate, token: str = Depends(auth.oauth2_scheme)):
    payload = auth.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = await models.User.get(payload.get("user_id"))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if update.name: user.name = update.name
    if update.email and update.email != user.email:
        existing_user = await models.User.find_one(models.User.email == update.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already taken by another user")
        user.email = update.email
    if update.register_number: user.register_number = update.register_number
    if update.department: user.department = update.department
    if update.year: user.year = update.year
    if update.phone: user.phone = update.phone
    
    await user.save()
    return user

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
    title: str = Form("Grievance"),
    category: str = Form(...),
    description: str = Form(...),
    is_anonymous: bool = Form(False),
    incident_date: Optional[str] = Form(None),
    attachment: Optional[UploadFile] = File(None),
    token: str = Depends(auth.oauth2_scheme)
):
    try:
    try:
        payload = auth.decode_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        user_id = payload.get("user_id")
        
        attachment_db_path = None
        if attachment and attachment.filename:
            os.makedirs("uploads", exist_ok=True)
            safe_filename = attachment.filename.replace(" ", "_")
            filename = f"{int(datetime.utcnow().timestamp())}_{safe_filename}"
            attachment_save_path = f"uploads/{filename}"
            attachment_db_path = attachment_save_path
            content = await attachment.read()
            with open(attachment_save_path, "wb") as f:
                f.write(content)

        dt_incident = None
        if incident_date and incident_date not in ["null", ""]:
            try:
                dt_incident = datetime.fromisoformat(incident_date.replace('Z', '+00:00')) if 'T' in incident_date else datetime.strptime(incident_date, "%Y-%m-%d")
            except: pass

        new_complaint = models.Complaint(
            student_id=user_id,
            title=title,
            category=category,
            description=description,
            is_anonymous=is_anonymous,
            incident_date=dt_incident,
            attachment=attachment_db_path
        )
        await new_complaint.insert()
        return new_complaint
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/complaints/my", response_model=List[schemas.ComplaintResponse])
async def get_my_complaints(
    status: Optional[str] = None, 
    category: Optional[str] = None,
    token: str = Depends(auth.oauth2_scheme)
):
    payload = auth.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user_id = payload.get("user_id")
    query = {"student_id": user_id}
    if status: query["status"] = status
    if category: query["category"] = category
    
    complaints = await models.Complaint.find(query).to_list()
    result = []
    for c in complaints:
        d = c.dict()
        d["id"] = str(c.id)
        result.append(d)
    return result

@app.get("/api/admin/complaints", response_model=List[schemas.ComplaintResponse])
async def get_all_complaints(
    status: Optional[str] = None, 
    category: Optional[str] = None,
    from_date: Optional[str] = None,
    token: str = Depends(auth.oauth2_scheme)
):
    payload = auth.decode_token(token)
    if not payload or payload.get("role") != "admin":
         raise HTTPException(status_code=403, detail="Admin access required")
    
    query = {}
    if status: query["status"] = status
    if category: query["category"] = category
    if from_date:
        try:
            dt = datetime.fromisoformat(from_date)
            query["created_at"] = {"$gte": dt}
        except: pass

    complaints = await models.Complaint.find(query).to_list()
    
    # Map student names
    user_map = {}
    try:
        student_ids = list(set([c.student_id for c in complaints]))
        valid_ids = [ObjectId(uid) for uid in student_ids if ObjectId.is_valid(uid)]
        
        if valid_ids:
            users = await models.User.find({"_id": {"$in": valid_ids}}).to_list()
            user_map = {str(u.id): u.name for u in users}
    except Exception as e:
        print(f"Error mapping users: {e}")

    # Convert to response format
    result = []
    for c in complaints:
        c_dict = c.dict()
        c_dict["id"] = str(c.id)
        c_dict["student_name"] = user_map.get(c.student_id, "Unknown")
        result.append(c_dict)
    
    return result

@app.put("/api/admin/complaints/{id}")
async def update_complaint_status(id: str, update: schemas.ComplaintUpdate, token: str = Depends(auth.oauth2_scheme)):
    payload = auth.decode_token(token)
    if not payload or payload.get("role") != "admin":
         raise HTTPException(status_code=403, detail="Admin access required")
    
    complaint = await models.Complaint.get(id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    old_status = complaint.status
    complaint.status = update.status
    if update.admin_remark:
        complaint.admin_remark = update.admin_remark
    
    await complaint.save()

    # Create Notification for student
    notif_msg = f"Your complaint '{complaint.title}' status has been updated to '{update.status}'."
    if update.status == "Resolved":
        notif_msg = f"✅ Your complaint '{complaint.title}' has been resolved. Please provide feedback!"
    
    notification = models.Notification(user_id=complaint.student_id, message=notif_msg)
    await notification.insert()

    # Send Email Alert (Mock implementation)
    user = await models.User.get(complaint.student_id)
    if user:
        print(f"MOCK EMAIL to {user.email}: {notif_msg}")
        # In real production, use smtplib here.

    return {"message": "Status updated successfully"}

# --- Notification Routes ---
@app.get("/api/notifications", response_model=List[schemas.NotificationResponse])
async def get_notifications(token: str = Depends(auth.oauth2_scheme)):
    payload = auth.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    notifs = await models.Notification.find(models.Notification.user_id == payload.get("user_id")).sort("-created_at").to_list()
    return [schemas.NotificationResponse(id=str(n.id), message=n.message, is_read=n.is_read, created_at=n.created_at) for n in notifs]

@app.put("/api/notifications/read/{id}")
async def mark_notification_read(id: str, token: str = Depends(auth.oauth2_scheme)):
    notif = await models.Notification.get(id)
    if notif:
        notif.is_read = True
        await notif.save()
    return {"message": "Marked as read"}

# --- Feedback Routes ---
@app.post("/api/feedback", response_model=schemas.FeedbackResponse)
async def submit_feedback(fb: schemas.FeedbackCreate, token: str = Depends(auth.oauth2_scheme)):
    existing = await models.Feedback.find_one(models.Feedback.complaint_id == fb.complaint_id)
    if existing:
        raise HTTPException(status_code=400, detail="Feedback already submitted for this complaint")
    
    new_fb = models.Feedback(complaint_id=fb.complaint_id, rating=fb.rating, feedback_text=fb.feedback_text)
    await new_fb.insert()
    return schemas.FeedbackResponse(id=str(new_fb.id), **fb.dict(), created_at=new_fb.created_at)

# --- Support Routes ---
@app.post("/api/support/message")
async def send_support_msg(msg: schemas.SupportMessageCreate, token: str = Depends(auth.oauth2_scheme)):
    payload = auth.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    new_msg = models.SupportMessage(user_id=payload.get("user_id"), message=msg.message)
    await new_msg.insert()
    return {"message": "Message sent to support"}

@app.get("/api/support/messages", response_model=List[schemas.SupportMessageResponse])
async def get_all_support_msgs(token: str = Depends(auth.oauth2_scheme)):
    payload = auth.decode_token(token)
    if payload.get("role") != "admin": raise HTTPException(status_code=403)
    msgs = await models.SupportMessage.find_all().to_list()
    return [schemas.SupportMessageResponse(id=str(m.id), **m.dict()) for m in msgs]

@app.put("/api/support/reply/{id}")
async def reply_support_msg(id: str, update: schemas.SupportMessageUpdate, token: str = Depends(auth.oauth2_scheme)):
    payload = auth.decode_token(token)
    if payload.get("role") != "admin": raise HTTPException(status_code=403)
    msg = await models.SupportMessage.get(id)
    if msg:
        msg.reply = update.reply
        await msg.save()
        # Notify user
        notif = models.Notification(user_id=msg.user_id, message=f"Support Team replied to your message: {update.reply[:30]}...")
        await notif.insert()
    return {"message": "Reply sent"}

# --- Analytics Routes ---
@app.get("/api/admin/analytics", response_model=schemas.AnalyticsResponse)
async def get_analytics(token: str = Depends(auth.oauth2_scheme)):
    payload = auth.decode_token(token)
    if payload.get("role") != "admin": raise HTTPException(status_code=403)
    
    all_c = await models.Complaint.all().to_list()
    total = len(all_c)
    resolved = len([c for c in all_c if c.status == "Resolved"])
    pending = total - resolved
    
    pending_p = (pending / total * 100) if total > 0 else 0
    resolved_p = (resolved / total * 100) if total > 0 else 0
    
    # Monthly data (Simple group by)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_stats = {m: 0 for m in months}
    for c in all_c:
        m_name = c.created_at.strftime("%b")
        if m_name in monthly_stats: monthly_stats[m_name] += 1
    
    monthly_data = [{"month": k, "count": v} for k, v in monthly_stats.items()]
    
    return schemas.AnalyticsResponse(
        total=total, pending=pending, resolved=resolved,
        pending_percent=round(pending_p, 1), resolved_percent=round(resolved_p, 1),
        monthly_data=monthly_data
    )

@app.get("/")
async def read_root():
    return {"message": "Student Grievance API v2 is running"}


