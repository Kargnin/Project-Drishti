"""
Knowledge graph builder for extracting entities and relationships from geospatial data.
"""

import os
import logging
import json
from typing import List, Dict, Any, Optional, Union, Tuple
from datetime import datetime, timezone
import asyncio
import re
from dataclasses import dataclass

from dotenv import load_dotenv
from graphiti_core.nodes import EpisodeType

# Load environment variables
load_dotenv()

# Set up logging first
logger = logging.getLogger(__name__)

# Import graph utilities
try:
    from .graph_utils import GraphitiClient
except ImportError:
    # For direct execution or testing
    try:
        import graph_utils
        GraphitiClient = graph_utils.GraphitiClient
    except ImportError:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        import graph_utils
        GraphitiClient = graph_utils.GraphitiClient

# Import enhanced location schema (from same directory)
SCHEMA_AVAILABLE = False
try:
    from .enhanced_location_schema import (
        EnhancedLocationData, EnhancedGeometry, ZoneProperties,
        InfrastructurePoint, EntryExitPoint, ZoneType, SecurityLevel,
        InfrastructureType, AccessLevel, IncidentType
    )
    SCHEMA_AVAILABLE = True
    logger.info("✓ Enhanced location schema imported successfully")
except ImportError:
    # Try direct import for standalone execution
    try:
        import enhanced_location_schema
        EnhancedLocationData = enhanced_location_schema.EnhancedLocationData
        EnhancedGeometry = enhanced_location_schema.EnhancedGeometry
        ZoneProperties = enhanced_location_schema.ZoneProperties
        InfrastructurePoint = enhanced_location_schema.InfrastructurePoint
        EntryExitPoint = enhanced_location_schema.EntryExitPoint
        ZoneType = enhanced_location_schema.ZoneType
        SecurityLevel = enhanced_location_schema.SecurityLevel
        InfrastructureType = enhanced_location_schema.InfrastructureType
        AccessLevel = enhanced_location_schema.AccessLevel
        IncidentType = enhanced_location_schema.IncidentType
        SCHEMA_AVAILABLE = True
        logger.info("✓ Enhanced location schema imported successfully (direct import)")
    except ImportError as e:
        logger.warning(f"Could not import enhanced_location_schema: {e}")
        logger.info("Continuing without schema validation - will use dict structures")
        # Create dummy classes to avoid NameError
        class DummySchema:
            pass
        EnhancedLocationData = DummySchema
        EnhancedGeometry = DummySchema
        ZoneProperties = DummySchema
        InfrastructurePoint = DummySchema
        EntryExitPoint = DummySchema
        ZoneType = DummySchema
        SecurityLevel = DummySchema
        InfrastructureType = DummySchema
        AccessLevel = DummySchema
        IncidentType = DummySchema


@dataclass
class GeoChunk:
    """Represents a geospatial chunk containing zone and infrastructure data."""
    zone_id: str
    zone_name: str
    zone_type: str
    content: str  # JSON representation of the zone
    geometry: Dict[str, Any]  # GeoJSON geometry
    properties: Dict[str, Any]  # Zone properties
    infrastructure_points: List[Dict[str, Any]]
    entry_exit_points: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    index: int = 0


class GraphBuilder:
    """Builds knowledge graph from geospatial document chunks."""
    
    def __init__(self):
        """Initialize graph builder."""
        self.graph_client = GraphitiClient()
        self._initialized = False
    
    async def initialize(self):
        """Initialize graph client."""
        if not self._initialized:
            await self.graph_client.initialize()
            self._initialized = True
    
    async def close(self):
        """Close graph client."""
        if self._initialized:
            await self.graph_client.close()
            self._initialized = False
    
    def load_geojson_from_file(self, file_path: str) -> Union[Dict[str, Any], Any]:
        """Load and validate GeoJSON from file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Try to validate against schema if available
            if SCHEMA_AVAILABLE:
                try:
                    enhanced_data = EnhancedLocationData(**data)
                    logger.info(f"Loaded {len(enhanced_data.features)} zones from {file_path} (with schema validation)")
                    return enhanced_data
                except Exception as e:
                    logger.warning(f"Schema validation failed: {e}")
                    logger.info(f"Loaded {len(data.get('features', []))} zones from {file_path} (fallback to raw data)")
                    return data
            else:
                # Schema not available, return raw data
                logger.info(f"Loaded {len(data.get('features', []))} zones from {file_path} (without schema validation)")
                return data
            
        except Exception as e:
            logger.error(f"Failed to load GeoJSON from {file_path}: {e}")
            raise
    
    def create_geochunks_from_geojson(self, enhanced_data: Union[Dict[str, Any], Any]) -> List[GeoChunk]:
        """
        Create hierarchical geo chunks from enhanced GeoJSON data.
        Each chunk represents a zone with its infrastructure context.
        """
        geo_chunks = []
        
        # Handle both validated and raw data formats
        if hasattr(enhanced_data, 'features'):
            features = enhanced_data.features
            metadata = getattr(enhanced_data, 'metadata', {})
        else:
            features = enhanced_data.get('features', [])
            metadata = enhanced_data.get('metadata', {})
        
        for index, feature in enumerate(features):
            # Extract zone properties - handle both dict and object formats
            if hasattr(feature, 'properties'):
                properties = feature.properties
                geometry = feature.geometry
            else:
                properties = feature.get('properties', {})
                geometry = feature.get('geometry', {})
            
            # Create comprehensive content for the zone
            zone_content = self._create_zone_content(feature, metadata)
            
            # Handle properties access for both dict and object formats
            def safe_get(obj, attr, default=None):
                if hasattr(obj, attr):
                    return getattr(obj, attr)
                elif isinstance(obj, dict):
                    return obj.get(attr, default)
                return default
            
            # Create GeoChunk
            geo_chunk = GeoChunk(
                zone_id=safe_get(properties, 'id', f'zone_{index}'),
                zone_name=safe_get(properties, 'name', f'Zone {index}'),
                zone_type=safe_get(properties, 'zone_type', 'unknown'),
                content=zone_content,
                geometry=geometry.dict() if hasattr(geometry, 'dict') else geometry,
                properties=properties.dict() if hasattr(properties, 'dict') else properties,
                infrastructure_points=safe_get(properties, 'infrastructure_points', []),
                entry_exit_points=safe_get(properties, 'entry_exit_points', []),
                metadata={
                    "index": index,
                    "security_level": safe_get(properties, 'security_level'),
                    "access_level": safe_get(properties, 'access_level'),
                    "assigned_agents": safe_get(properties, 'assigned_agents', []),
                    "response_team_coverage": safe_get(properties, 'response_team_coverage', []),
                    "creation_date": datetime.now().isoformat()
                },
                index=index
            )
            
            geo_chunks.append(geo_chunk)
        
        logger.info(f"Created {len(geo_chunks)} geo chunks from GeoJSON data")
        return geo_chunks
    
    def _create_zone_content(self, feature: Any, global_metadata: Dict[str, Any]) -> str:
        """Create comprehensive textual content for a zone chunk."""
        # Handle both dict and object formats
        if hasattr(feature, 'properties'):
            properties = feature.properties
            geometry = feature.geometry
        else:
            properties = feature.get('properties', {})
            geometry = feature.get('geometry', {})
        
        # Helper function for safe access
        def safe_get(obj, attr, default=None):
            if hasattr(obj, attr):
                return getattr(obj, attr)
            elif isinstance(obj, dict):
                return obj.get(attr, default)
            return default
        
        content_parts = []
        
        # Zone header
        content_parts.append(f"=== ZONE: {safe_get(properties, 'name', 'Unknown')} ({safe_get(properties, 'id', 'Unknown')}) ===")
        content_parts.append(f"Type: {safe_get(properties, 'zone_type', 'unknown')}")
        content_parts.append(f"Security Level: {safe_get(properties, 'security_level', 'unknown')}")
        content_parts.append(f"Access Level: {safe_get(properties, 'access_level', 'unknown')}")
        
        # Capacity and population
        population_capacity = safe_get(properties, 'population_capacity')
        if population_capacity:
            content_parts.append(f"Capacity: {population_capacity} people")
        
        current_population = safe_get(properties, 'current_population')
        if current_population is not None:
            content_parts.append(f"Current Population: {current_population} people")
        
        # Emergency information
        evacuation_time = safe_get(properties, 'evacuation_time_minutes')
        if evacuation_time:
            content_parts.append(f"Evacuation Time: {evacuation_time} minutes")
        
        emergency_protocols = safe_get(properties, 'emergency_protocols', [])
        if emergency_protocols:
            content_parts.append(f"Emergency Protocols: {', '.join(emergency_protocols)}")
        
        # Agent assignments (HIGH PRIORITY)
        assigned_agents = safe_get(properties, 'assigned_agents', [])
        if assigned_agents:
            content_parts.append(f"\n--- ASSIGNED AGENTS ---")
            for agent in assigned_agents:
                content_parts.append(f"• Agent: {agent}")
        
        response_teams = safe_get(properties, 'response_team_coverage', [])
        if response_teams:
            content_parts.append(f"Response Teams: {', '.join(response_teams)}")
        
        # Infrastructure points
        infrastructure_points = safe_get(properties, 'infrastructure_points', [])
        if infrastructure_points:
            content_parts.append(f"\n--- INFRASTRUCTURE ({len(infrastructure_points)} points) ---")
            for infra in infrastructure_points:
                content_parts.append(f"• {safe_get(infra, 'name', 'Unknown')} ({safe_get(infra, 'type', 'unknown')})")
                content_parts.append(f"  - ID: {safe_get(infra, 'id', 'Unknown')}")
                
                # Handle coordinates - may be Point object or dict
                coords = safe_get(infra, 'coordinates')
                if coords:
                    coord_values = safe_get(coords, 'coordinates', coords)
                    content_parts.append(f"  - Coordinates: {coord_values}")
                
                content_parts.append(f"  - Operational: {safe_get(infra, 'operational_status', 'Unknown')}")
                content_parts.append(f"  - Access: {safe_get(infra, 'access_level', 'Unknown')}")
                content_parts.append(f"  - Emergency Priority: {safe_get(infra, 'emergency_priority', 'Unknown')}")
                
                resources = safe_get(infra, 'resources_available', [])
                if resources:
                    content_parts.append(f"  - Resources: {', '.join(resources)}")
                
                incidents = safe_get(infra, 'supported_incidents', [])
                if incidents:
                    # Handle both enum objects and strings
                    incident_strs = [str(inc) for inc in incidents]
                    content_parts.append(f"  - Handles Incidents: {', '.join(incident_strs)}")
        
        # Entry/Exit points
        entry_exit_points = safe_get(properties, 'entry_exit_points', [])
        if entry_exit_points:
            content_parts.append(f"\n--- ENTRY/EXIT POINTS ({len(entry_exit_points)} points) ---")
            for point in entry_exit_points:
                content_parts.append(f"• {safe_get(point, 'name', 'Unknown')} ({safe_get(point, 'id', 'Unknown')})")
                content_parts.append(f"  - Entry: {safe_get(point, 'is_entry', False)}, Exit: {safe_get(point, 'is_exit', False)}")
                content_parts.append(f"  - Status: {'Open' if safe_get(point, 'current_status', False) else 'Closed'}")
        
        # Communication and resources
        communication_channels = safe_get(properties, 'communication_channels', [])
        if communication_channels:
            content_parts.append(f"\nCommunication: {', '.join(communication_channels)}")
        
        resource_requirements = safe_get(properties, 'resource_requirements', {})
        if resource_requirements:
            content_parts.append(f"\nResource Requirements:")
            for resource, count in resource_requirements.items():
                content_parts.append(f"• {resource}: {count}")
        
        # Operational status
        operational_status = safe_get(properties, 'operational_status', True)
        content_parts.append(f"\nOperational Status: {'Active' if operational_status else 'Inactive'}")
        
        last_updated = safe_get(properties, 'last_updated', 'Unknown')
        content_parts.append(f"Last Updated: {last_updated}")
        
        # Geometry information
        geometry_coords = safe_get(geometry, 'coordinates') if geometry else None
        geometry_type = safe_get(geometry, 'type') if geometry else None
        
        if geometry and geometry_coords:
            content_parts.append(f"\nGeometry: {geometry_type}")
            # Add bounding box or center point for spatial context
            if geometry_type == "Polygon" and geometry_coords:
                coords = geometry_coords[0]  # Outer ring
                lons = [coord[0] for coord in coords]
                lats = [coord[1] for coord in coords]
                bbox = {
                    "min_lon": min(lons), "max_lon": max(lons),
                    "min_lat": min(lats), "max_lat": max(lats)
                }
                content_parts.append(f"Bounding Box: {bbox}")
        
        return "\n".join(content_parts)

    async def add_geojson_to_graph(
        self,
        geo_chunks: List[GeoChunk],
        source_name: str,
        source_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Add GeoJSON chunks to the knowledge graph.
        
        Args:
            geo_chunks: List of geo chunks
            source_name: Name of the GeoJSON source
            source_metadata: Additional metadata
        
        Returns:
            Processing results
        """
        if not self._initialized:
            await self.initialize()
        
        if not geo_chunks:
            return {"episodes_created": 0, "errors": []}
        
        logger.info(f"Adding {len(geo_chunks)} geo chunks to knowledge graph from: {source_name}")
        
        episodes_created = 0
        errors = []
        
        # Process chunks one by one
        for i, chunk in enumerate(geo_chunks):
            try:
                # Create episode ID
                episode_id = f"{source_name}_{chunk.zone_id}_{datetime.now().timestamp()}"
                
                # Prepare episode content with size limits
                episode_content = self._prepare_geo_episode_content(
                    chunk,
                    source_name,
                    source_metadata
                )
                
                # Create source description
                source_description = f"Zone: {chunk.zone_name} ({chunk.zone_id}) from {source_name}"
                
                # Enhanced metadata for graph
                graph_metadata = {
                    "source_name": source_name,
                    "zone_id": chunk.zone_id,
                    "zone_name": chunk.zone_name,
                    "zone_type": chunk.zone_type,
                    "security_level": chunk.metadata.get("security_level"),
                    "assigned_agents": chunk.metadata.get("assigned_agents", []),
                    "infrastructure_count": len(chunk.infrastructure_points),
                    "entry_exit_count": len(chunk.entry_exit_points),
                    "original_length": len(chunk.content),
                    "processed_length": len(episode_content)
                }

                # Print details being added to the graph
                # print(f"Adding episode {episode_id} to knowledge graph from: {source_name}")
                # print(f"Episode content: {episode_content}")
                # print(f"Source description: {source_description}")
                # print(f"Graph metadata: {graph_metadata}")
                
                # Add episode to graph using EpisodeType.text
                await self.graph_client.add_episode(
                    episode_id=episode_id,
                    content=episode_content,
                    source=source_description,
                    timestamp=datetime.now(timezone.utc),
                    metadata=graph_metadata,
                )
                
                episodes_created += 1
                logger.info(f"✓ Added episode {episode_id} to knowledge graph ({episodes_created}/{len(geo_chunks)})")
                
                # Small delay between episodes
                if i < len(geo_chunks) - 1:
                    await asyncio.sleep(0.5)
                    
            except Exception as e:
                error_msg = f"Failed to add geo chunk {chunk.zone_id} to graph: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                continue
        
        result = {
            "episodes_created": episodes_created,
            "total_chunks": len(geo_chunks),
            "errors": errors
        }
        
        logger.info(f"GeoJSON graph building complete: {episodes_created} episodes created, {len(errors)} errors")
        return result
    
    def _prepare_geo_episode_content(
        self,
        chunk: GeoChunk,
        source_name: str,
        source_metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Prepare episode content optimized for Graphiti with geospatial context.
        """
        max_content_length = 6000
        
        content = chunk.content
        if len(content) > max_content_length:
            # Truncate but try to preserve complete sections
            truncated = content[:max_content_length]
            
            # Try to end at a section boundary
            section_ends = [
                truncated.rfind('\n--- '),
                truncated.rfind('\n=== '),
                truncated.rfind('. \n'),
                truncated.rfind('\n\n')
            ]
            
            best_end = max([end for end in section_ends if end > max_content_length * 0.7], default=-1)
            
            if best_end > 0:
                content = truncated[:best_end] + "\n[TRUNCATED - Additional infrastructure details available]"
            else:
                content = truncated + "\n[TRUNCATED]"
            
            logger.warning(f"Truncated geo chunk {chunk.zone_id} from {len(chunk.content)} to {len(content)} chars")
        
        # Add source context
        if source_name and len(content) < max_content_length - 100:
            episode_content = f"[Source: {source_name}]\n\n{content}"
        else:
            episode_content = content
        
        return episode_content

    async def extract_entities_from_geochunks(
        self,
        geo_chunks: List[GeoChunk]
    ) -> List[GeoChunk]:
        """
        Extract entities from geo chunks with focus on agents, infrastructure, and operational data.
        """
        logger.info(f"Extracting entities from {len(geo_chunks)} geo chunks")
        
        enriched_chunks = []
        
        for chunk in geo_chunks:
            entities = self._extract_geospatial_entities(chunk)
            
            # Add entities to chunk metadata
            chunk.metadata["entities"] = entities
            chunk.metadata["entity_extraction_date"] = datetime.now().isoformat()
            
            enriched_chunks.append(chunk)
        
        logger.info("Geospatial entity extraction complete")
        return enriched_chunks
    
    def _safe_get_chunk_property(self, chunk: GeoChunk, attr: str, default=None):
        """Safely get property from chunk.properties whether it's a Pydantic object or dict."""
        properties = chunk.properties
        if hasattr(properties, attr):
            return getattr(properties, attr)
        elif isinstance(properties, dict):
            return properties.get(attr, default)
        return default

    def _extract_geospatial_entities(self, chunk: GeoChunk) -> Dict[str, Any]:
        """Extract comprehensive entities from a geo chunk."""
        entities = {
            # Agent-focused entities (HIGH PRIORITY)
            "agents": self._extract_agent_entities(chunk),
            "response_teams": self._safe_get_chunk_property(chunk, "response_team_coverage", []),
            
            # Infrastructure entities
            "infrastructure": self._extract_infrastructure_entities(chunk),
            "entry_exit_points": self._extract_entry_exit_entities(chunk),
            
            # Operational entities
            "security_info": self._extract_security_entities(chunk),
            "emergency_protocols": self._safe_get_chunk_property(chunk, "emergency_protocols", []),
            "communication_channels": self._safe_get_chunk_property(chunk, "communication_channels", []),
            "resources": self._extract_resource_entities(chunk),
            
            # Geospatial entities
            "location_info": self._extract_location_entities(chunk),
            
            # Capacity and operational status
            "operational_data": self._extract_operational_entities(chunk)
        }
        
        return entities
    
    def _extract_agent_entities(self, chunk: GeoChunk) -> List[Dict[str, Any]]:
        """Extract detailed agent information."""
        agents = []
        
        for agent_id in self._safe_get_chunk_property(chunk, "assigned_agents", []):
            # Infer agent type and capabilities from ID
            agent_info = {
                "id": agent_id,
                "type": self._infer_agent_type(agent_id),
                "zone_assignment": chunk.zone_id,
                "zone_name": chunk.zone_name,
                "security_clearance": self._safe_get_chunk_property(chunk, "security_level"),
                "access_level": self._safe_get_chunk_property(chunk, "access_level"),
                "capabilities": self._infer_agent_capabilities(agent_id, chunk)
            }
            agents.append(agent_info)
        
        return agents
    
    def _infer_agent_type(self, agent_id: str) -> str:
        """Infer agent type from agent ID."""
        agent_id_lower = agent_id.lower()
        
        if "security" in agent_id_lower:
            return "security_agent"
        elif "medical" in agent_id_lower or "medassist" in agent_id_lower:
            return "medical_agent"
        elif "infrastructure" in agent_id_lower:
            return "infrastructure_agent"
        elif "queue" in agent_id_lower or "crowd" in agent_id_lower:
            return "crowd_management_agent"
        else:
            return "general_agent"
    
    def _infer_agent_capabilities(self, agent_id: str, chunk: GeoChunk) -> List[str]:
        """Infer agent capabilities based on zone context."""
        capabilities = []
        
        agent_type = self._infer_agent_type(agent_id)
        zone_type = self._safe_get_chunk_property(chunk, "zone_type")  # Use safe access for zone_type
        security_level = self._safe_get_chunk_property(chunk, "security_level")
        
        # Base capabilities by agent type
        if agent_type == "security_agent":
            capabilities.extend(["access_control", "threat_assessment", "evacuation_coordination"])
            if security_level in ["high", "critical"]:
                capabilities.append("high_security_operations")
        
        elif agent_type == "medical_agent":
            capabilities.extend(["emergency_medical_response", "triage", "medical_evacuation"])
        
        elif agent_type == "infrastructure_agent":
            capabilities.extend(["infrastructure_monitoring", "maintenance_coordination", "resource_management"])
        
        elif agent_type == "crowd_management_agent":
            capabilities.extend(["crowd_flow_analysis", "queue_management", "crowd_safety"])
        
        # Zone-specific capabilities
        if zone_type == "emergency":
            capabilities.append("emergency_response")
        elif zone_type == "medical":
            capabilities.append("medical_facility_management")
        elif zone_type == "security":
            capabilities.append("security_zone_management")
        
        return list(set(capabilities))  # Remove duplicates

    def _extract_infrastructure_entities(self, chunk: GeoChunk) -> List[Dict[str, Any]]:
        """Extract infrastructure entities with operational context."""
        # Helper function for safe access
        def safe_get(obj, attr, default=None):
            if hasattr(obj, attr):
                return getattr(obj, attr)
            elif isinstance(obj, dict):
                return obj.get(attr, default)
            return default
        
        infrastructure = []
        
        for infra in chunk.infrastructure_points:
            # Handle coordinates - may be Point object or dict
            coords = safe_get(infra, 'coordinates')
            if coords:
                coord_values = safe_get(coords, 'coordinates', coords)
            else:
                coord_values = []
            
            infra_entity = {
                "id": safe_get(infra, "id", "unknown"),
                "name": safe_get(infra, "name", "Unknown"),
                "type": safe_get(infra, "type", "unknown"),
                "coordinates": coord_values,
                "operational": safe_get(infra, "operational_status", True),
                "access_level": safe_get(infra, "access_level", "unknown"),
                "emergency_priority": safe_get(infra, "emergency_priority", 4),
                "resources": safe_get(infra, "resources_available", []),
                "supported_incidents": [str(inc) for inc in safe_get(infra, "supported_incidents", [])],  # Convert enums to strings
                "parent_zone": chunk.zone_id
            }
            infrastructure.append(infra_entity)
        
        return infrastructure
    
    def _extract_entry_exit_entities(self, chunk: GeoChunk) -> List[Dict[str, Any]]:
        """Extract entry/exit point entities."""
        # Helper function for safe access
        def safe_get(obj, attr, default=None):
            if hasattr(obj, attr):
                return getattr(obj, attr)
            elif isinstance(obj, dict):
                return obj.get(attr, default)
            return default
        
        points = []
        
        for point in chunk.entry_exit_points:
            # Handle coordinates - may be Point object or dict
            coords = safe_get(point, 'coordinates')
            if coords:
                coord_values = safe_get(coords, 'coordinates', coords)
            else:
                coord_values = []
            
            point_entity = {
                "id": safe_get(point, "id", "unknown"),
                "name": safe_get(point, "name", "Unknown"),
                "coordinates": coord_values,
                "is_entry": safe_get(point, "is_entry", False),
                "is_exit": safe_get(point, "is_exit", False),
                "status": "open" if safe_get(point, "current_status", False) else "closed",
                "access_level": safe_get(point, "access_level", "unknown"),
                "parent_zone": chunk.zone_id
            }
            points.append(point_entity)
        
        return points
    
    def _extract_security_entities(self, chunk: GeoChunk) -> Dict[str, Any]:
        """Extract security-related entities."""
        return {
            "level": self._safe_get_chunk_property(chunk, "security_level"),
            "access_level": self._safe_get_chunk_property(chunk, "access_level"),
            "protocols": self._safe_get_chunk_property(chunk, "emergency_protocols", []),
            "zone_type": self._safe_get_chunk_property(chunk, "zone_type")
        }
    
    def _extract_resource_entities(self, chunk: GeoChunk) -> Dict[str, Any]:
        """Extract resource-related entities."""
        # Helper function for safe access
        def safe_get(obj, attr, default=None):
            if hasattr(obj, attr):
                return getattr(obj, attr)
            elif isinstance(obj, dict):
                return obj.get(attr, default)
            return default
        
        return {
            "requirements": self._safe_get_chunk_property(chunk, "resource_requirements", {}),
            "available_at_infrastructure": [
                {"point": safe_get(infra, "id", "unknown"), "resources": safe_get(infra, "resources_available", [])}
                for infra in chunk.infrastructure_points
                if safe_get(infra, "resources_available", [])
            ]
        }
    
    def _extract_location_entities(self, chunk: GeoChunk) -> Dict[str, Any]:
        """Extract location and spatial entities."""
        # Helper function for safe access
        def safe_get(obj, attr, default=None):
            if hasattr(obj, attr):
                return getattr(obj, attr)
            elif isinstance(obj, dict):
                return obj.get(attr, default)
            return default
        
        geometry = chunk.geometry
        location_info = {
            "zone_id": chunk.zone_id,
            "zone_name": chunk.zone_name,
            "geometry_type": safe_get(geometry, "type"),
            "coordinates": safe_get(geometry, "coordinates")
        }
        
        # Calculate bounding box for spatial queries
        if safe_get(geometry, "type") == "Polygon" and safe_get(geometry, "coordinates"):
            coords = safe_get(geometry, "coordinates")[0]  # Outer ring
            lons = [coord[0] for coord in coords]
            lats = [coord[1] for coord in coords]
            location_info["bounding_box"] = {
                "min_lon": min(lons), "max_lon": max(lons),
                "min_lat": min(lats), "max_lat": max(lats),
                "center_lon": (min(lons) + max(lons)) / 2,
                "center_lat": (min(lats) + max(lats)) / 2
            }
        
        return location_info
    
    def _extract_operational_entities(self, chunk: GeoChunk) -> Dict[str, Any]:
        """Extract operational status and capacity entities."""
        return {
            "operational_status": self._safe_get_chunk_property(chunk, "operational_status"),
            "population_capacity": self._safe_get_chunk_property(chunk, "population_capacity"),
            "current_population": self._safe_get_chunk_property(chunk, "current_population"),
            "evacuation_time_minutes": self._safe_get_chunk_property(chunk, "evacuation_time_minutes"),
            "last_updated": self._safe_get_chunk_property(chunk, "last_updated")
        }

    async def clear_graph(self):
        """Clear all data from the knowledge graph."""
        if not self._initialized:
            await self.initialize()
        
        logger.warning("Clearing knowledge graph...")
        await self.graph_client.clear_graph()
        logger.info("Knowledge graph cleared")


# Factory function
def create_graph_builder() -> GraphBuilder:
    """Create graph builder instance."""
    return GraphBuilder()


# Example usage
async def main():
    """Example usage of the geo-enabled graph builder."""
    graph_builder = create_graph_builder()
    
    try:
        # Load GeoJSON data (update path as needed)
        geojson_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "complete_all_108_zones_enhanced.geojson")
        if not os.path.exists(geojson_path):
            geojson_path = "complete_all_108_zones_enhanced.geojson"  # Try relative path
            
        enhanced_data = graph_builder.load_geojson_from_file(geojson_path)
        
        # Create geo chunks
        geo_chunks = graph_builder.create_geochunks_from_geojson(enhanced_data)
        
        print(f"Created {len(geo_chunks)} geo chunks")
        
        # Extract entities with focus on agents
        enriched_chunks = await graph_builder.extract_entities_from_geochunks(geo_chunks)
        
        # Print sample entity extraction
        for i, chunk in enumerate(enriched_chunks[:2]):  # First 2 chunks
            print(f"\nChunk {i} ({chunk.zone_name}):")
            entities = chunk.metadata.get("entities", {})
            print(f"  Agents: {entities.get('agents', [])}")
            print(f"  Infrastructure: {len(entities.get('infrastructure', []))}")
            print(f"  Security Level: {entities.get('security_info', {}).get('level')}")
        
        # Add to knowledge graph
        result = await graph_builder.add_geojson_to_graph(
            geo_chunks=enriched_chunks,
            source_name="enhanced_zones_108",
            source_metadata={"version": "1.0", "type": "emergency_response_zones"}
        )
        
        print(f"\nGraph building result: {result}")
        
    except Exception as e:
        print(f"Graph building failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await graph_builder.close()


if __name__ == "__main__":
    # Set override ggole cloud project env variables
    # os.environ["GOOGLE_CLOUD_PROJECT"] = "eventide-intel-jn8fi"
    # os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
    # os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
    # os.environ["GOOGLE_CLOUD_STAGING_BUCKET"] = "gs://namaste-agents"
    # Load env
    load_dotenv()
    asyncio.run(main())
    # Print env details
    # print(f"GOOGLE_CLOUD_PROJECT: {os.environ['GOOGLE_CLOUD_PROJECT']}")
    # print(f"GOOGLE_CLOUD_LOCATION: {os.environ['GOOGLE_CLOUD_LOCATION']}")
    # print(f"GOOGLE_GENAI_USE_VERTEXAI: {os.environ['GOOGLE_GENAI_USE_VERTEXAI']}")
    # print(f"GOOGLE_CLOUD_STAGING_BUCKET: {os.environ['GOOGLE_CLOUD_STAGING_BUCKET']}")

