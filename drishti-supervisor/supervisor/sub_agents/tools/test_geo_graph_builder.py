#!/usr/bin/env python3
"""
Test script for the geo-enabled graph builder.
"""

import asyncio
import sys
import os
import logging

# Set up logging first
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import graph_builder - handle both module and standalone execution
try:
    # When run as module
    from .graph_builder import create_graph_builder
    logger.info("✓ Imported graph_builder as module")
except ImportError:
    try:
        # When run standalone in same directory
        import graph_builder
        create_graph_builder = graph_builder.create_graph_builder
        logger.info("✓ Imported graph_builder directly")
    except ImportError:
        # Alternative import path
        try:
            import importlib.util
            current_dir = os.path.dirname(os.path.abspath(__file__))
            spec = importlib.util.spec_from_file_location(
                "graph_builder", 
                os.path.join(current_dir, "graph_builder.py")
            )
            graph_builder_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(graph_builder_module)
            create_graph_builder = graph_builder_module.create_graph_builder
            logger.info("✓ Imported graph_builder via importlib")
        except Exception as e:
            logger.error(f"❌ Failed to import graph_builder: {e}")
            sys.exit(1)


async def test_geo_graph_builder():
    """Test the geo-enabled graph builder with a sample of the GeoJSON data."""
    graph_builder = create_graph_builder()
    
    try:
        # Find the GeoJSON file - now we're in tools directory, so go up more levels
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        geojson_path = os.path.join(project_root, "complete_all_108_zones_enhanced.geojson")
        
        if not os.path.exists(geojson_path):
            logger.error(f"GeoJSON file not found at: {geojson_path}")
            logger.info("Please ensure the complete_all_108_zones_enhanced.geojson file is in the project root")
            return
        
        logger.info(f"Loading GeoJSON from: {geojson_path}")
        
        # Load GeoJSON data
        enhanced_data = graph_builder.load_geojson_from_file(geojson_path)
        logger.info("✓ Successfully loaded GeoJSON data")
        
        # Create geo chunks
        geo_chunks = graph_builder.create_geochunks_from_geojson(enhanced_data)
        logger.info(f"✓ Created {len(geo_chunks)} geo chunks")
        
        # Test with a small subset first
        test_chunks = geo_chunks[:3]  # First 3 zones
        logger.info(f"Testing with {len(test_chunks)} chunks")
        
        # Extract entities with focus on agents
        enriched_chunks = await graph_builder.extract_entities_from_geochunks(test_chunks)
        logger.info("✓ Entity extraction completed")
        
        # Print sample entity extraction results
        for i, chunk in enumerate(enriched_chunks):
            print(f"\n{'='*60}")
            print(f"CHUNK {i+1}: {chunk.zone_name} ({chunk.zone_id})")
            print(f"{'='*60}")
            
            entities = chunk.metadata.get("entities", {})
            
            # Agent information (high priority)
            agents = entities.get('agents', [])
            print(f"🤖 AGENTS ({len(agents)}):")
            for agent in agents:
                print(f"   • {agent.get('id', 'Unknown')} ({agent.get('type', 'unknown')})")
                print(f"     - Zone: {agent.get('zone_name', 'Unknown')}")
                print(f"     - Security Clearance: {agent.get('security_clearance', 'Unknown')}")
                print(f"     - Capabilities: {', '.join(agent.get('capabilities', []))}")
            
            # Infrastructure
            infrastructure = entities.get('infrastructure', [])
            print(f"\n🏗️  INFRASTRUCTURE ({len(infrastructure)}):")
            for infra in infrastructure[:3]:  # Show first 3
                print(f"   • {infra.get('name', 'Unknown')} ({infra.get('type', 'unknown')})")
                print(f"     - Operational: {infra.get('operational', 'Unknown')}")
                print(f"     - Resources: {', '.join(infra.get('resources', []))}")
            
            # Security info
            security = entities.get('security_info', {})
            print(f"\n🔒 SECURITY:")
            print(f"   • Level: {security.get('level', 'Unknown')}")
            print(f"   • Access: {security.get('access_level', 'Unknown')}")
            print(f"   • Protocols: {', '.join(security.get('protocols', []))}")
            
            # Location info
            location = entities.get('location_info', {})
            bbox = location.get('bounding_box', {})
            if bbox:
                print(f"\n📍 LOCATION:")
                print(f"   • Center: ({bbox.get('center_lat', 'N/A')}, {bbox.get('center_lon', 'N/A')})")
                print(f"   • Bounds: [{bbox.get('min_lat', 'N/A')}, {bbox.get('min_lon', 'N/A')}] to [{bbox.get('max_lat', 'N/A')}, {bbox.get('max_lon', 'N/A')}]")
        
        print(f"\n{'='*60}")
        print("🎯 AGENT-FOCUSED ANALYSIS")
        print(f"{'='*60}")
        
        # Analyze agents across all chunks
        all_agents = []
        agent_types = {}
        zone_agent_map = {}
        
        for chunk in enriched_chunks:
            entities = chunk.metadata.get("entities", {})
            agents = entities.get('agents', [])
            all_agents.extend(agents)
            
            for agent in agents:
                agent_type = agent.get('type', 'unknown')
                agent_types[agent_type] = agent_types.get(agent_type, 0) + 1
                
                zone_id = agent.get('zone_assignment', 'unknown')
                if zone_id not in zone_agent_map:
                    zone_agent_map[zone_id] = []
                zone_agent_map[zone_id].append(agent)
        
        print(f"\n📊 AGENT STATISTICS:")
        print(f"   • Total Agents: {len(all_agents)}")
        print(f"   • Agent Types:")
        for agent_type, count in agent_types.items():
            print(f"     - {agent_type}: {count}")
        
        print(f"\n🗺️  ZONE-AGENT MAPPING:")
        for zone_id, agents in zone_agent_map.items():
            zone_name = next((chunk.zone_name for chunk in enriched_chunks if chunk.zone_id == zone_id), "Unknown")
            print(f"   • {zone_name} ({zone_id}): {len(agents)} agents")
            for agent in agents:
                capabilities = agent.get('capabilities', [])
                print(f"     - {agent.get('id', 'Unknown')} | Capabilities: {', '.join(capabilities[:3])}{' +more' if len(capabilities) > 3 else ''}")
        
        # Simulate knowledge graph addition (without actually connecting to Graphiti)
        logger.info("\n🔗 Knowledge Graph Integration:")
        logger.info("   Note: To test full graph integration, ensure Graphiti is configured")
        logger.info("   and uncomment the graph addition code below")
        
        # Uncomment to test actual graph addition:
        # result = await graph_builder.add_geojson_to_graph(
        #     geo_chunks=enriched_chunks,
        #     source_name="test_enhanced_zones",
        #     source_metadata={"version": "1.0", "type": "emergency_response_zones", "test": True}
        # )
        # logger.info(f"✓ Graph building result: {result}")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await graph_builder.close()
        logger.info("✓ Graph builder closed")


if __name__ == "__main__":
    print("🚀 Testing Geo-Enabled Graph Builder")
    print("="*60)
    asyncio.run(test_geo_graph_builder()) 