from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from ..database.mongodb import get_db
from ..models.insight import (
    Insight, InsightCreate, InsightInDB, InsightQuery, 
    InsightResponse, ConversationHistory, ConversationMessage
)
from ..services.langgraph.gemini_insight_agent import GeminiInsightAgent
from .student_controller import StudentController

class InsightController:
    def __init__(self):
        self.insights_collection = "insights"
        self.conversations_collection = "conversations"
        self.insight_agent = GeminiInsightAgent()
        self.student_controller = StudentController()

    async def get_db(self) -> AsyncIOMotorDatabase:
        return await get_db()

    async def generate_insight(
        self, 
        student_id: str, 
        parent_id: str, 
        query: InsightQuery
    ) -> InsightResponse:
        """Generate AI-powered insight for a student."""
        
        # Get student data
        academic_data = await self.student_controller.get_academic_performance(student_id)
        attendance_data = await self.student_controller.get_attendance_data(student_id)
        engagement_data = await self.student_controller.get_engagement_data(student_id)
        
        # Convert to dict format for the AI agent
        academic_dict = academic_data if isinstance(academic_data, dict) else academic_data.dict() if academic_data else None
        attendance_dict = attendance_data.dict() if attendance_data else None
        engagement_dict = engagement_data.dict() if engagement_data else None
        
        # Generate insight using LangGraph agent
        insight_response = await self.insight_agent.generate_insight(
            student_id=student_id,
            query=query.query,
            academic_data=academic_dict,
            attendance_data=attendance_dict,
            engagement_data=engagement_dict
        )
        
        # Store the insight in database
        await self._store_insight(
            student_id=student_id,
            parent_id=parent_id,
            query=query.query,
            response=insight_response
        )
        
        # Update conversation history
        await self._update_conversation(
            parent_id=parent_id,
            student_id=student_id,
            user_message=query.query,
            ai_response=insight_response.insight
        )
        
        return insight_response

    async def get_insights_by_student(
        self, 
        student_id: str, 
        parent_id: str,
        skip: int = 0, 
        limit: int = 20
    ) -> List[Insight]:
        """Get insights for a student."""
        db = await self.get_db()
        
        cursor = db[self.insights_collection].find({
            "student_id": student_id,
            "parent_id": parent_id,
            "is_active": True
        }).sort("created_at", -1).skip(skip).limit(limit)
        
        insights = []
        async for insight_doc in cursor:
            insights.append(self._convert_to_insight(insight_doc))
        
        return insights

    async def get_insight_by_id(self, insight_id: str, parent_id: str) -> Optional[Insight]:
        """Get insight by ID."""
        db = await self.get_db()
        
        try:
            object_id = ObjectId(insight_id)
            insight_doc = await db[self.insights_collection].find_one({
                "_id": object_id,
                "parent_id": parent_id
            })
            
            if insight_doc:
                return self._convert_to_insight(insight_doc)
        except Exception:
            pass
        
        return None

    async def get_conversation_history(
        self, 
        parent_id: str, 
        student_id: str,
        limit: int = 50
    ) -> Optional[ConversationHistory]:
        """Get conversation history for a parent-student pair."""
        db = await self.get_db()
        
        conversation_doc = await db[self.conversations_collection].find_one({
            "parent_id": parent_id,
            "student_id": student_id,
            "is_active": True
        })
        
        if conversation_doc:
            # Limit messages to the most recent ones
            messages = conversation_doc.get("messages", [])[-limit:]
            conversation_doc["messages"] = messages
            return self._convert_to_conversation(conversation_doc)
        
        return None

    async def clear_conversation_history(self, parent_id: str, student_id: str) -> bool:
        """Clear conversation history for a parent-student pair."""
        db = await self.get_db()
        
        result = await db[self.conversations_collection].update_one(
            {
                "parent_id": parent_id,
                "student_id": student_id
            },
            {
                "$set": {
                    "messages": [],
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        return result.modified_count > 0

    async def get_insight_summary(self, student_id: str, parent_id: str) -> Dict[str, Any]:
        """Get a summary of insights for a student."""
        db = await self.get_db()
        
        # Get recent insights
        recent_insights = await self.get_insights_by_student(student_id, parent_id, limit=5)
        
        # Get insight statistics
        total_insights = await db[self.insights_collection].count_documents({
            "student_id": student_id,
            "parent_id": parent_id,
            "is_active": True
        })
        
        # Get insights by type
        pipeline = [
            {
                "$match": {
                    "student_id": student_id,
                    "parent_id": parent_id,
                    "is_active": True
                }
            },
            {
                "$group": {
                    "_id": "$insight_type",
                    "count": {"$sum": 1}
                }
            }
        ]
        
        type_cursor = db[self.insights_collection].aggregate(pipeline)
        insights_by_type = {}
        async for doc in type_cursor:
            insights_by_type[doc["_id"]] = doc["count"]
        
        # Calculate average confidence
        pipeline = [
            {
                "$match": {
                    "student_id": student_id,
                    "parent_id": parent_id,
                    "is_active": True
                }
            },
            {
                "$group": {
                    "_id": None,
                    "avg_confidence": {"$avg": "$confidence_score"}
                }
            }
        ]
        
        confidence_cursor = db[self.insights_collection].aggregate(pipeline)
        avg_confidence = 0.0
        async for doc in confidence_cursor:
            avg_confidence = doc.get("avg_confidence", 0.0)
        
        return {
            "total_insights": total_insights,
            "recent_insights": recent_insights,
            "insights_by_type": insights_by_type,
            "average_confidence": avg_confidence,
            "last_generated": recent_insights[0].created_at if recent_insights else None
        }

    async def generate_weekly_summary(self, student_id: str, parent_id: str) -> InsightResponse:
        """Generate a weekly summary insight."""
        
        # Get data for the past week
        week_start = datetime.utcnow() - timedelta(days=7)
        
        query = InsightQuery(
            query=f"Provide a comprehensive weekly summary of the student's performance, highlighting key achievements, areas of concern, and recommendations for the upcoming week.",
            context="weekly_summary"
        )
        
        return await self.generate_insight(student_id, parent_id, query)

    async def generate_subject_specific_insight(
        self, 
        student_id: str, 
        parent_id: str, 
        subject: str
    ) -> InsightResponse:
        """Generate subject-specific insight."""
        
        query = InsightQuery(
            query=f"Analyze the student's performance specifically in {subject}. Include recent grades, participation, engagement, and specific recommendations for improvement.",
            context=f"subject_analysis_{subject.lower()}"
        )
        
        return await self.generate_insight(student_id, parent_id, query)

    async def _store_insight(
        self, 
        student_id: str, 
        parent_id: str, 
        query: str, 
        response: InsightResponse
    ) -> Insight:
        """Store generated insight in database."""
        db = await self.get_db()
        
        # Determine insight type based on query content
        insight_type = self._classify_insight_type(query)
        
        insight_data = {
            "student_id": student_id,
            "parent_id": parent_id,
            "title": self._generate_insight_title(query, response),
            "content": response.insight,
            "insight_type": insight_type,
            "confidence_score": response.confidence,
            "data_sources": response.data_used,
            "recommendations": response.recommendations,
            "metadata": {
                "query": query,
                "generated_at": response.generated_at.isoformat()
            },
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_active": True
        }
        
        result = await db[self.insights_collection].insert_one(insight_data)
        
        # Return created insight
        created_insight = await db[self.insights_collection].find_one({"_id": result.inserted_id})
        return self._convert_to_insight(created_insight)

    async def _update_conversation(
        self, 
        parent_id: str, 
        student_id: str, 
        user_message: str, 
        ai_response: str
    ):
        """Update conversation history."""
        db = await self.get_db()
        
        # Create message objects
        user_msg = {
            "role": "user",
            "content": user_message,
            "timestamp": datetime.utcnow()
        }
        
        ai_msg = {
            "role": "assistant",
            "content": ai_response,
            "timestamp": datetime.utcnow()
        }
        
        # Update or create conversation
        await db[self.conversations_collection].update_one(
            {
                "parent_id": parent_id,
                "student_id": student_id
            },
            {
                "$push": {
                    "messages": {
                        "$each": [user_msg, ai_msg],
                        "$slice": -100  # Keep only last 100 messages
                    }
                },
                "$set": {
                    "updated_at": datetime.utcnow()
                },
                "$setOnInsert": {
                    "created_at": datetime.utcnow(),
                    "is_active": True
                }
            },
            upsert=True
        )

    def _classify_insight_type(self, query: str) -> str:
        """Classify insight type based on query content."""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["grade", "score", "academic", "subject", "test", "exam"]):
            return "academic"
        elif any(word in query_lower for word in ["attendance", "absent", "present", "late"]):
            return "attendance"
        elif any(word in query_lower for word in ["engagement", "participation", "activity", "focus"]):
            return "engagement"
        elif any(word in query_lower for word in ["behavior", "conduct", "discipline"]):
            return "behavioral"
        else:
            return "recommendation"

    def _generate_insight_title(self, query: str, response: InsightResponse) -> str:
        """Generate a title for the insight."""
        query_words = query.split()[:5]  # First 5 words
        return f"Insight: {' '.join(query_words)}..."

    def _convert_to_insight(self, insight_doc: dict) -> Insight:
        """Convert database document to Insight model."""
        insight_doc["id"] = str(insight_doc["_id"])
        del insight_doc["_id"]
        return Insight(**insight_doc)

    def _convert_to_conversation(self, conversation_doc: dict) -> ConversationHistory:
        """Convert database document to ConversationHistory model."""
        conversation_doc["id"] = str(conversation_doc["_id"])
        del conversation_doc["_id"]
        
        # Convert message timestamps
        messages = []
        for msg in conversation_doc.get("messages", []):
            messages.append(ConversationMessage(**msg))
        
        conversation_doc["messages"] = messages
        return ConversationHistory(**conversation_doc)
