from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId
from .user import PyObjectId

class InsightBase(BaseModel):
    student_id: str
    parent_id: str
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1, max_length=2000)
    insight_type: str = Field(..., pattern="^(academic|attendance|engagement|behavioral|recommendation)$")
    confidence_score: float = Field(..., ge=0, le=1)
    data_sources: List[str] = []  # academic, attendance, engagement, etc.
    recommendations: List[str] = []
    metadata: Optional[Dict[str, Any]] = {}

class InsightCreate(InsightBase):
    pass

class InsightInDB(InsightBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

class Insight(InsightBase):
    id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

class InsightQuery(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    context: Optional[str] = None
    include_recommendations: bool = True

class InsightResponse(BaseModel):
    insight: str
    recommendations: List[str] = []
    confidence: float = Field(..., ge=0, le=1)
    data_used: List[str] = []
    generated_at: datetime = Field(default_factory=datetime.utcnow)

class ConversationMessage(BaseModel):
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ConversationHistory(BaseModel):
    id: Optional[str] = None
    parent_id: str
    student_id: str
    messages: List[ConversationMessage] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True
