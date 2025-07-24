# Drishti Security Agent

The Security Agent is a key component of the Drishti Event Management System that analyzes security threats and incidents using multimodal AI capabilities.

## Features

- **Multimodal Analysis**: Processes both text descriptions and images
- **Threat Level Assessment**: Evaluates security concerns as low, medium, or high priority
- **Google Cloud Integration**: Uses Vertex AI for advanced AI analysis
- **Real-time Processing**: Fast threat assessment for immediate response
- **Comprehensive Logging**: Stores all assessments and alerts in Firestore

## Architecture

The Security Agent consists of:

- `agent.py`: Main security agent implementation
- `config.py`: Configuration settings and threat level definitions
- `prompt.py`: AI prompt templates for security analysis
- `requirements.txt`: Python dependencies

## Threat Assessment Framework

### Threat Levels

- **LOW (1-3)**: Non-threatening issues like lost items, general assistance
- **MEDIUM (4-7)**: Suspicious behavior, unauthorized access, minor disturbances  
- **HIGH (8-10)**: Immediate danger, weapons, violence, emergencies

### Analysis Process

1. **Keyword Analysis**: Initial assessment based on security-related keywords
2. **AI Analysis**: Advanced evaluation using Gemini 1.5 Flash model
3. **Image Processing**: Visual threat detection (when image provided)
4. **Threat Scoring**: 1-10 scale assessment with confidence scoring
5. **Response Generation**: Recommended actions and escalation requirements

## API Endpoints

### POST /analyze_threat

Analyzes security threats from text description and optional image.

**Parameters:**
- `description` (required): Text description of the security issue
- `image` (optional): Image file for visual analysis
- `incident_id` (optional): Reference to existing incident
- `location` (optional): Location of the incident
- `reporter_id` (optional): ID of the person reporting

**Response:**
```json
{
    "is_security_concern": true,
    "threat_level": "medium",
    "confidence_score": 0.85,
    "threat_score": 6,
    "analysis": "Detailed analysis of the threat...",
    "recommended_actions": ["action1", "action2"],
    "requires_immediate_response": false,
    "visual_threats_detected": ["threat1"],
    "assessment_id": "assessment_123",
    "alert_id": "alert_456"
}
```

### GET /health

Health check endpoint.

### GET /threat_levels

Returns available threat levels and their configurations.

## Setup and Installation

### Prerequisites

- Python 3.8+
- Google Cloud Project with Vertex AI enabled
- Firestore database
- Service account with appropriate permissions

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
export PROJECT_ID="your-gcp-project-id"
export LOCATION="us-central1"
export APP_ID="your-app-id"
```

3. Set up Google Cloud authentication:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account-key.json"
```

### Running the Agent

#### As a FastAPI Service
```bash
python agent.py
```

The service will start on `http://localhost:8081`

#### As a Python Module
```python
from security_agent import SecurityAgent

agent = SecurityAgent()
result = await agent.analyze_security_threat(
    description="Suspicious person near entrance",
    location="Main entrance"
)
print(f"Threat level: {result['threat_level']}")
```

## Configuration

### Threat Level Thresholds

Modify `THREAT_LEVELS` in `config.py` to adjust scoring thresholds:

```python
THREAT_LEVELS = {
    'low': {'score_range': (0, 3), 'response_time': '30 minutes'},
    'medium': {'score_range': (4, 7), 'response_time': '10 minutes'},
    'high': {'score_range': (8, 10), 'response_time': 'immediate'}
}
```

### Security Keywords

Update `SECURITY_KEYWORDS` in `config.py` to modify keyword-based detection:

```python
SECURITY_KEYWORDS = {
    'high_risk': ['weapon', 'knife', 'gun', 'fire', 'emergency'],
    'medium_risk': ['suspicious', 'unauthorized', 'disturbance'],
    'low_risk': ['lost', 'found', 'noise complaint']
}
```

## Testing

Run the test script to validate functionality:

```bash
python test_security_agent.py
```

## Integration with Drishti System

The Security Agent integrates with other Drishti components:

- **Supervisor Agent**: Receives incident reports and dispatches to Security Agent
- **Firestore**: Stores threat assessments and security alerts
- **Event Management**: Triggers response protocols based on threat levels

## Monitoring and Logging

- All threat assessments are logged to Firestore
- Security alerts are created for medium/high threats
- Error logging for failed analyses
- Performance metrics tracking

## Security Considerations

- Image validation and size limits
- Input sanitization for text descriptions
- Rate limiting on API endpoints
- Audit logging for all security assessments
- Encrypted storage of sensitive data

## Future Enhancements

- Real-time video stream analysis
- Integration with physical security systems
- Machine learning model improvements
- Advanced behavioral analysis
- Automated response coordination

## Support

For issues or questions, refer to the main Drishti documentation or contact the development team. 