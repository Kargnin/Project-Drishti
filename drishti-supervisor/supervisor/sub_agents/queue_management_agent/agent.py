from google.adk.agents import Agent
from vertexai.preview.reasoning_engines import AdkApp
import vertexai
import os
from dotenv import load_dotenv

from .prompt import QUEUE_MANAGEMENT_PROMPT

# Load environment variables
load_dotenv()

# Initialize Vertex AI
project_id = os.environ.get('PROJECT_ID', 'noted-throne-466513-v6')
location = os.environ.get('LOCATION', 'us-central1')
vertexai.init(project=project_id, location=location)

# Queue Management agent configured for crowd flow optimization and bottleneck prevention
queue_management_agent = Agent(
    name="queue_management_agent",
    model="gemini-2.0-flash-001",
    description="Queue Management Agent that optimizes crowd flow, manages entry/exit processes, prevents bottlenecks, and ensures safe and efficient people movement throughout event venues.",
    instruction=QUEUE_MANAGEMENT_PROMPT,
    tools=[],
    # generation_config={
    #     "temperature": 0.1,  # Low temperature for consistent crowd management decisions
    #     "top_p": 0.8,
    #     "top_k": 40,
    #     "max_output_tokens": 2048,
    #     "response_mime_type": "application/json"
    # }
)

# Create the AdkApp wrapper
queue_management_app = AdkApp(agent=queue_management_agent)

# Alias for backward compatibility
root_agent = queue_management_agent 