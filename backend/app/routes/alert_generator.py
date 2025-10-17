"""
API routes for Student Alert Generator feature.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any, List

from ..models.user import User
from ..models.student_alert_request import (
    StudentAlertRequest, 
    AlertGenerationResponse, 
    GeneratedAlertResponse,
    SaveGeneratedAlertsRequest
)
from ..models.alert import AlertCreate
from ..services.alert_generator_agent import AlertGeneratorAgent, StudentAlertInput
from ..controllers.alert_controller import AlertController
from ..utils.auth import get_current_active_user

router = APIRouter()


@router.post("/generate", response_model=AlertGenerationResponse)
async def generate_student_alerts(
    request: StudentAlertRequest,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Generate AI-powered alerts for a student based on their information.
    
    This endpoint analyzes student data including attendance, academic performance,
    behavior, and participation to generate intelligent, actionable alerts.
    """
    
    try:
        # Initialize the AI alert generator
        agent = AlertGeneratorAgent()
        
        # Convert request to agent input format
        student_input = StudentAlertInput(
            name=request.name,
            roll_number=request.roll_number,
            attendance_percentage=request.attendance_percentage,
            academic_performance=request.academic_performance,
            behavior_notes=request.behavior_notes or "",
            participation_level=request.participation_level or "medium",
            additional_comments=request.additional_comments or ""
        )
        
        # Generate alerts using AI
        generated_alerts = await agent.generate_alerts(student_input)
        
        # Get summary
        summary = agent.get_alert_summary(generated_alerts)
        
        # Convert to response format
        alert_responses = [
            GeneratedAlertResponse(
                alert_type=alert.alert_type,
                priority=alert.priority,
                category=alert.category,
                title=alert.title,
                message=alert.message,
                action_required=alert.action_required,
                suggestions=alert.suggestions,
                reasoning=alert.reasoning,
                confidence_score=alert.confidence_score
            )
            for alert in generated_alerts
        ]
        
        return AlertGenerationResponse(
            student_name=request.name,
            student_roll_number=request.roll_number,
            alerts=alert_responses,
            summary=summary,
            ai_powered=agent.model is not None
        )
        
    except Exception as e:
        print(f"Error generating alerts: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate alerts: {str(e)}"
        )


@router.post("/generate-and-save")
async def generate_and_save_alerts(
    request: StudentAlertRequest,
    student_id: str,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Generate AI-powered alerts and save them to the database.
    
    This endpoint generates alerts and immediately saves them to the alerts collection,
    making them visible on the dashboard.
    """
    
    try:
        # Initialize the AI alert generator
        agent = AlertGeneratorAgent()
        
        # Convert request to agent input format
        student_input = StudentAlertInput(
            name=request.name,
            roll_number=request.roll_number,
            attendance_percentage=request.attendance_percentage,
            academic_performance=request.academic_performance,
            behavior_notes=request.behavior_notes or "",
            participation_level=request.participation_level or "medium",
            additional_comments=request.additional_comments or ""
        )
        
        # Generate alerts using AI
        generated_alerts = await agent.generate_alerts(student_input)
        
        # Save alerts to database
        alert_controller = AlertController()
        saved_alerts = []
        
        for alert in generated_alerts:
            alert_create = AlertCreate(
                parent_id=current_user.id,
                student_id=student_id,
                title=alert.title,
                message=alert.message,
                type=alert.alert_type,
                priority=alert.priority,
                category=alert.category,
                action_required=alert.action_required,
                suggestions=alert.suggestions,
                metadata={
                    "reasoning": alert.reasoning,
                    "confidence_score": alert.confidence_score,
                    "ai_generated": True,
                    "student_name": request.name,
                    "student_roll_number": request.roll_number
                }
            )
            
            saved_alert = await alert_controller.create_alert(alert_create)
            saved_alerts.append(saved_alert)
        
        # Get summary
        summary = agent.get_alert_summary(generated_alerts)
        
        return {
            "message": f"Successfully generated and saved {len(saved_alerts)} alerts",
            "student_name": request.name,
            "student_roll_number": request.roll_number,
            "alerts": saved_alerts,
            "summary": summary,
            "ai_powered": agent.model is not None
        }
        
    except Exception as e:
        print(f"Error generating and saving alerts: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate and save alerts: {str(e)}"
        )


@router.post("/save-generated-alerts")
async def save_generated_alerts(
    request: SaveGeneratedAlertsRequest,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Save previously generated alerts to the database.
    
    This endpoint allows saving alerts that were generated on the frontend
    to the database for persistence and dashboard display.
    """
    
    # Verify the parent_id matches current user
    if request.parent_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    try:
        alert_controller = AlertController()
        saved_alerts = []
        
        for alert in request.alerts:
            alert_create = AlertCreate(
                parent_id=request.parent_id,
                student_id=request.student_id,
                title=alert.title,
                message=alert.message,
                type=alert.alert_type,
                priority=alert.priority,
                category=alert.category,
                action_required=alert.action_required,
                suggestions=alert.suggestions,
                metadata={
                    "reasoning": alert.reasoning,
                    "confidence_score": alert.confidence_score,
                    "ai_generated": True
                }
            )
            
            saved_alert = await alert_controller.create_alert(alert_create)
            saved_alerts.append(saved_alert)
        
        return {
            "message": f"Successfully saved {len(saved_alerts)} alerts",
            "alerts": saved_alerts
        }
        
    except Exception as e:
        print(f"Error saving alerts: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save alerts: {str(e)}"
        )


@router.get("/test-connection")
async def test_alert_generator(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Test the alert generator service and AI connection.
    """
    
    agent = AlertGeneratorAgent()
    
    return {
        "status": "operational",
        "ai_available": agent.model is not None,
        "message": "Alert generator is ready" if agent.model else "Using rule-based fallback"
    }
