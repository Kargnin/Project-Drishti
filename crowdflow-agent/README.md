# CrowdFlow Agent - Two-Agent Pipeline

The CrowdFlow Agent is a sequential two-agent pipeline component of the Drishti Event Management System designed to analyze video input, generate structured crowd data, and provide forecasting with severity assessment for comprehensive crowd management.

## Pipeline Architecture

This system implements a **sequential two-agent pipeline** using Google's Agent Development Kit (ADK):

### Agent 1: Video Analysis Agent

-   **Input**: Video streams, camera feeds, image sequences
-   **Processing**: Analyzes at 5 FPS (every 5 seconds) using YOLOv3 detection
-   **Output**: Structured JSON tabular data with timestamp, crowd_density, crowd_velocity, crowd_behavior
-   **Storage**: Data stored in BigQuery for downstream consumption

### Agent 2: Forecasting & Severity Analysis Agent

-   **Input**: Historical tabular data from Agent 1 or BigQuery
-   **Processing**: Time-series analysis, trend prediction, anomaly detection
-   **Output**: Predicted future values + severity scores (1-10 scale)
-   **Features**: Early warning system, risk assessment, actionable recommendations

## Key Features

### Video Analysis (Agent 1)

-   **Frame Sampling**: 5 FPS analysis rate (every 5 seconds)
-   **Computer Vision**: YOLOv3 person detection with >0.5 confidence
-   **Density Calculation**: People per square meter analysis
-   **Velocity Tracking**: Movement speed analysis (m/s)
-   **Behavior Classification**: Normal, congested, excited, agitated, panic, dispersing

### Forecasting & Severity (Agent 2)

-   **Time Series Prediction**: Forecast next timestamp values
-   **Severity Scoring**: 1-10 risk assessment scale
-   **Anomaly Detection**: Statistical outlier identification
-   **Trend Analysis**: Growth rate and pattern recognition
-   **Early Warnings**: Critical threshold predictions

### Data Pipeline

-   **BigQuery Integration**: Structured data storage and retrieval
-   **Real-time Processing**: 5-second analysis cycles
-   **A2A Communication**: Agent-to-agent data flow
-   **Scalable Architecture**: Cloud-native deployment ready

## Usage

### Complete Pipeline (Video → Analysis → Forecasting)

```python
from crowdflow_agent import crowdflow_app

# Video analysis pipeline
video_input = {
    "type": "video_analysis",
    "video_source": "camera_feed_zone_a.mp4",
    "analysis_params": {
        "fps_sampling": 5,
        "frame_interval": "5_seconds"
    }
}

# The pipeline automatically:
# 1. Processes video with video_analysis_agent
# 2. Generates tabular data
# 3. Calls forecasting_agent with the data
# 4. Returns integrated analysis + predictions
result = await crowdflow_app.query(video_input)
```

### Historical Data Analysis (Forecasting Only)

```python
# Direct forecasting from historical data
historical_data = {
    "type": "forecasting_analysis",
    "historical_data": [
        {
            "timestamp": "2024-01-15T14:25:00Z",
            "crowd_density": 3.2,
            "crowd_velocity": 0.6,
            "crowd_behavior": "normal"
        }
        # ... more data points
    ]
}

result = await crowdflow_app.query(historical_data)
```

### Response Format

````

## Output Format

### Video Analysis Output (Agent 1)
```json
{
    "pipeline_execution": {
        "stage_1_completed": true,
        "stage_2_completed": true,
        "execution_time": "2024-01-15T14:30:00Z",
        "data_quality_score": 0.92
    },
    "video_analysis_results": [
        {
            "timestamp": "2024-01-15T14:30:00Z",
            "crowd_density": 4.2,
            "crowd_velocity": 0.3,
            "crowd_behavior": "congested",
            "frame_analysis": {
                "detected_persons": 85,
                "coverage_area_sqm": 250,
                "confidence_score": 0.92
            }
        }
    ]
}
````

### Forecasting Output (Agent 2)

```json
{
    "forecast": {
        "next_timestamp": "2024-01-15T14:30:10Z",
        "predicted_crowd_density": 5.4,
        "predicted_crowd_velocity": 0.1,
        "predicted_crowd_behavior": "agitated",
        "prediction_confidence": 0.85
    },
    "severity_analysis": {
        "severity_score": 7,
        "risk_level": "high",
        "primary_risk_factors": ["increasing_density", "decreasing_velocity"],
        "trend_analysis": {
            "density_trend": "increasing",
            "velocity_trend": "decreasing"
        }
    },
    "recommendations": ["Monitor density levels closely", "Prepare crowd control measures", "Consider opening additional exit routes"],
    "early_warnings": {
        "critical_threshold_eta": "10-15 minutes",
        "intervention_recommended": true,
        "alert_level": "yellow"
    }
}
```

## BigQuery Data Schema

### crowd_analysis_data Table

-   `timestamp`: Analysis timestamp (5-second intervals)
-   `crowd_density`: People per square meter
-   `crowd_velocity`: Average movement speed (m/s)
-   `crowd_behavior`: Categorical behavior classification
-   `detected_persons`: YOLOv3 detection count
-   `coverage_area_sqm`: Analysis area in square meters
-   `confidence_score`: Analysis confidence (0.0-1.0)

### crowd_forecasts Table

-   `analysis_timestamp`: When forecast was generated
-   `forecast_timestamp`: Predicted timestamp
-   `predicted_crowd_density`: Forecasted density
-   `severity_score`: Risk score (1-10)
-   `risk_level`: low/moderate/high/critical
-   `recommendations`: Array of action items

## Severity Scoring (1-10 Scale)

-   **1-2 (Minimal)**: Low density, normal behavior, stable trends
-   **3-4 (Low)**: Moderate density, steady patterns
-   **5-6 (Moderate)**: Increasing density, behavior changes
-   **7-8 (High)**: High density, rapid changes, concerning patterns
-   **9-10 (Critical)**: Dangerous overcrowding, panic behavior

## Deployment

### Google Cloud Agent Engine

```python
from vertexai import agent_engines
from crowdflow_agent import crowdflow_app

# Deploy with A2A enabled
remote_app = agent_engines.create(
    agent_engine=crowdflow_app,  # Already A2A enabled
    requirements=[
        "google-cloud-aiplatform[adk,agent_engines]",
        "google-cloud-bigquery",
        "opencv-python",
        "numpy"
    ],
    extra_packages=["./crowdflow-agent"]
)
```

### BigQuery Setup

```bash
# Create dataset and tables
bq mk --dataset --location=US project_id:crowdflow_data
python bigquery_schema.py  # Creates tables with proper schema
```

## Architecture Benefits

1. **Modular Design**: Separate video analysis and forecasting concerns
2. **Scalable Processing**: Each agent can be optimized independently
3. **Data-Driven**: Structured tabular output enables analytics
4. **Real-time Capability**: 5-second analysis cycles for live monitoring
5. **Predictive Insights**: Early warning system for proactive management
6. **Cloud-Native**: Built for Google Cloud deployment and scaling

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export PROJECT_ID="your-gcp-project-id"
export LOCATION="us-central1"
export GOOGLE_CLOUD_STAGING_BUCKET="your-staging-bucket"
```

## Files Structure

```
crowdflow-agent/
├── agent.py                    # Main pipeline orchestrator
├── video_analysis_agent.py     # Agent 1: Video processing
├── forecasting_agent.py        # Agent 2: Forecasting & severity
├── pipeline_orchestrator.py    # Pipeline coordination logic
├── bigquery_schema.py          # BigQuery table schemas
├── pipeline_usage_examples.py  # Usage examples
├── README.md                   # This documentation
└── requirements.txt            # Dependencies
```

## Environment Variables

-   `PROJECT_ID`: Google Cloud Project ID
-   `LOCATION`: Google Cloud location (default: us-central1)
-   `GOOGLE_CLOUD_STAGING_BUCKET`: Staging bucket for deployments

## Key Metrics

### Crowd Detection Accuracy

-   Person detection precision and recall
-   Tracking accuracy across frames
-   Density calculation error rates
-   Prediction confidence scores

### Performance Metrics

-   Real-time processing latency
-   Model inference speed
-   Memory and compute utilization
-   Scalability across multiple camera feeds

### Safety Metrics

-   Early warning accuracy for dangerous conditions
-   Emergency response trigger reliability
-   False positive/negative rates for safety alerts

## Best Practices

1. **Camera Placement**: Optimize camera angles for crowd visibility
2. **Model Calibration**: Regular recalibration for different venues
3. **Real-time Processing**: Balance accuracy with processing speed
4. **Safety Thresholds**: Conservative settings for crowd safety
5. **Integration**: Coordinate with Queue Management and Security agents

## Integration with Other Agents

-   **Queue Management**: Provides crowd data for queue optimization
-   **Security**: Alerts for dangerous crowd conditions
-   **MedAssist**: Crowd density info for emergency response planning
-   **Supervisor**: High-level crowd status and coordination

This agent provides the foundational computer vision and ML capabilities needed for comprehensive crowd management and safety at large-scale events.
