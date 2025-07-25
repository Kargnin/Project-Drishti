from google.adk.agents import Agent
from vertexai.preview.reasoning_engines import AdkApp
import vertexai
import os
from dotenv import load_dotenv

from .prompt import USER_INPUT_ANALYSIS_PROMPT
from .infrastructure_agent.agent import infrastructure_agent

# Load environment variables
load_dotenv()

# Initialize Vertex AI
project_id = os.environ.get('PROJECT_ID', 'noted-throne-466513-v6')
location = os.environ.get('LOCATION', 'us-central1')
vertexai.init(project=project_id, location=location)

# User Input Analysis agent configured for input processing and routing
user_input_agent = Agent(
    name="user_input_agent",
    model="gemini-2.0-flash-001", 
    description="A user input analysis agent that processes and validates user-reported incidents from text reports, images, voice messages, and other inputs, then categorizes and routes them to appropriate specialized agents using Cloud Functions and Natural Language AI for intelligent incident triage.",
    instruction=USER_INPUT_ANALYSIS_PROMPT,
    tools=[],
    sub_agents=[
        infrastructure_agent
    ],
    # # Enable multimodal input processing capabilities
    # generation_config={
    #     "temperature": 0.1,  # Low temperature for consistent categorization and routing
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
    #         "threshold": "BLOCK_ONLY_HIGH"  # Allow processing of incident reports
    #     }
    # ]
)

# Create the AdkApp wrapper to provide the correct interface
user_input_app = AdkApp(agent=user_input_agent)

# Alias for backward compatibility
root_agent = user_input_agent 