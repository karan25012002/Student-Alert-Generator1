"""
AI-Powered Student Alert Generator using Google Gemini.
Analyzes student data and generates intelligent alerts with recommendations.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import google.generativeai as genai
from pydantic import BaseModel

from ..core.config import settings


class StudentAlertInput(BaseModel):
    """Input data for alert generation."""
    name: str
    roll_number: str
    attendance_percentage: float
    academic_performance: float  # GPA or marks
    behavior_notes: Optional[str] = ""
    participation_level: Optional[str] = "medium"  # low, medium, high
    additional_comments: Optional[str] = ""


class GeneratedAlert(BaseModel):
    """Generated alert with AI analysis."""
    alert_type: str  # warning, info, success, error
    priority: str  # low, medium, high
    category: str  # academic, attendance, engagement, general
    title: str
    message: str
    action_required: bool
    suggestions: List[str]
    reasoning: str  # AI's reasoning for this alert
    confidence_score: float


class AlertGeneratorAgent:
    """AI agent for generating student alerts using Google Gemini."""
    
    def __init__(self):
        self.model = None
        if settings.GOOGLE_API_KEY:
            try:
                genai.configure(api_key=settings.GOOGLE_API_KEY)
                self.model = genai.GenerativeModel('gemini-pro')
                print("✓ Gemini Alert Generator initialized successfully")
            except Exception as e:
                print(f"⚠ Failed to initialize Gemini: {e}")
                self.model = None
    
    async def generate_alerts(self, student_data: StudentAlertInput) -> List[GeneratedAlert]:
        """
        Generate intelligent alerts based on student data.
        Uses AI to analyze multiple parameters and create actionable alerts.
        """
        
        if self.model:
            try:
                return await self._generate_ai_alerts(student_data)
            except Exception as e:
                print(f"AI generation failed, using rule-based fallback: {e}")
                return self._generate_rule_based_alerts(student_data)
        else:
            return self._generate_rule_based_alerts(student_data)
    
    async def _generate_ai_alerts(self, student_data: StudentAlertInput) -> List[GeneratedAlert]:
        """Generate alerts using Google Gemini AI."""
        
        prompt = f"""
You are an intelligent educational alert system. Analyze the following student data and generate appropriate alerts.

Student Information:
- Name: {student_data.name}
- Roll Number: {student_data.roll_number}
- Attendance: {student_data.attendance_percentage}%
- Academic Performance: {student_data.academic_performance} (GPA/Marks)
- Behavior Notes: {student_data.behavior_notes or "No specific notes"}
- Participation Level: {student_data.participation_level}
- Additional Comments: {student_data.additional_comments or "None"}

Based on this data, generate 1-4 alerts (only generate alerts that are truly relevant). For each alert, provide:

1. Alert Type: Choose from [warning, info, success, error]
2. Priority: Choose from [low, medium, high]
3. Category: Choose from [academic, attendance, engagement, general]
4. Title: Brief, clear title (max 60 characters)
5. Message: Detailed explanation (2-3 sentences)
6. Action Required: true or false
7. Suggestions: 2-4 specific, actionable recommendations
8. Reasoning: Your analysis explaining why this alert was generated
9. Confidence Score: 0.0 to 1.0

Guidelines:
- Attendance < 75%: Generate HIGH priority warning
- Attendance 75-85%: Generate MEDIUM priority warning
- Attendance > 95%: Consider success alert
- GPA/Marks < 2.0 or 50%: Generate HIGH priority academic warning
- GPA/Marks 2.0-3.0 or 50-70%: Generate MEDIUM priority academic alert
- GPA/Marks > 3.5 or 85%: Consider success alert
- Behavior issues: Generate appropriate warnings
- Low participation: Generate engagement alerts
- Always be constructive and supportive in tone

Return the response as a valid JSON array of alerts. Example format:
[
  {{
    "alert_type": "warning",
    "priority": "high",
    "category": "attendance",
    "title": "Low Attendance Alert",
    "message": "Student attendance has fallen below acceptable threshold...",
    "action_required": true,
    "suggestions": ["Contact parents", "Schedule meeting", "Review attendance policy"],
    "reasoning": "Attendance at 65% is significantly below the 75% minimum requirement",
    "confidence_score": 0.95
  }}
]

Generate only relevant alerts. Return valid JSON only, no additional text.
"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean up response - remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()
            
            # Parse JSON response
            alerts_data = json.loads(response_text)
            
            # Convert to GeneratedAlert objects
            alerts = []
            for alert_dict in alerts_data:
                try:
                    alert = GeneratedAlert(**alert_dict)
                    alerts.append(alert)
                except Exception as e:
                    print(f"Failed to parse alert: {e}")
                    continue
            
            return alerts if alerts else self._generate_rule_based_alerts(student_data)
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Response was: {response_text[:200]}")
            return self._generate_rule_based_alerts(student_data)
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self._generate_rule_based_alerts(student_data)
    
    def _generate_rule_based_alerts(self, student_data: StudentAlertInput) -> List[GeneratedAlert]:
        """Fallback rule-based alert generation."""
        
        alerts = []
        
        # Attendance alerts
        if student_data.attendance_percentage < 75:
            alerts.append(GeneratedAlert(
                alert_type="error",
                priority="high",
                category="attendance",
                title="Critical Attendance Alert",
                message=f"{student_data.name}'s attendance is at {student_data.attendance_percentage}%, which is critically below the required 75% minimum. Immediate intervention is necessary to prevent academic consequences.",
                action_required=True,
                suggestions=[
                    "Schedule immediate meeting with student and parents",
                    "Review reasons for absences",
                    "Create attendance improvement plan",
                    "Monitor daily attendance closely"
                ],
                reasoning=f"Attendance at {student_data.attendance_percentage}% is below minimum threshold",
                confidence_score=0.95
            ))
        elif student_data.attendance_percentage < 85:
            alerts.append(GeneratedAlert(
                alert_type="warning",
                priority="medium",
                category="attendance",
                title="Attendance Needs Improvement",
                message=f"{student_data.name}'s attendance is at {student_data.attendance_percentage}%, which is below optimal levels. Consistent attendance is crucial for academic success.",
                action_required=True,
                suggestions=[
                    "Contact parents about attendance patterns",
                    "Identify barriers to regular attendance",
                    "Set attendance improvement goals"
                ],
                reasoning=f"Attendance at {student_data.attendance_percentage}% is below optimal range",
                confidence_score=0.85
            ))
        elif student_data.attendance_percentage >= 95:
            alerts.append(GeneratedAlert(
                alert_type="success",
                priority="low",
                category="attendance",
                title="Excellent Attendance Record",
                message=f"Congratulations! {student_data.name} has maintained excellent attendance at {student_data.attendance_percentage}%. This dedication to regular attendance supports academic success.",
                action_required=False,
                suggestions=[
                    "Recognize and reward consistent attendance",
                    "Use as positive example for other students"
                ],
                reasoning=f"Attendance at {student_data.attendance_percentage}% exceeds excellence threshold",
                confidence_score=0.90
            ))
        
        # Academic performance alerts
        if student_data.academic_performance < 2.0 or student_data.academic_performance < 50:
            alerts.append(GeneratedAlert(
                alert_type="error",
                priority="high",
                category="academic",
                title="Academic Performance Concern",
                message=f"{student_data.name}'s academic performance ({student_data.academic_performance}) is significantly below expectations. Immediate academic support and intervention are required.",
                action_required=True,
                suggestions=[
                    "Arrange tutoring or academic support sessions",
                    "Meet with teachers to identify specific challenges",
                    "Develop personalized learning plan",
                    "Consider additional study resources"
                ],
                reasoning=f"Academic performance of {student_data.academic_performance} is critically low",
                confidence_score=0.92
            ))
        elif student_data.academic_performance < 3.0 or student_data.academic_performance < 70:
            alerts.append(GeneratedAlert(
                alert_type="warning",
                priority="medium",
                category="academic",
                title="Academic Performance Below Average",
                message=f"{student_data.name}'s academic performance ({student_data.academic_performance}) shows room for improvement. Additional support could help achieve better results.",
                action_required=True,
                suggestions=[
                    "Review study habits and time management",
                    "Identify subjects needing extra attention",
                    "Consider peer study groups or tutoring"
                ],
                reasoning=f"Academic performance of {student_data.academic_performance} is below average",
                confidence_score=0.80
            ))
        elif student_data.academic_performance >= 3.5 or student_data.academic_performance >= 85:
            alerts.append(GeneratedAlert(
                alert_type="success",
                priority="low",
                category="academic",
                title="Outstanding Academic Performance",
                message=f"Excellent work! {student_data.name} is performing exceptionally well with a {student_data.academic_performance} performance level. This demonstrates strong academic capability.",
                action_required=False,
                suggestions=[
                    "Encourage continued excellence",
                    "Consider advanced or enrichment opportunities",
                    "Recognize achievement publicly"
                ],
                reasoning=f"Academic performance of {student_data.academic_performance} is excellent",
                confidence_score=0.88
            ))
        
        # Participation/Engagement alerts
        if student_data.participation_level == "low":
            alerts.append(GeneratedAlert(
                alert_type="warning",
                priority="medium",
                category="engagement",
                title="Low Class Participation",
                message=f"{student_data.name} shows low participation levels in class activities. Increased engagement could improve learning outcomes and social development.",
                action_required=True,
                suggestions=[
                    "Encourage active participation in discussions",
                    "Identify barriers to engagement",
                    "Create opportunities for comfortable participation",
                    "Build confidence through smaller group activities"
                ],
                reasoning="Low participation level indicates engagement concerns",
                confidence_score=0.75
            ))
        elif student_data.participation_level == "high":
            alerts.append(GeneratedAlert(
                alert_type="success",
                priority="low",
                category="engagement",
                title="Excellent Class Engagement",
                message=f"{student_data.name} demonstrates high levels of class participation and engagement. This active involvement enhances learning and contributes positively to the classroom environment.",
                action_required=False,
                suggestions=[
                    "Continue encouraging active participation",
                    "Consider leadership opportunities"
                ],
                reasoning="High participation level shows strong engagement",
                confidence_score=0.82
            ))
        
        # Behavior alerts
        if student_data.behavior_notes and len(student_data.behavior_notes) > 10:
            if any(word in student_data.behavior_notes.lower() for word in ['disruptive', 'concerning', 'issue', 'problem', 'inappropriate']):
                alerts.append(GeneratedAlert(
                    alert_type="warning",
                    priority="high",
                    category="general",
                    title="Behavioral Attention Required",
                    message=f"Behavioral concerns have been noted for {student_data.name}: {student_data.behavior_notes}. Addressing these issues promptly will support a positive learning environment.",
                    action_required=True,
                    suggestions=[
                        "Schedule counseling session",
                        "Meet with parents to discuss behavior",
                        "Develop behavior improvement plan",
                        "Identify underlying causes"
                    ],
                    reasoning="Behavior notes indicate concerns requiring attention",
                    confidence_score=0.85
                ))
            elif any(word in student_data.behavior_notes.lower() for word in ['excellent', 'outstanding', 'positive', 'good', 'respectful']):
                alerts.append(GeneratedAlert(
                    alert_type="success",
                    priority="low",
                    category="general",
                    title="Positive Behavior Recognition",
                    message=f"{student_data.name} demonstrates excellent behavior: {student_data.behavior_notes}. This positive conduct contributes to a productive learning environment.",
                    action_required=False,
                    suggestions=[
                        "Recognize positive behavior publicly",
                        "Continue positive reinforcement"
                    ],
                    reasoning="Behavior notes indicate positive conduct",
                    confidence_score=0.80
                ))
        
        return alerts
    
    def get_alert_summary(self, alerts: List[GeneratedAlert]) -> Dict[str, Any]:
        """Generate a summary of all alerts."""
        
        return {
            "total_alerts": len(alerts),
            "high_priority_count": len([a for a in alerts if a.priority == "high"]),
            "action_required_count": len([a for a in alerts if a.action_required]),
            "categories": {
                "academic": len([a for a in alerts if a.category == "academic"]),
                "attendance": len([a for a in alerts if a.category == "attendance"]),
                "engagement": len([a for a in alerts if a.category == "engagement"]),
                "general": len([a for a in alerts if a.category == "general"])
            },
            "types": {
                "error": len([a for a in alerts if a.alert_type == "error"]),
                "warning": len([a for a in alerts if a.alert_type == "warning"]),
                "success": len([a for a in alerts if a.alert_type == "success"]),
                "info": len([a for a in alerts if a.alert_type == "info"])
            },
            "average_confidence": sum(a.confidence_score for a in alerts) / len(alerts) if alerts else 0.0
        }
