from google.adk.agents import Agent
from vertexai.preview.reasoning_engines import AdkApp
import vertexai
import os
from dotenv import load_dotenv

from .prompt import MEDICAL_ANALYSIS_PROMPT

# Load environment variables
load_dotenv()

# Initialize Vertex AI
project_id = os.environ.get('PROJECT_ID', 'noted-throne-466513-v6')
location = os.environ.get('LOCATION', 'us-central1')
vertexai.init(project=project_id, location=location)

# MedAssist agent configured for multimodal medical emergency analysis
medassist_agent = Agent(
    name="medassist_agent",
    model="gemini-2.0-flash-001", 
    description="A multimodal medical emergency agent that analyzes text descriptions, images, and video to detect medical emergencies, assess symptoms, and coordinate appropriate medical response at large-scale events.",
    instruction=MEDICAL_ANALYSIS_PROMPT,
    tools=[],
    # # Enable multimodal capabilities for image, video and text analysis
    # generation_config={
    #     "temperature": 0.1,  # Low temperature for consistent medical analysis
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
    #         "threshold": "BLOCK_ONLY_HIGH"  # Allow medical emergency content analysis
    #     }
    # ]
)

# Create the AdkApp wrapper to provide the correct interface
medassist_app = AdkApp(agent=medassist_agent)

# Alias for backward compatibility
root_agent = medassist_agent 