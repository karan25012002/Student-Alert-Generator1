from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from bson import ObjectId
from .user import PyObjectId

class StudentBase(BaseModel):
    student_id: str = Field(..., min_length=3, max_length=50)
    name: str = Field(..., min_length=2, max_length=100)
    grade: str = Field(..., max_length=20)
    class_section: str = Field(..., max_length=20)
    parent_id: str
    school_name: Optional[str] = Field(None, max_length=200)
    date_of_birth: Optional[date] = None
    enrollment_date: Optional[date] = None

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    grade: Optional[str] = Field(None, max_length=20)
    class_section: Optional[str] = Field(None, max_length=20)
    school_name: Optional[str] = Field(None, max_length=200)

class StudentInDB(StudentBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

class Student(StudentBase):
    id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

# Academic Performance Models
class Assignment(BaseModel):
    name: str
    subject: str
    score: float = Field(..., ge=0, le=100)
    max_score: float = Field(..., ge=1)
    date: date
    type: str  # quiz, exam, homework, project, etc.
    weight: Optional[float] = Field(None, ge=0, le=1)

class SubjectPerformance(BaseModel):
    subject: str
    current_grade: str
    percentage: float = Field(..., ge=0, le=100)
    assignments: List[Assignment] = []
    trend: str = Field(..., pattern="^(up|down|stable)$")
    teacher: Optional[str] = None

class AcademicData(BaseModel):
    id: Optional[str] = None
    student_id: str
    semester: str
    year: int
    overall_gpa: float = Field(..., ge=0, le=4.0)
    subjects: List[SubjectPerformance] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Attendance Models
class AttendanceRecord(BaseModel):
    date: date
    status: str = Field(..., pattern="^(present|absent|late|excused)$")
    arrival_time: Optional[str] = None
    departure_time: Optional[str] = None
    reason: Optional[str] = None

class SubjectAttendance(BaseModel):
    subject: str
    total_classes: int = Field(..., ge=0)
    attended_classes: int = Field(..., ge=0)
    percentage: float = Field(..., ge=0, le=100)

class AttendanceData(BaseModel):
    id: Optional[str] = None
    student_id: str
    month: int = Field(..., ge=1, le=12)
    year: int
    overall_percentage: float = Field(..., ge=0, le=100)
    total_days: int = Field(..., ge=0)
    present_days: int = Field(..., ge=0)
    absent_days: int = Field(..., ge=0)
    late_days: int = Field(..., ge=0)
    records: List[AttendanceRecord] = []
    subject_attendance: List[SubjectAttendance] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Engagement Models
class StudySession(BaseModel):
    date: date
    subject: str
    duration_minutes: int = Field(..., ge=0)
    activity_type: str  # reading, problem_solving, research, discussion
    engagement_score: float = Field(..., ge=0, le=100)
    focus_time_minutes: int = Field(..., ge=0)

class OnlineActivity(BaseModel):
    platform: str
    session_duration_minutes: int = Field(..., ge=0)
    resources_accessed: int = Field(..., ge=0)
    interactions: int = Field(..., ge=0)
    completion_rate: float = Field(..., ge=0, le=100)
    date: date

class EngagementData(BaseModel):
    id: Optional[str] = None
    student_id: str
    week_start_date: date
    overall_engagement_score: float = Field(..., ge=0, le=100)
    total_study_hours: float = Field(..., ge=0)
    average_daily_hours: float = Field(..., ge=0)
    participation_score: float = Field(..., ge=0, le=100)
    focus_score: float = Field(..., ge=0, le=100)
    study_sessions: List[StudySession] = []
    online_activities: List[OnlineActivity] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
