"""
Drishti CrowdFlow Agent Package

This package provides crowd density prediction and management capabilities for the Drishti Event Management System.
It uses computer vision and custom ML models to detect crowds, analyze density patterns, and predict flow behaviors
using YOLOv3 detection and advanced density algorithms.

Main Components:
- CrowdFlowAgent: Main agent class for crowd detection and density analysis
- Configuration: Crowd detection keywords, density levels, and settings
- Prompts: AI prompt templates for crowd flow analysis

Usage:
    from crowdflow_agent import CrowdFlowAgent
    
    agent = CrowdFlowAgent()
    result = await agent.analyze_crowd_density(
        description="Dense crowd gathering near main stage",
        camera_feed_data=camera_data,
        location="Main stage area"
    )
    
    print(f"Crowd density: {result['crowd_density_level']}")
"""
from . import agent
from . import prompt


# from .config import DENSITY_LEVELS, CROWD_KEYWORDS, CROWDFLOW_AGENT_ID
# from .prompt import CROWDFLOW_ANALYSIS_PROMPT

# __version__ = "1.0.0"
# __author__ = "Drishti Team"

# __all__ = [
#     "CrowdFlowAgent",
#     "app", 
#     "DENSITY_LEVELS",
#     "CROWD_KEYWORDS",
#     "CROWDFLOW_AGENT_ID",
#     "CROWDFLOW_ANALYSIS_PROMPT"
# ] 