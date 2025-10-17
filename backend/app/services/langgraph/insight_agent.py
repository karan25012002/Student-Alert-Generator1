from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
import random
from langchain.schema import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain.chat_models import ChatOpenAI
from langgraph import StateGraph, END
from langgraph.graph import MessageGraph
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
    messages: List[BaseMessage] = []

class InsightAgent:
    def __init__(self):
        self.llm = None
        if settings.OPENAI_API_KEY:
            try:
                self.llm = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    temperature=0.3,
                    openai_api_key=settings.OPENAI_API_KEY
                )
            except Exception:
                pass
        
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow for student analysis."""
        workflow = StateGraph(StudentAnalysisState)
        
        # Add nodes
        workflow.add_node("data_collector", self._collect_data)
        workflow.add_node("analyzer", self._analyze_data)
        workflow.add_node("insight_generator", self._generate_insights)
        workflow.add_node("recommendation_engine", self._generate_recommendations)
        
        # Add edges
        workflow.add_edge("data_collector", "analyzer")
        workflow.add_edge("analyzer", "insight_generator")
        workflow.add_edge("insight_generator", "recommendation_engine")
        workflow.add_edge("recommendation_engine", END)
        
        # Set entry point
        workflow.set_entry_point("data_collector")
        
        return workflow.compile()

    async def generate_insight(
        self, 
        student_id: str, 
        query: str, 
        academic_data: Dict = None,
        attendance_data: Dict = None,
        engagement_data: Dict = None
    ) -> InsightResponse:
        """Generate AI-powered insights for a student."""
        
        # Initialize state
        initial_state = StudentAnalysisState(
            student_id=student_id,
            query=query,
            academic_data=academic_data,
            attendance_data=attendance_data,
            engagement_data=engagement_data
        )
        
        try:
            # Run the graph
            if self.llm:
                result = await self.graph.ainvoke(initial_state.dict())
            else:
                # Fallback to mock analysis if no OpenAI key
                result = await self._mock_analysis(initial_state)
            
            return InsightResponse(
                insight=result.get("analysis_results", {}).get("summary", "Analysis completed"),
                recommendations=result.get("recommendations", []),
                confidence=result.get("confidence_score", 0.8),
                data_used=self._get_data_sources(result),
                generated_at=datetime.utcnow()
            )
            
        except Exception as e:
            # Fallback to mock response
            return await self._mock_analysis(initial_state)

    async def _collect_data(self, state: StudentAnalysisState) -> Dict:
        """Collect and prepare student data for analysis."""
        # In a real implementation, this would fetch data from various sources
        # For now, we'll use the provided data or generate mock data
        
        if not state.academic_data:
            state.academic_data = self._generate_mock_academic_data()
        
        if not state.attendance_data:
            state.attendance_data = self._generate_mock_attendance_data()
            
        if not state.engagement_data:
            state.engagement_data = self._generate_mock_engagement_data()
        
        return state.dict()

    async def _analyze_data(self, state: StudentAnalysisState) -> Dict:
        """Analyze the collected data to identify patterns and trends."""
        
        analysis = {
            "academic_trends": self._analyze_academic_trends(state.academic_data),
            "attendance_patterns": self._analyze_attendance_patterns(state.attendance_data),
            "engagement_insights": self._analyze_engagement_patterns(state.engagement_data),
            "cross_domain_correlations": self._find_correlations(
                state.academic_data, 
                state.attendance_data, 
                state.engagement_data
            )
        }
        
        state.analysis_results = analysis
        return state.dict()

    async def _generate_insights(self, state: StudentAnalysisState) -> Dict:
        """Generate human-readable insights from the analysis."""
        
        if self.llm:
            # Use OpenAI to generate insights
            insights = await self._llm_generate_insights(state)
        else:
            # Use rule-based insights
            insights = self._rule_based_insights(state)
        
        state.analysis_results["summary"] = insights
        return state.dict()

    async def _generate_recommendations(self, state: StudentAnalysisState) -> Dict:
        """Generate actionable recommendations based on insights."""
        
        recommendations = []
        analysis = state.analysis_results
        
        # Academic recommendations
        if analysis.get("academic_trends", {}).get("declining_subjects"):
            declining = analysis["academic_trends"]["declining_subjects"]
            for subject in declining:
                recommendations.append(f"Consider additional tutoring in {subject}")
                recommendations.append(f"Review {subject} homework completion patterns")
        
        # Attendance recommendations
        if analysis.get("attendance_patterns", {}).get("low_attendance"):
            recommendations.append("Establish a consistent morning routine")
            recommendations.append("Contact school counselor about attendance concerns")
        
        # Engagement recommendations
        if analysis.get("engagement_insights", {}).get("low_engagement_subjects"):
            low_engagement = analysis["engagement_insights"]["low_engagement_subjects"]
            for subject in low_engagement:
                recommendations.append(f"Find engaging resources for {subject}")
                recommendations.append(f"Discuss {subject} interests with your child")
        
        # Calculate confidence score
        confidence = self._calculate_confidence(analysis)
        
        state.recommendations = recommendations
        state.confidence_score = confidence
        
        return state.dict()

    async def _llm_generate_insights(self, state: StudentAnalysisState) -> str:
        """Use LLM to generate insights."""
        
        system_prompt = """You are an educational AI assistant that analyzes student data to provide insights for parents. 
        Analyze the provided student data and generate clear, actionable insights that help parents understand their child's academic progress.
        Focus on trends, patterns, and areas that need attention or celebration."""
        
        user_prompt = f"""
        Student Query: {state.query}
        
        Academic Data: {json.dumps(state.academic_data, indent=2)}
        Attendance Data: {json.dumps(state.attendance_data, indent=2)}
        Engagement Data: {json.dumps(state.engagement_data, indent=2)}
        Analysis Results: {json.dumps(state.analysis_results, indent=2)}
        
        Please provide clear, parent-friendly insights about this student's performance.
        """
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        try:
            response = await self.llm.agenerate([messages])
            return response.generations[0][0].text
        except Exception:
            return self._rule_based_insights(state)

    def _rule_based_insights(self, state: StudentAnalysisState) -> str:
        """Generate insights using rule-based logic."""
        
        insights = []
        analysis = state.analysis_results
        
        # Academic insights
        if analysis.get("academic_trends", {}).get("overall_gpa", 0) > 3.5:
            insights.append("Your child is performing well academically with a strong GPA.")
        elif analysis.get("academic_trends", {}).get("overall_gpa", 0) < 3.0:
            insights.append("Academic performance may need attention. Consider additional support.")
        
        # Attendance insights
        attendance_rate = analysis.get("attendance_patterns", {}).get("overall_rate", 0)
        if attendance_rate > 95:
            insights.append("Excellent attendance record! Consistency is key to academic success.")
        elif attendance_rate < 90:
            insights.append("Attendance has room for improvement. Regular attendance is crucial for learning.")
        
        # Engagement insights
        engagement_score = analysis.get("engagement_insights", {}).get("overall_score", 0)
        if engagement_score > 85:
            insights.append("High engagement levels show your child is actively participating in learning.")
        elif engagement_score < 70:
            insights.append("Engagement could be improved. Consider discussing learning preferences with your child.")
        
        return " ".join(insights) if insights else "Overall performance is within normal ranges."

    def _analyze_academic_trends(self, academic_data: Dict) -> Dict:
        """Analyze academic performance trends."""
        if not academic_data:
            return {}
        
        subjects = academic_data.get("subjects", [])
        declining_subjects = []
        improving_subjects = []
        overall_gpa = academic_data.get("overall_gpa", 0)
        
        for subject in subjects:
            if subject.get("trend") == "down":
                declining_subjects.append(subject.get("subject", "Unknown"))
            elif subject.get("trend") == "up":
                improving_subjects.append(subject.get("subject", "Unknown"))
        
        return {
            "overall_gpa": overall_gpa,
            "declining_subjects": declining_subjects,
            "improving_subjects": improving_subjects,
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
            "low_attendance": overall_rate < 90,
            "frequent_tardiness": late_days > 5
        }

    def _analyze_engagement_patterns(self, engagement_data: Dict) -> Dict:
        """Analyze engagement patterns."""
        if not engagement_data:
            return {}
        
        overall_score = engagement_data.get("overall_engagement_score", 0)
        study_hours = engagement_data.get("total_study_hours", 0)
        participation = engagement_data.get("participation_score", 0)
        
        low_engagement_subjects = []
        # This would be populated based on subject-specific engagement data
        
        return {
            "overall_score": overall_score,
            "study_hours": study_hours,
            "participation_score": participation,
            "low_engagement_subjects": low_engagement_subjects,
            "sufficient_study_time": study_hours >= 20  # 20 hours per week
        }

    def _find_correlations(self, academic_data: Dict, attendance_data: Dict, engagement_data: Dict) -> Dict:
        """Find correlations between different data domains."""
        correlations = {}
        
        # Simple correlation analysis
        attendance_rate = attendance_data.get("overall_percentage", 0) if attendance_data else 0
        academic_gpa = academic_data.get("overall_gpa", 0) if academic_data else 0
        engagement_score = engagement_data.get("overall_engagement_score", 0) if engagement_data else 0
        
        # Attendance-Academic correlation
        if attendance_rate > 95 and academic_gpa > 3.5:
            correlations["attendance_academic"] = "Strong positive correlation between attendance and academic performance"
        elif attendance_rate < 85 and academic_gpa < 3.0:
            correlations["attendance_academic"] = "Low attendance may be impacting academic performance"
        
        # Engagement-Academic correlation
        if engagement_score > 85 and academic_gpa > 3.5:
            correlations["engagement_academic"] = "High engagement correlates with strong academic performance"
        
        return correlations

    def _calculate_confidence(self, analysis: Dict) -> float:
        """Calculate confidence score for the analysis."""
        # Simple confidence calculation based on data completeness and consistency
        confidence = 0.8
        
        if analysis.get("academic_trends"):
            confidence += 0.1
        if analysis.get("attendance_patterns"):
            confidence += 0.05
        if analysis.get("engagement_insights"):
            confidence += 0.05
        
        return min(confidence, 1.0)

    def _get_data_sources(self, result: Dict) -> List[str]:
        """Get list of data sources used in analysis."""
        sources = []
        if result.get("academic_data"):
            sources.append("academic_performance")
        if result.get("attendance_data"):
            sources.append("attendance_records")
        if result.get("engagement_data"):
            sources.append("engagement_metrics")
        return sources

    async def _mock_analysis(self, state: StudentAnalysisState) -> InsightResponse:
        """Provide mock analysis when OpenAI is not available."""
        
        mock_insights = [
            "Your child shows consistent academic performance with room for improvement in mathematics.",
            "Attendance patterns are generally good, with occasional tardiness that could be addressed.",
            "Engagement levels are strong in science and English, but could be enhanced in history.",
            "Overall progress is positive with steady improvement over the past month."
        ]
        
        mock_recommendations = [
            "Consider additional math practice sessions",
            "Establish a consistent morning routine",
            "Explore interactive history resources",
            "Maintain current study schedule",
            "Celebrate achievements in strong subjects"
        ]
        
        return InsightResponse(
            insight=random.choice(mock_insights),
            recommendations=random.sample(mock_recommendations, 3),
            confidence=0.75,
            data_used=["academic_performance", "attendance_records", "engagement_metrics"],
            generated_at=datetime.utcnow()
        )

    def _generate_mock_academic_data(self) -> Dict:
        """Generate mock academic data."""
        return {
            "overall_gpa": random.uniform(3.0, 3.8),
            "subjects": [
                {"subject": "Mathematics", "grade": "B+", "trend": "down", "percentage": 85},
                {"subject": "Science", "grade": "A-", "trend": "up", "percentage": 90},
                {"subject": "English", "grade": "A", "trend": "stable", "percentage": 92}
            ]
        }

    def _generate_mock_attendance_data(self) -> Dict:
        """Generate mock attendance data."""
        return {
            "overall_percentage": random.uniform(88, 96),
            "late_days": random.randint(2, 8),
            "absent_days": random.randint(3, 12)
        }

    def _generate_mock_engagement_data(self) -> Dict:
        """Generate mock engagement data."""
        return {
            "overall_engagement_score": random.uniform(75, 92),
            "total_study_hours": random.uniform(18, 28),
            "participation_score": random.uniform(80, 95)
        }
