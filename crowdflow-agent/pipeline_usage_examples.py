"""
Usage example for the CrowdFlow Two-Agent Pipeline

This demonstrates how to use the sequential pipeline:
1. Video Analysis Agent - processes video at 5 FPS, generates tabular data
2. Forecasting & Severity Agent - predicts future values and severity scores
"""

# from agent import crowdflow_app, crowdflow_agent
import json


def example_video_analysis():
    """
    Example 1: Video Analysis Pipeline
    Input: Video file for crowd analysis
    Output: Tabular data + forecasting + severity assessment
    """

    # Example video analysis request
    video_input = {
        "type": "video_analysis",
        "video_source": "camera_feed_zone_a.mp4",
        "analysis_params": {
            "fps_sampling": 5,
            "frame_interval": "5_seconds",
            "detection_confidence": 0.5
        },
        "context": "Concert main stage area during peak hours"
    }

    # The pipeline will automatically:
    # 1. Call video_analysis_agent to process video
    # 2. Generate tabular data (timestamp, density, velocity, behavior)
    # 3. Call forecasting_agent with the generated data
    # 4. Return integrated analysis with predictions and severity scores

    print("🎥 Starting Video Analysis Pipeline...")
    print(f"Input: {json.dumps(video_input, indent=2)}")

    # Simulate agent call (replace with actual deployment call)
    response = """
    Pipeline would process video and return:
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
                "crowd_behavior": "congested"
            },
            {
                "timestamp": "2024-01-15T14:30:05Z", 
                "crowd_density": 4.8,
                "crowd_velocity": 0.2,
                "crowd_behavior": "congested"
            }
        ],
        "forecasting_results": {
            "forecast": {
                "next_timestamp": "2024-01-15T14:30:10Z",
                "predicted_crowd_density": 5.4,
                "predicted_crowd_velocity": 0.1,
                "predicted_crowd_behavior": "agitated"
            },
            "severity_analysis": {
                "severity_score": 7,
                "risk_level": "high",
                "primary_risk_factors": ["increasing_density", "decreasing_velocity"]
            }
        }
    }
    """

    print("📊 Pipeline Results:")
    print(response)


def example_historical_analysis():
    """
    Example 2: Historical Data Analysis
    Input: Historical tabular data from BigQuery
    Output: Forecasting and severity assessment only
    """

    # Example historical data input (would come from BigQuery)
    historical_data = {
        "type": "forecasting_analysis",
        "data_source": "bigquery.crowd_analysis_data",
        "historical_data": [
            {
                "timestamp": "2024-01-15T14:25:00Z",
                "crowd_density": 2.8,
                "crowd_velocity": 0.8,
                "crowd_behavior": "normal"
            },
            {
                "timestamp": "2024-01-15T14:25:05Z",
                "crowd_density": 3.1,
                "crowd_velocity": 0.7,
                "crowd_behavior": "normal"
            },
            {
                "timestamp": "2024-01-15T14:25:10Z",
                "crowd_density": 3.6,
                "crowd_velocity": 0.5,
                "crowd_behavior": "congested"
            }
        ]
    }

    print("📈 Starting Historical Analysis...")
    print(f"Input: {json.dumps(historical_data, indent=2)}")

    # This would skip video analysis and go directly to forecasting
    response = """
    {
        "pipeline_execution": {
            "stage_1_completed": false,
            "stage_2_completed": true,
            "execution_time": "2024-01-15T14:30:00Z"
        },
        "forecasting_results": {
            "forecast": {
                "next_timestamp": "2024-01-15T14:25:15Z",
                "predicted_crowd_density": 4.2,
                "predicted_crowd_velocity": 0.4,
                "predicted_crowd_behavior": "congested"
            },
            "severity_analysis": {
                "severity_score": 6,
                "risk_level": "moderate",
                "trend_analysis": {
                    "density_trend": "increasing",
                    "velocity_trend": "decreasing"
                }
            },
            "recommendations": [
                "Monitor density levels closely",
                "Consider crowd flow management interventions"
            ]
        }
    }
    """

    print("📊 Forecasting Results:")
    print(response)


def bigquery_integration_example():
    """
    Example 3: BigQuery Integration Workflow
    Shows how data flows between pipeline stages and storage
    """

    print("🗄️  BigQuery Integration Workflow:")
    print("""
    Step 1: Video Analysis Agent
    ├── Input: Video stream at 5 FPS
    ├── Processing: YOLOv3 detection, density calculation
    ├── Output: JSON tabular data
    └── Storage: INSERT INTO crowd_analysis_data
    
    Step 2: Data Storage in BigQuery
    ├── Table: crowd_analysis_data
    ├── Schema: timestamp, crowd_density, crowd_velocity, crowd_behavior
    ├── Partitioning: By timestamp (hourly)
    └── Retention: 30 days for real-time, 1 year for analytics
    
    Step 3: Forecasting Agent
    ├── Input: SELECT * FROM crowd_analysis_data WHERE timestamp > NOW() - INTERVAL 30 MINUTE
    ├── Processing: Time series analysis, trend prediction
    ├── Output: Forecasted values + severity scores
    └── Storage: INSERT INTO crowd_forecasts
    
    BigQuery Tables:
    ├── crowd_analysis_data (raw video analysis results)
    ├── crowd_forecasts (predictions and severity scores)
    └── crowd_alerts (high severity incidents)
    """)


def deployment_example():
    """
    Example 4: Deployment Configuration
    Shows how to deploy the pipeline with proper settings
    """

    print("🚀 Deployment Configuration:")
    print("""
    # Deploy the pipeline with A2A enabled
    from crowdflow-agent.agent import crowdflow_app
    
    # The app is already configured with:
    # - A2A enabled for agent communication
    # - Sub-agents: video_analysis_agent, forecasting_agent
    # - Tracing enabled for debugging
    
    # Deploy to Google Cloud Agent Engine
    remote_app = agent_engines.create(
        agent_engine=crowdflow_app,
        requirements=[
            "google-cloud-aiplatform[adk,agent_engines]",
            "google-cloud-bigquery",
            "opencv-python",
            "numpy"
        ],
        extra_packages=["./crowdflow-agent"]
    )
    
    # Real-time usage:
    for event in remote_app.stream_query(
        user_id="crowd_monitor",
        session_id="zone_a_analysis", 
        message="Analyze video feed from camera_zone_a.mp4"
    ):
        print(event)
    """)


if __name__ == "__main__":
    print("🎯 CrowdFlow Two-Agent Pipeline Examples")
    print("=" * 50)

    print("\n1. Video Analysis Pipeline (Complete Flow)")
    example_video_analysis()

    print("\n" + "="*50)
    print("\n2. Historical Data Analysis (Forecasting Only)")
    example_historical_analysis()

    print("\n" + "="*50)
    print("\n3. BigQuery Integration")
    bigquery_integration_example()

    print("\n" + "="*50)
    print("\n4. Deployment Configuration")
    deployment_example()

    print("\n🎉 Pipeline ready for deployment!")
