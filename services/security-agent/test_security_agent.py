#!/usr/bin/env python3
"""
Test script for Security Agent

This script demonstrates how to use the Security Agent to analyze security threats
from text descriptions and optional images.
"""

import asyncio
import json
import base64
from pathlib import Path

from agent import SecurityAgent

async def test_text_only_analysis():
    """Test security analysis with text only"""
    print("\n=== Testing Text-Only Security Analysis ===")
    
    agent = SecurityAgent()
    
    test_cases = [
        {
            "description": "Person found a lost wallet near the food court",
            "location": "Food court",
            "expected_level": "low"
        },
        {
            "description": "Suspicious person loitering near the entrance for 30 minutes",
            "location": "Main entrance", 
            "expected_level": "medium"
        },
        {
            "description": "Someone spotted with a knife threatening other attendees",
            "location": "Main hall",
            "expected_level": "high"
        },
        {
            "description": "Fire alarm triggered in building west wing",
            "location": "West wing",
            "expected_level": "high"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"Description: {case['description']}")
        print(f"Location: {case['location']}")
        
        try:
            result = await agent.analyze_security_threat(
                description=case['description'],
                location=case['location'],
                reporter_id=f"test_user_{i}",
                incident_id=f"test_incident_{i}"
            )
            
            print(f"✅ Analysis Result:")
            print(f"   - Is Security Concern: {result['is_security_concern']}")
            print(f"   - Threat Level: {result['threat_level']} (expected: {case['expected_level']})")
            print(f"   - Threat Score: {result['threat_score']}/10")
            print(f"   - Confidence: {result['confidence_score']:.2f}")
            print(f"   - Immediate Response Required: {result['requires_immediate_response']}")
            print(f"   - Analysis: {result['analysis'][:100]}...")
            
        except Exception as e:
            print(f"❌ Error analyzing threat: {e}")

async def test_image_analysis():
    """Test security analysis with image (simulated)"""
    print("\n=== Testing Image Security Analysis ===")
    
    agent = SecurityAgent()
    
    # Simulate image data (in real use, this would be actual image bytes)
    # For testing purposes, we'll create a small dummy image
    try:
        from PIL import Image
        import io
        
        # Create a small test image
        img = Image.new('RGB', (100, 100), color='red')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        image_data = img_bytes.getvalue()
        
        result = await agent.analyze_security_threat(
            description="Crowd forming near the exit, people seem agitated",
            image_data=image_data,
            image_content_type="image/jpeg",
            location="Emergency exit A",
            reporter_id="security_camera_01"
        )
        
        print(f"✅ Multimodal Analysis Result:")
        print(f"   - Is Security Concern: {result['is_security_concern']}")
        print(f"   - Threat Level: {result['threat_level']}")
        print(f"   - Threat Score: {result['threat_score']}/10")
        print(f"   - Visual Threats: {result.get('visual_threats_detected', [])}")
        print(f"   - Analysis: {result['analysis'][:150]}...")
        
    except ImportError:
        print("⚠️  PIL not available for image testing")
    except Exception as e:
        print(f"❌ Error in image analysis: {e}")

def test_keyword_analysis():
    """Test the keyword-based threat assessment"""
    print("\n=== Testing Keyword Analysis ===")
    
    agent = SecurityAgent()
    
    test_descriptions = [
        "Lost my phone somewhere in the venue",
        "Suspicious person with a large backpack near restricted area", 
        "Someone has a knife and is threatening people",
        "Fire started in the kitchen area"
    ]
    
    for desc in test_descriptions:
        keyword_result = agent._analyze_text_for_keywords(desc)
        threat_level = agent._determine_threat_level(keyword_result['initial_threat_score'])
        
        print(f"\nDescription: {desc}")
        print(f"Initial Threat Score: {keyword_result['initial_threat_score']}")
        print(f"Threat Level: {threat_level}")
        print(f"High-risk keywords: {keyword_result['high_risk_keywords']}")
        print(f"Medium-risk keywords: {keyword_result['medium_risk_keywords']}")

async def main():
    """Run all tests"""
    print("🚀 Starting Security Agent Tests")
    print("=" * 50)
    
    try:
        # Test keyword analysis (doesn't require Vertex AI)
        test_keyword_analysis()
        
        # Test text-only analysis (requires Vertex AI)
        print("\n" + "="*50)
        print("⚠️  The following tests require Google Cloud credentials")
        print("   and Vertex AI access. They may fail without proper setup.")
        print("="*50)
        
        # Uncomment these lines when you have GCP credentials set up:
        # await test_text_only_analysis()
        # await test_image_analysis()
        
        print("\n✅ Basic tests completed successfully!")
        print("\n📝 To run full tests with Vertex AI:")
        print("   1. Set up Google Cloud credentials")
        print("   2. Enable Vertex AI API")
        print("   3. Uncomment the test functions in main()")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 