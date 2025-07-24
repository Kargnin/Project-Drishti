"""
Drishti Infrastructure Agent Package

This package provides infrastructure monitoring and management capabilities for the Drishti Event Management System.
It can analyze both text descriptions and images to assess infrastructure status, power systems, connectivity, 
and structural integrity.

Main Components:
- InfrastructureAgent: Main agent class for infrastructure analysis
- Configuration: Infrastructure keywords, monitoring levels, and settings
- Prompts: AI prompt templates for infrastructure analysis

Usage:
    from infrastructure_agent import InfrastructureAgent
    
    agent = InfrastructureAgent()
    result = await agent.analyze_infrastructure_status(
        description="Power fluctuations in main pavilion",
        image_data=image_bytes,
        location="Main pavilion"
    )
    
    print(f"Infrastructure status: {result['status_level']}")
"""
from . import agent
from . import prompt


# from .config import STATUS_LEVELS, INFRASTRUCTURE_KEYWORDS, INFRASTRUCTURE_AGENT_ID
# from .prompt import INFRASTRUCTURE_ANALYSIS_PROMPT

# __version__ = "1.0.0"
# __author__ = "Drishti Team"

# __all__ = [
#     "InfrastructureAgent",
#     "app", 
#     "STATUS_LEVELS",
#     "INFRASTRUCTURE_KEYWORDS",
#     "INFRASTRUCTURE_AGENT_ID",
#     "INFRASTRUCTURE_ANALYSIS_PROMPT"
# ] 