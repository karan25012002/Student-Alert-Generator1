from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId
from .user import PyObjectId

class AlertBase(BaseModel):
    parent_id: str
    student_id: str
    title: str = Field(..., min_length=1, max_length=200)
    message: str = Field(..., min_length=1, max_length=1000)
    type: str = Field(..., pattern="^(info|warning|error|success)$")
    priority: str = Field(..., pattern="^(low|medium|high)$")
    category: str = Field(..., pattern="^(academic|attendance|engagement|general)$")
    action_required: bool = False
    suggestions: List[str] = []
    metadata: Optional[Dict[str, Any]] = {}

class AlertCreate(AlertBase):
    pass

class AlertUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    message: Optional[str] = Field(None, min_length=1, max_length=1000)
    type: Optional[str] = Field(None, pattern="^(info|warning|error|success)$")
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    category: Optional[str] = Field(None, pattern="^(academic|attendance|engagement|general)$")
    action_required: Optional[bool] = None
    suggestions: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None

class AlertInDB(AlertBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    read: bool = False
    read_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

class Alert(AlertBase):
    id: str
    read: bool = False
    read_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    expires_at: Optional[datetime] = None

class AlertMarkRead(BaseModel):
    read: bool = True

class AlertStats(BaseModel):
    total_alerts: int
    unread_alerts: int
    high_priority_alerts: int
    alerts_by_category: Dict[str, int]
    alerts_by_type: Dict[str, int]
    recent_alerts: List[Alert]
