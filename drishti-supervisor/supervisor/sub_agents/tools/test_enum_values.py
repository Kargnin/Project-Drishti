#!/usr/bin/env python3
"""
Diagnostic script to identify missing enum values in the GeoJSON data.
"""

import json
import sys
import os
from collections import defaultdict

# Import the schema
try:
    from enhanced_location_schema import ZoneType, SecurityLevel, AccessLevel, InfrastructureType, IncidentType
except ImportError:
    import enhanced_location_schema
    ZoneType = enhanced_location_schema.ZoneType
    SecurityLevel = enhanced_location_schema.SecurityLevel
    AccessLevel = enhanced_location_schema.AccessLevel
    InfrastructureType = enhanced_location_schema.InfrastructureType
    IncidentType = enhanced_location_schema.IncidentType

def analyze_enum_values():
    """Analyze what enum values are missing from actual data."""
    
    # Load the GeoJSON file
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    geojson_path = os.path.join(project_root, "complete_all_108_zones_enhanced.geojson")
    
    if not os.path.exists(geojson_path):
        print(f"❌ GeoJSON file not found at: {geojson_path}")
        return
    
    with open(geojson_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Collect actual values from the data
    actual_values = {
        'zone_types': set(),
        'security_levels': set(),
        'access_levels': set(),
        'infrastructure_types': set(),
        'supported_incidents': set()
    }
    
    # Analyze features
    for feature in data.get('features', []):
        props = feature.get('properties', {})
        
        # Zone properties
        if props.get('zone_type'):
            actual_values['zone_types'].add(props['zone_type'])
        if props.get('security_level'):
            actual_values['security_levels'].add(props['security_level'])
        if props.get('access_level'):
            actual_values['access_levels'].add(props['access_level'])
        
        # Infrastructure properties
        for infra in props.get('infrastructure_points', []):
            if infra.get('type'):
                actual_values['infrastructure_types'].add(infra['type'])
            if infra.get('access_level'):
                actual_values['access_levels'].add(infra['access_level'])
            for incident in infra.get('supported_incidents', []):
                actual_values['supported_incidents'].add(incident)
    
    # Get current enum values
    current_enums = {
        'zone_types': {e.value for e in ZoneType},
        'security_levels': {e.value for e in SecurityLevel},
        'access_levels': {e.value for e in AccessLevel},
        'infrastructure_types': {e.value for e in InfrastructureType},
        'supported_incidents': {e.value for e in IncidentType}
    }
    
    # Find missing values
    print("🔍 ENUM VALUE ANALYSIS")
    print("=" * 50)
    
    for category, actual in actual_values.items():
        current = current_enums[category]
        missing = actual - current
        extra = current - actual
        
        print(f"\n📊 {category.upper()}:")
        print(f"  Actual values in data: {sorted(actual)}")
        print(f"  Current enum values: {sorted(current)}")
        
        if missing:
            print(f"  ❌ Missing from enum: {sorted(missing)}")
        else:
            print(f"  ✅ All values covered")
            
        if extra:
            print(f"  ℹ️  Extra in enum: {sorted(extra)}")
    
    return actual_values, current_enums

if __name__ == "__main__":
    analyze_enum_values() 