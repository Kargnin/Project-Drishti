from google.adk.agents import Agent
from vertexai.preview.reasoning_engines import AdkApp
import vertexai
import os
from dotenv import load_dotenv

from .prompt import UNIFIED_DRISHTI_PROMPT
from .sub_agents.infrastructure_agent import infrastructure_agent
from .sub_agents.medassist_agent import medassist_agent
from .sub_agents.queue_management_agent import queue_management_agent
from .sub_agents.security_agent import security_agent
from .sub_agents.tools import graph_search_tool, get_entity_relationships_tool, get_entity_timeline_tool

# Load environment variables
load_dotenv()

# Initialize Vertex AI
project_id = os.environ.get('PROJECT_ID', 'noted-throne-466513-v6')
location = os.environ.get('LOCATION', 'us-central1')
vertexai.init(project=project_id, location=location)

# Create the root supervisor agent with sub-agents
root_agent = Agent(
    name="drishti_supervisor",
    model="gemini-2.0-flash-001",
    description="Drishti Supervisor Agent - Multimodal AI system that analyzes situations (text/images) and coordinates specialized sub-agents for comprehensive event management and emergency response using enhanced location schema.",
    instruction=UNIFIED_DRISHTI_PROMPT,
    sub_agents=[
        infrastructure_agent,
        medassist_agent,
        queue_management_agent,
        security_agent
    ],
    tools=[graph_search_tool, get_entity_relationships_tool, get_entity_timeline_tool]
)

# # Create the AdkApp wrapper for the supervisor agent  
# supervisor_app = AdkApp(agent=root_agent,  a2a_enabled=True)
