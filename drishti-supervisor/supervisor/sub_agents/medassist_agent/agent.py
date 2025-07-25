from google.adk.agents import Agent
from vertexai.preview.reasoning_engines import AdkApp
import vertexai
import os
from dotenv import load_dotenv

from .prompt import MEDICAL_ASSISTANCE_PROMPT

# Load environment variables
load_dotenv()

# Initialize Vertex AI
project_id = os.environ.get('PROJECT_ID', 'noted-throne-466513-v6')
location = os.environ.get('LOCATION', 'us-central1')
vertexai.init(project=project_id, location=location)

# Medical Assistance agent configured for emergency response and health management
medassist_agent = Agent(
    name="medassist_agent",
    model="gemini-2.0-flash-001",
    description="Medical Assistance Agent that coordinates emergency medical response, health monitoring, medical resource deployment, and healthcare support for comprehensive event medical management.",
    instruction=MEDICAL_ASSISTANCE_PROMPT,
    tools=[],
    # generation_config={
    #     "temperature": 0.1,  # Low temperature for consistent medical decisions
    #     "top_p": 0.8,
    #     "top_k": 40,
    #     "max_output_tokens": 2048,
    #     "response_mime_type": "application/json"
    # }
)

# Create the AdkApp wrapper
medassist_app = AdkApp(agent=medassist_agent)

# Alias for backward compatibility
root_agent = medassist_agent 