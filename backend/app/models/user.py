from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Annotated, Any
from datetime import datetime
from bson import ObjectId

# Simple ObjectId type alias for Pydantic v2
PyObjectId = Annotated[str, Field(..., description="MongoDB ObjectId")]

class UserBase(BaseModel):
    email: str
    name: str
    student_name: str
    student_id: str
    phone: Optional[str] = None
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    student_name: Optional[str] = None
    phone: Optional[str] = None

class UserInDB(UserBase):
    id: Optional[str] = Field(None, alias="_id")
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    role: str = "parent"

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

class User(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    role: str = "parent"

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: User

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[str] = None
