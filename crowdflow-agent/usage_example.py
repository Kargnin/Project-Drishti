"""
CrowdFlow Agent Usage Example

This example demonstrates how to use the CrowdFlow Agent to analyze
crowd density, predict flow patterns, and generate density maps using computer vision
and ML models in the Drishti Event Management System.
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()

# Import the crowdflow agent
from agent import crowdflow_app

async def analyze_crowd_density():
    """Example: Analyze crowd density using computer vision"""
    
    text_description = """
    Dense crowd has formed in front of the main stage for the headliner performance. 
    Estimated several thousand people packed into the area with limited movement space. 
    Crowd appears to be pressing forward toward the stage barriers and people are 
    having difficulty moving freely. Security is monitoring for safety concerns.
    """
    
    print("👥 Analyzing crowd density using computer vision...")
    print(f"Description: {text_description}")
    print("\n" + "="*50)
    
    try:
        result = await crowdflow_app.query(input_text=text_description)
        
        print("🔍 CrowdFlow Analysis Results:")
        print(f"👥 Crowd Detected: {result.get('crowd_detected', 'N/A')}")
        print(f"📊 Density Level: {result.get('crowd_density_level', 'N/A')}")
        print(f"🎯 Confidence Score: {result.get('confidence_score', 'N/A')}")
        print(f"📈 Density Score: {result.get('density_score', 'N/A')}/10")
        print(f"🚨 Requires Intervention: {result.get('requires_intervention', 'N/A')}")
        
        if result.get('crowd_metrics'):
            metrics = result['crowd_metrics']
            print(f"\n📊 Crowd Metrics:")
            print(f"   Estimated Count: {metrics.get('estimated_count', 'N/A')}")
            print(f"   Density per m²: {metrics.get('density_per_sqm', 'N/A')}")
            print(f"   Coverage Area: {metrics.get('coverage_area_sqm', 'N/A')} m²")
            print(f"   Movement Speed: {metrics.get('movement_speed', 'N/A')}")
        
        if result.get('flow_predictions'):
            flow = result['flow_predictions']
            print(f"\n🌊 Flow Predictions:")
            print(f"   Direction: {flow.get('direction', 'N/A')}")
            print(f"   Growth Trend: {flow.get('predicted_growth', 'N/A')}")
            print(f"   Peak Time: {flow.get('peak_time_estimate', 'N/A')}")
            print(f"   Pattern: {flow.get('dispersion_pattern', 'N/A')}")
        
        if result.get('safety_assessment'):
            safety = result['safety_assessment']
            print(f"\n⚠️ Safety Assessment:")
            print(f"   Crush Risk: {safety.get('crush_risk', 'N/A')}")
            print(f"   Exit Access: {safety.get('exit_accessibility', 'N/A')}")
            print(f"   Response Time: {safety.get('emergency_response_time', 'N/A')}")
        
        print(f"\n📝 Analysis: {result.get('analysis', 'N/A')}")
        
        if result.get('recommended_actions'):
            print(f"\n🎯 Recommended Actions:")
            for i, action in enumerate(result['recommended_actions'], 1):
                print(f"   {i}. {action}")
                
    except Exception as e:
        print(f"❌ Error analyzing crowd density: {e}")

async def analyze_with_computer_vision():
    """Example: Analyze crowd using computer vision and camera feeds"""
    
    # This is a placeholder - in real usage, you'd load actual camera feed data
    camera_feed_path = "../images/normal1.jfif"  # Using existing image as example
    
    text_description = """
    Camera feed from overhead view shows crowd formation near food court. 
    Multiple clusters of people visible with varying density levels. 
    Some areas appear more congested than others with noticeable movement patterns.
    """
    
    print("📹 Analyzing crowd using computer vision and YOLOv3...")
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
            result = await crowdflow_app.query(
                input_text=text_description,
                # Note: Actual camera feed handling may vary based on ADK implementation
                camera_feed_data=camera_data
            )
        else:
            print("⚠️ Camera feed not found, analyzing text only...")
            result = await crowdflow_app.query(input_text=text_description)
        
        print("🔍 Computer Vision Analysis Results:")
        print(f"📊 Density Level: {result.get('crowd_density_level', 'N/A')}")
        print(f"📈 Density Score: {result.get('density_score', 'N/A')}/10")
        
        if result.get('ml_model_outputs'):
            ml_outputs = result['ml_model_outputs']
            print(f"\n🤖 ML Model Outputs:")
            print(f"   YOLOv3 Detections: {ml_outputs.get('yolo_detections', 'N/A')}")
            print(f"   Tracking Accuracy: {ml_outputs.get('tracking_accuracy', 'N/A')}")
            print(f"   Prediction Confidence: {ml_outputs.get('prediction_confidence', 'N/A')}")
        
        if result.get('density_map_regions'):
            print(f"\n🗺️ Density Map Regions:")
            for region in result['density_map_regions']:
                print(f"   {region.get('region', 'Unknown')}: {region.get('density', 'N/A')} density, {region.get('risk_level', 'N/A')} risk")
        
        print(f"\n📝 Analysis: {result.get('analysis', 'N/A')}")
        
        if result.get('recommended_actions'):
            print(f"\n🎯 Recommended Actions:")
            for i, action in enumerate(result['recommended_actions'], 1):
                print(f"   {i}. {action}")
                
    except Exception as e:
        print(f"❌ Error analyzing with computer vision: {e}")

async def test_crowd_scenarios():
    """Test different crowd density scenarios"""
    
    scenarios = [
        {
            "name": "Critical Overcrowding",
            "description": "Extremely dense crowd at main stage, people pressed against barriers, difficulty breathing reported, emergency evacuation may be needed.",
            "expected_density": "critical"
        },
        {
            "name": "High Density Concert",
            "description": "Popular performer on stage, high crowd density but manageable, people standing close together but can still move.",
            "expected_density": "high"
        },
        {
            "name": "Moderate Food Court",
            "description": "Busy food court area with moderate crowd density, people queuing and moving around vendors with reasonable space.",
            "expected_density": "moderate"
        },
        {
            "name": "Low Density Entrance",
            "description": "Early morning entrance area, sparse crowd with plenty of space between people, free movement throughout.",
            "expected_density": "low"
        },
        {
            "name": "Dynamic Flow Corridor",
            "description": "Main corridor with steady stream of people moving between venues, good flow but consistent density.",
            "expected_density": "moderate"
        },
        {
            "name": "Convergent Flow Bottleneck",
            "description": "Multiple pathways converging at narrow exit, crowd density building up, movement slowing significantly.",
            "expected_density": "high"
        },
        {
            "name": "Static Gathering Speaker",
            "description": "Crowd gathered around outdoor speaker area, mostly stationary, medium density with little movement.",
            "expected_density": "moderate"
        },
        {
            "name": "Emergency Dispersal",
            "description": "Crowd rapidly dispersing due to weather warning, chaotic movement patterns, varying density levels.",
            "expected_density": "high"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n🧪 Testing Crowd Scenario: {scenario['name']}")
        print("="*60)
        
        try:
            result = await crowdflow_app.query(input_text=scenario['description'])
            
            print(f"📊 Density Level: {result.get('crowd_density_level', 'N/A')}")
            print(f"📈 Density Score: {result.get('density_score', 'N/A')}/10")
            print(f"👥 Person Count: {result.get('crowd_metrics', {}).get('estimated_count', 'N/A')}")
            print(f"🌊 Flow Direction: {result.get('flow_predictions', {}).get('direction', 'N/A')}")
            print(f"⚠️ Crush Risk: {result.get('safety_assessment', {}).get('crush_risk', 'N/A')}")
            print(f"🚨 Intervention: {result.get('requires_intervention', 'N/A')}")
            
            # Check if assessment matches expected density
            expected = scenario.get('expected_density', 'unknown')
            actual = result.get('crowd_density_level', 'unknown')
            match_indicator = "✅" if expected == actual else "⚠️"
            print(f"{match_indicator} Expected: {expected}, Got: {actual}")
            
        except Exception as e:
            print(f"❌ Error: {e}")

async def test_flow_prediction_scenarios():
    """Test crowd flow prediction capabilities"""
    
    print("\n🌊 Testing Crowd Flow Prediction Scenarios")
    print("="*60)
    
    flow_scenarios = [
        "Large crowd moving toward main stage as headliner approaches, steady directional flow building",
        "Event ending, massive crowd dispersing through multiple exits, chaotic multi-directional movement",
        "Rain starting, crowds converging on covered areas, rapid change in movement patterns",
        "Emergency announcement made, crowd flow reversing direction toward emergency exits"
    ]
    
    for i, scenario in enumerate(flow_scenarios, 1):
        print(f"\n🌊 Flow Scenario {i}: {scenario}")
        print("-" * 40)
        
        try:
            result = await crowdflow_app.query(input_text=scenario)
            
            if result.get('flow_predictions'):
                flow = result['flow_predictions']
                print(f"📍 Direction: {flow.get('direction', 'N/A')}")
                print(f"📈 Growth: {flow.get('predicted_growth', 'N/A')}")
                print(f"⏰ Peak Time: {flow.get('peak_time_estimate', 'N/A')}")
                print(f"🔄 Pattern: {flow.get('dispersion_pattern', 'N/A')}")
            
            print(f"🎯 Actions: {result.get('recommended_actions', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Error analyzing flow scenario: {e}")

async def test_density_mapping():
    """Test density mapping and heat map generation"""
    
    print("\n🗺️ Testing Density Mapping Capabilities")
    print("="*60)
    
    mapping_scenarios = [
        "Multi-zone venue with varying density: stage area packed, food court moderate, entrance light",
        "Stadium concert with clear density gradients from front to back sections",
        "Festival grounds with multiple stages creating complex density patterns",
        "Conference venue with session rooms, networking areas, and exhibition halls"
    ]
    
    for i, scenario in enumerate(mapping_scenarios, 1):
        print(f"\n🗺️ Mapping Scenario {i}: {scenario}")
        print("-" * 40)
        
        try:
            result = await crowdflow_app.query(input_text=scenario)
            
            if result.get('density_map_regions'):
                print(f"📊 Density Map Regions:")
                for region in result['density_map_regions']:
                    print(f"   • {region.get('region', 'Unknown')}: {region.get('density', 'N/A')} density")
                    print(f"     Risk Level: {region.get('risk_level', 'N/A')}")
            
            print(f"📈 Overall Density: {result.get('crowd_density_level', 'N/A')}")
            print(f"🚨 Intervention Needed: {result.get('requires_intervention', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Error analyzing mapping scenario: {e}")

async def main():
    """Main example function"""
    print("👥 CrowdFlow Agent Usage Examples")
    print("="*60)
    
    # Test basic crowd density analysis
    await analyze_crowd_density()
    print("\n" + "="*60)
    
    # Test computer vision analysis
    await analyze_with_computer_vision()
    print("\n" + "="*60)
    
    # Test different crowd scenarios
    await test_crowd_scenarios()
    print("\n" + "="*60)
    
    # Test flow prediction scenarios
    await test_flow_prediction_scenarios()
    print("\n" + "="*60)
    
    # Test density mapping
    await test_density_mapping()
    
    print("\n✅ All crowd flow analysis examples completed!")
    print("\n🔍 Advanced computer vision and ML-powered crowd management ready!")

if __name__ == "__main__":
    # Run the examples
    asyncio.run(main()) 