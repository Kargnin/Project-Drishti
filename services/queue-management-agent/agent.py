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

# Queue Management agent configured for multimodal crowd flow analysis
queue_management_agent = Agent(
    name="queue_management_agent",
    model="gemini-2.0-flash-001", 
    description="A multimodal queue management agent that analyzes camera feeds, historical patterns, and user input to optimize crowd flow, reduce wait times, and provide staff allocation recommendations at large-scale events.",
    instruction=QUEUE_MANAGEMENT_PROMPT,
    tools=[],
    # # Enable multimodal capabilities for camera feed and text analysis
    # generation_config={
    #     "temperature": 0.1,  # Low temperature for consistent queue management analysis
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
    #         "threshold": "BLOCK_ONLY_HIGH"  # Allow crowd management content analysis
    #     }
    # ]
)

# Create the AdkApp wrapper to provide the correct interface
queue_management_app = AdkApp(agent=queue_management_agent)

# Alias for backward compatibility
root_agent = queue_management_agent 