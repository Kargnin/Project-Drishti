import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from vertexai.preview.reasoning_engines import AdkApp
import vertexai

from .prompt import INFRASTRUCTURE_MANAGEMENT_PROMPT
from ..tools.tools import graph_search_tool, get_entity_relationships_tool, get_entity_timeline_tool

# Load environment variables
load_dotenv()

# Initialize Vertex AI
project_id = os.environ.get('PROJECT_ID', 'noted-throne-466513-v6')
location = os.environ.get('LOCATION', 'us-central1')
vertexai.init(project=project_id, location=location)

# Infrastructure Management agent configured for facilities, utilities, and equipment management
infrastructure_agent = Agent(
    name="infrastructure_agent",
    model="gemini-2.0-flash-001",
    description="Infrastructure Management Agent that oversees venue facilities, utility systems, equipment deployment, and infrastructure safety for comprehensive event management and emergency response.",
    instruction=INFRASTRUCTURE_MANAGEMENT_PROMPT,
    tools=[graph_search_tool, get_entity_relationships_tool, get_entity_timeline_tool]
)

# Create the AdkApp wrapper
infrastructure_app = AdkApp(agent=infrastructure_agent)

# Alias for backward compatibility
root_agent = infrastructure_agent 