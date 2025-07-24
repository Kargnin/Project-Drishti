"""
Drishti Queue Management Agent Package

This package provides crowd flow optimization and queue management capabilities for the Drishti Event Management System.
It can analyze camera feeds, historical patterns, and user input to optimize crowd flow, reduce wait times,
and provide staff allocation recommendations.

Main Components:
- QueueManagementAgent: Main agent class for queue and crowd flow analysis
- Configuration: Queue management keywords, flow levels, and settings
- Prompts: AI prompt templates for queue management analysis

Usage:
    from queue_management_agent import QueueManagementAgent
    
    agent = QueueManagementAgent()
    result = await agent.analyze_queue_situation(
        description="Long lines forming at entrance gate 3",
        camera_feed_data=camera_data,
        location="Main entrance"
    )
    
    print(f"Flow recommendation: {result['flow_recommendation']}")
"""
from . import agent
from . import prompt


# from .config import FLOW_LEVELS, QUEUE_KEYWORDS, QUEUE_MANAGEMENT_AGENT_ID
# from .prompt import QUEUE_ANALYSIS_PROMPT

# __version__ = "1.0.0"
# __author__ = "Drishti Team"

# __all__ = [
#     "QueueManagementAgent",
#     "app", 
#     "FLOW_LEVELS",
#     "QUEUE_KEYWORDS",
#     "QUEUE_MANAGEMENT_AGENT_ID",
#     "QUEUE_ANALYSIS_PROMPT"
# ] 