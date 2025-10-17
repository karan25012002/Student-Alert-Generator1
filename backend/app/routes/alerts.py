from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Any, Optional, List

from ..models.user import User
from ..models.alert import Alert, AlertCreate, AlertUpdate, AlertStats, AlertMarkRead
from ..controllers.alert_controller import AlertController
from ..controllers.student_controller import StudentController
from ..utils.auth import get_current_active_user

router = APIRouter()

@router.get("/{parent_id}", response_model=List[Alert])
async def get_alerts(
    parent_id: str,
    skip: int = Query(0, ge=0, description="Number of alerts to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of alerts to return"),
    unread_only: bool = Query(False, description="Return only unread alerts"),
    category: Optional[str] = Query(None, description="Filter by category"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get alerts for a parent."""
    
    # Verify the parent_id matches current user
    if parent_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    alert_controller = AlertController()
    
    alerts = await alert_controller.get_alerts_by_parent(
        parent_id=parent_id,
        skip=skip,
        limit=limit,
        unread_only=unread_only,
        category=category,
        priority=priority
    )
    
    return alerts

@router.get("/{parent_id}/stats", response_model=AlertStats)
async def get_alert_stats(
    parent_id: str,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get alert statistics for a parent."""
    
    # Verify the parent_id matches current user
    if parent_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    alert_controller = AlertController()
    stats = await alert_controller.get_alert_stats(parent_id)
    
    return stats

@router.patch("/{alert_id}/read")
async def mark_alert_as_read(
    alert_id: str,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Mark an alert as read."""
    
    alert_controller = AlertController()
    
    success = await alert_controller.mark_alert_as_read(alert_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found or access denied"
        )
    
    return {"message": "Alert marked as read"}

@router.patch("/{parent_id}/read-all")
async def mark_all_alerts_as_read(
    parent_id: str,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Mark all alerts as read for a parent."""
    
    # Verify the parent_id matches current user
    if parent_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    alert_controller = AlertController()
    
    count = await alert_controller.mark_all_alerts_as_read(parent_id)
    
    return {"message": f"Marked {count} alerts as read"}

@router.delete("/{alert_id}")
async def delete_alert(
    alert_id: str,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Delete an alert."""
    
    alert_controller = AlertController()
    
    success = await alert_controller.delete_alert(alert_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found or access denied"
        )
    
    return {"message": "Alert deleted"}

@router.post("/", response_model=Alert)
async def create_alert(
    alert_data: AlertCreate,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Create a new alert (admin only)."""
    
    # For now, allow parents to create alerts for testing
    # In production, this might be restricted to admin users or system-generated
    
    alert_controller = AlertController()
    
    try:
        alert = await alert_controller.create_alert(alert_data)
        return alert
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create alert"
        )

@router.post("/generate-samples")
async def generate_sample_alerts(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Generate sample alerts for demo purposes."""
    
    # Get student for current user
    student_controller = StudentController()
    student = await student_controller.get_student_by_parent(current_user.id)
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No student found for this parent"
        )
    
    alert_controller = AlertController()
    
    try:
        alerts = await alert_controller.generate_sample_alerts(
            parent_id=current_user.id,
            student_id=student.student_id
        )
        
        return {
            "message": f"Generated {len(alerts)} sample alerts",
            "alerts": alerts
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate sample alerts"
        )

@router.get("/alert/{alert_id}", response_model=Alert)
async def get_alert_by_id(
    alert_id: str,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get a specific alert by ID."""
    
    alert_controller = AlertController()
    
    alert = await alert_controller.get_alert_by_id(alert_id)
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    # Verify the alert belongs to the current user
    if alert.parent_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return alert
