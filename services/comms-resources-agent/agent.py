from google.adk.agents import Agent
from vertexai.preview.reasoning_engines import AdkApp
import vertexai
import os
from dotenv import load_dotenv

from .prompt import COMMUNICATION_COORDINATION_PROMPT

# Load environment variables
load_dotenv()

# Initialize Vertex AI
project_id = os.environ.get('PROJECT_ID', 'noted-throne-466513-v6')
location = os.environ.get('LOCATION', 'us-central1')
vertexai.init(project=project_id, location=location)

# Communication & Resource Management agent configured for coordination and deployment
comms_resources_agent = Agent(
    name="comms_resources_agent",
    model="gemini-2.0-flash-001", 
    description="A communication and resource management agent that coordinates multilingual broadcasting, resource deployment, drone dispatch, weather monitoring, and announcements using GCP Translation API, Text-to-Speech, and Pub/Sub messaging for large-scale event management.",
    instruction=COMMUNICATION_COORDINATION_PROMPT,
    tools=[],
    # # Enable communication and coordination capabilities
    # generation_config={
    #     "temperature": 0.1,  # Low temperature for consistent coordination decisions
    #     "top_p": 0.8,
    #     "top_k": 40,
    #     "max_output_tokens": 2048,
    #     "response_mime_type": "application/json"  # Ensure JSON response format
    # },
    # safety_settings=[
    #     {
    #         "category": "HARM_CATEGORY_HARASSMENT",
    #         "threshold": "BLOCK_ONLY_HIGH"
    #     },
    #     {
    #         "category": "HARM_CATEGORY_HATE_SPEECH", 
    #         "threshold": "BLOCK_ONLY_HIGH"
    #     },
    #     {
    #         "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    #         "threshold": "BLOCK_ONLY_HIGH"
    #     },
    #     {
    #         "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    #         "threshold": "BLOCK_ONLY_HIGH"  # Allow emergency communication content
    #     }
    # ]
)

# Create the AdkApp wrapper to provide the correct interface
comms_resources_app = AdkApp(agent=comms_resources_agent)

# Alias for backward compatibility
root_agent = comms_resources_agent 