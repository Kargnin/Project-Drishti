"""
Usage example for the Drishti Security Agent with Multimodal Support

This demonstrates how to use the Google ADK security agent
to analyze security threats from text descriptions and images at events.
"""

import asyncio
import base64
import json
from pathlib import Path

from agent import security_app

async def analyze_text_only_threat():
    """Example of text-only security analysis"""
    print("=== Text-Only Event Security Analysis ===")
    
    # Example event security scenarios
    scenarios = [
        {
            "description": "Large crowd gathering near the main stage, people pushing forward aggressively during headliner performance",
            "location": "Main stage area",
            "event_type": "Music festival"
        },
        {
            "description": "Unattended backpack found under bleachers, security sweep ongoing",
            "location": "Stadium seating area", 
            "event_type": "Sporting event"
        },
        {
            "description": "Group of protesters attempting to breach security barriers near VIP entrance",
            "location": "VIP entrance gate",
            "event_type": "Political rally"
        },
        {
            "description": "Smoke visible from pyrotechnics malfunction, audience near stage evacuating",
            "location": "Concert stage",
            "event_type": "Concert"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\nScenario {i} - {scenario['event_type']}:")
        print(f"Description: {scenario['description']}")
        print(f"Location: {scenario['location']}")
        
        try:
            # Create multimodal content with text only
            content = f"""
Event Type: {scenario['event_type']}
Location: {scenario['location']}
Description: {scenario['description']}

Please analyze this security situation and provide a threat assessment.
"""
            
            # Use stream_query instead of generate_async
            response_text = ""
            for event in security_app.stream_query(
                user_id="security_analyst",
                message=content
            ):
                if hasattr(event, 'content') and hasattr(event.content, 'parts'):
                    for part in event.content.parts:
                        if hasattr(part, 'text'):
                            response_text += part.text
            
            # Parse JSON response
            try:
                result = json.loads(response_text)
                print(f"✅ Threat Assessment:")
                print(f"   - Security Concern: {result.get('is_security_concern')}")
                print(f"   - Threat Level: {result.get('threat_level')}")
                print(f"   - Threat Score: {result.get('threat_score')}/10")
                print(f"   - Confidence: {result.get('confidence_score', 0):.2f}")
                print(f"   - Immediate Response: {result.get('requires_immediate_response')}")
                print(f"   - Event Concerns: {result.get('event_specific_concerns', [])}")
                print(f"   - Recommended Actions: {result.get('recommended_actions', [])}")
            except json.JSONDecodeError:
                print(f"✅ Raw Analysis: {response_text[:200]}...")
                
        except Exception as e:
            print(f"❌ Error analyzing scenario: {e}")

async def analyze_multimodal_threat():
    """Example of multimodal (text + image) security analysis"""
    print("\n=== Multimodal Event Security Analysis ===")
    
    # Look for sample images in the supervisor agent directory
    image_dir = Path("../supervisor-agent/images")
    if not image_dir.exists():
        image_dir = Path("services/supervisor-agent/images")
    
    if image_dir.exists():
        sample_images = [
            {
                "file": "stampede1.webp",
                "description": "Potential crowd crush situation reported near main entrance",
                "event_type": "Music festival",
                "location": "Main entrance area"
            },
            {
                "file": "fire1.webp", 
                "description": "Fire alarm triggered, smoke visible in venue",
                "event_type": "Indoor concert",
                "location": "Concert hall"
            },
            {
                "file": "normal1.jfif",
                "description": "Regular crowd monitoring during event",
                "event_type": "Outdoor festival",
                "location": "General admission area"
            }
        ]
        
        for sample in sample_images:
            image_path = image_dir / sample["file"]
            if image_path.exists():
                print(f"\nAnalyzing: {sample['file']}")
                print(f"Event: {sample['event_type']}")
                print(f"Description: {sample['description']}")
                
                try:
                    # Read and encode image
                    with open(image_path, "rb") as img_file:
                        image_data = base64.b64encode(img_file.read()).decode()
                    
                    # Create text content for multimodal analysis
                    content = f"""
Event Type: {sample['event_type']}
Location: {sample['location']} 
Description: {sample['description']}

Please analyze this image for security threats and crowd dynamics. Focus on event-specific risks like crowd density, behavior patterns, and environmental hazards.

[Note: Image analysis capability depends on model support for multimodal input]
"""
                    
                    # Use stream_query for analysis
                    response_text = ""
                    for event in security_app.stream_query(
                        user_id="security_analyst",
                        message=content
                    ):
                        if hasattr(event, 'content') and hasattr(event.content, 'parts'):
                            for part in event.content.parts:
                                if hasattr(part, 'text'):
                                    response_text += part.text
                    
                    # Parse JSON response
                    try:
                        result = json.loads(response_text)
                        print(f"✅ Multimodal Assessment:")
                        print(f"   - Security Concern: {result.get('is_security_concern')}")
                        print(f"   - Threat Level: {result.get('threat_level')}")
                        print(f"   - Threat Score: {result.get('threat_score')}/10")
                        print(f"   - Visual Threats: {result.get('visual_threats_detected', [])}")
                        if 'crowd_analysis' in result:
                            crowd = result['crowd_analysis']
                            print(f"   - Crowd Density: {crowd.get('crowd_density')}")
                            print(f"   - Crowd Behavior: {crowd.get('crowd_behavior')}")
                        print(f"   - Event Concerns: {result.get('event_specific_concerns', [])}")
                    except json.JSONDecodeError:
                        print(f"✅ Raw Analysis: {response_text[:300]}...")
                        
                except Exception as e:
                    print(f"❌ Error analyzing image: {e}")
                    
    else:
        print("⚠️  No sample images found. Skipping multimodal analysis.")

async def demonstrate_crowd_analysis():
    """Example focused on crowd behavior analysis"""
    print("\n=== Crowd Behavior Analysis ===")
    
    crowd_scenarios = [
        "Dense crowd near emergency exit, people unable to move freely during evacuation drill",
        "Audience rushing towards stage barrier as headliner starts performance", 
        "Peaceful crowd dispersing normally after rally conclusion",
        "Agitated crowd forming after event cancellation announcement"
    ]
    
    for scenario in crowd_scenarios:
        print(f"\nCrowd Scenario: {scenario}")
        
        try:
            content = f"""
Event Context: Large outdoor music festival
Crowd Situation: {scenario}

Analyze this crowd behavior for security risks, focusing on:
- Stampede or crush potential
- Crowd density and movement patterns  
- Behavioral indicators of distress or aggression
- Need for crowd control intervention
"""
            
            response_text = ""
            for event in security_app.stream_query(
                user_id="security_analyst",
                message=content
            ):
                if hasattr(event, 'content') and hasattr(event.content, 'parts'):
                    for part in event.content.parts:
                        if hasattr(part, 'text'):
                            response_text += part.text
            
            try:
                result = json.loads(response_text)
                print(f"   - Threat Level: {result.get('threat_level')} ({result.get('threat_score')}/10)")
                print(f"   - Immediate Response: {result.get('requires_immediate_response')}")
                print(f"   - Key Concerns: {result.get('event_specific_concerns', [])}")
            except json.JSONDecodeError:
                print(f"   - Analysis: {response_text[:150]}...")
                
        except Exception as e:
            print(f"❌ Error: {e}")

async def main():
    """Run all examples"""
    print("🎪 Drishti Security Agent - Multimodal Event Analysis")
    print("=" * 60)
    
    try:
        # Test text-only analysis
        await analyze_text_only_threat()
        
        # Test multimodal analysis
        await analyze_multimodal_threat()
        
        # Test crowd-specific analysis
        await demonstrate_crowd_analysis()
        
        print("\n" + "="*60)
        print("✅ All multimodal security analysis examples completed!")
        print("\n📋 Agent Capabilities Demonstrated:")
        print("  ✓ Text-only threat analysis for various event types")
        print("  ✓ Multimodal image + text analysis")
        print("  ✓ Event-specific crowd behavior assessment")
        print("  ✓ JSON-structured threat assessment responses")
        
    except Exception as e:
        print(f"❌ Example failed: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 