#!/usr/bin/env python3
"""
Usage example for User Input Agent with Infrastructure Agent as subagent
"""

import asyncio
import json
from agent import user_input_app

async def test_infrastructure_incident():
    """Test infrastructure-related incident processing"""
    
    # Example 1: Text-based infrastructure incident
    text_incident = """
    There's a power outage in the main pavilion area. The lights went out about 10 minutes ago 
    and none of the sound equipment is working. This is affecting the main stage performance 
    and people are getting confused. Some emergency lighting is on but it's very dim.
    """
    
    print("=== Testing Infrastructure Incident (Text) ===")
    print(f"Input: {text_incident}")
    
    try:
        response = await user_input_app.query(text_incident)
        print("\nUser Input Agent Response:")
        print(json.dumps(response, indent=2))
        
        # The user_input_agent should automatically call infrastructure_agent
        # when it detects infrastructure-related content
        
    except Exception as e:
        print(f"Error processing text incident: {e}")

async def test_infrastructure_with_image():
    """Test infrastructure incident with image analysis"""
    
    # Example 2: Infrastructure incident with image description
    multimodal_incident = """
    I'm sending a photo of a damaged electrical panel near the food court. 
    There are sparks coming from it and it looks like some wires are exposed. 
    People are staying away from it but it seems dangerous.
    """
    
    print("\n=== Testing Infrastructure Incident (Multimodal) ===")
    print(f"Input: {multimodal_incident}")
    
    try:
        response = await user_input_app.query(multimodal_incident)
        print("\nUser Input Agent Response:")
        print(json.dumps(response, indent=2))
        
    except Exception as e:
        print(f"Error processing multimodal incident: {e}")

async def test_structural_issue():
    """Test structural infrastructure issue"""
    
    # Example 3: Structural infrastructure concern
    structural_incident = """
    The temporary stage structure is making creaking sounds and seems to be swaying 
    more than normal. There are about 200 people watching the performance right now. 
    I'm worried about safety - should we evacuate the area?
    """
    
    print("\n=== Testing Structural Infrastructure Issue ===")
    print(f"Input: {structural_incident}")
    
    try:
        response = await user_input_app.query(structural_incident)
        print("\nUser Input Agent Response:")
        print(json.dumps(response, indent=2))
        
    except Exception as e:
        print(f"Error processing structural incident: {e}")

async def test_non_infrastructure_incident():
    """Test non-infrastructure incident to verify routing logic"""
    
    # Example 4: Non-infrastructure incident (should not call infrastructure agent)
    medical_incident = """
    Someone just collapsed near the entrance gate. They appear to be unconscious 
    and people are gathering around. We need medical assistance immediately.
    """
    
    print("\n=== Testing Non-Infrastructure Incident (Medical) ===")
    print(f"Input: {medical_incident}")
    
    try:
        response = await user_input_app.query(medical_incident)
        print("\nUser Input Agent Response:")
        print(json.dumps(response, indent=2))
        
        # This should route to medical agent, not infrastructure agent
        
    except Exception as e:
        print(f"Error processing medical incident: {e}")

async def main():
    """Run all test scenarios"""
    
    print("User Input Agent with Infrastructure Subagent - Usage Examples")
    print("=" * 70)
    
    # Test different types of incidents
    await test_infrastructure_incident()
    await test_infrastructure_with_image() 
    await test_structural_issue()
    await test_non_infrastructure_incident()
    
    print("\n" + "=" * 70)
    print("Testing completed!")
    
    print("\nKey Points:")
    print("1. The user_input_agent automatically calls infrastructure_agent when it detects infrastructure-related content")
    print("2. The infrastructure_agent analyzes the specific infrastructure issues and provides detailed assessments")
    print("3. The routing is intelligent - non-infrastructure incidents won't trigger the infrastructure_agent")
    print("4. Both text and multimodal inputs are supported")

if __name__ == "__main__":
    asyncio.run(main()) 