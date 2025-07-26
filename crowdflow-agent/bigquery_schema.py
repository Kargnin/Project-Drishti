"""
BigQuery Integration for CrowdFlow Pipeline
Defines schemas and helper functions for data storage and retrieval
"""

# BigQuery table schemas for the CrowdFlow pipeline

CROWD_ANALYSIS_DATA_SCHEMA = [
    {
        "name": "timestamp",
        "type": "TIMESTAMP",
        "mode": "REQUIRED",
        "description": "Analysis timestamp (5-second intervals)"
    },
    {
        "name": "crowd_density",
        "type": "FLOAT64",
        "mode": "REQUIRED",
        "description": "People per square meter"
    },
    {
        "name": "crowd_velocity",
        "type": "FLOAT64",
        "mode": "REQUIRED",
        "description": "Average movement speed in m/s"
    },
    {
        "name": "crowd_behavior",
        "type": "STRING",
        "mode": "REQUIRED",
        "description": "Categorical behavior: normal, congested, excited, agitated, panic, dispersing"
    },
    {
        "name": "detected_persons",
        "type": "INTEGER",
        "mode": "NULLABLE",
        "description": "Number of persons detected by YOLOv3"
    },
    {
        "name": "coverage_area_sqm",
        "type": "FLOAT64",
        "mode": "NULLABLE",
        "description": "Area covered by analysis in square meters"
    },
    {
        "name": "confidence_score",
        "type": "FLOAT64",
        "mode": "NULLABLE",
        "description": "Analysis confidence score (0.0-1.0)"
    },
    {
        "name": "camera_zone",
        "type": "STRING",
        "mode": "NULLABLE",
        "description": "Camera zone identifier"
    },
    {
        "name": "event_id",
        "type": "STRING",
        "mode": "NULLABLE",
        "description": "Event identifier for grouping"
    }
]

CROWD_FORECASTS_SCHEMA = [
    {
        "name": "analysis_timestamp",
        "type": "TIMESTAMP",
        "mode": "REQUIRED",
        "description": "When the forecast was generated"
    },
    {
        "name": "forecast_timestamp",
        "type": "TIMESTAMP",
        "mode": "REQUIRED",
        "description": "Timestamp for predicted values"
    },
    {
        "name": "predicted_crowd_density",
        "type": "FLOAT64",
        "mode": "REQUIRED",
        "description": "Predicted people per square meter"
    },
    {
        "name": "predicted_crowd_velocity",
        "type": "FLOAT64",
        "mode": "REQUIRED",
        "description": "Predicted movement speed in m/s"
    },
    {
        "name": "predicted_crowd_behavior",
        "type": "STRING",
        "mode": "REQUIRED",
        "description": "Predicted behavior category"
    },
    {
        "name": "prediction_confidence",
        "type": "FLOAT64",
        "mode": "REQUIRED",
        "description": "Forecast confidence (0.0-1.0)"
    },
    {
        "name": "severity_score",
        "type": "INTEGER",
        "mode": "REQUIRED",
        "description": "Risk severity score (1-10)"
    },
    {
        "name": "risk_level",
        "type": "STRING",
        "mode": "REQUIRED",
        "description": "Risk level: low, moderate, high, critical"
    },
    {
        "name": "primary_risk_factors",
        "type": "STRING",
        "mode": "REPEATED",
        "description": "Array of identified risk factors"
    },
    {
        "name": "recommendations",
        "type": "STRING",
        "mode": "REPEATED",
        "description": "Array of recommended actions"
    },
    {
        "name": "anomalies_detected",
        "type": "BOOLEAN",
        "mode": "NULLABLE",
        "description": "Whether anomalies were detected"
    },
    {
        "name": "camera_zone",
        "type": "STRING",
        "mode": "NULLABLE",
        "description": "Camera zone identifier"
    },
    {
        "name": "event_id",
        "type": "STRING",
        "mode": "NULLABLE",
        "description": "Event identifier"
    }
]

CROWD_ALERTS_SCHEMA = [
    {
        "name": "alert_timestamp",
        "type": "TIMESTAMP",
        "mode": "REQUIRED",
        "description": "When alert was generated"
    },
    {
        "name": "alert_level",
        "type": "STRING",
        "mode": "REQUIRED",
        "description": "Alert level: yellow, orange, red"
    },
    {
        "name": "severity_score",
        "type": "INTEGER",
        "mode": "REQUIRED",
        "description": "Triggering severity score"
    },
    {
        "name": "alert_reason",
        "type": "STRING",
        "mode": "REQUIRED",
        "description": "Primary reason for alert"
    },
    {
        "name": "camera_zone",
        "type": "STRING",
        "mode": "REQUIRED",
        "description": "Affected camera zone"
    },
    {
        "name": "current_density",
        "type": "FLOAT64",
        "mode": "NULLABLE",
        "description": "Current crowd density"
    },
    {
        "name": "predicted_density",
        "type": "FLOAT64",
        "mode": "NULLABLE",
        "description": "Predicted crowd density"
    },
    {
        "name": "recommended_actions",
        "type": "STRING",
        "mode": "REPEATED",
        "description": "Immediate actions recommended"
    },
    {
        "name": "event_id",
        "type": "STRING",
        "mode": "NULLABLE",
        "description": "Event identifier"
    },
    {
        "name": "resolved",
        "type": "BOOLEAN",
        "mode": "NULLABLE",
        "description": "Whether alert has been resolved"
    }
]

# SQL queries for common operations

INSERT_ANALYSIS_DATA = """
INSERT INTO `{project_id}.{dataset_id}.crowd_analysis_data` 
(timestamp, crowd_density, crowd_velocity, crowd_behavior, detected_persons, 
 coverage_area_sqm, confidence_score, camera_zone, event_id)
VALUES 
(@timestamp, @crowd_density, @crowd_velocity, @crowd_behavior, @detected_persons,
 @coverage_area_sqm, @confidence_score, @camera_zone, @event_id)
"""

INSERT_FORECAST_DATA = """
INSERT INTO `{project_id}.{dataset_id}.crowd_forecasts`
(analysis_timestamp, forecast_timestamp, predicted_crowd_density, predicted_crowd_velocity,
 predicted_crowd_behavior, prediction_confidence, severity_score, risk_level,
 primary_risk_factors, recommendations, anomalies_detected, camera_zone, event_id)
VALUES
(@analysis_timestamp, @forecast_timestamp, @predicted_crowd_density, @predicted_crowd_velocity,
 @predicted_crowd_behavior, @prediction_confidence, @severity_score, @risk_level,
 @primary_risk_factors, @recommendations, @anomalies_detected, @camera_zone, @event_id)
"""

INSERT_ALERT = """
INSERT INTO `{project_id}.{dataset_id}.crowd_alerts`
(alert_timestamp, alert_level, severity_score, alert_reason, camera_zone,
 current_density, predicted_density, recommended_actions, event_id)
VALUES
(@alert_timestamp, @alert_level, @severity_score, @alert_reason, @camera_zone,
 @current_density, @predicted_density, @recommended_actions, @event_id)
"""

GET_RECENT_DATA_FOR_FORECASTING = """
SELECT 
    timestamp,
    crowd_density,
    crowd_velocity, 
    crowd_behavior
FROM `{project_id}.{dataset_id}.crowd_analysis_data`
WHERE camera_zone = @camera_zone
    AND event_id = @event_id
    AND timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 MINUTE)
ORDER BY timestamp DESC
LIMIT 10
"""

GET_SEVERITY_TRENDS = """
SELECT 
    DATE_TRUNC(analysis_timestamp, HOUR) as hour,
    camera_zone,
    AVG(severity_score) as avg_severity,
    MAX(severity_score) as max_severity,
    COUNT(*) as forecast_count
FROM `{project_id}.{dataset_id}.crowd_forecasts`
WHERE analysis_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)
GROUP BY hour, camera_zone
ORDER BY hour DESC, camera_zone
"""

# Helper function for BigQuery integration


def create_bigquery_tables_sql(project_id: str, dataset_id: str) -> str:
    """
    Generate SQL commands to create all required BigQuery tables
    """

    return f"""
-- Create dataset
CREATE SCHEMA IF NOT EXISTS `{project_id}.{dataset_id}`
OPTIONS (
    description = "CrowdFlow pipeline data storage",
    location = "US"
);

-- Create crowd_analysis_data table
CREATE OR REPLACE TABLE `{project_id}.{dataset_id}.crowd_analysis_data` (
    timestamp TIMESTAMP NOT NULL,
    crowd_density FLOAT64 NOT NULL,
    crowd_velocity FLOAT64 NOT NULL, 
    crowd_behavior STRING NOT NULL,
    detected_persons INT64,
    coverage_area_sqm FLOAT64,
    confidence_score FLOAT64,
    camera_zone STRING,
    event_id STRING
)
PARTITION BY DATE(timestamp)
CLUSTER BY camera_zone, event_id
OPTIONS (
    description = "Raw crowd analysis data from video processing",
    partition_expiration_days = 30
);

-- Create crowd_forecasts table  
CREATE OR REPLACE TABLE `{project_id}.{dataset_id}.crowd_forecasts` (
    analysis_timestamp TIMESTAMP NOT NULL,
    forecast_timestamp TIMESTAMP NOT NULL,
    predicted_crowd_density FLOAT64 NOT NULL,
    predicted_crowd_velocity FLOAT64 NOT NULL,
    predicted_crowd_behavior STRING NOT NULL,
    prediction_confidence FLOAT64 NOT NULL,
    severity_score INT64 NOT NULL,
    risk_level STRING NOT NULL,
    primary_risk_factors ARRAY<STRING>,
    recommendations ARRAY<STRING>,
    anomalies_detected BOOLEAN,
    camera_zone STRING,
    event_id STRING
)
PARTITION BY DATE(analysis_timestamp)
CLUSTER BY camera_zone, severity_score
OPTIONS (
    description = "Crowd forecasting and severity analysis results",
    partition_expiration_days = 365
);

-- Create crowd_alerts table
CREATE OR REPLACE TABLE `{project_id}.{dataset_id}.crowd_alerts` (
    alert_timestamp TIMESTAMP NOT NULL,
    alert_level STRING NOT NULL,
    severity_score INT64 NOT NULL, 
    alert_reason STRING NOT NULL,
    camera_zone STRING NOT NULL,
    current_density FLOAT64,
    predicted_density FLOAT64,
    recommended_actions ARRAY<STRING>,
    event_id STRING,
    resolved BOOLEAN DEFAULT FALSE
)
PARTITION BY DATE(alert_timestamp)
CLUSTER BY camera_zone, alert_level
OPTIONS (
    description = "High-severity crowd alerts and incidents", 
    partition_expiration_days = 365
);

-- Create views for real-time monitoring
CREATE OR REPLACE VIEW `{project_id}.{dataset_id}.realtime_crowd_status` AS
SELECT 
    camera_zone,
    MAX(timestamp) as last_update,
    LAST_VALUE(crowd_density) OVER (PARTITION BY camera_zone ORDER BY timestamp) as current_density,
    LAST_VALUE(crowd_behavior) OVER (PARTITION BY camera_zone ORDER BY timestamp) as current_behavior,
    LAST_VALUE(confidence_score) OVER (PARTITION BY camera_zone ORDER BY timestamp) as confidence
FROM `{project_id}.{dataset_id}.crowd_analysis_data`
WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 5 MINUTE)
GROUP BY camera_zone, timestamp, crowd_density, crowd_behavior, confidence_score;

-- Create view for active alerts
CREATE OR REPLACE VIEW `{project_id}.{dataset_id}.active_alerts` AS  
SELECT *
FROM `{project_id}.{dataset_id}.crowd_alerts`
WHERE resolved = FALSE
    AND alert_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 2 HOUR)
ORDER BY severity_score DESC, alert_timestamp DESC;
"""


if __name__ == "__main__":
    # Example usage
    project_id = "your-project-id"
    dataset_id = "crowdflow_data"

    print("BigQuery Schema Setup for CrowdFlow Pipeline")
    print("=" * 50)
    print(create_bigquery_tables_sql(project_id, dataset_id))
