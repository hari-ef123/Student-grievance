import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from backend import models, database, auth

async def seed_data():
    print("Starting data seeding...")
    # Initialize DB
    client = AsyncIOMotorClient(database.MONGODB_URL)
    await init_beanie(database=client[database.DATABASE_NAME], document_models=[models.User, models.Complaint])

    # 1. Create Sample Student
    student_email = "student@example.com"
    existing_student = await models.User.find_one(models.User.email == student_email)
    if not existing_student:
        student = models.User(
            name="Sample Student",
            email=student_email,
            hashed_password=auth.get_password_hash("password123"),
            role="student"
        )
        await student.insert()
        print(f"Created Student: {student_email}")
    else:
        student = existing_student
        print(f"Student {student_email} already exists.")

    # 2. Create Sample Admin
    admin_email = "admin@college.com"
    existing_admin = await models.User.find_one(models.User.email == admin_email)
    if not existing_admin:
        admin = models.User(
            name="Principal Admin",
            email=admin_email,
            hashed_password=auth.get_password_hash("admin123"),
            role="admin"
        )
        await admin.insert()
        print(f"Created Admin: {admin_email}")
    else:
        admin = existing_admin
        print(f"Admin {admin_email} already exists.")

    # 3. Create 3 Sample Complaints
    complaints_data = [
        {"cat": "Infrastructure", "desc": "The ceiling fan in Room 302 is not working properly and making loud noise."},
        {"cat": "Academic", "desc": "Request for extending library hours during the final examination period."},
        {"cat": "Hostel", "desc": "Water supply issues in the Boys Hostel Block B since yesterday morning."}
    ]

    for data in complaints_data:
        complaint = models.Complaint(
            student_id=str(student.id),
            category=data["cat"],
            description=data["desc"],
            is_anonymous=False,
            status="Pending"
        )
        await complaint.insert()
    
    print(f"Successfully inserted {len(complaints_data)} sample complaints.")
    print("Seeding complete.")

if __name__ == "__main__":
    asyncio.run(seed_data())
