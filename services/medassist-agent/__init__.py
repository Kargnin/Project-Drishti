"""
Drishti MedAssist Agent Package

This package provides medical emergency response and coordination capabilities for the Drishti Event Management System.
It can analyze both text descriptions and images/video to assess medical situations, detect emergencies, 
and coordinate appropriate medical response.

Main Components:
- MedAssistAgent: Main agent class for medical emergency analysis
- Configuration: Medical keywords, triage levels, and settings
- Prompts: AI prompt templates for medical analysis

Usage:
    from medassist_agent import MedAssistAgent
    
    agent = MedAssistAgent()
    result = await agent.analyze_medical_situation(
        description="Person collapsed and appears unconscious",
        image_data=image_bytes,
        location="Main stage area"
    )
    
    print(f"Emergency level: {result['emergency_level']}")
"""
from . import agent
from . import prompt


# from .config import TRIAGE_LEVELS, MEDICAL_KEYWORDS, MEDASSIST_AGENT_ID
# from .prompt import MEDICAL_ANALYSIS_PROMPT

# __version__ = "1.0.0"
# __author__ = "Drishti Team"

# __all__ = [
#     "MedAssistAgent",
#     "app", 
#     "TRIAGE_LEVELS",
#     "MEDICAL_KEYWORDS",
#     "MEDASSIST_AGENT_ID",
#     "MEDICAL_ANALYSIS_PROMPT"
# ] 