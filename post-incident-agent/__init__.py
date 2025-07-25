"""
Drishti Post-Incident Analysis Agent Package

This package provides post-incident analysis and system optimization capabilities for the Drishti Event Management System.
It analyzes past incidents, evaluates response effectiveness, identifies patterns, and provides recommendations for
system improvements using BigQuery, Vertex AI, and Cloud Analytics.

Main Components:
- PostIncidentAgent: Main agent class for incident analysis and optimization
- Configuration: Analysis frameworks, evaluation metrics, and improvement protocols
- Prompts: AI prompt templates for incident analysis and system optimization

Usage:
    from post_incident_agent import PostIncidentAgent
    
    agent = PostIncidentAgent()
    result = await agent.analyze_incident(
        incident_data=incident_record,
        response_actions=response_log,
        outcome_metrics=effectiveness_data
    )
    
    print(f"Effectiveness Score: {result['effectiveness_score']}")
    print(f"Recommendations: {result['improvement_recommendations']}")
"""
from . import agent
from . import prompt


# from .config import ANALYSIS_FRAMEWORKS, EVALUATION_METRICS, POST_INCIDENT_AGENT_ID
# from .prompt import POST_INCIDENT_ANALYSIS_PROMPT

# __version__ = "1.0.0"
# __author__ = "Drishti Team"

# __all__ = [
#     "PostIncidentAgent",
#     "app", 
#     "ANALYSIS_FRAMEWORKS",
#     "EVALUATION_METRICS",
#     "POST_INCIDENT_AGENT_ID",
#     "POST_INCIDENT_ANALYSIS_PROMPT"
# ] 