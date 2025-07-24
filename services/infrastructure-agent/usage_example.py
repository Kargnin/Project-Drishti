"""
Infrastructure Agent Usage Example

This example demonstrates how to use the Infrastructure Agent to analyze
infrastructure status and issues in the Drishti Event Management System.
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()

# Import the infrastructure agent
from agent import infrastructure_app

async def analyze_text_only():
    """Example: Analyze infrastructure issue from text description only"""
    
    text_description = """
    Power fluctuations detected in the main pavilion area. 
    Several lighting circuits are intermittently failing, and the backup generator 
    kicked in twice in the last hour. The main electrical panel shows warning lights.
    """
    
    print("🔍 Analyzing infrastructure issue from text description...")
    print(f"Description: {text_description}")
    print("\n" + "="*50)
    
    try:
        result = await infrastructure_app.query(input_text=text_description)
        
        print("📊 Infrastructure Analysis Results:")
        print(f"✅ Infrastructure Concern: {result.get('is_infrastructure_concern', 'N/A')}")
        print(f"📈 Status Level: {result.get('status_level', 'N/A')}")
        print(f"🎯 Confidence Score: {result.get('confidence_score', 'N/A')}")
        print(f"📊 Status Score: {result.get('status_score', 'N/A')}/10")
        print(f"🚨 Immediate Response Required: {result.get('requires_immediate_response', 'N/A')}")
        print(f"⚙️  Affected Systems: {result.get('affected_systems', 'N/A')}")
        print(f"🔧 Maintenance Priority: {result.get('maintenance_priority', 'N/A')}")
        print(f"⏱️  Estimated Downtime: {result.get('estimated_downtime', 'N/A')}")
        
        print(f"\n📝 Analysis: {result.get('analysis', 'N/A')}")
        
        if result.get('recommended_actions'):
            print(f"\n🛠️  Recommended Actions:")
            for i, action in enumerate(result['recommended_actions'], 1):
                print(f"   {i}. {action}")
                
    except Exception as e:
        print(f"❌ Error analyzing infrastructure issue: {e}")

async def analyze_with_image():
    """Example: Analyze infrastructure issue with both text and image"""
    
    # This is a placeholder - in real usage, you'd load an actual image
    # For example, an image of damaged electrical equipment or structural issues
    image_path = "../images/normal1.jfif"  # Using existing image as example
    
    text_description = """
    Structural damage observed in the stage platform. There appear to be cracks 
    in the support beams and some bolts look loose. This could pose a safety risk.
    """
    
    print("🔍 Analyzing infrastructure issue with text and image...")
    print(f"Description: {text_description}")
    print(f"Image: {image_path}")
    print("\n" + "="*50)
    
    try:
        # Load and encode image (if it exists)
        image_data = None
        if os.path.exists(image_path):
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode()
        
        # Query with both text and image
        if image_data:
            result = await infrastructure_app.query(
                input_text=text_description,
                # Note: Actual image handling may vary based on ADK implementation
                image_data=image_data
            )
        else:
            print("⚠️  Image not found, analyzing text only...")
            result = await infrastructure_app.query(input_text=text_description)
        
        print("📊 Infrastructure Analysis Results:")
        print(f"✅ Infrastructure Concern: {result.get('is_infrastructure_concern', 'N/A')}")
        print(f"📈 Status Level: {result.get('status_level', 'N/A')}")
        print(f"🎯 Confidence Score: {result.get('confidence_score', 'N/A')}")
        print(f"📊 Status Score: {result.get('status_score', 'N/A')}/10")
        print(f"🚨 Immediate Response Required: {result.get('requires_immediate_response', 'N/A')}")
        print(f"⚙️  Affected Systems: {result.get('affected_systems', 'N/A')}")
        print(f"🔧 Maintenance Priority: {result.get('maintenance_priority', 'N/A')}")
        print(f"⏱️  Estimated Downtime: {result.get('estimated_downtime', 'N/A')}")
        
        if result.get('visual_issues_detected'):
            print(f"👁️  Visual Issues Detected: {result.get('visual_issues_detected', 'N/A')}")
        
        print(f"\n📝 Analysis: {result.get('analysis', 'N/A')}")
        
        if result.get('recommended_actions'):
            print(f"\n🛠️  Recommended Actions:")
            for i, action in enumerate(result['recommended_actions'], 1):
                print(f"   {i}. {action}")
                
    except Exception as e:
        print(f"❌ Error analyzing infrastructure issue: {e}")

async def test_different_scenarios():
    """Test different infrastructure scenarios"""
    
    scenarios = [
        {
            "name": "Power System Issue",
            "description": "Main power transformer making unusual buzzing sounds. Temperature readings are elevated and there's a slight burning smell."
        },
        {
            "name": "Network Connectivity Problem", 
            "description": "Internet connectivity is down in the south pavilion. Network switches show red status lights and attendees cannot access Wi-Fi."
        },
        {
            "name": "Structural Integrity Concern",
            "description": "Heavy rain has caused water to pool on the main stage roof. There's visible sagging and water is beginning to leak through."
        },
        {
            "name": "Environmental System Failure",
            "description": "HVAC system in the main hall has stopped working. Temperature is rising and air circulation is poor."
        },
        {
            "name": "Minor Maintenance Issue",
            "description": "One of the security cameras in parking lot B is not rotating properly. Image quality is still good but coverage is limited."
        }
    ]
    
    for scenario in scenarios:
        print(f"\n🧪 Testing Scenario: {scenario['name']}")
        print("="*60)
        
        try:
            result = await infrastructure_app.query(input_text=scenario['description'])
            
            print(f"📈 Status Level: {result.get('status_level', 'N/A')}")
            print(f"📊 Status Score: {result.get('status_score', 'N/A')}/10")
            print(f"🚨 Immediate Response: {result.get('requires_immediate_response', 'N/A')}")
            print(f"⚙️  Affected Systems: {result.get('affected_systems', 'N/A')}")
            print(f"🔧 Priority: {result.get('maintenance_priority', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Error: {e}")

async def main():
    """Main example function"""
    print("🏗️  Infrastructure Agent Usage Examples")
    print("="*60)
    
    # Test basic text analysis
    await analyze_text_only()
    print("\n" + "="*60)
    
    # Test with image (if available)
    await analyze_with_image()
    print("\n" + "="*60)
    
    # Test different scenarios
    await test_different_scenarios()
    
    print("\n✅ All examples completed!")

if __name__ == "__main__":
    # Run the examples
    asyncio.run(main()) 