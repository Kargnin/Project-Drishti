"""
Drishti Communication & Resource Management Agent Package

This package provides communication coordination and resource deployment capabilities for the Drishti Event Management System.
It manages multilingual broadcasting, resource optimization, drone dispatch, weather monitoring, and announcements
using GCP Translation API, Text-to-Speech, and Pub/Sub messaging.

Main Components:
- CommsResourcesAgent: Main agent class for communication and resource coordination
- Configuration: Communication protocols, resource types, and deployment settings
- Prompts: AI prompt templates for communication and resource management

Usage:
    from comms_resources_agent import CommsResourcesAgent
    
    agent = CommsResourcesAgent()
    result = await agent.coordinate_response(
        instruction="Deploy medical team to main stage area",
        priority="high",
        language="en"
    )
    
    print(f"Resources deployed: {result['deployed_resources']}")
"""
from . import agent
from . import prompt


# from .config import RESOURCE_TYPES, COMMUNICATION_PROTOCOLS, COMMS_AGENT_ID
# from .prompt import COMMUNICATION_COORDINATION_PROMPT

# __version__ = "1.0.0"
# __author__ = "Drishti Team"

# __all__ = [
#     "CommsResourcesAgent",
#     "app", 
#     "RESOURCE_TYPES",
#     "COMMUNICATION_PROTOCOLS",
#     "COMMS_AGENT_ID",
#     "COMMUNICATION_COORDINATION_PROMPT"
# ] 