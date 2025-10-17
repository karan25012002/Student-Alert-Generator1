from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Any, Optional
from datetime import date

from ..models.user import User
from ..models.student import Student, AcademicData, AttendanceData, EngagementData
from ..controllers.student_controller import StudentController
from ..utils.auth import get_current_active_user

router = APIRouter()

@router.get("/data/{student_id}")
async def get_student_data(
    student_id: str,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get comprehensive student data overview."""
    student_controller = StudentController()
    
    # Verify the student belongs to the current user
    student = await student_controller.get_student_by_parent(current_user.id)
    if not student or student.student_id != student_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found or access denied"
        )
    
    # Get comprehensive overview
    overview = await student_controller.get_student_overview(student_id)
    
    if not overview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student data not found"
        )
    
    return overview

@router.get("/{student_id}/academic")
async def get_academic_performance(
    student_id: str,
    semester: Optional[str] = Query(None, description="Semester filter"),
    year: Optional[int] = Query(None, description="Year filter"),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get academic performance data for a student."""
    student_controller = StudentController()
    
    # Verify access
    student = await student_controller.get_student_by_parent(current_user.id)
    if not student or student.student_id != student_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found or access denied"
        )
    
    academic_data = await student_controller.get_academic_performance(student_id)
    
    if not academic_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Academic data not found"
        )
    
    return academic_data

@router.get("/{student_id}/attendance")
async def get_attendance_data(
    student_id: str,
    month: Optional[int] = Query(None, ge=1, le=12, description="Month filter (1-12)"),
    year: Optional[int] = Query(None, description="Year filter"),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get attendance data for a student."""
    student_controller = StudentController()
    
    # Verify access
    student = await student_controller.get_student_by_parent(current_user.id)
    if not student or student.student_id != student_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found or access denied"
        )
    
    attendance_data = await student_controller.get_attendance_data(student_id, month, year)
    
    if not attendance_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance data not found"
        )
    
    return attendance_data

@router.get("/{student_id}/engagement")
async def get_engagement_data(
    student_id: str,
    week_start: Optional[date] = Query(None, description="Week start date filter"),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get engagement data for a student."""
    student_controller = StudentController()
    
    # Verify access
    student = await student_controller.get_student_by_parent(current_user.id)
    if not student or student.student_id != student_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found or access denied"
        )
    
    engagement_data = await student_controller.get_engagement_data(student_id, week_start)
    
    if not engagement_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Engagement data not found"
        )
    
    return engagement_data

@router.get("/profile")
async def get_student_profile(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get student profile for the current parent."""
    student_controller = StudentController()
    
    student = await student_controller.get_student_by_parent(current_user.id)
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No student found for this parent"
        )
    
    return student

@router.get("/{student_id}/summary")
async def get_student_summary(
    student_id: str,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get a summary of student's key metrics."""
    student_controller = StudentController()
    
    # Verify access
    student = await student_controller.get_student_by_parent(current_user.id)
    if not student or student.student_id != student_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found or access denied"
        )
    
    # Get all data types
    academic_data = await student_controller.get_academic_performance(student_id)
    attendance_data = await student_controller.get_attendance_data(student_id)
    engagement_data = await student_controller.get_engagement_data(student_id)
    
    # Create summary
    summary = {
        "student_id": student_id,
        "student_name": student.name,
        "grade": student.grade,
        "class_section": student.class_section,
        "metrics": {
            "overall_gpa": academic_data.get("overall_gpa", 0) if academic_data else 0,
            "attendance_rate": attendance_data.overall_percentage if attendance_data else 0,
            "engagement_score": engagement_data.overall_engagement_score if engagement_data else 0,
        },
        "recent_performance": {
            "academic_trend": "stable",  # This would be calculated from actual data
            "attendance_trend": "stable",
            "engagement_trend": "improving"
        },
        "alerts_count": 0,  # This would come from alert controller
        "last_updated": student.updated_at
    }
    
    return summary
