"""
Queue Management Agent Usage Example

This example demonstrates how to use the Queue Management Agent to analyze
crowd flow, optimize queues, and provide staff allocation recommendations in the Drishti Event Management System.
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()

# Import the queue management agent
from agent import queue_management_app

async def analyze_queue_congestion():
    """Example: Analyze queue congestion from text description"""
    
    text_description = """
    Extremely long lines have formed at the main entrance gate 3. Wait times are 
    approaching 45 minutes and people are getting frustrated and pushing. The queue 
    extends beyond the designated area and is blocking emergency exits. Staff members 
    report they need immediate assistance to manage the crowd.
    """
    
    print("🚶‍♂️ Analyzing queue congestion from text description...")
    print(f"Description: {text_description}")
    print("\n" + "="*50)
    
    try:
        result = await queue_management_app.query(input_text=text_description)
        
        print("📊 Queue Management Analysis Results:")
        print(f"🚨 Requires Intervention: {result.get('requires_intervention', 'N/A')}")
        print(f"🌊 Flow Efficiency: {result.get('flow_efficiency', 'N/A')}")
        print(f"🎯 Confidence Score: {result.get('confidence_score', 'N/A')}")
        print(f"📈 Congestion Score: {result.get('congestion_score', 'N/A')}/10")
        print(f"⏱️ Current Wait Time: {result.get('estimated_wait_times', {}).get('current_wait', 'N/A')}")
        print(f"🔮 Predicted Wait Time: {result.get('estimated_wait_times', {}).get('predicted_wait', 'N/A')}")
        print(f"📍 Bottleneck Locations: {result.get('bottleneck_locations', 'N/A')}")
        print(f"📊 Capacity Utilization: {result.get('capacity_utilization', 'N/A')}")
        
        if result.get('staff_allocation'):
            staff = result['staff_allocation']
            print(f"\n👥 Staff Allocation Recommendations:")
            print(f"   Additional Staff Needed: {staff.get('additional_staff_needed', 'N/A')}")
            print(f"   Priority Locations: {staff.get('priority_locations', 'N/A')}")
            if staff.get('redeployment_suggestions'):
                print(f"   Redeployment Suggestions:")
                for suggestion in staff['redeployment_suggestions']:
                    print(f"     • {suggestion}")
        
        print(f"\n📝 Flow Analysis: {result.get('analysis', 'N/A')}")
        
        if result.get('flow_recommendations'):
            print(f"\n🎯 Flow Recommendations:")
            for i, rec in enumerate(result['flow_recommendations'], 1):
                print(f"   {i}. {rec}")
                
        if result.get('recommended_actions'):
            actions = result['recommended_actions']
            print(f"\n⚡ Immediate Actions: {actions.get('immediate', 'N/A')}")
            print(f"📅 Short-term Actions: {actions.get('short_term', 'N/A')}")
            print(f"🎯 Long-term Actions: {actions.get('long_term', 'N/A')}")
                
    except Exception as e:
        print(f"❌ Error analyzing queue situation: {e}")

async def analyze_with_camera_feed():
    """Example: Analyze queue situation with camera feed data"""
    
    # This is a placeholder - in real usage, you'd load actual camera feed data
    camera_feed_path = "../images/normal1.jfif"  # Using existing image as example
    
    text_description = """
    Camera feed from food court area shows moderate crowding. Multiple service lines 
    visible with varying queue lengths. Some vendors appear to have longer waits 
    than others, suggesting uneven distribution of customers.
    """
    
    print("📹 Analyzing queue situation with camera feed...")
    print(f"Description: {text_description}")
    print(f"Camera Feed: {camera_feed_path}")
    print("\n" + "="*50)
    
    try:
        # Load and encode camera feed (if it exists)
        camera_data = None
        if os.path.exists(camera_feed_path):
            with open(camera_feed_path, "rb") as feed_file:
                camera_data = base64.b64encode(feed_file.read()).decode()
        
        # Query with both text and camera feed
        if camera_data:
            result = await queue_management_app.query(
                input_text=text_description,
                # Note: Actual camera feed handling may vary based on ADK implementation
                camera_feed_data=camera_data
            )
        else:
            print("⚠️ Camera feed not found, analyzing text only...")
            result = await queue_management_app.query(input_text=text_description)
        
        print("📊 Queue Management Analysis Results:")
        print(f"🌊 Flow Efficiency: {result.get('flow_efficiency', 'N/A')}")
        print(f"📈 Congestion Score: {result.get('congestion_score', 'N/A')}/10")
        print(f"📍 Queue Categories: {result.get('queue_categories', 'N/A')}")
        
        if result.get('visual_crowd_metrics'):
            metrics = result['visual_crowd_metrics']
            print(f"\n👁️ Visual Crowd Metrics:")
            print(f"   Queue Length: {metrics.get('queue_length', 'N/A')}")
            print(f"   Crowd Density: {metrics.get('crowd_density', 'N/A')}")
            print(f"   Movement Flow: {metrics.get('movement_flow', 'N/A')}")
        
        if result.get('estimated_wait_times'):
            wait_times = result['estimated_wait_times']
            print(f"\n⏱️ Wait Time Analysis:")
            print(f"   Current: {wait_times.get('current_wait', 'N/A')}")
            print(f"   Predicted: {wait_times.get('predicted_wait', 'N/A')}")
            print(f"   Peak Time: {wait_times.get('peak_time_wait', 'N/A')}")
        
        print(f"\n📝 Analysis: {result.get('analysis', 'N/A')}")
        
        if result.get('flow_recommendations'):
            print(f"\n🎯 Flow Recommendations:")
            for i, rec in enumerate(result['flow_recommendations'], 1):
                print(f"   {i}. {rec}")
                
    except Exception as e:
        print(f"❌ Error analyzing camera feed: {e}")

async def test_queue_scenarios():
    """Test different queue management scenarios"""
    
    scenarios = [
        {
            "name": "Entry Gate Congestion",
            "description": "Main entrance backed up with security checkpoint delays. Metal detectors running slow and bag checks taking longer than usual.",
            "expected_efficiency": "congested"
        },
        {
            "name": "Food Vendor Rush",
            "description": "Popular food truck has extremely long line, while nearby vendors have no wait. Crowd concentrated in one area.",
            "expected_efficiency": "congested"
        },
        {
            "name": "Restroom Queue",
            "description": "Long lines at restroom facilities near main stage. Wait times about 10 minutes, but moving steadily.",
            "expected_efficiency": "moderate"
        },
        {
            "name": "Merchandise Booth",
            "description": "Merchandise sales area flowing well. Multiple checkout lines open and wait times under 5 minutes.",
            "expected_efficiency": "optimal"
        },
        {
            "name": "Exit Bottleneck",
            "description": "Event ending and all exits severely congested. Dangerous crowding near exit gates with people pushing.",
            "expected_efficiency": "critical"
        },
        {
            "name": "Parking Shuttle",
            "description": "Shuttle service to parking lot running smoothly. Regular intervals and minimal wait for transportation.",
            "expected_efficiency": "optimal"
        },
        {
            "name": "VIP Area Check-in",
            "description": "VIP check-in area has some queuing but staff handling efficiently. Wait times around 8-10 minutes.",
            "expected_efficiency": "moderate"
        },
        {
            "name": "Emergency Evacuation",
            "description": "Emergency drill activated. All exits need to handle maximum capacity quickly and safely.",
            "expected_efficiency": "critical"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n🧪 Testing Queue Scenario: {scenario['name']}")
        print("="*60)
        
        try:
            result = await queue_management_app.query(input_text=scenario['description'])
            
            print(f"🌊 Flow Efficiency: {result.get('flow_efficiency', 'N/A')}")
            print(f"📈 Congestion Score: {result.get('congestion_score', 'N/A')}/10")
            print(f"🚨 Intervention Needed: {result.get('requires_intervention', 'N/A')}")
            print(f"📍 Categories: {result.get('queue_categories', 'N/A')}")
            print(f"👥 Additional Staff: {result.get('staff_allocation', {}).get('additional_staff_needed', 'N/A')}")
            print(f"⏱️ Wait Time: {result.get('estimated_wait_times', {}).get('current_wait', 'N/A')}")
            
            # Check if assessment matches expected efficiency
            expected = scenario.get('expected_efficiency', 'unknown')
            actual = result.get('flow_efficiency', 'unknown')
            match_indicator = "✅" if expected == actual else "⚠️"
            print(f"{match_indicator} Expected: {expected}, Got: {actual}")
            
        except Exception as e:
            print(f"❌ Error: {e}")

async def test_staff_allocation_scenarios():
    """Test staff allocation recommendations"""
    
    print("\n👥 Testing Staff Allocation Scenarios")
    print("="*60)
    
    staff_scenarios = [
        "Multiple gates showing long delays, need to redistribute staff from low-traffic areas",
        "Food court overwhelmed during lunch rush, vendors need additional cashiers",
        "Evening rush hour approaching, historical data shows parking shuttle needs more drivers",
        "One entrance gate closed due to technical issue, need to redirect staff and crowd flow"
    ]
    
    for i, scenario in enumerate(staff_scenarios, 1):
        print(f"\n👥 Staff Scenario {i}: {scenario}")
        print("-" * 40)
        
        try:
            result = await queue_management_app.query(input_text=scenario)
            
            if result.get('staff_allocation'):
                staff = result['staff_allocation']
                print(f"📊 Additional Staff Needed: {staff.get('additional_staff_needed', 'N/A')}")
                print(f"📍 Priority Locations: {staff.get('priority_locations', 'N/A')}")
                print(f"🔄 Redeployment: {staff.get('redeployment_suggestions', 'N/A')}")
            
            print(f"⚡ Immediate Actions: {result.get('recommended_actions', {}).get('immediate', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Error analyzing staff scenario: {e}")

async def main():
    """Main example function"""
    print("🚶‍♂️ Queue Management Agent Usage Examples")
    print("="*60)
    
    # Test basic queue analysis
    await analyze_queue_congestion()
    print("\n" + "="*60)
    
    # Test with camera feed (if available)
    await analyze_with_camera_feed()
    print("\n" + "="*60)
    
    # Test different queue scenarios
    await test_queue_scenarios()
    print("\n" + "="*60)
    
    # Test staff allocation scenarios
    await test_staff_allocation_scenarios()
    
    print("\n✅ All queue management examples completed!")
    print("\n📊 Remember: Optimize for both efficiency and safety!")

if __name__ == "__main__":
    # Run the examples
    asyncio.run(main()) 