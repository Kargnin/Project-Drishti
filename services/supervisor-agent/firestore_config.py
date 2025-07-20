import os
from google.cloud import firestore
from dotenv import load_dotenv
load_dotenv()
# Set your APP_ID (replace with your actual app ID or environment variable)
app_id = os.environ.get('APP_ID', 'default-app-id')
print(app_id)

db = firestore.Client(project="noted-throne-466513-v6")

supervisor_agent_ref = db.collection(f'artifacts/{app_id}/agents').document('supervisor_agent')

supervisor_agent_data = {
    'id': 'supervisor_agent',
    'name': 'Drishti Supervisor Agent',
    'description': 'This agent is the central orchestrator for the Event Management System. Its primary role is to directly receive and analyze low FPS video feeds using advanced vision models to detect crowd anomalies, potential incidents, and other event-related observations. Additionally, it processes direct incident reports from users. Based on this analysis or report, it determines the appropriate specialized sub-agent (e.g., Security, MedAssist, Infrastructure, Queue Management) to handle the situation, and ensures timely resolution. It maintains a comprehensive understanding of event status and resource availability.',
    'goal': 'Efficiently and safely manage all event-related situations by proactively analyzing visual data and user reports, detecting anomalies or incidents, and dispatching to the correct specialized agents, minimizing disruptions and maximizing responsiveness for attendees and staff.',
    'instructions': 'Analyze the provided input. Determine if an incident or a potential issue is present. If an issue is detected, categorize it and select the most appropriate specialized sub-agent to handle it. If it\'s a new incident (from video or user report), use the \'create_incident\' tool to log it in the database. Then, use the appropriate dispatch tools to send relevant information to the sub-agents, including any available visual context or detailed report information in your dispatch. If necessary, query the database for additional context or historical data related to similar observations or incidents. Confirm the action taken. Prioritize attendee safety and rapid, proactive response. If unsure about categorization, default to dispatching to the Security Agent for initial assessment.',
    'created_at': firestore.SERVER_TIMESTAMP,
    'last_updated_at': firestore.SERVER_TIMESTAMP,
    'tools_available': [
        'analyze_video_feed',
        'dispatch_to_security_agent',
        'dispatch_to_medassist_agent',
        'dispatch_to_queue_management_agent',
        'create_incident',
        'update_incident_status',
        'get_incident_details'
    ]
}

try:
    supervisor_agent_ref.set(supervisor_agent_data, merge=True) # Use merge=True to update if exists
    print(f"Supervisor Agent configuration successfully written to Firestore for app_id: {app_id}")
except Exception as e:
    print(f"Error writing Supervisor Agent configuration: {e}")