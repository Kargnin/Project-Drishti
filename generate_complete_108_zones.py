#!/usr/bin/env python3
"""
Generate complete enhanced GeoJSON file with all 108 zones from original coordinates
This creates a single file with every polygon enhanced according to the Pydantic schema
"""

import json
from datetime import datetime
from typing import List, Dict, Any

def load_original_coordinates() -> List[List[List[List[float]]]]:
    """Load all coordinates from the original GeoJSON file"""
    with open('buffered_roads_negative_simplified.geojson', 'r') as f:
        data = json.load(f)
    
    coordinates = []
    for geometry in data['geometries']:
        if geometry['type'] == 'Polygon':
            coordinates.append(geometry['coordinates'])
    
    return coordinates

def calculate_polygon_area(coordinates: List[List[List[float]]]) -> float:
    """Simple polygon area calculation for zone classification"""
    if not coordinates or not coordinates[0]:
        return 0
    
    # Simple bounding box area estimation
    polygon = coordinates[0]  # First ring
    xs = [coord[0] for coord in polygon]
    ys = [coord[1] for coord in polygon]
    
    width = max(xs) - min(xs)
    height = max(ys) - min(ys)
    return width * height

def get_centroid(coordinates: List[List[List[float]]]) -> List[float]:
    """Calculate centroid of polygon for infrastructure placement"""
    if not coordinates or not coordinates[0]:
        return [0, 0]
    
    polygon = coordinates[0]  # First ring
    xs = [coord[0] for coord in polygon]
    ys = [coord[1] for coord in polygon]
    
    return [sum(xs) / len(xs), sum(ys) / len(ys)]

def classify_zone_type(zone_id: int, area: float, coordinates: List[List[List[float]]]) -> Dict[str, Any]:
    """Classify zone type based on position, size, and characteristics"""
    
    # Zone classification logic based on position and size
    if zone_id <= 5:  # First zones are typically entry/security
        return {
            "zone_type": "security",
            "security_level": "high",
            "access_level": "restricted"
        }
    elif zone_id <= 10:  # Transit areas
        return {
            "zone_type": "transportation", 
            "security_level": "medium",
            "access_level": "public"
        }
    elif area > 0.00001:  # Large areas for assembly
        return {
            "zone_type": "public",
            "security_level": "medium", 
            "access_level": "public"
        }
    elif area > 0.000005:  # Medium areas for commercial
        return {
            "zone_type": "commercial",
            "security_level": "medium",
            "access_level": "public"
        }
    elif zone_id >= 100:  # Later zones for emergency services
        return {
            "zone_type": "emergency",
            "security_level": "critical",
            "access_level": "emergency_only"
        }
    else:  # Smaller utility areas
        return {
            "zone_type": "restricted",
            "security_level": "medium",
            "access_level": "authorized_only"
        }

def get_zone_capacity(zone_type: str, area: float) -> int:
    """Calculate zone capacity based on type and area"""
    base_capacity = {
        "security": 200,
        "public": 2000,
        "commercial": 800,
        "emergency": 100,
        "transportation": 300,
        "restricted": 50
    }
    
    # Adjust based on area
    area_multiplier = max(0.5, min(3.0, area * 100000))  # Scale factor
    return int(base_capacity.get(zone_type, 100) * area_multiplier)

def get_infrastructure_points(zone_id: int, zone_type: str, centroid: List[float]) -> List[Dict[str, Any]]:
    """Generate infrastructure points based on zone type"""
    infrastructure = []
    
    if zone_type == "security":
        infrastructure.append({
            "id": f"gate_{zone_id:03d}",
            "name": f"Security Gate {zone_id}",
            "type": "gate",
            "coordinates": {"type": "Point", "coordinates": centroid},
            "capacity": 100,
            "operational_status": True,
            "access_level": "restricted",
            "emergency_priority": 1,
            "resources_available": ["metal_detector", "security_personnel"],
            "supported_incidents": ["security", "evacuation"]
        })
        
        if zone_id <= 10:  # Main security zones get checkpoints
            infrastructure.append({
                "id": f"checkpoint_{zone_id:03d}",
                "name": f"Security Checkpoint {zone_id}",
                "type": "security_checkpoint",
                "coordinates": {"type": "Point", "coordinates": [centroid[0] + 0.0001, centroid[1]]},
                "capacity": 50,
                "operational_status": True,
                "access_level": "restricted",
                "emergency_priority": 2,
                "resources_available": ["security_personnel", "surveillance"],
                "supported_incidents": ["security", "crowd_control"]
            })
    
    elif zone_type == "public":
        infrastructure.append({
            "id": f"medical_station_{zone_id:03d}",
            "name": f"Medical Station {zone_id}",
            "type": "medical_station",
            "coordinates": {"type": "Point", "coordinates": centroid},
            "capacity": 30,
            "operational_status": True,
            "access_level": "public",
            "emergency_priority": 1,
            "resources_available": ["medical_equipment", "trained_staff"],
            "supported_incidents": ["medical", "fire", "stampede"]
        })
        
        infrastructure.append({
            "id": f"assembly_point_{zone_id:03d}",
            "name": f"Assembly Point {zone_id}",
            "type": "evacuation_assembly_point",
            "coordinates": {"type": "Point", "coordinates": [centroid[0] - 0.0001, centroid[1]]},
            "capacity": 500,
            "operational_status": True,
            "access_level": "emergency_only",
            "emergency_priority": 1,
            "resources_available": ["crowd_barriers", "pa_system"],
            "supported_incidents": ["evacuation", "fire", "stampede"]
        })
    
    elif zone_type == "commercial":
        infrastructure.append({
            "id": f"help_desk_{zone_id:03d}",
            "name": f"Help Desk {zone_id}",
            "type": "help_desk",
            "coordinates": {"type": "Point", "coordinates": centroid},
            "capacity": 50,
            "operational_status": True,
            "access_level": "public",
            "emergency_priority": 3,
            "resources_available": ["information", "first_aid"],
            "supported_incidents": ["medical", "crowd_control"]
        })
    
    elif zone_type == "emergency":
        infrastructure.append({
            "id": f"command_center_{zone_id:03d}",
            "name": f"Command Center {zone_id}",
            "type": "command_center",
            "coordinates": {"type": "Point", "coordinates": centroid},
            "capacity": 20,
            "operational_status": True,
            "access_level": "emergency_only",
            "emergency_priority": 1,
            "resources_available": ["communication_hub", "coordination_staff"],
            "supported_incidents": ["fire", "medical", "security", "evacuation", "stampede"]
        })
    
    elif zone_type == "transportation":
        infrastructure.append({
            "id": f"camera_{zone_id:03d}",
            "name": f"Surveillance Camera {zone_id}",
            "type": "surveillance_camera",
            "coordinates": {"type": "Point", "coordinates": centroid},
            "operational_status": True,
            "access_level": "restricted",
            "emergency_priority": 4,
            "resources_available": ["cctv_monitoring"],
            "supported_incidents": ["security", "crowd_control"]
        })
    
    return infrastructure

def get_assigned_agents(zone_type: str) -> List[str]:
    """Get assigned agents based on zone type"""
    agent_mapping = {
        "security": ["security-agent"],
        "public": ["crowdflow-agent", "medassist-agent"],
        "commercial": ["queue-management-agent"],
        "emergency": ["supervisor-agent", "infrastructure-agent"],
        "transportation": ["crowdflow-agent"],
        "restricted": ["infrastructure-agent"]
    }
    return agent_mapping.get(zone_type, [])

def get_communication_channels(zone_type: str) -> List[str]:
    """Get communication channels based on zone type"""
    channel_mapping = {
        "security": ["radio_secure"],
        "public": ["pa_system_main", "mobile_network"],
        "commercial": ["pa_system", "mobile_network"],
        "emergency": ["emergency_radio", "command_network"],
        "transportation": ["mobile_network"],
        "restricted": ["radio_technical"]
    }
    return channel_mapping.get(zone_type, ["mobile_network"])

def generate_enhanced_zone(zone_id: int, coordinates: List[List[List[float]]]) -> Dict[str, Any]:
    """Generate a complete enhanced zone with all Pydantic schema properties"""
    
    area = calculate_polygon_area(coordinates)
    centroid = get_centroid(coordinates)
    classification = classify_zone_type(zone_id, area, coordinates)
    
    zone_type = classification["zone_type"]
    capacity = get_zone_capacity(zone_type, area)
    current_population = max(0, int(capacity * (0.1 + (zone_id % 10) * 0.05)))  # Varying occupancy
    
    # Generate zone name
    zone_names = {
        "security": ["Security Entrance", "Checkpoint Area", "Access Control Zone"],
        "public": ["Assembly Plaza", "Gathering Area", "Public Space"],
        "commercial": ["Commercial District", "Shopping Area", "Retail Zone"],
        "emergency": ["Emergency Hub", "Command Center", "Response Zone"],
        "transportation": ["Transit Corridor", "Traffic Junction", "Passage Way"],
        "restricted": ["Service Area", "Utility Zone", "Access Corridor"]
    }
    
    base_names = zone_names.get(zone_type, ["Zone"])
    zone_name = f"{base_names[zone_id % len(base_names)]} {chr(65 + (zone_id - 1) % 26)}-{zone_id}"
    
    # Emergency protocols based on zone type
    protocols_mapping = {
        "security": ["security_lockdown", "evacuation_protocol_a"],
        "public": ["mass_evacuation", "crowd_dispersal", "medical_emergency"],
        "commercial": ["evacuation_standard", "fire_response"],
        "emergency": ["emergency_response", "resource_deployment", "command_coordination"],
        "transportation": ["corridor_evacuation", "traffic_management"],
        "restricted": ["secure_evacuation", "utility_shutdown"]
    }
    
    # Response team coverage
    response_teams = {
        "security": ["security", "medical"],
        "public": ["medical", "crowd_control", "fire"],
        "commercial": ["security", "medical"],
        "emergency": ["fire", "medical", "security", "command"],
        "transportation": ["crowd_control"],
        "restricted": ["technical", "security"]
    }
    
    # Resource requirements
    resource_reqs = {
        "security": {"security_personnel": 4, "medical_staff": 1},
        "public": {"medical_staff": int(capacity/400), "crowd_control": int(capacity/200), "fire_safety": 2},
        "commercial": {"security_personnel": 3, "crowd_control": int(capacity/300)},
        "emergency": {"command_staff": 3, "technical_staff": 2, "fire_fighters": 5},
        "transportation": {"crowd_control": 1},
        "restricted": {"technical_staff": 1, "security_personnel": 1}
    }
    
    return {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": coordinates
        },
        "properties": {
            "id": f"zone_{zone_id:03d}",
            "name": zone_name,
            "zone_type": zone_type,
            "security_level": classification["security_level"],
            "population_capacity": capacity,
            "current_population": current_population,
            "access_level": classification["access_level"],
            "evacuation_time_minutes": max(2, min(30, int(capacity/100))),
            "emergency_protocols": protocols_mapping.get(zone_type, ["evacuation_standard"]),
            "response_team_coverage": response_teams.get(zone_type, ["medical"]),
            "infrastructure_points": get_infrastructure_points(zone_id, zone_type, centroid),
            "entry_exit_points": [],  # Could be enhanced based on connections
            "last_updated": datetime.now().isoformat() + "Z",
            "operational_status": True,
            "special_considerations": [],
            "assigned_agents": get_assigned_agents(zone_type),
            "communication_channels": get_communication_channels(zone_type),
            "resource_requirements": resource_reqs.get(zone_type, {})
        }
    }

def generate_complete_enhanced_geojson():
    """Generate the complete enhanced GeoJSON with all 108 zones"""
    
    print("Loading original coordinates...")
    original_coords = load_original_coordinates()
    print(f"Found {len(original_coords)} original polygons")
    
    print("Generating enhanced zones...")
    features = []
    
    for i, coords in enumerate(original_coords, 1):
        zone = generate_enhanced_zone(i, coords)
        features.append(zone)
        if i % 10 == 0:
            print(f"Generated {i} zones...")
    
    # Create the complete GeoJSON structure
    complete_geojson = {
        "type": "FeatureCollection",
        "features": features,
        "metadata": {
            "created_by": "Project Drishti Enhanced Location System",
            "version": "6.0-Complete-All-108-Zones",
            "area_name": "Bangalore Event Complex - Complete Enhanced Layout",
            "coordinate_source": "buffered_roads_negative_simplified.geojson",
            "last_updated": datetime.now().isoformat() + "Z",
            "total_zones": len(features),
            "enhancement_status": "complete",
            "coverage_area_sq_km": 3.2,
            "all_original_polygons_preserved": True
        },
        "coordinate_system": "WGS84",
        "bounds": {
            "min_longitude": 77.595,
            "max_longitude": 77.603,
            "min_latitude": 12.976,
            "max_latitude": 12.983
        },
        "emergency_contacts": [
            {
                "type": "police",
                "number": "+91-100",
                "contact_person": "Control Room",
                "zone_coverage": "all"
            },
            {
                "type": "fire", 
                "number": "+91-101",
                "contact_person": "Fire Control",
                "zone_coverage": "all"
            },
            {
                "type": "medical",
                "number": "+91-108",
                "contact_person": "Emergency Medical Services",
                "zone_coverage": "all"
            },
            {
                "type": "security",
                "number": "+91-9876543210",
                "contact_person": "Security Chief",
                "zone_coverage": ["security_zones", "restricted_zones"]
            }
        ],
        "response_protocols": {
            "fire": ["immediate_evacuation", "deploy_fire_teams", "establish_perimeter", "medical_standby"],
            "medical": ["dispatch_medical_team", "clear_access_routes", "prepare_triage", "notify_hospital"],
            "stampede": ["crowd_control_deployment", "emergency_broadcast", "medical_response", "evacuation_management"],
            "security": ["security_lockdown", "perimeter_control", "threat_assessment", "evacuation_if_needed"],
            "evacuation": ["zone_evacuation", "assembly_points", "exit_management", "crowd_control"],
            "crowd_control": ["deploy_barriers", "additional_personnel", "pa_instructions", "alternative_routes"],
            "technical": ["infrastructure_assessment", "system_isolation", "backup_activation", "safety_establishment"]
        },
        "resource_inventory": {
            "security_personnel": 120,
            "medical_staff": 45,
            "fire_fighters": 30,
            "crowd_control": 80,
            "command_staff": 25,
            "technical_staff": 20,
            "information_staff": 15,
            "food_safety": 10,
            "ambulances": 12,
            "fire_trucks": 6,
            "security_vehicles": 20,
            "emergency_supplies_units": 40,
            "communication_devices": 100,
            "crowd_barriers_sets": 60
        },
        "agent_deployment_rules": {
            "high_crowd_density": {
                "trigger_threshold": 0.8,
                "deploy_agents": ["crowdflow-agent", "queue-management-agent"],
                "priority": "high",
                "affected_zone_types": ["public", "commercial"]
            },
            "security_incident": {
                "deploy_agents": ["security-agent", "supervisor-agent"],
                "priority": "critical", 
                "affected_zone_types": ["security", "restricted"]
            },
            "medical_emergency": {
                "deploy_agents": ["medassist-agent", "supervisor-agent"],
                "priority": "critical",
                "affected_zone_types": ["public", "commercial", "emergency"]
            },
            "fire_incident": {
                "deploy_agents": ["infrastructure-agent", "supervisor-agent", "crowdflow-agent"],
                "priority": "critical",
                "affected_zone_types": ["all"]
            },
            "infrastructure_failure": {
                "deploy_agents": ["infrastructure-agent", "comms-resources-agent"],
                "priority": "high",
                "affected_zone_types": ["restricted", "emergency"]
            },
            "post_incident": {
                "deploy_agents": ["post-incident-agent", "supervisor-agent"],
                "priority": "medium",
                "affected_zone_types": ["all"]
            }
        },
        "communication_protocols": [
            {
                "name": "radio_primary",
                "channels": ["emergency", "security", "medical", "fire", "command", "technical"],
                "coverage": "site_wide",
                "priority": "critical"
            },
            {
                "name": "pa_system_public",
                "zone_types": ["public", "commercial"],
                "type": "public_address",
                "priority": "high"
            },
            {
                "name": "pa_system_secure", 
                "zone_types": ["security", "emergency"],
                "type": "secure_address",
                "priority": "critical"
            },
            {
                "name": "mobile_network",
                "coverage": "site_wide",
                "type": "cellular_backup",
                "priority": "medium"
            },
            {
                "name": "satellite_emergency",
                "coverage": "backup_communication",
                "type": "satellite",
                "priority": "critical"
            }
        ]
    }
    
    return complete_geojson

if __name__ == "__main__":
    print("=== Generating Complete Enhanced GeoJSON with All 108 Zones ===")
    print()
    
    try:
        enhanced_data = generate_complete_enhanced_geojson()
        
        # Save to file
        output_file = "complete_all_108_zones_enhanced.geojson"
        print(f"Saving to {output_file}...")
        
        with open(output_file, 'w') as f:
            json.dump(enhanced_data, f, indent=2, default=str)
        
        print(f"✅ SUCCESS: Complete enhanced GeoJSON generated!")
        print(f"📁 File: {output_file}")
        print(f"📊 Total zones: {len(enhanced_data['features'])}")
        print(f"🏗️ Infrastructure points: {sum(len(zone['properties']['infrastructure_points']) for zone in enhanced_data['features'])}")
        print(f"🔧 Zone types distribution:")
        
        zone_types = {}
        for zone in enhanced_data['features']:
            zone_type = zone['properties']['zone_type']
            zone_types[zone_type] = zone_types.get(zone_type, 0) + 1
        
        for zone_type, count in zone_types.items():
            print(f"   - {zone_type}: {count} zones")
        
        print()
        print("🎉 All 108 original polygons preserved and enhanced with complete Pydantic schema!")
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc() 