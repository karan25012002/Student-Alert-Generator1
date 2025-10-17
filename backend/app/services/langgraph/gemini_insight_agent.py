from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
import random
import google.generativeai as genai
from pydantic import BaseModel

from ...core.config import settings
from ...models.insight import InsightResponse, ConversationMessage

class StudentAnalysisState(BaseModel):
    student_id: str
    query: str
    academic_data: Optional[Dict] = None
    attendance_data: Optional[Dict] = None
    engagement_data: Optional[Dict] = None
    analysis_results: Optional[Dict] = None
    recommendations: List[str] = []
    confidence_score: float = 0.0

class GeminiInsightAgent:
    def __init__(self):
        self.model = None
        if settings.GOOGLE_API_KEY:
            try:
                genai.configure(api_key=settings.GOOGLE_API_KEY)
                self.model = genai.GenerativeModel('gemini-pro')
            except Exception as e:
                print(f"Failed to initialize Gemini: {e}")
                self.model = None

    async def generate_insight(
        self, 
        student_id: str, 
        query: str, 
        academic_data: Dict = None,
        attendance_data: Dict = None,
        engagement_data: Dict = None
    ) -> InsightResponse:
        """Generate AI-powered insights for a student using Gemini."""
        
        try:
            # Collect and prepare data
            if not academic_data:
                academic_data = self._generate_mock_academic_data()
            if not attendance_data:
                attendance_data = self._generate_mock_attendance_data()
            if not engagement_data:
                engagement_data = self._generate_mock_engagement_data()
            
            # Analyze data
            analysis = self._analyze_student_data(academic_data, attendance_data, engagement_data)
            
            # Generate insights using Gemini
            if self.model:
                insight_text = await self._generate_gemini_insights(query, analysis)
                recommendations = await self._generate_gemini_recommendations(analysis)
                confidence = 0.85
            else:
                # Fallback to rule-based insights
                insight_text = self._generate_rule_based_insights(analysis)
                recommendations = self._generate_rule_based_recommendations(analysis)
                confidence = 0.75
            
            return InsightResponse(
                insight=insight_text,
                recommendations=recommendations,
                confidence=confidence,
                data_used=["academic_performance", "attendance_records", "engagement_metrics"],
                generated_at=datetime.utcnow()
            )
            
        except Exception as e:
            print(f"Error generating insight: {e}")
            return await self._fallback_insight(query)

    async def _generate_gemini_insights(self, query: str, analysis: Dict) -> str:
        """Generate insights using Google Gemini."""
        
        prompt = f"""
        You are an educational AI assistant helping parents understand their child's academic progress.
        
        Parent's Question: {query}
        
        Student Data Analysis:
        - Academic Performance: {json.dumps(analysis.get('academic_summary', {}), indent=2)}
        - Attendance Patterns: {json.dumps(analysis.get('attendance_summary', {}), indent=2)}
        - Engagement Metrics: {json.dumps(analysis.get('engagement_summary', {}), indent=2)}
        - Key Trends: {json.dumps(analysis.get('trends', {}), indent=2)}
        
        Please provide a clear, parent-friendly insight about this student's performance. Focus on:
        1. Current performance status
        2. Notable trends or patterns
        3. Areas of strength
        4. Areas needing attention
        
        Keep the response concise (2-3 sentences) and actionable for parents.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self._generate_rule_based_insights(analysis)

    async def _generate_gemini_recommendations(self, analysis: Dict) -> List[str]:
        """Generate recommendations using Google Gemini."""
        
        prompt = f"""
        Based on this student's performance data, provide 3-5 specific, actionable recommendations for parents:
        
        Student Analysis:
        {json.dumps(analysis, indent=2)}
        
        Provide recommendations as a simple list, each recommendation should be:
        - Specific and actionable
        - Appropriate for parents to implement
        - Focused on improving the student's performance
        
        Format as a numbered list.
        """
        
        try:
            response = self.model.generate_content(prompt)
            recommendations_text = response.text.strip()
            
            # Parse the numbered list into individual recommendations
            recommendations = []
            for line in recommendations_text.split('\n'):
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                    # Remove numbering and clean up
                    clean_rec = line.split('.', 1)[-1].strip() if '.' in line else line.strip()
                    clean_rec = clean_rec.lstrip('- •').strip()
                    if clean_rec:
                        recommendations.append(clean_rec)
            
            return recommendations[:5]  # Limit to 5 recommendations
            
        except Exception as e:
            print(f"Gemini API error for recommendations: {e}")
            return self._generate_rule_based_recommendations(analysis)

    def _analyze_student_data(self, academic_data: Dict, attendance_data: Dict, engagement_data: Dict) -> Dict:
        """Analyze student data to extract key insights."""
        
        analysis = {
            "academic_summary": self._analyze_academic_performance(academic_data),
            "attendance_summary": self._analyze_attendance_patterns(attendance_data),
            "engagement_summary": self._analyze_engagement_metrics(engagement_data),
            "trends": self._identify_trends(academic_data, attendance_data, engagement_data)
        }
        
        return analysis

    def _analyze_academic_performance(self, academic_data: Dict) -> Dict:
        """Analyze academic performance data."""
        if not academic_data:
            return {}
        
        subjects = academic_data.get("subjects", [])
        overall_gpa = academic_data.get("overall_gpa", 0)
        
        strong_subjects = []
        weak_subjects = []
        improving_subjects = []
        declining_subjects = []
        
        for subject in subjects:
            percentage = subject.get("percentage", 0)
            trend = subject.get("trend", "stable")
            subject_name = subject.get("subject", "Unknown")
            
            if percentage >= 90:
                strong_subjects.append(subject_name)
            elif percentage < 75:
                weak_subjects.append(subject_name)
            
            if trend == "up":
                improving_subjects.append(subject_name)
            elif trend == "down":
                declining_subjects.append(subject_name)
        
        return {
            "overall_gpa": overall_gpa,
            "strong_subjects": strong_subjects,
            "weak_subjects": weak_subjects,
            "improving_subjects": improving_subjects,
            "declining_subjects": declining_subjects,
            "total_subjects": len(subjects)
        }

    def _analyze_attendance_patterns(self, attendance_data: Dict) -> Dict:
        """Analyze attendance patterns."""
        if not attendance_data:
            return {}
        
        overall_rate = attendance_data.get("overall_percentage", 0)
        late_days = attendance_data.get("late_days", 0)
        absent_days = attendance_data.get("absent_days", 0)
        
        return {
            "overall_rate": overall_rate,
            "late_days": late_days,
            "absent_days": absent_days,
            "attendance_status": "excellent" if overall_rate >= 95 else "good" if overall_rate >= 90 else "needs_improvement",
            "punctuality_concern": late_days > 5
        }

    def _analyze_engagement_metrics(self, engagement_data: Dict) -> Dict:
        """Analyze engagement metrics."""
        if not engagement_data:
            return {}
        
        overall_score = engagement_data.get("overall_engagement_score", 0)
        study_hours = engagement_data.get("total_study_hours", 0)
        participation = engagement_data.get("participation_score", 0)
        
        return {
            "overall_score": overall_score,
            "study_hours_per_week": study_hours,
            "participation_score": participation,
            "engagement_level": "high" if overall_score >= 85 else "moderate" if overall_score >= 70 else "low",
            "study_time_adequate": study_hours >= 20
        }

    def _identify_trends(self, academic_data: Dict, attendance_data: Dict, engagement_data: Dict) -> Dict:
        """Identify key trends across all data."""
        trends = {}
        
        # Academic trends
        if academic_data and academic_data.get("subjects"):
            declining_count = sum(1 for s in academic_data["subjects"] if s.get("trend") == "down")
            improving_count = sum(1 for s in academic_data["subjects"] if s.get("trend") == "up")
            
            if declining_count > improving_count:
                trends["academic_trend"] = "declining"
            elif improving_count > declining_count:
                trends["academic_trend"] = "improving"
            else:
                trends["academic_trend"] = "stable"
        
        # Attendance trends
        if attendance_data:
            attendance_rate = attendance_data.get("overall_percentage", 0)
            if attendance_rate >= 95:
                trends["attendance_trend"] = "excellent"
            elif attendance_rate >= 90:
                trends["attendance_trend"] = "good"
            else:
                trends["attendance_trend"] = "concerning"
        
        # Engagement trends
        if engagement_data:
            engagement_score = engagement_data.get("overall_engagement_score", 0)
            if engagement_score >= 85:
                trends["engagement_trend"] = "high"
            elif engagement_score >= 70:
                trends["engagement_trend"] = "moderate"
            else:
                trends["engagement_trend"] = "low"
        
        return trends

    def _generate_rule_based_insights(self, analysis: Dict) -> str:
        """Generate insights using rule-based logic when Gemini is unavailable."""
        
        insights = []
        
        # Academic insights
        academic = analysis.get("academic_summary", {})
        if academic.get("overall_gpa", 0) > 3.5:
            insights.append("Your child is performing well academically with a strong GPA.")
        elif academic.get("declining_subjects"):
            subjects = ", ".join(academic["declining_subjects"][:2])
            insights.append(f"Academic performance shows some decline in {subjects}.")
        
        # Attendance insights
        attendance = analysis.get("attendance_summary", {})
        if attendance.get("attendance_status") == "excellent":
            insights.append("Excellent attendance record supports consistent learning.")
        elif attendance.get("attendance_status") == "needs_improvement":
            insights.append("Attendance could be improved for better academic outcomes.")
        
        # Engagement insights
        engagement = analysis.get("engagement_summary", {})
        if engagement.get("engagement_level") == "high":
            insights.append("High engagement levels show active participation in learning.")
        elif engagement.get("engagement_level") == "low":
            insights.append("Engagement could be enhanced through more interactive learning approaches.")
        
        return " ".join(insights) if insights else "Overall performance is within normal ranges with opportunities for growth."

    def _generate_rule_based_recommendations(self, analysis: Dict) -> List[str]:
        """Generate recommendations using rule-based logic."""
        
        recommendations = []
        
        # Academic recommendations
        academic = analysis.get("academic_summary", {})
        if academic.get("declining_subjects"):
            for subject in academic["declining_subjects"][:2]:
                recommendations.append(f"Consider additional tutoring or practice in {subject}")
        
        if academic.get("weak_subjects"):
            recommendations.append("Focus on strengthening performance in challenging subjects")
        
        # Attendance recommendations
        attendance = analysis.get("attendance_summary", {})
        if attendance.get("attendance_status") == "needs_improvement":
            recommendations.append("Establish consistent morning routines to improve attendance")
        
        if attendance.get("punctuality_concern"):
            recommendations.append("Work on time management to reduce tardiness")
        
        # Engagement recommendations
        engagement = analysis.get("engagement_summary", {})
        if engagement.get("engagement_level") == "low":
            recommendations.append("Explore interactive learning methods to boost engagement")
        
        if not engagement.get("study_time_adequate"):
            recommendations.append("Increase dedicated study time to meet grade-level expectations")
        
        # General recommendations
        recommendations.append("Maintain regular communication with teachers")
        recommendations.append("Celebrate achievements to maintain motivation")
        
        return recommendations[:5]

    async def _fallback_insight(self, query: str) -> InsightResponse:
        """Provide fallback insight when all else fails."""
        
        fallback_insights = [
            "Your child shows consistent academic performance with room for improvement in key areas.",
            "Overall progress is positive with steady development across multiple subjects.",
            "Current performance indicates good potential with opportunities for enhancement.",
            "Academic journey is on track with some areas requiring focused attention."
        ]
        
        fallback_recommendations = [
            "Maintain regular study schedule",
            "Communicate regularly with teachers",
            "Provide supportive learning environment at home",
            "Encourage participation in class activities",
            "Monitor homework completion consistently"
        ]
        
        return InsightResponse(
            insight=random.choice(fallback_insights),
            recommendations=random.sample(fallback_recommendations, 3),
            confidence=0.65,
            data_used=["academic_performance", "attendance_records", "engagement_metrics"],
            generated_at=datetime.utcnow()
        )

    def _generate_mock_academic_data(self) -> Dict:
        """Generate mock academic data for testing."""
        return {
            "overall_gpa": random.uniform(3.0, 3.8),
            "subjects": [
                {"subject": "Mathematics", "grade": "B+", "trend": "down", "percentage": 85},
                {"subject": "Science", "grade": "A-", "trend": "up", "percentage": 90},
                {"subject": "English", "grade": "A", "trend": "stable", "percentage": 92},
                {"subject": "History", "grade": "B", "trend": "down", "percentage": 78},
                {"subject": "Geography", "grade": "A-", "trend": "up", "percentage": 87}
            ]
        }

    def _generate_mock_attendance_data(self) -> Dict:
        """Generate mock attendance data for testing."""
        return {
            "overall_percentage": random.uniform(88, 96),
            "late_days": random.randint(2, 8),
            "absent_days": random.randint(3, 12)
        }

    def _generate_mock_engagement_data(self) -> Dict:
        """Generate mock engagement data for testing."""
        return {
            "overall_engagement_score": random.uniform(75, 92),
            "total_study_hours": random.uniform(18, 28),
            "participation_score": random.uniform(80, 95)
        }
