from fastapi import FastAPI, Request, HTTPException
from google.cloud import firestore
from vertexai.generative_models import GenerativeModel, Part, Tool
import json
import os
import base64
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Drishti Supervisor Agent",
    description="AI-powered agent for event incident management, processing video feeds and user reports."
)

# Initialize Firestore DB client
db = firestore.Client()

# Initialize Vertex AI Generative Model (Gemini)
# Ensure your service account has Vertex AI User role
model = GenerativeModel("gemini-1.5-flash") # Or gemini-1.0-pro, etc.

# --- Firestore Collection References (Using __app_id for multi-tenancy) ---
# In a real Cloud Run deployment, __app_id might be passed as an environment variable.
# For local testing, you can set it manually or use a default.
app_id = os.environ.get('APP_ID', 'default-app-id')

AGENTS_COLLECTION = db.collection(f'artifacts/{app_id}/agents')
AGENT_STATE_COLLECTION = db.collection(f'artifacts/{app_id}/agent_state')
AGENT_MEMORY_COLLECTION = db.collection(f'artifacts/{app_id}/agent_memory')
INCIDENTS_COLLECTION = db.collection(f'artifacts/{app_id}/public/data/incidents')
AGENT_ACTIONS_COLLECTION = db.collection(f'artifacts/{app_id}/public/data/agent_actions')

# --- Tool Definitions for Vertex AI ---
# These functions simulate interactions with other agents/services.
# In a real microservices architecture, these would make HTTP calls to other Cloud Run/Cloud Functions.

def analyze_video_feed(video_data_ref: str, camera_id: str):
    """
    Processes a low FPS video feed (or a single frame) using a vision model.
    This function would typically call Vertex AI Vision API or a custom model endpoint.
    For this example, it simulates detection.
    `video_data_ref` could be a GCS URL, or a base64 encoded image for small frames.
    """
    logger.info(f"TOOL CALL: Analyzing video feed from camera {camera_id} at {video_data_ref}")
    # Simulate calling a vision model (e.g., Vertex AI Vision, or a custom YOLOv8 endpoint)
    # In a real scenario, you'd send the video_data_ref to the vision service.

    # Example simulated output based on camera_id or random logic
    observations = {
        "camera_id": camera_id,
        "timestamp": firestore.SERVER_TIMESTAMP,
        "crowd_density_percentage": 0.0,
        "anomalies_detected": [],
        "object_counts": {"person": 0}
    }

    if "entrance" in camera_id:
        observations["crowd_density_percentage"] = 75.0
        observations["object_counts"]["person"] = 150
        observations["anomalies_detected"].append("rapid_crowd_increase")
    elif "queue" in camera_id:
        observations["crowd_density_percentage"] = 90.0
        observations["object_counts"]["person"] = 80
        observations["anomalies_detected"].append("queue_stagnation")
    elif "crowd" in camera_id:
        observations["crowd_density_percentage"] = 60.0
        observations["object_counts"]["person"] = 500
        # Sometimes simulate a security anomaly
        if os.urandom(1)[0] % 5 == 0: # 20% chance
            observations["anomalies_detected"].append("suspicious_loitering")
            observations["description"] = "Suspicious loitering detected in general crowd area."

    logger.info(f"Simulated Vision Model Output: {observations}")
    return {"status": "success", "observations": observations}

def dispatch_to_security_agent(incident_id: str, details: str, visual_context: dict = None, user_report_details: dict = None):
    """Dispatches an incident to the Security Agent."""
    logger.info(f"TOOL CALL: Dispatching incident {incident_id} to Security Agent with details: {details}. Visual Context: {visual_context}, User Report: {user_report_details}")
    update_data = {
        'current_status': 'assigned_to_security',
        'assigned_sub_agent_id': 'security_agent',
        'notes': firestore.ArrayUnion([{"timestamp": firestore.SERVER_TIMESTAMP, "agent": "supervisor", "note": "Dispatched to Security Agent."}])
    }
    if visual_context:
        update_data['visual_context'] = visual_context
    if user_report_details:
        update_data['user_report_details'] = user_report_details
    INCIDENTS_COLLECTION.document(incident_id).update(update_data)
    return {"status": "success", "message": f"Incident {incident_id} dispatched to Security Agent."}

def dispatch_to_medassist_agent(incident_id: str, details: str, location: str, visual_context: dict = None, user_report_details: dict = None):
    """Dispatches an incident to the MedAssist Agent."""
    logger.info(f"TOOL CALL: Dispatching incident {incident_id} to MedAssist Agent at {location} with details: {details}. Visual Context: {visual_context}, User Report: {user_report_details}")
    update_data = {
        'current_status': 'assigned_to_medassist',
        'assigned_sub_agent_id': 'medassist_agent',
        'notes': firestore.ArrayUnion([{"timestamp": firestore.SERVER_TIMESTAMP, "agent": "supervisor", "note": "Dispatched to MedAssist Agent."}])
    }
    if visual_context:
        update_data['visual_context'] = visual_context
    if user_report_details:
        update_data['user_report_details'] = user_report_details
    INCIDENTS_COLLECTION.document(incident_id).update(update_data)
    return {"status": "success", "message": f"Incident {incident_id} dispatched to MedAssist Agent."}

def dispatch_to_queue_management_agent(incident_id: str, details: str, affected_queue: str, visual_context: dict = None, user_report_details: dict = None):
    """Dispatches an incident to the Queue Management Agent."""
    logger.info(f"TOOL CALL: Dispatching incident {incident_id} to Queue Management Agent for {affected_queue} with details: {details}. Visual Context: {visual_context}, User Report: {user_report_details}")
    update_data = {
        'current_status': 'assigned_to_queue_management',
        'assigned_sub_agent_id': 'queue_management_agent',
        'notes': firestore.ArrayUnion([{"timestamp": firestore.SERVER_TIMESTAMP, "agent": "supervisor", "note": "Dispatched to Queue Management Agent."}])
    }
    if visual_context:
        update_data['visual_context'] = visual_context
    if user_report_details:
        update_data['user_report_details'] = user_report_details
    INCIDENTS_COLLECTION.document(incident_id).update(update_data)
    return {"status": "success", "message": f"Incident {incident_id} dispatched to Queue Management Agent."}

def create_incident(incident_type: str, description: str, location: str, severity: str, source: str, visual_context: dict = None, user_report_details: dict = None):
    """Creates a new incident record in Firestore."""
    logger.info(f"TOOL CALL: Creating new incident: Type={incident_type}, Desc={description}, Loc={location}, Severity={severity}, Source={source}. Visual Context: {visual_context}, User Report: {user_report_details}")
    new_incident_ref = INCIDENTS_COLLECTION.document() # Let Firestore auto-generate ID
    incident_id = new_incident_ref.id
    incident_data = {
        'incident_id': incident_id,
        'timestamp': firestore.SERVER_TIMESTAMP,
        'reporter_id': 'supervisor_agent_vision' if source == 'vision_system' else user_report_details.get('reporter_id', 'unknown_user'),
        'source': source,
        'type': incident_type,
        'description': description,
        'location': location,
        'severity': severity,
        'current_status': f'reported_by_{source}',
        'assigned_supervisor_agent_id': 'supervisor_agent',
        'notes': [{"timestamp": firestore.SERVER_TIMESTAMP, "agent": "supervisor", "note": f"Incident created based on {source}."}]
    }
    if visual_context:
        incident_data['visual_context'] = visual_context
    if user_report_details:
        incident_data['user_report_details'] = user_report_details

    new_incident_ref.set(incident_data)
    return {"status": "success", "incident_id": incident_id, "message": "New incident created."}

def update_incident_status(incident_id: str, new_status: str, notes: str = ""):
    """Updates the status of an existing incident in Firestore."""
    logger.info(f"TOOL CALL: Updating status of incident {incident_id} to {new_status}. Notes: {notes}")
    INCIDENTS_COLLECTION.document(incident_id).update({
        'current_status': new_status,
        'notes': firestore.ArrayUnion([{"timestamp": firestore.SERVER_TIMESTAMP, "agent": "supervisor", "note": f"Status updated to {new_status}. {notes}"}])
    })
    return {"status": "success", "message": f"Incident {incident_id} status updated to {new_status}."}

def get_incident_details(incident_id: str):
    """Retrieves full details of a specific incident from Firestore."""
    logger.info(f"TOOL CALL: Getting details for incident {incident_id}")
    doc_ref = INCIDENTS_COLLECTION.document(incident_id)
    doc = doc_ref.get()
    if doc.exists:
        return {"status": "success", "data": doc.to_dict()}
    else:
        return {"status": "error", "message": f"Incident {incident_id} not found."}

# Define the tools for the LLM
event_management_tools = [
    Tool.from_function(analyze_video_feed),
    Tool.from_function(dispatch_to_security_agent),
    Tool.from_function(dispatch_to_medassist_agent),
    Tool.from_function(dispatch_to_queue_management_agent),
    Tool.from_function(create_incident),
    Tool.from_function(update_incident_status),
    Tool.from_function(get_incident_details),
    # Add other tools like dispatch_to_infrastructure_agent, get_historical_incidents etc.
]

@app.post("/process_input")
async def process_input(request: Request):
    """
    HTTP endpoint for the Supervisor Agent to receive either:
    1. Video data reference (e.g., GCS URL) or base64 encoded frame.
    2. User incident report details.
    """
    try:
        request_json = await request.json()
    except Exception as e:
        logger.error(f"Error parsing request JSON: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON in request body")

    if not request_json:
        raise HTTPException(status_code=400, detail="Empty request body")

    # Determine input type
    is_video_input = 'video_data_ref' in request_json and 'camera_id' in request_json
    is_user_report_input = 'incident_type' in request_json and 'description' in request_json and 'source' in request_json and request_json['source'] == 'user_report'

    if not (is_video_input or is_user_report_input):
        raise HTTPException(status_code=400, detail="Invalid input: Must be either video data or a user incident report.")

    input_type_str = "video_feed" if is_video_input else "user_report"
    logger.info(f"Received new input of type: {input_type_str}")

    try:
        # 1. Retrieve Agent State and Memory
        supervisor_state_doc = AGENT_STATE_COLLECTION.document('supervisor_agent_state').get()
        supervisor_state = supervisor_state_doc.to_dict() if supervisor_state_doc.exists else {}

        supervisor_memory_doc = AGENT_MEMORY_COLLECTION.document('supervisor_agent_memory').get()
        supervisor_memory = supervisor_memory_doc.to_dict() if supervisor_memory_doc.exists else {}

        # 2. Process Input and Construct LLM Prompt
        prompt_parts = [
            Part.from_text(f"You are the Drishti Supervisor Agent for an Event Management System."),
            Part.from_text(f"Your description: {AGENTS_COLLECTION.document('supervisor_agent').get().to_dict().get('description', 'No description.')}"),
            Part.from_text(f"Your goal: {AGENTS_COLLECTION.document('supervisor_agent').get().to_dict().get('goal', 'No goal.')}"),
            Part.from_text(f"Current Agent State: {json.dumps(supervisor_state)}"),
            Part.from_text(f"Relevant Memory/Insights: {json.dumps(supervisor_memory.get('learned_insights', []))}"),
            Part.from_text(f"Learned Visual Patterns: {json.dumps(supervisor_memory.get('learned_visual_patterns', []))}"),
            Part.from_text(f"Learned Report Patterns: {json.dumps(supervisor_memory.get('learned_report_patterns', []))}"),
            Part.from_text(f"\n--- NEW INPUT RECEIVED ({input_type_str.upper()}) ---"),
        ]

        observations = {}
        user_report_details = {}
        incident_id_for_dispatch = None # To hold incident_id if created or provided

        if is_video_input:
            video_data_ref = request_json['video_data_ref']
            camera_id = request_json['camera_id']
            frame_timestamp = request_json.get('timestamp', firestore.SERVER_TIMESTAMP)

            # Use the 'analyze_video_feed' tool to process the raw video data
            vision_analysis_result = analyze_video_feed(video_data_ref=video_data_ref, camera_id=camera_id)

            if vision_analysis_result['status'] == 'error':
                raise Exception(f"Video analysis failed: {vision_analysis_result['message']}")

            observations = vision_analysis_result['observations']
            prompt_parts.append(Part.from_text(f"Camera ID: {camera_id}"))
            prompt_parts.append(Part.from_text(f"Timestamp: {frame_timestamp}"))
            prompt_parts.append(Part.from_text(f"Observations: {json.dumps(observations)}"))
            prompt_parts.append(Part.from_text(f"\n--- INSTRUCTIONS ---"))
            prompt_parts.append(Part.from_text(f"Analyze these observations. Determine if an incident or a potential issue is present. If an issue is detected, categorize it and use the 'create_incident' tool to log it, setting 'source' to 'vision_system'. Then, use the dispatch tools to send relevant information to the sub-agents, including the visual context. Prioritize attendee safety and rapid, proactive response."))

        elif is_user_report_input:
            incident_type = request_json['incident_type']
            description = request_json['description']
            location = request_json.get('location', 'unknown')
            severity = request_json.get('severity', 'medium')
            reporter_id = request_json.get('reporter_id', 'anonymous_user')
            # If an incident_id is provided in the report, it means it's an update or reference
            incident_id_for_dispatch = request_json.get('incident_id')

            user_report_details = {
                "reporter_id": reporter_id,
                "raw_text": description,
                "location": location,
                "severity": severity,
                "type": incident_type
            }

            prompt_parts.append(Part.from_text(f"User Report Details: {json.dumps(user_report_details)}"))
            prompt_parts.append(Part.from_text(f"\n--- INSTRUCTIONS ---"))
            if incident_id_for_dispatch:
                prompt_parts.append(Part.from_text(f"This is an update or reference to an existing incident (ID: {incident_id_for_dispatch}). Analyze the report and determine if the incident status needs to be updated or if a new dispatch is required. Use 'update_incident_status' or dispatch tools as appropriate."))
            else:
                prompt_parts.append(Part.from_text(f"This is a new incident report. Analyze the report, categorize it, and use the 'create_incident' tool to log it, setting 'source' to 'user_report'. Then, use the dispatch tools to send relevant information to the sub-agents. Prioritize attendee safety and rapid response."))


        # 3. Call the LLM with tools
        response = model.generate_content(
            prompt_parts,
            tools=event_management_tools
        )

        # 4. Process LLM's response (tool calls)
        tool_outputs = []
        final_message = "No specific action taken by Supervisor Agent based on current observations." # Default message
        incident_created_id = None

        for part in response.candidates[0].content.parts:
            if part.function_call:
                tool_call = part.function_call
                tool_name = tool_call.name
                tool_args = tool_call.args
                logger.info(f"LLM requested tool: {tool_name} with args: {tool_args}")

                # Add context (visual or user report) to dispatch/create tools
                if tool_name.startswith("dispatch_to_"):
                    if observations:
                        tool_args["visual_context"] = observations
                    if user_report_details:
                        tool_args["user_report_details"] = user_report_details
                    # Ensure incident_id is passed for dispatch, if already known
                    if 'incident_id' not in tool_args and incident_id_for_dispatch:
                        tool_args['incident_id'] = incident_id_for_dispatch
                elif tool_name == "create_incident":
                    if observations:
                        tool_args["visual_context"] = observations
                        tool_args["source"] = "vision_system" # Override source if visual context is present
                    if user_report_details:
                        tool_args["user_report_details"] = user_report_details
                        tool_args["source"] = "user_report" # Override source if user report is present

                # Execute the tool function based on its name
                output = {"status": "error", "message": f"Unknown tool: {tool_name}"} # Default error
                if tool_name == "analyze_video_feed":
                    output = analyze_video_feed(**tool_args)
                elif tool_name == "dispatch_to_security_agent":
                    output = dispatch_to_security_agent(**tool_args)
                elif tool_name == "dispatch_to_medassist_agent":
                    output = dispatch_to_medassist_agent(**tool_args)
                elif tool_name == "dispatch_to_queue_management_agent":
                    output = dispatch_to_queue_management_agent(**tool_args)
                elif tool_name == "create_incident":
                    output = create_incident(**tool_args)
                    if output.get("status") == "success":
                        incident_created_id = output.get("incident_id") # Capture newly created ID
                        # If incident was just created, use its ID for subsequent dispatches in this turn
                        incident_id_for_dispatch = incident_created_id
                elif tool_name == "update_incident_status":
                    output = update_incident_status(**tool_args)
                elif tool_name == "get_incident_details":
                    output = get_incident_details(**tool_args)
                else:
                    logger.warning(f"LLM requested an unhandled tool: {tool_name}")

                tool_outputs.append(Part.from_function_response(name=tool_name, response=output))
            elif part.text:
                logger.info(f"LLM's text response: {part.text}")
                final_message = part.text # Capture LLM's direct text response

        # If tools were called, send tool outputs back to the LLM for final response/confirmation
        if tool_outputs:
            try:
                final_response_after_tools = model.generate_content(
                    [response.candidates[0].content] + tool_outputs
                )
                final_message = final_response_after_tools.candidates[0].content.parts[0].text
                logger.info(f"LLM's final response after tool execution: {final_message}")
            except Exception as e:
                logger.error(f"Error getting final LLM response after tools: {e}")
                final_message = f"Supervisor Agent processed input and executed tools. Encountered an issue getting final LLM summary: {e}"


        # 5. Update Agent State
        state_update_data = {}
        if is_video_input:
            state_update_data['last_processed_video_timestamp'] = firestore.SERVER_TIMESTAMP
            state_update_data['active_incidents'] = firestore.ArrayUnion([{
                'incident_id': incident_created_id if incident_created_id else f"video_obs_{camera_id}_{firestore.SERVER_TIMESTAMP.isoformat()}", # Use isoformat for timestamp in ID if no incident_id
                'status': 'processed_by_supervisor_vision',
                'last_update_timestamp': firestore.SERVER_TIMESTAMP,
                'camera_id': camera_id,
                'observations_summary': observations
            }])
        elif is_user_report_input:
            state_update_data['last_processed_user_report_timestamp'] = firestore.SERVER_TIMESTAMP
            state_update_data['active_incidents'] = firestore.ArrayUnion([{
                'incident_id': incident_created_id if incident_created_id else (request_json.get('incident_id') or f'unknown_user_report_id_{firestore.SERVER_TIMESTAMP.isoformat()}'),
                'status': 'processed_by_supervisor_user_report',
                'last_update_timestamp': firestore.SERVER_TIMESTAMP,
                'user_report_summary': user_report_details
            }])
        AGENT_STATE_COLLECTION.document('supervisor_agent_state').set(state_update_data, merge=True)

        # 6. Log the action taken by the supervisor agent
        log_data = {
            'timestamp': firestore.SERVER_TIMESTAMP,
            'agent_id': 'supervisor_agent',
            'action_type': f'process_{input_type_str}',
            'outcome': 'success',
            'response_from_llm': final_message,
            'incident_id_created': incident_created_id
        }
        if is_video_input:
            log_data['target_entity_id'] = camera_id
            log_data['parameters'] = {'video_data_ref': video_data_ref, 'camera_id': camera_id, 'frame_timestamp': frame_timestamp, 'observations': observations}
        elif is_user_report_input:
            log_data['target_entity_id'] = incident_id_for_dispatch or 'new_user_report'
            log_data['parameters'] = request_json # Log the raw user report request
        AGENT_ACTIONS_COLLECTION.add(log_data)

        return {"message": final_message}

    except Exception as e:
        logger.exception(f"Error processing input for Supervisor Agent:") # Logs full traceback
        # Log error to Firestore
        error_log_data = {
            'timestamp': firestore.SERVER_TIMESTAMP,
            'agent_id': 'supervisor_agent',
            'action_type': f'process_{input_type_str}',
            'outcome': 'failure',
            'error_message': str(e)
        }
        if is_video_input:
            error_log_data['target_entity_id'] = request_json.get('camera_id', 'unknown_camera')
            error_log_data['parameters'] = request_json
        elif is_user_report_input:
            error_log_data['target_entity_id'] = request_json.get('incident_id') or 'new_user_report'
            error_log_data['parameters'] = request_json
        AGENT_ACTIONS_COLLECTION.add(error_log_data)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

# To run locally with Uvicorn:
# if __name__ == "__main__":
#     import uvicorn
#     # Set a dummy APP_ID for local testing if not already set in env
#     if 'APP_ID' not in os.environ:
#         os.environ['APP_ID'] = 'local-test-app'
#     uvicorn.run(app, host="0.0.0.0", port=8080)
