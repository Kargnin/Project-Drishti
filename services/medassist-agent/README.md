# MedAssist Agent

The MedAssist Agent is a component of the Drishti Event Management System designed to provide medical emergency response and coordination at large-scale events.

## Purpose

This agent specializes in:
- **Medical Emergency Detection**: Identifying life-threatening and urgent medical situations
- **Symptom Analysis**: Evaluating reported symptoms and medical conditions
- **Triage Assessment**: Prioritizing medical cases based on severity
- **Resource Allocation**: Coordinating medical personnel and equipment
- **Emergency Services Integration**: Connecting with ambulances and hospitals

## Capabilities

- **Multimodal Analysis**: Processes text descriptions, images, and video
- **Emergency Triage**: Classifies emergencies as critical, urgent, or non-urgent
- **Medical Response Coordination**: Provides actionable medical response guidance
- **Resource Management**: Recommends appropriate medical resources and timeline
- **Integration Support**: Connects with emergency services and medical databases

## Medical Categories

- **Trauma**: Falls, collisions, cuts, fractures, head injuries
- **Cardiac/Respiratory**: Heart attacks, breathing difficulties, chest pain
- **Neurological**: Seizures, unconsciousness, stroke symptoms
- **Allergic/Toxic**: Allergic reactions, poisoning, substance abuse
- **Environmental**: Heat stroke, dehydration, weather-related issues
- **Behavioral**: Mental health crises, psychiatric emergencies

## Usage

### Basic Usage

```python
from medassist_agent import medassist_agent, medassist_app

# Analyze medical emergency
result = await medassist_app.query(
    input_text="Person collapsed near main stage, appears unconscious",
    image_data=image_bytes  # optional
)

print(f"Emergency Level: {result['emergency_level']}")
print(f"Actions: {result['recommended_actions']}")
```

### Response Format

The agent returns a JSON response with:

```json
{
    "is_medical_emergency": true/false,
    "emergency_level": "critical"/"urgent"/"non-urgent",
    "confidence_score": 0.0-1.0,
    "triage_score": 1-10,
    "analysis": "Detailed medical assessment",
    "recommended_actions": ["action1", "action2"],
    "requires_immediate_response": true/false,
    "medical_categories": ["trauma", "cardiac", "neurological"],
    "visual_signs_detected": ["sign1", "sign2"],
    "resource_requirements": ["ambulance", "medical_team"],
    "estimated_response_time": "immediate"/"minutes"/"standard",
    "emergency_services_needed": true/false,
    "follow_up_care": "none"/"monitoring"/"transport"/"hospitalization"
}
```

## Triage Levels

- **CRITICAL (8-10)**: Life-threatening emergencies requiring immediate intervention
- **URGENT (4-7)**: Serious conditions requiring prompt medical attention
- **NON-URGENT (1-3)**: Minor injuries or routine medical needs

## Emergency Response Integration

### Emergency Services
- Automatic dispatch recommendations
- Resource requirement specifications
- Response time estimations
- Evacuation coordination

### Medical Databases
- Patient history integration (where available)
- Allergy and medication tracking
- Medical protocol adherence
- Documentation and reporting

## GCP Services Integration

- **Vertex AI**: Powers the AI analysis and decision-making
- **Cloud Healthcare API**: Integrates with medical databases and systems
- **Cloud Storage**: Stores medical images and documentation
- **Cloud Functions**: Triggers emergency response workflows

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export PROJECT_ID="your-gcp-project-id"
export LOCATION="us-central1"
export HEALTHCARE_PROJECT_ID="your-healthcare-project-id"
```

## Environment Variables

- `PROJECT_ID`: Google Cloud Project ID
- `LOCATION`: Google Cloud location (default: us-central1)
- `HEALTHCARE_PROJECT_ID`: Healthcare API project ID
- `EMERGENCY_SERVICES_ENDPOINT`: Emergency dispatch system endpoint

## Compliance and Privacy

- HIPAA compliance considerations
- Patient privacy protection
- Secure data transmission
- Audit logging and documentation
- Medical data retention policies

## Integration

This agent integrates with the broader Drishti Event Management System and works alongside security and infrastructure agents for comprehensive event safety and medical emergency management. 