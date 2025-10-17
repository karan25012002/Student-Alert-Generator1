from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import logging
from ..core.config import settings
from ..core.security import get_password_hash
class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    database = None

db = MongoDB()

async def get_database():
    return db.database

async def connect_to_mongo():
    """Create database connection"""
    try:
        db.client = AsyncIOMotorClient(settings.MONGODB_URL)
        db.database = db.client[settings.DATABASE_NAME]
        
        # Test the connection
        await db.client.admin.command('ping')
        logging.info("Successfully connected to MongoDB Atlas")
        
        # Additional verification: Check database accessibility
        db_list = await db.client.list_database_names()
        logging.info(f"Available databases: {db_list}")
        
        # Create indexes
        await create_indexes()
        
    except Exception as e:
        logging.error(f"Failed to connect to MongoDB Atlas: {e}")
        raise e

async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        logging.info("Disconnected from MongoDB")

async def create_indexes():
    """Create database indexes for better performance"""
    try:
        # Users collection indexes
        await db.database.users.create_index("email", unique=True)
        await db.database.users.create_index("student_id")
        
        # Students collection indexes
        await db.database.students.create_index("student_id", unique=True)
        await db.database.students.create_index("parent_id")
        
        # Academic data indexes
        await db.database.academic_data.create_index("student_id")
        await db.database.academic_data.create_index([("student_id", 1), ("date", -1)])
        
        # Attendance data indexes
        await db.database.attendance_data.create_index("student_id")
        await db.database.attendance_data.create_index([("student_id", 1), ("date", -1)])
        
        # Engagement data indexes
        await db.database.engagement_data.create_index("student_id")
        await db.database.engagement_data.create_index([("student_id", 1), ("date", -1)])
        
        # Alerts indexes
        await db.database.alerts.create_index("parent_id")
        await db.database.alerts.create_index([("parent_id", 1), ("created_at", -1)])
        await db.database.alerts.create_index("read")
        
        logging.info("Database indexes created successfully")
        
    except Exception as e:
        logging.error(f"Failed to create indexes: {e}")

async def seed_dummy_data():
    """Seed dummy data for testing (idempotent)"""
    try:
        # Seed users with upsert
        user_data = [
            {"email": "admin@example.com", "password": "hashedpassword", "role": "admin", "student_id": None},
            {"email": "parent1@example.com", "password": "hashedpassword", "role": "parent", "student_id": "STU001"},
        ]
        for user in user_data:
            try:
                hashed_password = get_password_hash(user["password"])
                user_doc = {
                    "email": user["email"],
                    "hashed_password": hashed_password,
                    "role": user["role"],
                    "student_id": user["student_id"],
                    "is_active": True,
                    "created_at": "2023-10-01T10:00:00Z",
                    "updated_at": "2023-10-01T10:00:00Z"
                }
                await db.database.users.update_one(
                    {"email": user["email"]},
                    {"$set": user_doc},
                    upsert=True
                )
            except Exception as e:
                logging.error(f"Failed to seed user {user['email']}: {e}")
        
        # Seed students with upsert
        student_data = [
            {"student_id": "STU001", "name": "John Doe", "parent_id": "parent1@example.com", "grade": "10th"},
            {"student_id": "STU002", "name": "Jane Smith", "parent_id": "parent1@example.com", "grade": "9th"},
        ]
        for student in student_data:
            try:
                await db.database.students.update_one(
                    {"student_id": student["student_id"]},
                    {"$set": student},
                    upsert=True
                )
            except Exception as e:
                logging.error(f"Failed to seed student {student['student_id']}: {e}")
        
        # Seed academic data with upsert
        academic_data = [
            {"student_id": "STU001", "subject": "Math", "score": 85, "date": "2023-10-01"},
            {"student_id": "STU002", "subject": "Science", "score": 92, "date": "2023-10-01"},
        ]
        for data in academic_data:
            try:
                await db.database.academic_data.update_one(
                    {"student_id": data["student_id"], "subject": data["subject"]},
                    {"$set": data},
                    upsert=True
                )
            except Exception as e:
                logging.error(f"Failed to seed academic data for {data['student_id']}: {e}")
        
        # Seed attendance data with upsert
        attendance_data = [
            {"student_id": "STU001", "status": "Present", "date": "2023-10-01"},
            {"student_id": "STU002", "status": "Absent", "date": "2023-10-01"},
        ]
        for data in attendance_data:
            try:
                await db.database.attendance_data.update_one(
                    {"student_id": data["student_id"], "date": data["date"]},
                    {"$set": data},
                    upsert=True
                )
            except Exception as e:
                logging.error(f"Failed to seed attendance data for {data['student_id']}: {e}")
        
        # Seed engagement data with upsert
        engagement_data = [
            {"student_id": "STU001", "activity": "Class Participation", "score": 80, "date": "2023-10-01"},
            {"student_id": "STU002", "activity": "Homework", "score": 90, "date": "2023-10-01"},
        ]
        for data in engagement_data:
            try:
                await db.database.engagement_data.update_one(
                    {"student_id": data["student_id"], "activity": data["activity"]},
                    {"$set": data},
                    upsert=True
                )
            except Exception as e:
                logging.error(f"Failed to seed engagement data for {data['student_id']}: {e}")
        
        # Seed alerts with upsert
        alert_data = [
            {"parent_id": "parent1@example.com", "message": "Low attendance alert for John Doe", "type": "attendance", "read": False, "created_at": "2023-10-01T10:00:00Z"},
            {"parent_id": "parent1@example.com", "message": "Academic performance alert for Jane Smith", "type": "academic", "read": False, "created_at": "2023-10-01T11:00:00Z"},
        ]
        for alert in alert_data:
            try:
                await db.database.alerts.update_one(
                    {"parent_id": alert["parent_id"], "message": alert["message"]},
                    {"$set": alert},
                    upsert=True
                )
            except Exception as e:
                logging.error(f"Failed to seed alert for {alert['parent_id']}: {e}")
        
        logging.info("Dummy data seeded/updated successfully")
        
    except Exception as e:
        logging.error(f"Failed to seed dummy data: {e}")
        raise

# Dependency to get database instance
async def get_db():
    return await get_database()
