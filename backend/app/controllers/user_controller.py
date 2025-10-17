from typing import Optional, List
from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from ..database.mongodb import get_db
from ..models.user import User, UserCreate, UserUpdate, UserInDB
from ..core.security import get_password_hash, verify_password

class UserController:
    def __init__(self):
        self.collection_name = "users"

    async def get_db(self) -> AsyncIOMotorDatabase:
        return await get_db()

    async def create_user(self, user_data: UserCreate) -> User:
        """Create a new user."""
        db = await self.get_db()
        
        # Check if user already exists
        existing_user = await db[self.collection_name].find_one({"email": user_data.email})
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Check if student_id is already taken
        existing_student = await db[self.collection_name].find_one({"student_id": user_data.student_id})
        if existing_student:
            raise ValueError("Student ID already registered")
        
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        
        # Create user document
        user_dict = user_data.model_dump()
        del user_dict["password"]
        user_dict["hashed_password"] = hashed_password
        user_dict["created_at"] = datetime.utcnow()
        user_dict["updated_at"] = datetime.utcnow()
        user_dict["role"] = "parent"
        
        # Insert user
        result = await db[self.collection_name].insert_one(user_dict)
        
        # Return created user
        created_user = await db[self.collection_name].find_one({"_id": result.inserted_id})
        return self._convert_to_user(created_user)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        db = await self.get_db()
        user_doc = await db[self.collection_name].find_one({"email": email})
        
        if user_doc:
            return self._convert_to_user(user_doc)
        return None

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        db = await self.get_db()
        
        try:
            object_id = ObjectId(user_id)
            user_doc = await db[self.collection_name].find_one({"_id": object_id})
            
            if user_doc:
                return self._convert_to_user(user_doc)
        except Exception:
            pass
        
        return None

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password."""
        db = await self.get_db()
        user_doc = await db[self.collection_name].find_one({"email": email})
        
        if not user_doc:
            return None
        
        if not verify_password(password, user_doc["hashed_password"]):
            return None
        
        # Update last login
        await db[self.collection_name].update_one(
            {"_id": user_doc["_id"]},
            {"$set": {"last_login": datetime.utcnow()}}
        )
        
        return self._convert_to_user(user_doc)

    async def update_user(self, user_id: str, user_data: UserUpdate) -> Optional[User]:
        """Update user information."""
        db = await self.get_db()
        
        try:
            object_id = ObjectId(user_id)
            
            # Prepare update data
            update_data = {k: v for k, v in user_data.dict().items() if v is not None}
            update_data["updated_at"] = datetime.utcnow()
            
            # Update user
            result = await db[self.collection_name].update_one(
                {"_id": object_id},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                updated_user = await db[self.collection_name].find_one({"_id": object_id})
                return self._convert_to_user(updated_user)
                
        except Exception:
            pass
        
        return None

    async def delete_user(self, user_id: str) -> bool:
        """Delete user (soft delete by setting is_active to False)."""
        db = await self.get_db()
        
        try:
            object_id = ObjectId(user_id)
            
            result = await db[self.collection_name].update_one(
                {"_id": object_id},
                {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
            )
            
            return result.modified_count > 0
            
        except Exception:
            return False

    async def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get list of users."""
        db = await self.get_db()
        
        cursor = db[self.collection_name].find({"is_active": True}).skip(skip).limit(limit)
        users = []
        
        async for user_doc in cursor:
            users.append(self._convert_to_user(user_doc))
        
        return users

    def _convert_to_user(self, user_doc: dict) -> User:
        """Convert database document to User model."""
        user_doc["id"] = str(user_doc["_id"])
        del user_doc["_id"]
        del user_doc["hashed_password"]  # Don't include password hash in response
        
        return User(**user_doc)
