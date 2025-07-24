# Queue Management Agent

The Queue Management Agent is a component of the Drishti Event Management System designed to optimize crowd flow and reduce wait times at large-scale events.

## Purpose

This agent specializes in:
- **Crowd Flow Optimization**: Analyzing and improving people movement patterns
- **Wait Time Reduction**: Minimizing queue delays and improving efficiency
- **Staff Allocation**: Optimizing personnel deployment based on crowd data
- **Bottleneck Identification**: Detecting and resolving flow impediments
- **Predictive Analytics**: Forecasting crowd patterns using historical data

## Capabilities

- **Multimodal Analysis**: Processes camera feeds, historical data, and user input
- **Flow Assessment**: Evaluates crowd efficiency as optimal, moderate, congested, or critical
- **Real-time Monitoring**: Provides live queue analysis and recommendations
- **Predictive Modeling**: Uses BigQuery Analytics for pattern recognition and forecasting
- **Staff Optimization**: Recommends personnel redeployment and additional staffing needs

## Queue Categories

- **Entry/Exit Points**: Gates, security checkpoints, venue entrances
- **Service Areas**: Food vendors, merchandise, restrooms, information booths
- **Entertainment Zones**: Stage areas, rides, attractions, photo opportunities
- **Transportation**: Parking, shuttle services, public transit connections

## Usage

### Basic Usage

```python
from queue_management_agent import queue_management_agent, queue_management_app

# Analyze queue situation
result = await queue_management_app.query(
    input_text="Long lines forming at entrance gate 3, people getting frustrated",
    camera_feed_data=camera_data  # optional
)

print(f"Flow Efficiency: {result['flow_efficiency']}")
print(f"Staff Needed: {result['staff_allocation']['additional_staff_needed']}")
```

### Response Format

The agent returns a JSON response with:

```json
{
    "requires_intervention": true/false,
    "flow_efficiency": "optimal"/"moderate"/"congested"/"critical",
    "confidence_score": 0.0-1.0,
    "congestion_score": 1-10,
    "analysis": "Detailed crowd flow assessment",
    "flow_recommendations": ["recommendation1", "recommendation2"],
    "staff_allocation": {
        "additional_staff_needed": 0-20,
        "redeployment_suggestions": ["suggestion1", "suggestion2"],
        "priority_locations": ["location1", "location2"]
    },
    "estimated_wait_times": {
        "current_wait": "5-15 minutes",
        "predicted_wait": "10-20 minutes",
        "peak_time_wait": "30-45 minutes"
    },
    "queue_categories": ["entry_exit", "service_areas"],
    "visual_crowd_metrics": {
        "queue_length": "short/medium/long/excessive",
        "crowd_density": "low/medium/high/critical",
        "movement_flow": "free/slow/stagnant"
    },
    "bottleneck_locations": ["location1", "location2"],
    "capacity_utilization": 0.0-1.0,
    "recommended_actions": {
        "immediate": ["action1", "action2"],
        "short_term": ["action1", "action2"],
        "long_term": ["action1", "action2"]
    }
}
```

## Flow Efficiency Levels

- **OPTIMAL (1)**: Free flow, minimal wait times (<5 min), efficient operations
- **MODERATE (2-3)**: Some queuing, acceptable wait times (5-15 min), manageable flow
- **CONGESTED (4-7)**: Moderate to heavy congestion, long wait times (15-60 min)
- **CRITICAL (8-10)**: Severe congestion, safety risks, excessive wait times (>60 min)

## Analytics Integration

### BigQuery Analytics
- Historical pattern analysis and trend identification
- Peak time prediction and capacity planning
- Performance metrics and KPI tracking
- Real-time data warehouse for crowd analytics

### Data Sources
- **Camera Feeds**: Real-time visual crowd analysis
- **Historical Patterns**: Past event data and trends
- **User Input**: Staff reports and attendee feedback
- **Sensor Data**: People counters and IoT devices

## GCP Services Integration

- **Vertex AI**: Powers the AI analysis and decision-making
- **BigQuery**: Stores and analyzes historical crowd data
- **Cloud Storage**: Manages camera feed data and analytics
- **Cloud Functions**: Triggers automated responses and alerts

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export PROJECT_ID="your-gcp-project-id"
export LOCATION="us-central1"
export BIGQUERY_DATASET="crowd_analytics"
export STORAGE_BUCKET="queue-management-data"
```

## Environment Variables

- `PROJECT_ID`: Google Cloud Project ID
- `LOCATION`: Google Cloud location (default: us-central1)
- `BIGQUERY_DATASET`: BigQuery dataset for crowd analytics
- `STORAGE_BUCKET`: Cloud Storage bucket for camera feed data

## Key Metrics

### Queue Performance
- Average wait time reduction
- Queue length optimization
- Service throughput improvement
- Customer satisfaction scores

### Staff Efficiency
- Staff utilization rates
- Response time to congestion
- Deployment effectiveness
- Cost per attendee managed

### Crowd Safety
- Density monitoring and alerts
- Emergency evacuation planning
- Accessibility compliance
- Incident prevention rates

## Best Practices

1. **Proactive Management**: Use predictive analytics to prevent issues
2. **Dynamic Staffing**: Adjust personnel based on real-time data
3. **Clear Communication**: Provide wait time information to attendees
4. **Accessibility Focus**: Ensure inclusive queue management
5. **Safety First**: Prioritize crowd safety over efficiency gains

## Integration

This agent integrates with the broader Drishti Event Management System and works alongside security, infrastructure, and medical agents for comprehensive event management and crowd safety optimization. 