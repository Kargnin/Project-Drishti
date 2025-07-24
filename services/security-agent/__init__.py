"""
Drishti Security Agent Package

This package provides security threat analysis capabilities for the Drishti Event Management System.
It can analyze both text descriptions and images to assess security threats and determine severity levels.

Main Components:
- SecurityAgent: Main agent class for threat analysis
- Configuration: Security keywords, threat levels, and settings
- Prompts: AI prompt templates for security analysis

Usage:
    from security_agent import SecurityAgent
    
    agent = SecurityAgent()
    result = await agent.analyze_security_threat(
        description="Suspicious person carrying a bag near entrance",
        image_data=image_bytes,
        location="Main entrance"
    )
    
    print(f"Threat level: {result['threat_level']}")
"""
from . import agent
from . import prompt


# from .config import THREAT_LEVELS, SECURITY_KEYWORDS, SECURITY_AGENT_ID
# from .prompt import SECURITY_ANALYSIS_PROMPT

# __version__ = "1.0.0"
# __author__ = "Drishti Team"

# __all__ = [
#     "SecurityAgent",
#     "app", 
#     "THREAT_LEVELS",
#     "SECURITY_KEYWORDS",
#     "SECURITY_AGENT_ID",
#     "SECURITY_ANALYSIS_PROMPT"
# ] 