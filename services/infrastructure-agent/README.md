# Infrastructure Agent

The Infrastructure Agent is a component of the Drishti Event Management System designed to monitor and manage physical infrastructure at large-scale events.

## Purpose

This agent specializes in monitoring:
- **Power Systems**: Electrical distribution, generators, UPS systems, lighting
- **Connectivity**: Network infrastructure, communication systems, internet connectivity  
- **Structural Integrity**: Buildings, stages, barriers, roofing, foundations
- **Environmental Systems**: HVAC, water supply, waste management, drainage

## Capabilities

- **Multimodal Analysis**: Processes both text descriptions and images
- **Status Assessment**: Evaluates infrastructure status as operational, degraded, or critical
- **Maintenance Recommendations**: Provides actionable maintenance and repair guidance
- **Failover Procedures**: Suggests backup systems and emergency procedures
- **Impact Analysis**: Assesses potential effects on event operations

## Usage

### Basic Usage

```python
from infrastructure_agent import infrastructure_agent, infrastructure_app

# Analyze infrastructure status
result = await infrastructure_app.query(
    input_text="Power fluctuations detected in main pavilion",
    image_data=image_bytes  # optional
)

print(f"Status: {result['status_level']}")
print(f"Actions: {result['recommended_actions']}")
```

### Response Format

The agent returns a JSON response with:

```json
{
    "is_infrastructure_concern": true/false,
    "status_level": "operational"/"degraded"/"critical",
    "confidence_score": 0.0-1.0,
    "status_score": 1-10,
    "analysis": "Detailed assessment",
    "recommended_actions": ["action1", "action2"],
    "requires_immediate_response": true/false,
    "affected_systems": ["power", "connectivity", "structural", "environmental"],
    "visual_issues_detected": ["issue1", "issue2"],
    "maintenance_priority": "low"/"medium"/"high",
    "estimated_downtime": "immediate"/"hours"/"days"/"planned"
}
```

## Status Levels

- **OPERATIONAL (1-3)**: Normal operations, minor maintenance needed
- **DEGRADED (4-7)**: Partial system failure, reduced functionality
- **CRITICAL (8-10)**: Complete system failure, immediate attention required

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export PROJECT_ID="your-gcp-project-id"
export LOCATION="us-central1"
```

## Environment Variables

- `PROJECT_ID`: Google Cloud Project ID
- `LOCATION`: Google Cloud location (default: us-central1)

## Integration

This agent integrates with the broader Drishti Event Management System and can be used alongside other specialized agents for comprehensive event monitoring and management. 