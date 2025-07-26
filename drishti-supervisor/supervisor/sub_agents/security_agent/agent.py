import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from vertexai.preview.reasoning_engines import AdkApp
import vertexai

from .prompt import SECURITY_MONITORING_PROMPT
from ..tools.tools import graph_search_tool, get_entity_relationships_tool, get_entity_timeline_tool

# Load environment variables
load_dotenv()

# Initialize Vertex AI
project_id = os.environ.get('PROJECT_ID', 'noted-throne-466513-v6')
location = os.environ.get('LOCATION', 'us-central1')
vertexai.init(project=project_id, location=location)

# Security Agent configured for threat monitoring and access control
security_agent = Agent(
    name="security_agent",
    model="gemini-2.0-flash-001",
    description="Security Agent that monitors threats, manages access control, coordinates security responses, and ensures comprehensive safety and security for event participants.",
    instruction=SECURITY_MONITORING_PROMPT,
    tools=[graph_search_tool, get_entity_relationships_tool, get_entity_timeline_tool]
)

# Create the AdkApp wrapper
security_app = AdkApp(agent=security_agent)

# Alias for backward compatibility
root_agent = security_agent 