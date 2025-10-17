"""
Models for Student Alert Generator feature.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone


class StudentAlertRequest(BaseModel):
    """Request model for generating student alerts."""
    
    name: str = Field(..., min_length=1, max_length=100, description="Student name")
    roll_number: str = Field(..., min_length=1, max_length=50, description="Student roll number or ID")
    attendance_percentage: float = Field(..., ge=0, le=100, description="Attendance percentage (0-100)")
    academic_performance: float = Field(..., description="GPA (0-4.0) or marks (0-100)")
    behavior_notes: Optional[str] = Field("", max_length=500, description="Behavioral observations")
    participation_level: Optional[str] = Field("medium", pattern="^(low|medium|high)$", description="Class participation level")
    additional_comments: Optional[str] = Field("", max_length=500, description="Additional comments or observations")
    
    @field_validator('academic_performance')
    @classmethod
    def validate_academic_performance(cls, v):
        """Validate academic performance is in reasonable range."""
        if v < 0:
            raise ValueError('Academic performance cannot be negative')
        if v > 100:
            raise ValueError('Academic performance cannot exceed 100')
        return v
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "John Doe",
                "roll_number": "STU12345",
                "attendance_percentage": 78.5,
                "academic_performance": 3.2,
                "behavior_notes": "Generally well-behaved, sometimes distracted",
                "participation_level": "medium",
                "additional_comments": "Shows improvement in recent weeks"
            }
        }
    }


class GeneratedAlertResponse(BaseModel):
    """Response model for a single generated alert."""
    
    alert_type: str = Field(..., pattern="^(info|warning|error|success)$")
    priority: str = Field(..., pattern="^(low|medium|high)$")
    category: str = Field(..., pattern="^(academic|attendance|engagement|general)$")
    title: str = Field(..., max_length=200)
    message: str = Field(..., max_length=1000)
    action_required: bool
    suggestions: List[str] = []
    reasoning: str = Field(..., description="AI reasoning for this alert")
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))



class AlertGenerationResponse(BaseModel):
    """Complete response for alert generation."""
    
    student_name: str
    student_roll_number: str
    alerts: List[GeneratedAlertResponse]
    summary: Dict[str, Any]
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    ai_powered: bool = True
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "student_name": "John Doe",
                "student_roll_number": "STU12345",
                "alerts": [
                    {
                        "alert_type": "warning",
                        "priority": "medium",
                        "category": "attendance",
                        "title": "Attendance Needs Improvement",
                        "message": "Student attendance is below optimal levels...",
                        "action_required": True,
                        "suggestions": ["Contact parents", "Review attendance patterns"],
                        "reasoning": "Attendance at 78.5% is below the 85% optimal threshold",
                        "confidence_score": 0.85,
                        "generated_at": "2024-10-17T10:30:00Z"
                    }
                ],
                "summary": {
                    "total_alerts": 3,
                    "high_priority_count": 1,
                    "action_required_count": 2
                },
                "generated_at": "2024-10-17T10:30:00Z",
                "ai_powered": True
            }
        }
    }


class SaveGeneratedAlertsRequest(BaseModel):
    """Request to save generated alerts to the database."""
    
    parent_id: str
    student_id: str
    alerts: List[GeneratedAlertResponse]
