# User Input Analysis Agent

The User Input Analysis Agent is a component of the Drishti Event Management System designed to process and validate user-reported incidents from various input types and intelligently route them to the appropriate specialized agents.

## Purpose

This agent specializes in:
- **Multimodal Input Processing**: Handle text reports, images, voice messages, and mixed inputs
- **Incident Validation**: Verify and structure user-reported information
- **Intelligent Categorization**: Classify incidents and determine appropriate responses
- **Agent Routing**: Direct validated incidents to the correct specialized agents
- **Natural Language Understanding**: Process user inputs in multiple languages and formats

## Capabilities

- **Text Analysis**: Natural language processing for incident reports and requests
- **Image Processing**: Visual analysis of user-submitted photos and screenshots
- **Voice Recognition**: Speech-to-text conversion and emotional analysis
- **Multilingual Support**: Process inputs in multiple languages with translation
- **Intelligent Routing**: Automated routing to appropriate specialized agents

## Technical Features

### GCP Services Integration
- **Natural Language AI**: Advanced text understanding and entity extraction
- **Cloud Speech-to-Text**: Voice message processing and transcription
- **Cloud Vision**: Image analysis and visual content understanding
- **Cloud Functions**: Serverless processing for real-time input handling
- **Cloud Storage**: Storage for multimedia inputs and processing results

### Input Types Supported
- **Text Reports**: Written descriptions in natural language
- **Images**: Photos, screenshots, visual evidence
- **Voice Messages**: Audio recordings with speech and emotional analysis
- **Structured Data**: Forms, surveys, and pre-formatted inputs
- **Multimodal**: Combinations of text, images, and voice

## Usage

### Basic Usage

```python
from user_input_agent import user_input_agent, user_input_app

# Process user text report
result = await user_input_app.query(
    input_text="There's a medical emergency near the main stage, person collapsed",
    input_type="text",
    user_context={"location": "festival_grounds", "user_type": "attendee"}
)

print(f"Target Agent: {result['routing_decision']['target_agent']}")
print(f"Urgency: {result['incident_details']['urgency_level']}")
```

### Response Format

The agent returns a JSON response with:

```json
{
    "input_processed": true/false,
    "input_summary": "Brief summary of user input and context",
    "validation_status": "valid"/"incomplete"/"invalid",
    "confidence_score": 0.0-1.0,
    "incident_details": {
        "category": "security"/"medical"/"infrastructure"/"crowd"/"communication"/"environmental"/"other",
        "subcategory": "specific incident type",
        "urgency_level": "critical"/"high"/"medium"/"low",
        "urgency_score": 1-10,
        "location": "specific location if provided",
        "time_reported": "timestamp or relative time",
        "people_involved": "number or description of people affected",
        "description": "structured description of the incident"
    },
    "extracted_data": {
        "key_keywords": ["keyword1", "keyword2"],
        "entities": ["person", "location", "object"],
        "sentiment": "urgent"/"concerned"/"calm"/"panicked",
        "language_detected": "en"/"es"/"fr"/etc,
        "location_coordinates": "if determinable from input"
    },
    "routing_decision": {
        "target_agent": "security_agent"/"medassist_agent"/"infrastructure_agent"/"crowdflow_agent"/"queue_management_agent"/"comms_resources_agent"/"supervisor_agent",
        "routing_reason": "explanation for agent selection",
        "priority_level": 1-10,
        "requires_multiple_agents": true/false,
        "additional_agents": ["agent1", "agent2"] if applicable
    },
    "data_for_target": {
        "formatted_input": "incident data formatted for target agent",
        "context_info": "additional context for processing",
        "user_contact": "contact information if provided",
        "follow_up_required": true/false
    },
    "validation_issues": {
        "missing_information": ["missing_field1", "missing_field2"],
        "clarification_needed": ["clarification1", "clarification2"],
        "follow_up_questions": ["question1", "question2"]
    },
    "processing_metadata": {
        "input_type": "text"/"image"/"voice"/"multimodal",
        "processing_time": "milliseconds",
        "language_processing": "translation_needed"/"direct_processing",
        "quality_score": 0.0-1.0
    },
    "requires_escalation": true/false
}
```

## Incident Categories

- **SECURITY**: Threats, suspicious activity, violence, unauthorized access
- **MEDICAL**: Injuries, illness, health emergencies, medical assistance needed
- **INFRASTRUCTURE**: Equipment failure, power issues, structural problems
- **CROWD**: Overcrowding, flow issues, stampede risk, density problems
- **COMMUNICATION**: Information requests, lost persons, general assistance
- **ENVIRONMENTAL**: Weather issues, hazards, safety concerns
- **OTHER**: Uncategorized or multi-category incidents

## Urgency Assessment

- **CRITICAL (8-10)**: Life-threatening emergency, immediate response required
- **HIGH (6-7)**: Urgent situation, prompt response needed
- **MEDIUM (4-5)**: Important issue, standard response timeline
- **LOW (1-3)**: Routine matter, non-urgent handling

## Agent Routing Logic

### Primary Agent Routing
- **Security Agent**: Security threats, violent incidents, theft, unauthorized access
- **MedAssist Agent**: Medical emergencies, injuries, health issues, first aid needs
- **Infrastructure Agent**: Equipment failures, power issues, structural problems
- **CrowdFlow Agent**: Crowd density analysis, overcrowding, stampede prevention
- **Queue Management Agent**: Line management, flow optimization, wait time issues
- **Communication & Resources Agent**: Resource requests, coordination needs
- **Supervisor Agent**: Complex incidents, multi-agent coordination, escalations

### Multi-Agent Scenarios
- **Medical + Security**: Medical emergency with security concerns
- **Crowd + Security**: Overcrowding with potential security risks
- **Infrastructure + Communication**: Equipment failure requiring resource coordination
- **Any + Supervisor**: Complex situations requiring strategic oversight

## Input Processing Pipeline

### Text Processing
1. **Language Detection**: Identify input language using langdetect
2. **Translation**: Convert to English if needed using Cloud Translation
3. **Entity Extraction**: Extract people, places, times, objects using NLP
4. **Intent Classification**: Determine user's primary intent
5. **Sentiment Analysis**: Assess emotional state and urgency level

### Image Processing
1. **Image Upload**: Receive and validate image files
2. **Vision Analysis**: Use Cloud Vision for scene understanding
3. **Safety Assessment**: Identify visible hazards or emergency indicators
4. **Text Extraction**: OCR for any text content in images
5. **Context Integration**: Combine visual and textual information

### Voice Processing
1. **Audio Reception**: Accept voice messages in various formats
2. **Speech-to-Text**: Convert audio to text using Cloud Speech-to-Text
3. **Emotional Analysis**: Analyze tone and speech patterns for urgency
4. **Background Analysis**: Process environmental sounds for context
5. **Text Processing**: Apply standard text analysis to transcribed content

## Validation Framework

### Quality Assessment
- **High Quality**: Complete information, clear description, verifiable facts
- **Medium Quality**: Most information present, minor ambiguities
- **Low Quality**: Incomplete information, significant gaps
- **Poor Quality**: Minimal information, unclear intent

### Validation Checks
- **Location Validation**: Verify location exists and is accessible
- **Timeline Validation**: Ensure reported timing makes sense
- **Severity Validation**: Assess if described severity matches incident type
- **Consistency Validation**: Check for internal contradictions

### Missing Information Handling
- **Critical Gaps**: Information essential for response
- **Important Gaps**: Information that improves response effectiveness
- **Minor Gaps**: Information that would be helpful but not necessary
- **Follow-up Questions**: Automated generation of clarifying questions

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export PROJECT_ID="your-gcp-project-id"
export LOCATION="us-central1"
export LANGUAGE_API_KEY="your-language-api-key"
export SPEECH_API_KEY="your-speech-api-key"
export VISION_API_KEY="your-vision-api-key"
```

## Environment Variables

- `PROJECT_ID`: Google Cloud Project ID
- `LOCATION`: Google Cloud location (default: us-central1)
- `LANGUAGE_API_KEY`: Natural Language AI API credentials
- `SPEECH_API_KEY`: Cloud Speech-to-Text API credentials
- `VISION_API_KEY`: Cloud Vision API credentials
- `STORAGE_BUCKET`: Cloud Storage bucket for input files

## Key Metrics

### Processing Effectiveness
- **Categorization Accuracy**: Percentage of correctly categorized incidents
- **Routing Precision**: Accuracy of agent routing decisions
- **Validation Success Rate**: Percentage of inputs successfully validated
- **Response Time**: Time from input to routing decision

### Input Quality Metrics
- **Completeness Score**: Average completeness of processed inputs
- **Clarity Rating**: Average clarity score of user inputs
- **Follow-up Rate**: Percentage of inputs requiring clarification
- **Resolution Success**: Percentage of inputs leading to successful incident resolution

### User Experience Metrics
- **User Satisfaction**: Feedback from users on input process
- **Ease of Use**: User rating of input submission process
- **Response Time**: Speed of initial acknowledgment and processing
- **Multilingual Effectiveness**: Success rate across different languages

## Integration with Other Agents

### Data Flow
1. **User Input Reception**: Accept and validate user submissions
2. **Processing and Analysis**: Extract and structure incident information
3. **Categorization and Routing**: Determine appropriate target agent
4. **Data Formatting**: Format data for target agent consumption
5. **Handoff and Tracking**: Transfer to target agent and monitor progress

### Agent Coordination
- **Security Agent**: Route security-related incidents with threat assessment
- **MedAssist Agent**: Route medical emergencies with urgency prioritization
- **Infrastructure Agent**: Route maintenance issues with asset information
- **CrowdFlow Agent**: Route crowd-related concerns with density context
- **Queue Management Agent**: Route flow issues with operational context
- **Communication Agent**: Coordinate response communications and updates
- **Supervisor Agent**: Escalate complex or multi-category incidents

## Best Practices

1. **User-Friendly Processing**: Make incident reporting as easy as possible
2. **Privacy Protection**: Handle user data securely and confidentially
3. **Cultural Sensitivity**: Respect cultural differences in communication styles
4. **Response Timeliness**: Process urgent incidents with minimal delay
5. **Quality Feedback**: Provide clear feedback on input quality and next steps
6. **Continuous Learning**: Improve categorization and routing based on outcomes

This agent serves as the intelligent front door for the entire Drishti Event Management System, making it accessible and responsive to user-reported incidents while ensuring efficient routing to specialized response capabilities. 