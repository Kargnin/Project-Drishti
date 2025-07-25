# CrowdFlow Agent

The CrowdFlow Agent is a component of the Drishti Event Management System designed to predict and manage crowd density patterns using advanced computer vision and machine learning techniques.

## Purpose

This agent specializes in:
- **Crowd Detection**: Using YOLOv3 and computer vision for accurate people counting
- **Density Analysis**: Real-time crowd density measurement and classification
- **Pattern Prediction**: Forecasting crowd movement and density evolution
- **Heat Map Generation**: Creating visual density maps and risk assessments
- **Flow Modeling**: Predicting crowd flow patterns and bottlenecks

## Capabilities

- **Computer Vision Processing**: YOLOv3 object detection for crowd analysis
- **Custom ML Models**: Vertex AI Vision integration with specialized crowd models
- **Real-time Density Mapping**: Live crowd density heat maps and visualizations
- **Predictive Analytics**: Forecasting crowd patterns and growth trends
- **Safety Assessment**: Risk evaluation and emergency response recommendations

## Technical Features

### Computer Vision & ML
- **YOLOv3 Integration**: State-of-the-art object detection for person identification
- **Density Algorithms**: Advanced spatial analysis for crowd density calculation
- **Custom Models**: Specialized ML models trained for crowd behavior prediction
- **Real-time Processing**: Live video feed analysis and instant predictions

### Analysis Categories
- **Static Gathering**: Stationary crowds around stages and attractions
- **Dynamic Flow**: Moving crowds through corridors and pathways
- **Convergent Flow**: Multiple crowd streams joining at bottlenecks
- **Divergent Flow**: Crowd dispersal from central points

## Usage

### Basic Usage

```python
from crowdflow_agent import crowdflow_agent, crowdflow_app

# Analyze crowd density
result = await crowdflow_app.query(
    input_text="Dense crowd gathering near main stage area",
    camera_feed_data=camera_data  # required for computer vision
)

print(f"Density Level: {result['crowd_density_level']}")
print(f"Person Count: {result['crowd_metrics']['estimated_count']}")
```

### Response Format

The agent returns a JSON response with:

```json
{
    "crowd_detected": true/false,
    "crowd_density_level": "low"/"moderate"/"high"/"critical",
    "confidence_score": 0.0-1.0,
    "density_score": 1-10,
    "analysis": "Detailed crowd density assessment",
    "crowd_metrics": {
        "estimated_count": 50-5000,
        "density_per_sqm": 0.5-8.0,
        "coverage_area_sqm": 100-10000,
        "movement_speed": "stationary/slow/moderate/fast"
    },
    "flow_predictions": {
        "direction": "north/south/east/west/convergent/divergent",
        "predicted_growth": "decreasing/stable/increasing/rapid_growth",
        "peak_time_estimate": "5-30 minutes",
        "dispersion_pattern": "organized/chaotic/bottlenecked"
    },
    "safety_assessment": {
        "crush_risk": "low/moderate/high/critical",
        "exit_accessibility": "clear/partially_blocked/blocked",
        "emergency_response_time": "immediate/minutes/delayed"
    },
    "density_map_regions": [
        {
            "region": "stage_front",
            "density": "high",
            "risk_level": "moderate"
        }
    ],
    "recommended_actions": ["action1", "action2"],
    "ml_model_outputs": {
        "yolo_detections": 150,
        "tracking_accuracy": 0.95,
        "prediction_confidence": 0.88
    },
    "requires_intervention": true/false
}
```

## Density Levels

- **LOW (1-2)**: Light density (<2 people/m²), free movement
- **MODERATE (3-5)**: Normal density (2-4 people/m²), comfortable movement
- **HIGH (6-7)**: Heavy density (4-6 people/m²), restricted movement
- **CRITICAL (8-10)**: Dangerous overcrowding (>6 people/m²), crush risk

## Computer Vision Pipeline

### YOLOv3 Object Detection
1. **Person Detection**: Identify all individuals in camera feeds
2. **Confidence Filtering**: Use detections with >0.5 confidence
3. **Bounding Box Analysis**: Extract spatial coordinates and dimensions
4. **Tracking**: Multi-frame analysis for movement patterns

### Density Calculation
1. **Spatial Calibration**: Convert pixel coordinates to real-world measurements
2. **Area Segmentation**: Divide space into analysis grids
3. **Density Mapping**: Calculate people per square meter
4. **Heat Map Generation**: Create visual density representations

### Predictive Modeling
1. **Pattern Recognition**: Identify recurring crowd behaviors
2. **Flow Prediction**: Forecast movement directions and speeds
3. **Growth Modeling**: Predict crowd size evolution
4. **Risk Assessment**: Evaluate safety conditions

## GCP Services Integration

- **Vertex AI Vision**: Powers computer vision and object detection
- **Custom ML Models**: Specialized crowd analysis models
- **Cloud Storage**: Video feed storage and model artifacts
- **AI Platform**: Model training and deployment infrastructure

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export PROJECT_ID="your-gcp-project-id"
export LOCATION="us-central1"
export VISION_MODEL_ENDPOINT="your-model-endpoint"
export STORAGE_BUCKET="crowdflow-data"
```

## Environment Variables

- `PROJECT_ID`: Google Cloud Project ID
- `LOCATION`: Google Cloud location (default: us-central1)
- `VISION_MODEL_ENDPOINT`: Custom ML model endpoint
- `STORAGE_BUCKET`: Cloud Storage bucket for video feeds

## Technical Dependencies

### Core ML/CV Libraries
- **TensorFlow**: Deep learning framework for custom models
- **OpenCV**: Computer vision processing and image manipulation
- **NumPy**: Numerical computing for density calculations
- **Scikit-learn**: Machine learning utilities and algorithms

### Visualization
- **Matplotlib**: Plotting and visualization for density maps
- **Seaborn**: Statistical visualization for crowd analytics

## Key Metrics

### Crowd Detection Accuracy
- Person detection precision and recall
- Tracking accuracy across frames
- Density calculation error rates
- Prediction confidence scores

### Performance Metrics
- Real-time processing latency
- Model inference speed
- Memory and compute utilization
- Scalability across multiple camera feeds

### Safety Metrics
- Early warning accuracy for dangerous conditions
- Emergency response trigger reliability
- False positive/negative rates for safety alerts

## Best Practices

1. **Camera Placement**: Optimize camera angles for crowd visibility
2. **Model Calibration**: Regular recalibration for different venues
3. **Real-time Processing**: Balance accuracy with processing speed
4. **Safety Thresholds**: Conservative settings for crowd safety
5. **Integration**: Coordinate with Queue Management and Security agents

## Integration with Other Agents

- **Queue Management**: Provides crowd data for queue optimization
- **Security**: Alerts for dangerous crowd conditions
- **MedAssist**: Crowd density info for emergency response planning
- **Supervisor**: High-level crowd status and coordination

This agent provides the foundational computer vision and ML capabilities needed for comprehensive crowd management and safety at large-scale events. 