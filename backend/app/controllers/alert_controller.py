from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
import random

from ..database.mongodb import get_db
from ..models.alert import Alert, AlertCreate, AlertUpdate, AlertInDB, AlertStats

class AlertController:
    def __init__(self):
        self.collection_name = "alerts"

    async def get_db(self) -> AsyncIOMotorDatabase:
        return await get_db()

    async def create_alert(self, alert_data: AlertCreate) -> Alert:
        """Create a new alert."""
        db = await self.get_db()
        
        # Create alert document
        alert_dict = alert_data.dict()
        alert_dict["read"] = False
        alert_dict["created_at"] = datetime.utcnow()
        alert_dict["updated_at"] = datetime.utcnow()
        
        # Set expiration date (30 days from now)
        alert_dict["expires_at"] = datetime.utcnow() + timedelta(days=30)
        
        # Insert alert
        result = await db[self.collection_name].insert_one(alert_dict)
        
        # Return created alert
        created_alert = await db[self.collection_name].find_one({"_id": result.inserted_id})
        return self._convert_to_alert(created_alert)

    async def get_alerts_by_parent(
        self, 
        parent_id: str, 
        skip: int = 0, 
        limit: int = 50,
        unread_only: bool = False,
        category: Optional[str] = None,
        priority: Optional[str] = None
    ) -> List[Alert]:
        """Get alerts for a parent with optional filters."""
        db = await self.get_db()
        
        # Build query
        query = {"parent_id": parent_id}
        
        if unread_only:
            query["read"] = False
            
        if category:
            query["category"] = category
            
        if priority:
            query["priority"] = priority
        
        # Get alerts sorted by creation date (newest first) and priority
        cursor = db[self.collection_name].find(query).sort([
            ("priority", -1),  # High priority first
            ("created_at", -1)  # Newest first
        ]).skip(skip).limit(limit)
        
        alerts = []
        async for alert_doc in cursor:
            alerts.append(self._convert_to_alert(alert_doc))
        
        return alerts

    async def get_alert_by_id(self, alert_id: str) -> Optional[Alert]:
        """Get alert by ID."""
        db = await self.get_db()
        
        try:
            object_id = ObjectId(alert_id)
            alert_doc = await db[self.collection_name].find_one({"_id": object_id})
            
            if alert_doc:
                return self._convert_to_alert(alert_doc)
        except Exception:
            pass
        
        return None

    async def mark_alert_as_read(self, alert_id: str, parent_id: str) -> bool:
        """Mark alert as read."""
        db = await self.get_db()
        
        try:
            object_id = ObjectId(alert_id)
            
            result = await db[self.collection_name].update_one(
                {"_id": object_id, "parent_id": parent_id},
                {
                    "$set": {
                        "read": True,
                        "read_at": datetime.utcnow(),
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            return result.modified_count > 0
            
        except Exception:
            return False

    async def mark_all_alerts_as_read(self, parent_id: str) -> int:
        """Mark all unread alerts as read for a parent."""
        db = await self.get_db()
        
        result = await db[self.collection_name].update_many(
            {"parent_id": parent_id, "read": False},
            {
                "$set": {
                    "read": True,
                    "read_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        return result.modified_count

    async def delete_alert(self, alert_id: str, parent_id: str) -> bool:
        """Delete an alert."""
        db = await self.get_db()
        
        try:
            object_id = ObjectId(alert_id)
            
            result = await db[self.collection_name].delete_one(
                {"_id": object_id, "parent_id": parent_id}
            )
            
            return result.deleted_count > 0
            
        except Exception:
            return False

    async def get_alert_stats(self, parent_id: str) -> AlertStats:
        """Get alert statistics for a parent."""
        db = await self.get_db()
        
        # Get total alerts
        total_alerts = await db[self.collection_name].count_documents({"parent_id": parent_id})
        
        # Get unread alerts
        unread_alerts = await db[self.collection_name].count_documents({
            "parent_id": parent_id,
            "read": False
        })
        
        # Get high priority alerts
        high_priority_alerts = await db[self.collection_name].count_documents({
            "parent_id": parent_id,
            "priority": "high",
            "read": False
        })
        
        # Get alerts by category
        pipeline = [
            {"$match": {"parent_id": parent_id}},
            {"$group": {"_id": "$category", "count": {"$sum": 1}}}
        ]
        category_cursor = db[self.collection_name].aggregate(pipeline)
        alerts_by_category = {}
        async for doc in category_cursor:
            alerts_by_category[doc["_id"]] = doc["count"]
        
        # Get alerts by type
        pipeline = [
            {"$match": {"parent_id": parent_id}},
            {"$group": {"_id": "$type", "count": {"$sum": 1}}}
        ]
        type_cursor = db[self.collection_name].aggregate(pipeline)
        alerts_by_type = {}
        async for doc in type_cursor:
            alerts_by_type[doc["_id"]] = doc["count"]
        
        # Get recent alerts (last 5)
        recent_alerts = await self.get_alerts_by_parent(parent_id, limit=5)
        
        return AlertStats(
            total_alerts=total_alerts,
            unread_alerts=unread_alerts,
            high_priority_alerts=high_priority_alerts,
            alerts_by_category=alerts_by_category,
            alerts_by_type=alerts_by_type,
            recent_alerts=recent_alerts
        )

    async def generate_sample_alerts(self, parent_id: str, student_id: str) -> List[Alert]:
        """Generate sample alerts for demo purposes."""
        sample_alerts = [
            {
                "parent_id": parent_id,
                "student_id": student_id,
                "title": "Math Performance Decline",
                "message": "Your child's math scores have dropped by 12% over the past two weeks. Recent quiz scores: 78%, 72%, 75%. Consider scheduling additional tutoring sessions.",
                "type": "warning",
                "priority": "high",
                "category": "academic",
                "action_required": True,
                "suggestions": [
                    "Schedule a meeting with the math teacher",
                    "Consider hiring a tutor",
                    "Review homework completion patterns"
                ]
            },
            {
                "parent_id": parent_id,
                "student_id": student_id,
                "title": "Excellent English Performance",
                "message": "Outstanding work in English class! Your child scored 95% on the recent essay and has maintained consistent A grades throughout the semester.",
                "type": "success",
                "priority": "low",
                "category": "academic",
                "action_required": False,
                "suggestions": []
            },
            {
                "parent_id": parent_id,
                "student_id": student_id,
                "title": "Attendance Alert",
                "message": "Attendance has dropped to 89% this month, below the required 95% threshold. Missing classes: Oct 8, Oct 12, Oct 14.",
                "type": "warning",
                "priority": "medium",
                "category": "attendance",
                "action_required": True,
                "suggestions": [
                    "Contact school about missed days",
                    "Ensure proper health management",
                    "Set up morning routine reminders"
                ]
            },
            {
                "parent_id": parent_id,
                "student_id": student_id,
                "title": "Low Engagement in History",
                "message": "Class participation in History has decreased significantly. Teacher notes indicate minimal interaction during discussions and group activities.",
                "type": "warning",
                "priority": "medium",
                "category": "engagement",
                "action_required": True,
                "suggestions": [
                    "Discuss interest in history topics",
                    "Meet with history teacher",
                    "Explore engaging history resources"
                ]
            },
            {
                "parent_id": parent_id,
                "student_id": student_id,
                "title": "Perfect Week Attendance",
                "message": "Congratulations! Your child maintained perfect attendance this week and arrived on time every day.",
                "type": "success",
                "priority": "low",
                "category": "attendance",
                "action_required": False,
                "suggestions": []
            }
        ]
        
        created_alerts = []
        for alert_data in sample_alerts:
            alert_create = AlertCreate(**alert_data)
            created_alert = await self.create_alert(alert_create)
            created_alerts.append(created_alert)
        
        return created_alerts

    async def cleanup_expired_alerts(self) -> int:
        """Clean up expired alerts."""
        db = await self.get_db()
        
        result = await db[self.collection_name].delete_many({
            "expires_at": {"$lt": datetime.utcnow()}
        })
        
        return result.deleted_count

    def _convert_to_alert(self, alert_doc: dict) -> Alert:
        """Convert database document to Alert model."""
        alert_doc["id"] = str(alert_doc["_id"])
        del alert_doc["_id"]
        return Alert(**alert_doc)
