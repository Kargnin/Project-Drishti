from google.adk.agents import Agent
from vertexai.preview.reasoning_engines import AdkApp
import vertexai
import os
from dotenv import load_dotenv

from .prompt import POST_INCIDENT_ANALYSIS_PROMPT

# Load environment variables
load_dotenv()

# Initialize Vertex AI
project_id = os.environ.get('PROJECT_ID', 'noted-throne-466513-v6')
location = os.environ.get('LOCATION', 'us-central1')
vertexai.init(project=project_id, location=location)

# Post-Incident Analysis agent configured for learning and optimization
post_incident_agent = Agent(
    name="post_incident_agent",
    model="gemini-2.0-flash-001", 
    description="A post-incident analysis agent that learns from past incidents, evaluates response effectiveness, identifies patterns, and provides system optimization recommendations using BigQuery, Vertex AI, and Cloud Analytics for continuous improvement of event management systems.",
    instruction=POST_INCIDENT_ANALYSIS_PROMPT,
    tools=[],
    # # Enable analytical and learning capabilities
    # generation_config={
    #     "temperature": 0.1,  # Low temperature for consistent analytical reasoning
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
    #         "threshold": "BLOCK_ONLY_HIGH"  # Allow analysis of dangerous incidents for learning
    #     }
    # ]
)

# Create the AdkApp wrapper to provide the correct interface
post_incident_app = AdkApp(agent=post_incident_agent)

# Alias for backward compatibility
root_agent = post_incident_agent 