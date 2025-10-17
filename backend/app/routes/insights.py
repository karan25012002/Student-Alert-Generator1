from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Any, Optional, List

from ..models.user import User
from ..models.insight import (
    Insight, InsightQuery, InsightResponse, 
    ConversationHistory
)
from ..controllers.insight_controller import InsightController
from ..controllers.student_controller import StudentController
from ..utils.auth import get_current_active_user

router = APIRouter()

@router.post("/{student_id}/generate", response_model=InsightResponse)
async def generate_insight(
    student_id: str,
    query: InsightQuery,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Generate AI-powered insight for a student."""
    
    # Verify student access
    student_controller = StudentController()
    student = await student_controller.get_student_by_parent(current_user.id)
    
    if not student or student.student_id != student_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found or access denied"
        )
    
    insight_controller = InsightController()
    
    try:
        insight_response = await insight_controller.generate_insight(
            student_id=student_id,
            parent_id=current_user.id,
            query=query
        )
        
        return insight_response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate insight: {str(e)}"
        )

@router.get("/{student_id}", response_model=List[Insight])
async def get_insights(
    student_id: str,
    skip: int = Query(0, ge=0, description="Number of insights to skip"),
    limit: int = Query(20, ge=1, le=50, description="Number of insights to return"),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get insights for a student."""
    
    # Verify student access
    student_controller = StudentController()
    student = await student_controller.get_student_by_parent(current_user.id)
    
    if not student or student.student_id != student_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found or access denied"
        )
    
    insight_controller = InsightController()
    
    insights = await insight_controller.get_insights_by_student(
        student_id=student_id,
        parent_id=current_user.id,
        skip=skip,
        limit=limit
    )
    
    return insights

@router.get("/{student_id}/summary")
async def get_insight_summary(
    student_id: str,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get insight summary for a student."""
    
    # Verify student access
    student_controller = StudentController()
    student = await student_controller.get_student_by_parent(current_user.id)
    
    if not student or student.student_id != student_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found or access denied"
        )
    
    insight_controller = InsightController()
    
    summary = await insight_controller.get_insight_summary(
        student_id=student_id,
        parent_id=current_user.id
    )
    
    return summary

@router.get("/{student_id}/conversation", response_model=ConversationHistory)
async def get_conversation_history(
    student_id: str,
    limit: int = Query(50, ge=1, le=100, description="Number of messages to return"),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get conversation history for a student."""
    
    # Verify student access
    student_controller = StudentController()
    student = await student_controller.get_student_by_parent(current_user.id)
    
    if not student or student.student_id != student_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found or access denied"
        )
    
    insight_controller = InsightController()
    
    conversation = await insight_controller.get_conversation_history(
        parent_id=current_user.id,
        student_id=student_id,
        limit=limit
    )
    
    if not conversation:
        # Return empty conversation if none exists
        return ConversationHistory(
            parent_id=current_user.id,
            student_id=student_id,
            messages=[]
        )
    
    return conversation

@router.delete("/{student_id}/conversation")
async def clear_conversation_history(
    student_id: str,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Clear conversation history for a student."""
    
    # Verify student access
    student_controller = StudentController()
    student = await student_controller.get_student_by_parent(current_user.id)
    
    if not student or student.student_id != student_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found or access denied"
        )
    
    insight_controller = InsightController()
    
    success = await insight_controller.clear_conversation_history(
        parent_id=current_user.id,
        student_id=student_id
    )
    
    if success:
        return {"message": "Conversation history cleared"}
    else:
        return {"message": "No conversation history found"}

@router.post("/{student_id}/weekly-summary", response_model=InsightResponse)
async def generate_weekly_summary(
    student_id: str,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Generate weekly summary insight for a student."""
    
    # Verify student access
    student_controller = StudentController()
    student = await student_controller.get_student_by_parent(current_user.id)
    
    if not student or student.student_id != student_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found or access denied"
        )
    
    insight_controller = InsightController()
    
    try:
        insight_response = await insight_controller.generate_weekly_summary(
            student_id=student_id,
            parent_id=current_user.id
        )
        
        return insight_response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate weekly summary: {str(e)}"
        )

@router.post("/{student_id}/subject-analysis/{subject}", response_model=InsightResponse)
async def generate_subject_analysis(
    student_id: str,
    subject: str,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Generate subject-specific analysis for a student."""
    
    # Verify student access
    student_controller = StudentController()
    student = await student_controller.get_student_by_parent(current_user.id)
    
    if not student or student.student_id != student_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found or access denied"
        )
    
    insight_controller = InsightController()
    
    try:
        insight_response = await insight_controller.generate_subject_specific_insight(
            student_id=student_id,
            parent_id=current_user.id,
            subject=subject
        )
        
        return insight_response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate subject analysis: {str(e)}"
        )

@router.get("/insight/{insight_id}", response_model=Insight)
async def get_insight_by_id(
    insight_id: str,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get a specific insight by ID."""
    
    insight_controller = InsightController()
    
    insight = await insight_controller.get_insight_by_id(
        insight_id=insight_id,
        parent_id=current_user.id
    )
    
    if not insight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insight not found or access denied"
        )
    
    return insight
