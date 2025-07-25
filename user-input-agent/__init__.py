"""
Drishti User Input Analysis Agent Package

This package provides user input processing and incident validation capabilities for the Drishti Event Management System.
It processes text reports, images, voice messages, and other user inputs to validate incidents and route them to the
appropriate specialized agents using Cloud Functions and Natural Language AI.

Main Components:
- UserInputAgent: Main agent class for input processing and validation
- Configuration: Input types, validation rules, and routing protocols
- Prompts: AI prompt templates for input analysis and incident categorization

Usage:
    from user_input_agent import UserInputAgent
    
    agent = UserInputAgent()
    result = await agent.process_user_input(
        input_data=user_report,
        input_type="text",
        user_context=user_info
    )
    
    print(f"Incident Category: {result['incident_category']}")
    print(f"Target Agent: {result['target_agent']}")
"""
from . import agent
from . import prompt


# from .config import INPUT_TYPES, VALIDATION_RULES, USER_INPUT_AGENT_ID
# from .prompt import USER_INPUT_ANALYSIS_PROMPT

# __version__ = "1.0.0"
# __author__ = "Drishti Team"

# __all__ = [
#     "UserInputAgent",
#     "app", 
#     "INPUT_TYPES",
#     "VALIDATION_RULES",
#     "USER_INPUT_AGENT_ID",
#     "USER_INPUT_ANALYSIS_PROMPT"
# ] 