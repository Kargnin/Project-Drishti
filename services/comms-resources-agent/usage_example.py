"""
Communication & Resource Management Agent Usage Example

This example demonstrates how to use the Communication & Resource Management Agent to coordinate
communication and deploy resources based on instructions in the Drishti Event Management System.
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the comms resources agent
from agent import comms_resources_app

async def coordinate_emergency_response():
    """Example: Coordinate emergency response with communication and resources"""
    
    instruction = """
    Medical emergency at main stage area. Person collapsed and unconscious. 
    Need immediate medical team deployment and crowd management. 
    Announce evacuation procedures in multiple languages to clear the area for emergency response.
    """
    
    print("🚨 Coordinating emergency response...")
    print(f"Instruction: {instruction}")
    print("\n" + "="*50)
    
    try:
        result = await comms_resources_app.query(input_text=instruction)
        
        print("📋 Communication & Resource Coordination Results:")
        print(f"✅ Instruction Understood: {result.get('instruction_understood', 'N/A')}")
        print(f"⚡ Priority Level: {result.get('priority_level', 'N/A')}")
        print(f"📊 Urgency Score: {result.get('urgency_score', 'N/A')}/10")
        print(f"🚨 Requires Escalation: {result.get('requires_escalation', 'N/A')}")
        
        if result.get('communication_actions'):
            comm = result['communication_actions']
            print(f"\n📢 Communication Actions:")
            print(f"   Broadcast Priority: {comm.get('broadcast_priority', 'N/A')}")
            print(f"   Delivery Method: {comm.get('delivery_method', 'N/A')}")
            print(f"   Languages Needed: {comm.get('translations_needed', 'N/A')}")
            
            if comm.get('announcements'):
                print(f"   Announcements:")
                for i, announcement in enumerate(comm['announcements'], 1):
                    print(f"     {i}. {announcement.get('message', 'N/A')}")
                    print(f"        Language: {announcement.get('language', 'N/A')}")
                    print(f"        Channel: {announcement.get('channel', 'N/A')}")
                    print(f"        Audience: {announcement.get('audience', 'N/A')}")
        
        if result.get('resource_deployment'):
            resources = result['resource_deployment']
            print(f"\n🚑 Resource Deployment:")
            
            if resources.get('personnel'):
                print(f"   Personnel:")
                for person in resources['personnel']:
                    print(f"     • {person.get('type', 'N/A')}: {person.get('quantity', 'N/A')} units")
                    print(f"       Location: {person.get('location', 'N/A')}")
                    print(f"       ETA: {person.get('eta', 'N/A')}")
            
            if resources.get('equipment'):
                print(f"   Equipment:")
                for equipment in resources['equipment']:
                    print(f"     • {equipment.get('type', 'N/A')}: {equipment.get('quantity', 'N/A')} units")
                    print(f"       Location: {equipment.get('location', 'N/A')}")
            
            if resources.get('vehicles'):
                print(f"   Vehicles:")
                for vehicle in resources['vehicles']:
                    print(f"     • {vehicle.get('type', 'N/A')}: {vehicle.get('purpose', 'N/A')}")
                    print(f"       Area: {vehicle.get('deployment_area', 'N/A')}")
        
        print(f"\n📝 Coordination Plan: {result.get('coordination_plan', 'N/A')}")
        
        if result.get('estimated_timeline'):
            timeline = result['estimated_timeline']
            print(f"\n⏱️ Timeline:")
            print(f"   Immediate (0-5 min): {timeline.get('immediate', 'N/A')}")
            print(f"   Short-term (5-30 min): {timeline.get('short_term', 'N/A')}")
            print(f"   Long-term (30+ min): {timeline.get('long_term', 'N/A')}")
                
    except Exception as e:
        print(f"❌ Error coordinating emergency response: {e}")

async def coordinate_multilingual_announcement():
    """Example: Coordinate multilingual announcement and broadcasting"""
    
    instruction = """
    Weather warning: Severe thunderstorm approaching in 30 minutes. 
    Need to broadcast evacuation notice for outdoor areas to all attendees 
    in English, Spanish, French, and German. Direct people to covered areas and emergency shelters.
    """
    
    print("🌩️ Coordinating weather emergency announcement...")
    print(f"Instruction: {instruction}")
    print("\n" + "="*50)
    
    try:
        result = await comms_resources_app.query(input_text=instruction)
        
        print("📢 Multilingual Broadcasting Coordination:")
        print(f"⚡ Priority Level: {result.get('priority_level', 'N/A')}")
        print(f"📊 Urgency Score: {result.get('urgency_score', 'N/A')}/10")
        
        if result.get('communication_actions'):
            comm = result['communication_actions']
            print(f"\n🗣️ Communication Strategy:")
            print(f"   Languages: {comm.get('translations_needed', 'N/A')}")
            print(f"   Priority: {comm.get('broadcast_priority', 'N/A')}")
            print(f"   Method: {comm.get('delivery_method', 'N/A')}")
            
            if comm.get('announcements'):
                print(f"\n📻 Multilingual Announcements:")
                for announcement in comm['announcements']:
                    print(f"   • Language: {announcement.get('language', 'N/A')}")
                    print(f"     Message: {announcement.get('message', 'N/A')}")
                    print(f"     Channel: {announcement.get('channel', 'N/A')}")
        
        if result.get('weather_considerations'):
            weather = result['weather_considerations']
            print(f"\n🌤️ Weather Considerations:")
            print(f"   Current: {weather.get('current_conditions', 'N/A')}")
            print(f"   Impact: {weather.get('impact_on_operations', 'N/A')}")
            print(f"   Alerts: {weather.get('weather_alerts', 'N/A')}")
        
        if result.get('coordination_requirements'):
            coord = result['coordination_requirements']
            print(f"\n🤝 Coordination Requirements:")
            print(f"   Notify Agents: {coord.get('agents_to_notify', 'N/A')}")
            print(f"   External Services: {coord.get('external_services', 'N/A')}")
            print(f"   Follow-up: {coord.get('follow_up_actions', 'N/A')}")
                
    except Exception as e:
        print(f"❌ Error coordinating announcement: {e}")

async def coordinate_drone_deployment():
    """Example: Coordinate drone deployment for surveillance and monitoring"""
    
    instruction = """
    Security concern reported in parking lot C. Need aerial surveillance to assess the situation.
    Deploy drone for reconnaissance and crowd monitoring. 
    Coordinate with security team on the ground for real-time intelligence.
    """
    
    print("🚁 Coordinating drone deployment...")
    print(f"Instruction: {instruction}")
    print("\n" + "="*50)
    
    try:
        result = await comms_resources_app.query(input_text=instruction)
        
        print("🛸 Drone Deployment Coordination:")
        print(f"⚡ Priority Level: {result.get('priority_level', 'N/A')}")
        print(f"📊 Urgency Score: {result.get('urgency_score', 'N/A')}/10")
        
        if result.get('resource_deployment') and result['resource_deployment'].get('vehicles'):
            vehicles = result['resource_deployment']['vehicles']
            print(f"\n🚁 Drone Operations:")
            for vehicle in vehicles:
                if vehicle.get('type') == 'drone':
                    print(f"   • Type: {vehicle.get('type', 'N/A')}")
                    print(f"     Purpose: {vehicle.get('purpose', 'N/A')}")
                    print(f"     Deployment Area: {vehicle.get('deployment_area', 'N/A')}")
        
        if result.get('coordination_requirements'):
            coord = result['coordination_requirements']
            print(f"\n📡 Coordination with:")
            print(f"   Agents: {coord.get('agents_to_notify', 'N/A')}")
            print(f"   External: {coord.get('external_services', 'N/A')}")
        
        print(f"\n📝 Plan: {result.get('coordination_plan', 'N/A')}")
                
    except Exception as e:
        print(f"❌ Error coordinating drone deployment: {e}")

async def test_coordination_scenarios():
    """Test different coordination scenarios"""
    
    scenarios = [
        {
            "name": "Staff Redeployment",
            "instruction": "Queue building up at entrance gate 2. Need additional security staff and crowd management. Redeploy personnel from quieter gates.",
            "expected_priority": "medium"
        },
        {
            "name": "Infrastructure Maintenance",
            "instruction": "Power outage in vendor area. Deploy maintenance crew with backup generators. Announce temporary service disruption to attendees.",
            "expected_priority": "high"
        },
        {
            "name": "VIP Security Coordination",
            "instruction": "VIP arrival in 15 minutes. Need security perimeter, crowd barriers, and communication blackout in arrival area.",
            "expected_priority": "high"
        },
        {
            "name": "Lost Child Alert",
            "instruction": "Lost child reported. Need public announcement in multiple languages and deploy search teams. Coordinate with security and medical.",
            "expected_priority": "high"
        },
        {
            "name": "Food Service Support",
            "instruction": "Popular food vendor running low on supplies. Need supply delivery coordination and crowd flow management to reduce wait times.",
            "expected_priority": "low"
        },
        {
            "name": "Stage Technical Issue",
            "instruction": "Audio system failure on main stage. Deploy technical crew, backup equipment, and manage crowd disappointment with announcements.",
            "expected_priority": "medium"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n🧪 Testing Coordination Scenario: {scenario['name']}")
        print("="*60)
        
        try:
            result = await comms_resources_app.query(input_text=scenario['instruction'])
            
            print(f"⚡ Priority Level: {result.get('priority_level', 'N/A')}")
            print(f"📊 Urgency Score: {result.get('urgency_score', 'N/A')}/10")
            print(f"✅ Understood: {result.get('instruction_understood', 'N/A')}")
            print(f"🚨 Escalation: {result.get('requires_escalation', 'N/A')}")
            
            # Resource summary
            if result.get('resource_deployment'):
                resources = result['resource_deployment']
                personnel_count = len(resources.get('personnel', []))
                equipment_count = len(resources.get('equipment', []))
                vehicle_count = len(resources.get('vehicles', []))
                print(f"🚑 Resources: {personnel_count} personnel, {equipment_count} equipment, {vehicle_count} vehicles")
            
            # Communication summary
            if result.get('communication_actions'):
                comm = result['communication_actions']
                announcement_count = len(comm.get('announcements', []))
                languages = len(comm.get('translations_needed', []))
                print(f"📢 Communications: {announcement_count} announcements, {languages} languages")
            
            # Check if assessment matches expected priority
            expected = scenario.get('expected_priority', 'unknown')
            actual = result.get('priority_level', 'unknown')
            match_indicator = "✅" if expected == actual else "⚠️"
            print(f"{match_indicator} Expected: {expected}, Got: {actual}")
            
        except Exception as e:
            print(f"❌ Error: {e}")

async def test_resource_optimization():
    """Test resource optimization and allocation"""
    
    print("\n🎯 Testing Resource Optimization Scenarios")
    print("="*60)
    
    optimization_scenarios = [
        "Multiple simultaneous emergencies: medical at stage, security in parking, infrastructure failure at food court",
        "Large event ending: coordinate mass exodus with transportation, security, and crowd management",
        "Weather emergency: incoming severe weather requiring shelter coordination and evacuation",
        "VIP event during peak hours: balance VIP security needs with general attendee experience"
    ]
    
    for i, scenario in enumerate(optimization_scenarios, 1):
        print(f"\n🎯 Optimization Scenario {i}: {scenario}")
        print("-" * 40)
        
        try:
            result = await comms_resources_app.query(input_text=scenario)
            
            print(f"⚡ Priority: {result.get('priority_level', 'N/A')}")
            print(f"📊 Urgency: {result.get('urgency_score', 'N/A')}/10")
            
            if result.get('coordination_requirements'):
                coord = result['coordination_requirements']
                agents = len(coord.get('agents_to_notify', []))
                services = len(coord.get('external_services', []))
                print(f"🤝 Coordination: {agents} agents, {services} external services")
            
            if result.get('estimated_timeline'):
                timeline = result['estimated_timeline']
                print(f"⏱️ Timeline: {timeline.get('immediate', 'N/A')} | {timeline.get('short_term', 'N/A')} | {timeline.get('long_term', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Error analyzing optimization scenario: {e}")

async def main():
    """Main example function"""
    print("📡 Communication & Resource Management Agent Usage Examples")
    print("="*60)
    
    # Test emergency response coordination
    await coordinate_emergency_response()
    print("\n" + "="*60)
    
    # Test multilingual announcement
    await coordinate_multilingual_announcement()
    print("\n" + "="*60)
    
    # Test drone deployment
    await coordinate_drone_deployment()
    print("\n" + "="*60)
    
    # Test different coordination scenarios
    await test_coordination_scenarios()
    print("\n" + "="*60)
    
    # Test resource optimization
    await test_resource_optimization()
    
    print("\n✅ All communication and resource coordination examples completed!")
    print("\n📡 Advanced coordination and deployment capabilities ready!")

if __name__ == "__main__":
    # Run the examples
    asyncio.run(main()) 