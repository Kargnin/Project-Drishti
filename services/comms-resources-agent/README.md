# Communication & Resource Management Agent

The Communication & Resource Management Agent is a component of the Drishti Event Management System designed to coordinate communication and deploy resources based on instructions from other agents or supervisors.

## Purpose

This agent specializes in:
- **Communication Coordination**: Multilingual broadcasting and announcement management
- **Resource Deployment**: Staff, equipment, and vehicle allocation and dispatch
- **Emergency Broadcasting**: Critical announcement systems and emergency alerts
- **Drone Operations**: Aerial surveillance, delivery, and monitoring coordination
- **Weather Integration**: Environmental monitoring and weather-based resource adjustment

## Capabilities

- **Multilingual Support**: Real-time translation and culturally appropriate messaging
- **Resource Optimization**: Efficient allocation based on priority and availability
- **Multi-Channel Broadcasting**: PA systems, digital displays, mobile apps, social media
- **Emergency Coordination**: Integration with emergency services and authorities
- **Weather-Aware Planning**: Environmental factor consideration in all deployments

## Technical Features

### GCP Services Integration
- **Translation API**: Real-time multilingual communication
- **Text-to-Speech**: Audio announcement generation and delivery
- **Pub/Sub**: Messaging and coordination between services
- **Cloud Storage**: Resource documentation and communication assets

### Communication Channels
- **Public Address Systems**: Live announcements with speaker networks
- **Digital Displays**: Visual messaging and multilingual text
- **Mobile Applications**: Push notifications in user's preferred language
- **Social Media**: Real-time updates on official event channels
- **Radio Systems**: Staff coordination and emergency services

## Usage

### Basic Usage

```python
from comms_resources_agent import comms_resources_agent, comms_resources_app

# Coordinate emergency response
result = await comms_resources_app.query(
    input_text="Deploy medical team to main stage area immediately",
    priority="emergency",
    language_preferences=["en", "es", "fr"]
)

print(f"Resources Deployed: {result['resource_deployment']}")
print(f"Announcements: {result['communication_actions']}")
```

### Response Format

The agent returns a JSON response with:

```json
{
    "instruction_understood": true/false,
    "priority_level": "emergency"/"high"/"medium"/"low",
    "urgency_score": 1-10,
    "coordination_plan": "Detailed coordination approach",
    "communication_actions": {
        "announcements": [
            {
                "message": "Emergency evacuation notice",
                "language": "en",
                "channel": "public_address",
                "audience": "all_attendees"
            }
        ],
        "translations_needed": ["es", "fr", "de"],
        "broadcast_priority": "emergency"/"high"/"standard",
        "delivery_method": "audio"/"visual"/"both"
    },
    "resource_deployment": {
        "personnel": [
            {
                "type": "medical_team",
                "quantity": 2,
                "location": "main_stage",
                "eta": "5 minutes"
            }
        ],
        "equipment": [
            {
                "type": "emergency_barriers",
                "quantity": 10,
                "location": "exit_gate_3"
            }
        ],
        "vehicles": [
            {
                "type": "drone",
                "purpose": "aerial_assessment",
                "deployment_area": "festival_grounds"
            }
        ]
    },
    "weather_considerations": {
        "current_conditions": "partly_cloudy",
        "impact_on_operations": "minimal"/"moderate"/"significant",
        "weather_alerts": ["rain_warning"]
    },
    "coordination_requirements": {
        "agents_to_notify": ["security_agent", "medassist_agent"],
        "external_services": ["emergency_dispatch", "weather_service"],
        "follow_up_actions": ["monitor_situation", "prepare_backup_plan"]
    },
    "estimated_timeline": {
        "immediate": "0-5 minutes",
        "short_term": "5-30 minutes", 
        "long_term": "30+ minutes"
    },
    "success_metrics": ["resource_deployment_time", "communication_reach"],
    "requires_escalation": true/false
}
```

## Priority Levels

- **EMERGENCY (8-10)**: Life-threatening situations, immediate broadcast, all resources
- **HIGH (6-7)**: Urgent situations, priority communication, significant resources
- **MEDIUM (4-5)**: Important situations, standard communication, moderate allocation
- **LOW (1-3)**: Routine operations, informational communication, minimal resources

## Resource Categories

### Personnel
- **Security Staff**: Crowd control, access management, threat response
- **Medical Teams**: Emergency response, first aid, triage support
- **Maintenance Crews**: Infrastructure repair, equipment setup, environmental management
- **Crowd Management**: Flow coordination, queue management, guidance services

### Equipment
- **Communication Devices**: Radios, speakers, translation equipment
- **Medical Equipment**: First aid supplies, stretchers, defibrillators
- **Safety Equipment**: Barriers, signage, emergency lighting
- **Technical Equipment**: Monitoring devices, cameras, weather stations

### Vehicles
- **Drones**: Surveillance, delivery, emergency response, monitoring
- **Ambulances**: Medical transport and emergency response
- **Security Vehicles**: Patrol, crowd control, equipment transport
- **Maintenance Trucks**: Equipment delivery, infrastructure support

## Communication Features

### Multilingual Broadcasting
- **Real-time Translation**: 50+ languages supported via GCP Translation API
- **Cultural Adaptation**: Context-aware messaging for different audiences
- **Accessibility**: Visual and audio support for diverse needs
- **Voice Synthesis**: Natural-sounding announcements via Text-to-Speech

### Emergency Broadcasting
- **Priority Messaging**: Override capabilities for critical announcements
- **Multi-Channel Delivery**: Simultaneous broadcast across all platforms
- **Confirmation Systems**: Delivery verification and acknowledgment tracking
- **Escalation Protocols**: Automatic escalation for failed deliveries

## Drone Operations

### Mission Types
- **Surveillance**: Crowd monitoring, security assessment, incident investigation
- **Emergency Response**: Search and rescue, medical supply delivery
- **Environmental Monitoring**: Weather tracking, air quality assessment
- **Communication Relay**: Emergency broadcasting, network extension

### Safety Protocols
- **Airspace Compliance**: FAA and local authority coordination
- **Crowd Safety**: Minimum altitude and safety zone maintenance
- **Emergency Procedures**: Automatic landing and failsafe protocols
- **Weather Restrictions**: Operational limits based on conditions

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export PROJECT_ID="your-gcp-project-id"
export LOCATION="us-central1"
export TRANSLATION_API_KEY="your-translation-key"
export PUBSUB_TOPIC="event-coordination"
export WEATHER_API_KEY="your-weather-api-key"
```

## Environment Variables

- `PROJECT_ID`: Google Cloud Project ID
- `LOCATION`: Google Cloud location (default: us-central1)
- `TRANSLATION_API_KEY`: GCP Translation API credentials
- `PUBSUB_TOPIC`: Pub/Sub topic for inter-agent communication
- `WEATHER_API_KEY`: Weather service API credentials
- `DRONE_CONTROL_ENDPOINT`: Drone management system endpoint

## Integration Capabilities

### Agent Coordination
- **Security Agent**: Resource deployment for threat response
- **MedAssist Agent**: Medical resource allocation and emergency communication
- **Infrastructure Agent**: Maintenance crew deployment and equipment allocation
- **Queue Management**: Staff redeployment and flow optimization
- **CrowdFlow Agent**: Density-based resource allocation and safety broadcasts
- **Supervisor Agent**: Strategic coordination and resource oversight

### External Services
- **Emergency Services**: 911 dispatch, fire department, police coordination
- **Weather Services**: Real-time weather data and alert integration
- **Transportation**: Public transit, parking, shuttle coordination
- **Media Relations**: Press coordination and public information management

## Key Metrics

### Communication Effectiveness
- Message delivery success rates across channels
- Translation accuracy and cultural appropriateness
- Response time for emergency broadcasts
- Audience reach and engagement metrics

### Resource Deployment Efficiency
- Response time from request to deployment
- Resource utilization and availability tracking
- Cost optimization and efficiency metrics
- Success rate of deployment objectives

### Coordination Quality
- Inter-agent communication effectiveness
- External service integration success
- Escalation and resolution timelines
- Overall system coordination performance

## Best Practices

1. **Clear Communication**: Use simple, direct language for all announcements
2. **Cultural Sensitivity**: Adapt messages for diverse audiences and cultures
3. **Resource Optimization**: Balance efficiency with redundancy for critical resources
4. **Weather Awareness**: Factor environmental conditions into all decisions
5. **Safety First**: Prioritize life safety over operational efficiency
6. **Continuous Monitoring**: Track all deployments and communications in real-time

This agent serves as the central nervous system for communication and resource coordination, ensuring efficient and effective response to all event management needs. 