from typing import List, Optional, Dict, Any, Literal, Union
from pydantic import BaseModel, Field, validator
from enum import Enum
from datetime import datetime

# Enums for standardized values
class ZoneType(str, Enum):
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    EMERGENCY = "emergency"
    RESTRICTED = "restricted"
    PUBLIC = "public"
    TRANSPORTATION = "transportation"
    MEDICAL = "medical"
    SECURITY = "security"
    EDUCATIONAL = "educational"
    RECREATIONAL = "recreational"

class SecurityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    RESTRICTED = "restricted"

class InfrastructureType(str, Enum):
    GATE = "gate"
    SECURITY_CHECKPOINT = "security_checkpoint"
    MEDICAL_STATION = "medical_station"
    HELP_DESK = "help_desk"
    EMERGENCY_EXIT = "emergency_exit"
    FIRE_STATION = "fire_station"
    COMMUNICATION_TOWER = "communication_tower"
    SURVEILLANCE_CAMERA = "surveillance_camera"
    EVACUATION_ASSEMBLY_POINT = "evacuation_assembly_point"
    RESOURCE_DEPOT = "resource_depot"
    COMMAND_CENTER = "command_center"

class AccessLevel(str, Enum):
    PUBLIC = "public"
    RESTRICTED = "restricted"
    AUTHORIZED_ONLY = "authorized_only"
    EMERGENCY_ONLY = "emergency_only"

class IncidentType(str, Enum):
    FIRE = "fire"
    MEDICAL = "medical"
    SECURITY = "security"
    STAMPEDE = "stampede"
    EVACUATION = "evacuation"
    CROWD_CONTROL = "crowd_control"
    TECHNICAL = "technical"

# Base coordinate model
class Coordinate(BaseModel):
    longitude: float = Field(..., ge=-180, le=180)
    latitude: float = Field(..., ge=-90, le=90)
    altitude: Optional[float] = None

# Point geometry
class Point(BaseModel):
    type: Literal["Point"] = "Point"
    coordinates: List[float] = Field(..., min_items=2, max_items=3)

# Polygon geometry
class Polygon(BaseModel):
    type: Literal["Polygon"] = "Polygon"
    coordinates: List[List[List[float]]] = Field(..., min_items=1)

# Infrastructure point model
class InfrastructurePoint(BaseModel):
    id: str = Field(..., description="Unique identifier for the infrastructure point")
    name: str = Field(..., description="Human-readable name")
    type: InfrastructureType
    coordinates: Point
    capacity: Optional[int] = Field(None, description="Maximum capacity (people/resources)")
    operational_status: bool = Field(True, description="Whether the infrastructure is operational")
    access_level: AccessLevel = AccessLevel.PUBLIC
    emergency_priority: int = Field(1, ge=1, le=5, description="Priority level for emergency response (1=highest)")
    contact_info: Optional[Dict[str, Any]] = Field(None, description="Contact information")
    resources_available: List[str] = Field(default_factory=list, description="Available resources at this point")
    supported_incidents: List[IncidentType] = Field(default_factory=list, description="Types of incidents this infrastructure can handle")

# Entry/Exit point model
class EntryExitPoint(BaseModel):
    id: str
    name: str
    coordinates: Point
    is_entry: bool = True
    is_exit: bool = True
    access_level: AccessLevel = AccessLevel.PUBLIC
    operational_hours: Optional[Dict[str, Any]] = Field(None, description="Operating hours")
    max_throughput: Optional[int] = Field(None, description="Maximum people per hour")
    current_status: bool = Field(True, description="Currently open/closed")
    connected_zones: List[str] = Field(default_factory=list, description="Zone IDs this point connects")

# Zone properties model
class ZoneProperties(BaseModel):
    id: str = Field(..., description="Unique zone identifier")
    name: str = Field(..., description="Human-readable zone name")
    zone_type: ZoneType
    security_level: SecurityLevel = SecurityLevel.LOW
    population_capacity: Optional[int] = Field(None, description="Maximum occupancy")
    current_population: Optional[int] = Field(None, description="Current estimated occupancy")
    access_level: AccessLevel = AccessLevel.PUBLIC
    
    # Emergency response capabilities
    evacuation_time_minutes: Optional[int] = Field(None, description="Estimated evacuation time in minutes")
    emergency_protocols: List[str] = Field(default_factory=list)
    response_team_coverage: List[str] = Field(default_factory=list, description="Available response teams")
    
    # Infrastructure within zone
    infrastructure_points: List[InfrastructurePoint] = Field(default_factory=list)
    entry_exit_points: List[EntryExitPoint] = Field(default_factory=list)
    
    # Operational metadata
    last_updated: datetime = Field(default_factory=datetime.now)
    operational_status: bool = Field(True, description="Whether zone is operational")
    special_considerations: List[str] = Field(default_factory=list, description="Special notes for emergency response")
    
    # Agent system metadata
    assigned_agents: List[str] = Field(default_factory=list, description="Agent IDs assigned to this zone")
    communication_channels: List[str] = Field(default_factory=list, description="Available communication channels")
    resource_requirements: Dict[str, int] = Field(default_factory=dict, description="Resource requirements by type")

# Enhanced geometry with properties
class EnhancedGeometry(BaseModel):
    type: Literal["Polygon"] = "Polygon"
    coordinates: List[List[List[float]]]
    properties: ZoneProperties

# Main enhanced GeoJSON model
class EnhancedLocationData(BaseModel):
    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: List[EnhancedGeometry]
    
    # Global metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)
    coordinate_system: str = Field("WGS84", description="Coordinate reference system")
    bounds: Optional[Dict[str, float]] = Field(None, description="Bounding box of the entire area")
    
    # Emergency response metadata
    emergency_contacts: List[Dict[str, Any]] = Field(default_factory=list)
    response_protocols: Dict[IncidentType, List[str]] = Field(default_factory=dict)
    resource_inventory: Dict[str, int] = Field(default_factory=dict)
    
    # Agent system configuration
    agent_deployment_rules: Dict[str, Any] = Field(default_factory=dict)
    communication_protocols: List[str] = Field(default_factory=list)
    
    @validator('features')
    def validate_features(cls, v):
        if not v:
            raise ValueError("At least one feature must be provided")
        return v

# Utility models for agent responses
class EmergencyResponse(BaseModel):
    incident_id: str
    incident_type: IncidentType
    location: Point
    affected_zones: List[str]
    required_resources: Dict[str, int]
    response_plan: List[str]
    estimated_response_time_minutes: int
    priority_level: int = Field(..., ge=1, le=5)

class ResourceDeployment(BaseModel):
    deployment_id: str
    target_zones: List[str]
    resources: Dict[str, int]
    deployment_points: List[str]  # Infrastructure point IDs
    estimated_deployment_time_minutes: int
    instructions: List[str]

class ZoneStatus(BaseModel):
    zone_id: str
    current_status: str
    population_count: Optional[int] = None
    operational_infrastructure: List[str]
    active_incidents: List[str]
    available_resources: Dict[str, int]
    recommendations: List[str]

# Example data generation helper
def create_sample_zone(
    zone_id: str,
    name: str,
    coordinates: List[List[List[float]]],
    zone_type: ZoneType = ZoneType.PUBLIC,
    security_level: SecurityLevel = SecurityLevel.LOW
) -> EnhancedGeometry:
    """Helper function to create sample zone data"""
    
    # Create sample infrastructure points based on zone type
    infrastructure = []
    if zone_type in [ZoneType.COMMERCIAL, ZoneType.PUBLIC]:
        infrastructure.extend([
            InfrastructurePoint(
                id=f"{zone_id}_help_desk_1",
                name=f"{name} Help Desk",
                type=InfrastructureType.HELP_DESK,
                coordinates=Point(coordinates=[coordinates[0][0][0], coordinates[0][0][1]]),
                capacity=50,
                supported_incidents=[IncidentType.MEDICAL, IncidentType.CROWD_CONTROL]
            ),
            InfrastructurePoint(
                id=f"{zone_id}_security_1",
                name=f"{name} Security Checkpoint",
                type=InfrastructureType.SECURITY_CHECKPOINT,
                coordinates=Point(coordinates=[coordinates[0][1][0], coordinates[0][1][1]]),
                access_level=AccessLevel.RESTRICTED,
                supported_incidents=[IncidentType.SECURITY, IncidentType.EVACUATION]
            )
        ])
    
    if zone_type in [ZoneType.EMERGENCY, ZoneType.MEDICAL]:
        infrastructure.append(
            InfrastructurePoint(
                id=f"{zone_id}_medical_1",
                name=f"{name} Medical Station",
                type=InfrastructureType.MEDICAL_STATION,
                coordinates=Point(coordinates=[coordinates[0][2][0], coordinates[0][2][1]]),
                capacity=20,
                emergency_priority=1,
                supported_incidents=[IncidentType.MEDICAL, IncidentType.FIRE, IncidentType.STAMPEDE]
            )
        )
    
    # Create entry/exit points
    entry_points = [
        EntryExitPoint(
            id=f"{zone_id}_entry_1",
            name=f"{name} Main Entry",
            coordinates=Point(coordinates=[coordinates[0][0][0], coordinates[0][0][1]]),
            max_throughput=500,
            connected_zones=[zone_id]
        )
    ]
    
    properties = ZoneProperties(
        id=zone_id,
        name=name,
        zone_type=zone_type,
        security_level=security_level,
        population_capacity=1000,
        current_population=0,
        evacuation_time_minutes=15,
        emergency_protocols=["standard_evacuation", "fire_response", "medical_emergency"],
        infrastructure_points=infrastructure,
        entry_exit_points=entry_points,
        response_team_coverage=["security", "medical", "fire"],
        communication_channels=["radio", "mobile", "pa_system"],
        resource_requirements={"security_personnel": 5, "medical_staff": 2, "fire_safety": 3}
    )
    
    return EnhancedGeometry(
        type="Polygon",
        coordinates=coordinates,
        properties=properties
    ) 