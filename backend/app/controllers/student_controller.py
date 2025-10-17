from typing import Optional, List, Dict, Any
from datetime import datetime, date, timedelta
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
import random
from faker import Faker

from ..database.mongodb import get_db
from ..models.student import (
    Student, StudentCreate, StudentUpdate, StudentInDB,
    AcademicData, AttendanceData, EngagementData,
    Assignment, SubjectPerformance, AttendanceRecord, SubjectAttendance,
    StudySession, OnlineActivity
)

fake = Faker()

class StudentController:
    def __init__(self):
        self.students_collection = "students"
        self.academic_collection = "academic_data"
        self.attendance_collection = "attendance_data"
        self.engagement_collection = "engagement_data"

    async def get_db(self) -> AsyncIOMotorDatabase:
        return await get_db()

    # Student CRUD operations
    async def create_student(self, student_data: StudentCreate) -> Student:
        """Create a new student."""
        db = await self.get_db()
        
        # Check if student_id already exists
        existing_student = await db[self.students_collection].find_one({"student_id": student_data.student_id})
        if existing_student:
            raise ValueError("Student with this ID already exists")
        
        # Create student document
        student_dict = student_data.dict()
        student_dict["created_at"] = datetime.utcnow()
        student_dict["updated_at"] = datetime.utcnow()
        student_dict["is_active"] = True
        
        # Insert student
        result = await db[self.students_collection].insert_one(student_dict)
        
        # Return created student
        created_student = await db[self.students_collection].find_one({"_id": result.inserted_id})
        return self._convert_to_student(created_student)

    async def get_student_by_id(self, student_id: str) -> Optional[Student]:
        """Get student by student_id."""
        db = await self.get_db()
        student_doc = await db[self.students_collection].find_one({"student_id": student_id})
        
        if student_doc:
            return self._convert_to_student(student_doc)
        return None

    async def get_student_by_parent(self, parent_id: str) -> Optional[Student]:
        """Get student by parent_id."""
        db = await self.get_db()
        student_doc = await db[self.students_collection].find_one({"parent_id": parent_id})
        
        if student_doc:
            return self._convert_to_student(student_doc)
        return None

    # Academic Data operations
    async def get_academic_data(self, student_id: str, semester: str = None, year: int = None) -> Optional[AcademicData]:
        """Get academic data for a student."""
        db = await self.get_db()
        
        # For demo purposes, generate mock data
        return self._generate_mock_academic_data(student_id, semester, year)

    async def get_academic_performance(self, student_id: str) -> Dict[str, Any]:
        """Get comprehensive academic performance data."""
        # Generate mock academic performance data
        subjects = ["Mathematics", "Science", "English", "History", "Geography"]
        
        subject_performance = []
        for subject in subjects:
            assignments = []
            for i in range(5):
                assignments.append(Assignment(
                    name=f"{subject} {fake.random_element(['Quiz', 'Test', 'Assignment', 'Project'])} {i+1}",
                    subject=subject,
                    score=random.uniform(70, 98),
                    max_score=100,
                    date=fake.date_between(start_date='-30d', end_date='today'),
                    type=fake.random_element(['quiz', 'test', 'homework', 'project']),
                    weight=random.uniform(0.1, 0.3)
                ))
            
            avg_score = sum(a.score for a in assignments) / len(assignments)
            grade = self._calculate_grade(avg_score)
            trend = random.choice(['up', 'down', 'stable'])
            
            subject_performance.append(SubjectPerformance(
                subject=subject,
                current_grade=grade,
                percentage=avg_score,
                assignments=assignments,
                trend=trend,
                teacher=fake.name()
            ))
        
        return {
            "student_id": student_id,
            "semester": "Fall 2024",
            "year": 2024,
            "overall_gpa": random.uniform(3.2, 3.9),
            "subjects": subject_performance,
            "monthly_progress": [
                {"month": "August", "gpa": 3.6},
                {"month": "September", "gpa": 3.7},
                {"month": "October", "gpa": 3.8}
            ]
        }

    # Attendance Data operations
    async def get_attendance_data(self, student_id: str, month: int = None, year: int = None) -> Optional[AttendanceData]:
        """Get attendance data for a student."""
        # Generate mock attendance data
        if not month:
            month = datetime.now().month
        if not year:
            year = datetime.now().year
            
        return self._generate_mock_attendance_data(student_id, month, year)

    # Engagement Data operations
    async def get_engagement_data(self, student_id: str, week_start: date = None) -> Optional[EngagementData]:
        """Get engagement data for a student."""
        # Generate mock engagement data
        if not week_start:
            today = date.today()
            week_start = today - timedelta(days=today.weekday())
            
        return self._generate_mock_engagement_data(student_id, week_start)

    async def get_student_overview(self, student_id: str) -> Dict[str, Any]:
        """Get comprehensive student overview."""
        student = await self.get_student_by_id(student_id)
        if not student:
            return None
            
        academic_data = await self.get_academic_performance(student_id)
        attendance_data = await self.get_attendance_data(student_id)
        engagement_data = await self.get_engagement_data(student_id)
        
        return {
            "student": student,
            "academic": academic_data,
            "attendance": attendance_data,
            "engagement": engagement_data,
            "summary": {
                "overall_gpa": academic_data.get("overall_gpa", 0),
                "attendance_rate": attendance_data.overall_percentage if attendance_data else 0,
                "engagement_score": engagement_data.overall_engagement_score if engagement_data else 0
            }
        }

    # Helper methods
    def _convert_to_student(self, student_doc: dict) -> Student:
        """Convert database document to Student model."""
        student_doc["id"] = str(student_doc["_id"])
        del student_doc["_id"]
        return Student(**student_doc)

    def _calculate_grade(self, percentage: float) -> str:
        """Calculate letter grade from percentage."""
        if percentage >= 97: return "A+"
        elif percentage >= 93: return "A"
        elif percentage >= 90: return "A-"
        elif percentage >= 87: return "B+"
        elif percentage >= 83: return "B"
        elif percentage >= 80: return "B-"
        elif percentage >= 77: return "C+"
        elif percentage >= 73: return "C"
        elif percentage >= 70: return "C-"
        elif percentage >= 67: return "D+"
        elif percentage >= 65: return "D"
        else: return "F"

    def _generate_mock_academic_data(self, student_id: str, semester: str, year: int) -> AcademicData:
        """Generate mock academic data."""
        subjects = ["Mathematics", "Science", "English", "History", "Geography"]
        subject_performance = []
        
        for subject in subjects:
            assignments = []
            for i in range(3):
                assignments.append(Assignment(
                    name=f"{subject} Assignment {i+1}",
                    subject=subject,
                    score=random.uniform(75, 95),
                    max_score=100,
                    date=fake.date_between(start_date='-30d', end_date='today'),
                    type=random.choice(['quiz', 'test', 'homework', 'project'])
                ))
            
            avg_score = sum(a.score for a in assignments) / len(assignments)
            
            subject_performance.append(SubjectPerformance(
                subject=subject,
                current_grade=self._calculate_grade(avg_score),
                percentage=avg_score,
                assignments=assignments,
                trend=random.choice(['up', 'down', 'stable'])
            ))
        
        return AcademicData(
            student_id=student_id,
            semester=semester or "Fall 2024",
            year=year or 2024,
            overall_gpa=random.uniform(3.2, 3.9),
            subjects=subject_performance
        )

    def _generate_mock_attendance_data(self, student_id: str, month: int, year: int) -> AttendanceData:
        """Generate mock attendance data."""
        # Generate attendance records for the month
        records = []
        total_days = 0
        present_days = 0
        late_days = 0
        
        # Get all weekdays in the month
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(year, month + 1, 1) - timedelta(days=1)
        
        current_date = start_date
        while current_date <= end_date:
            # Only count weekdays
            if current_date.weekday() < 5:  # Monday = 0, Friday = 4
                total_days += 1
                
                # 90% chance of being present
                is_present = random.random() > 0.1
                is_late = is_present and random.random() > 0.85
                
                if is_present:
                    present_days += 1
                    if is_late:
                        late_days += 1
                
                status = "present" if is_present else "absent"
                if is_late:
                    status = "late"
                
                arrival_time = None
                if is_present:
                    if is_late:
                        arrival_time = f"08:{random.randint(15, 45):02d}"
                    else:
                        arrival_time = f"0{random.randint(7, 8)}:{random.randint(0, 59):02d}"
                
                records.append(AttendanceRecord(
                    date=current_date,
                    status=status,
                    arrival_time=arrival_time
                ))
            
            current_date += timedelta(days=1)
        
        absent_days = total_days - present_days
        overall_percentage = (present_days / total_days * 100) if total_days > 0 else 0
        
        # Generate subject attendance
        subjects = ["Mathematics", "Science", "English", "History", "Geography"]
        subject_attendance = []
        
        for subject in subjects:
            total_classes = random.randint(15, 25)
            attended = int(total_classes * random.uniform(0.85, 0.98))
            percentage = (attended / total_classes * 100) if total_classes > 0 else 0
            
            subject_attendance.append(SubjectAttendance(
                subject=subject,
                total_classes=total_classes,
                attended_classes=attended,
                percentage=percentage
            ))
        
        return AttendanceData(
            student_id=student_id,
            month=month,
            year=year,
            overall_percentage=overall_percentage,
            total_days=total_days,
            present_days=present_days,
            absent_days=absent_days,
            late_days=late_days,
            records=records,
            subject_attendance=subject_attendance
        )

    def _generate_mock_engagement_data(self, student_id: str, week_start: date) -> EngagementData:
        """Generate mock engagement data."""
        subjects = ["Mathematics", "Science", "English", "History", "Geography"]
        study_sessions = []
        online_activities = []
        
        # Generate study sessions for the week
        for day_offset in range(7):
            current_date = week_start + timedelta(days=day_offset)
            
            # 2-4 study sessions per day
            for _ in range(random.randint(2, 4)):
                subject = random.choice(subjects)
                duration = random.randint(30, 120)
                
                study_sessions.append(StudySession(
                    date=current_date,
                    subject=subject,
                    duration_minutes=duration,
                    activity_type=random.choice(['reading', 'problem_solving', 'research', 'discussion']),
                    engagement_score=random.uniform(70, 95),
                    focus_time_minutes=int(duration * random.uniform(0.6, 0.9))
                ))
            
            # 1-2 online activities per day
            for _ in range(random.randint(1, 2)):
                online_activities.append(OnlineActivity(
                    platform=random.choice(['LMS', 'Khan Academy', 'Coursera', 'EdX']),
                    session_duration_minutes=random.randint(20, 90),
                    resources_accessed=random.randint(3, 15),
                    interactions=random.randint(5, 25),
                    completion_rate=random.uniform(80, 100),
                    date=current_date
                ))
        
        total_study_hours = sum(session.duration_minutes for session in study_sessions) / 60
        average_daily_hours = total_study_hours / 7
        
        return EngagementData(
            student_id=student_id,
            week_start_date=week_start,
            overall_engagement_score=random.uniform(80, 95),
            total_study_hours=total_study_hours,
            average_daily_hours=average_daily_hours,
            participation_score=random.uniform(85, 95),
            focus_score=random.uniform(75, 90),
            study_sessions=study_sessions,
            online_activities=online_activities
        )
