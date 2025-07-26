from google.adk.agents import Agent, SequentialAgent
from vertexai.preview.reasoning_engines import AdkApp
import vertexai
import os
from dotenv import load_dotenv

from .prompt import VIDEO_ANALYSIS_PROMPT
from .prompt import FORECASTING_ANALYSIS_PROMPT

# Load environment variables
load_dotenv()

# Initialize Vertex AI
project_id = os.environ.get('PROJECT_ID', 'noted-throne-466513-v6')
location = os.environ.get('LOCATION', 'us-central1')
vertexai.init(project=project_id, location=location)




# Video Analysis Agent for frame-by-frame crowd analysis
video_analysis_agent = Agent(
    name="video_analysis_agent",
    model="gemini-2.5-flash-lite",  # Using full model for complex video analysis
    description="Analyzes video input at 5 FPS to generate structured tabular data on crowd density, velocity, and behavior for storage in BigQuery",
    instruction=VIDEO_ANALYSIS_PROMPT,
    tools=[]
)

# Forecasting & Severity Analysis Agent
forecasting_agent = Agent(
    name="forecasting_severity_agent",
    model="gemini-2.5-flash-lite",  # Using full model for complex forecasting
    description="Analyzes historical crowd data to predict future conditions and assign severity ratings for crowd management and safety",
    instruction=FORECASTING_ANALYSIS_PROMPT,
    tools=[]
)

# Pipeline Orchestrator Agent that manages both video analysis and forecasting agents
pipeline_orchestrator = SequentialAgent(
    name="crowdflow_pipeline_orchestrator",
    description="Orchestrates a sequential two-agent pipeline that accepts video input, processes it through video analysis, and performs crowd forecasting in the Drishti system",
    sub_agents=[
        video_analysis_agent,
        forecasting_agent
    ]
)



# For ADK tools compatibility, the root agent must be named `root_agent`
root_agent = pipeline_orchestrator
# Create the AdkApp wrapper with A2A enabled for agent communication
# crowdflow_pipeline_app = AdkApp(
#     agent=pipeline_orchestrator,
#     enable_tracing=True
# )
