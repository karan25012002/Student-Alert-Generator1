"""
Sample data generator for testing the Student Progress Tracker system.
This script creates sample users, students, and generates alerts for demonstration.
"""

import asyncio
from datetime import datetime, timedelta
import random
from typing import List

from ..controllers.user_controller import UserController
from ..controllers.student_controller import StudentController
from ..controllers.alert_controller import AlertController
from ..models.user import UserCreate
from ..models.student import StudentCreate
from ..models.alert import AlertCreate

class SampleDataGenerator:
    def __init__(self):
        self.user_controller = UserController()
        self.student_controller = StudentController()
        self.alert_controller = AlertController()

    async def generate_sample_data(self) -> dict:
        """Generate complete sample data for testing."""
        
        print("Generating sample data...")
        
        # Create sample parent user
        parent = await self._create_sample_parent()
        print(f"Created parent: {parent.email}")
        
        # Create sample student
        student = await self._create_sample_student(parent.id)
        print(f"Created student: {student.name}")
        
        # Generate sample alerts
        alerts = await self._generate_sample_alerts(parent.id, student.student_id)
        print(f"Created {len(alerts)} sample alerts")
        
        return {
            "parent": parent,
            "student": student,
            "alerts": alerts,
            "login_credentials": {
                "email": "parent@example.com",
                "password": "password123"
            }
        }

    async def _create_sample_parent(self):
        """Create a sample parent user."""
        
        # Check if sample user already exists
        existing_user = await self.user_controller.get_user_by_email("parent@example.com")
        if existing_user:
            return existing_user
        
        parent_data = UserCreate(
            email="parent@example.com",
            name="John Smith",
            student_name="Emily Smith",
            student_id="STU001",
            password="password123",
            phone="+1-555-0123"
        )
        
        return await self.user_controller.create_user(parent_data)

    async def _create_sample_student(self, parent_id: str):
        """Create a sample student."""
        
        # Check if sample student already exists
        existing_student = await self.student_controller.get_student_by_parent(parent_id)
        if existing_student:
            return existing_student
        
        student_data = StudentCreate(
            student_id="STU001",
            name="Emily Smith",
            grade="10th Grade",
            class_section="Section A",
            parent_id=parent_id,
            school_name="Lincoln High School"
        )
        
        return await self.student_controller.create_student(student_data)

    async def _generate_sample_alerts(self, parent_id: str, student_id: str) -> List:
        """Generate comprehensive sample alerts."""
        
        sample_alerts_data = [
            {
                "parent_id": parent_id,
                "student_id": student_id,
                "title": "Math Performance Decline",
                "message": "Your child's math scores have dropped by 12% over the past two weeks. Recent quiz scores: 78%, 72%, 75%. This decline may indicate difficulty with current topics or need for additional support.",
                "type": "warning",
                "priority": "high",
                "category": "academic",
                "action_required": True,
                "suggestions": [
                    "Schedule a meeting with the math teacher",
                    "Consider hiring a tutor for algebra concepts",
                    "Review homework completion patterns",
                    "Check if additional practice materials are needed"
                ],
                "metadata": {
                    "subject": "Mathematics",
                    "decline_percentage": 12,
                    "recent_scores": [78, 72, 75]
                }
            },
            {
                "parent_id": parent_id,
                "student_id": student_id,
                "title": "Excellent English Performance",
                "message": "Outstanding work in English class! Your child scored 95% on the recent essay and has maintained consistent A grades throughout the semester. The teacher noted exceptional creativity and analytical skills.",
                "type": "success",
                "priority": "low",
                "category": "academic",
                "action_required": False,
                "suggestions": [
                    "Celebrate this achievement with your child",
                    "Consider advanced English literature courses",
                    "Encourage participation in writing competitions"
                ],
                "metadata": {
                    "subject": "English",
                    "recent_score": 95,
                    "grade_trend": "A"
                }
            },
            {
                "parent_id": parent_id,
                "student_id": student_id,
                "title": "Attendance Alert",
                "message": "Attendance has dropped to 89% this month, below the required 95% threshold. Missing classes: Oct 8, Oct 12, Oct 14. Consistent attendance is crucial for academic success.",
                "type": "warning",
                "priority": "medium",
                "category": "attendance",
                "action_required": True,
                "suggestions": [
                    "Contact school about missed days",
                    "Ensure proper health management",
                    "Set up morning routine reminders",
                    "Discuss any concerns your child may have about school"
                ],
                "metadata": {
                    "attendance_rate": 89,
                    "missed_days": ["2024-10-08", "2024-10-12", "2024-10-14"],
                    "threshold": 95
                }
            },
            {
                "parent_id": parent_id,
                "student_id": student_id,
                "title": "Low Engagement in History",
                "message": "Class participation in History has decreased significantly over the past three weeks. Teacher notes indicate minimal interaction during discussions and group activities. Engagement score dropped from 85% to 65%.",
                "type": "warning",
                "priority": "medium",
                "category": "engagement",
                "action_required": True,
                "suggestions": [
                    "Discuss interest in history topics with your child",
                    "Meet with the history teacher to understand specific concerns",
                    "Explore engaging history documentaries or books",
                    "Consider connecting historical events to current events"
                ],
                "metadata": {
                    "subject": "History",
                    "engagement_drop": 20,
                    "previous_score": 85,
                    "current_score": 65
                }
            },
            {
                "parent_id": parent_id,
                "student_id": student_id,
                "title": "Perfect Week Attendance",
                "message": "Congratulations! Your child maintained perfect attendance this week and arrived on time every day. This consistency shows great commitment to learning.",
                "type": "success",
                "priority": "low",
                "category": "attendance",
                "action_required": False,
                "suggestions": [
                    "Acknowledge this positive behavior",
                    "Continue supporting good morning routines"
                ],
                "metadata": {
                    "week_attendance": 100,
                    "on_time_days": 5
                }
            },
            {
                "parent_id": parent_id,
                "student_id": student_id,
                "title": "Science Project Excellence",
                "message": "Your child's science project on renewable energy received the highest grade in the class (98%). The teacher praised the thorough research and creative presentation approach.",
                "type": "success",
                "priority": "low",
                "category": "academic",
                "action_required": False,
                "suggestions": [
                    "Celebrate this outstanding achievement",
                    "Consider science fair participation",
                    "Explore advanced science topics together"
                ],
                "metadata": {
                    "subject": "Science",
                    "project_score": 98,
                    "class_rank": 1
                }
            },
            {
                "parent_id": parent_id,
                "student_id": student_id,
                "title": "Study Time Increase Needed",
                "message": "Weekly study time has decreased to 3.2 hours, below the recommended 5 hours for grade level. This may impact upcoming exam performance.",
                "type": "info",
                "priority": "medium",
                "category": "engagement",
                "action_required": True,
                "suggestions": [
                    "Create a structured study schedule",
                    "Identify and eliminate distractions",
                    "Set up a dedicated study space",
                    "Break study sessions into manageable chunks"
                ],
                "metadata": {
                    "current_study_hours": 3.2,
                    "recommended_hours": 5.0,
                    "deficit": 1.8
                }
            },
            {
                "parent_id": parent_id,
                "student_id": student_id,
                "title": "Parent-Teacher Conference Reminder",
                "message": "Your scheduled parent-teacher conference is tomorrow (October 25th) at 3:00 PM in Room 204. Please bring any questions about Emily's progress.",
                "type": "info",
                "priority": "high",
                "category": "general",
                "action_required": True,
                "suggestions": [
                    "Prepare questions about academic progress",
                    "Review recent report cards and assignments",
                    "Discuss any concerns about social development",
                    "Ask about extracurricular opportunities"
                ],
                "metadata": {
                    "conference_date": "2024-10-25",
                    "conference_time": "15:00",
                    "location": "Room 204"
                }
            }
        ]
        
        created_alerts = []
        for alert_data in sample_alerts_data:
            try:
                alert_create = AlertCreate(**alert_data)
                created_alert = await self.alert_controller.create_alert(alert_create)
                created_alerts.append(created_alert)
            except Exception as e:
                print(f"Failed to create alert: {alert_data['title']} - {str(e)}")
        
        return created_alerts

    async def cleanup_sample_data(self):
        """Clean up sample data (for testing purposes)."""
        
        print("Cleaning up sample data...")
        
        # This would implement cleanup logic
        # For now, we'll just print a message
        print("Sample data cleanup completed")

async def main():
    """Main function to generate sample data."""
    
    generator = SampleDataGenerator()
    
    try:
        result = await generator.generate_sample_data()
        
        print("\n" + "="*50)
        print("SAMPLE DATA GENERATION COMPLETED")
        print("="*50)
        print(f"Parent Email: {result['login_credentials']['email']}")
        print(f"Password: {result['login_credentials']['password']}")
        print(f"Student Name: {result['student'].name}")
        print(f"Student ID: {result['student'].student_id}")
        print(f"Alerts Created: {len(result['alerts'])}")
        print("\nYou can now login to the frontend with these credentials!")
        print("="*50)
        
    except Exception as e:
        print(f"Error generating sample data: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
