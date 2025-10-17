from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import logging
from ..core.config import settings

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
        logging.info("Successfully connected to MongoDB")
        
        # Create indexes
        await create_indexes()
        
    except Exception as e:
        logging.error(f"Failed to connect to MongoDB: {e}")
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

# Dependency to get database instance
async def get_db():
    return await get_database()
