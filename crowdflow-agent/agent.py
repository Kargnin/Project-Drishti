from google.adk.agents import Agent
from vertexai.preview.reasoning_engines import AdkApp
import vertexai
import os
from dotenv import load_dotenv

from .prompt import CROWDFLOW_ANALYSIS_PROMPT

# Load environment variables
load_dotenv()

# Initialize Vertex AI
project_id = os.environ.get('PROJECT_ID', 'noted-throne-466513-v6')
location = os.environ.get('LOCATION', 'us-central1')
vertexai.init(project=project_id, location=location)

# CrowdFlow agent configured for computer vision and crowd density analysis
crowdflow_agent = Agent(
    name="crowdflow_agent",
    model="gemini-2.0-flash-001", 
    description="A computer vision and ML-powered crowd flow agent that uses YOLOv3 detection and density algorithms to predict crowd patterns, analyze density levels, and generate crowd density maps and flow predictions at large-scale events.",
    instruction=CROWDFLOW_ANALYSIS_PROMPT,
    tools=[],
    # # Enable computer vision capabilities for crowd detection
    # generation_config={
    #     "temperature": 0.1,  # Low temperature for consistent crowd analysis
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
    #         "threshold": "BLOCK_ONLY_HIGH"  # Allow crowd analysis content
    #     }
    # ]
)

# Create the AdkApp wrapper to provide the correct interface
crowdflow_app = AdkApp(agent=crowdflow_agent)

# Alias for backward compatibility
root_agent = crowdflow_agent 