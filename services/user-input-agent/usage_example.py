"""
User Input Analysis Agent Usage Example

This example demonstrates how to use the User Input Analysis Agent to process
various types of user inputs and route them to appropriate specialized agents
in the Drishti Event Management System.
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()

# Import the user input agent
from agent import user_input_app

async def process_text_emergency_report():
    """Example: Process urgent text-based emergency report"""
    
    user_text_input = """
    EMERGENCY! Someone collapsed at the main stage and isn't breathing! 
    There's a big crowd around and people are panicking. I think it might be a heart attack.
    This is happening right now near the front barrier. Please send help immediately!
    """
    
    print("🚨 Processing Emergency Text Report...")
    print(f"User Input: {user_text_input}")
    print("\n" + "="*50)
    
    try:
        result = await user_input_app.query(input_text=user_text_input)
        
        print("🔍 User Input Analysis Results:")
        print(f"✅ Input Processed: {result.get('input_processed', 'N/A')}")
        print(f"📊 Validation Status: {result.get('validation_status', 'N/A')}")
        print(f"🎯 Confidence Score: {result.get('confidence_score', 'N/A')}")
        print(f"🚨 Requires Escalation: {result.get('requires_escalation', 'N/A')}")
        
        if result.get('incident_details'):
            details = result['incident_details']
            print(f"\n📋 Incident Details:")
            print(f"   Category: {details.get('category', 'N/A')}")
            print(f"   Subcategory: {details.get('subcategory', 'N/A')}")
            print(f"   Urgency Level: {details.get('urgency_level', 'N/A')}")
            print(f"   Urgency Score: {details.get('urgency_score', 'N/A')}/10")
            print(f"   Location: {details.get('location', 'N/A')}")
            print(f"   People Involved: {details.get('people_involved', 'N/A')}")
        
        if result.get('routing_decision'):
            routing = result['routing_decision']
            print(f"\n🎯 Routing Decision:")
            print(f"   Target Agent: {routing.get('target_agent', 'N/A')}")
            print(f"   Routing Reason: {routing.get('routing_reason', 'N/A')}")
            print(f"   Priority Level: {routing.get('priority_level', 'N/A')}/10")
            print(f"   Multiple Agents: {routing.get('requires_multiple_agents', 'N/A')}")
            if routing.get('additional_agents'):
                print(f"   Additional Agents: {routing['additional_agents']}")
        
        if result.get('extracted_data'):
            extracted = result['extracted_data']
            print(f"\n🔍 Extracted Data:")
            print(f"   Keywords: {extracted.get('key_keywords', 'N/A')}")
            print(f"   Entities: {extracted.get('entities', 'N/A')}")
            print(f"   Sentiment: {extracted.get('sentiment', 'N/A')}")
            print(f"   Language: {extracted.get('language_detected', 'N/A')}")
        
        if result.get('data_for_target'):
            target_data = result['data_for_target']
            print(f"\n📤 Data for Target Agent:")
            print(f"   Formatted Input: {target_data.get('formatted_input', 'N/A')}")
            print(f"   Follow-up Required: {target_data.get('follow_up_required', 'N/A')}")
                
    except Exception as e:
        print(f"❌ Error processing emergency report: {e}")

async def process_infrastructure_complaint():
    """Example: Process infrastructure-related complaint"""
    
    user_complaint = """
    The power went out in the food vendor area about 10 minutes ago. 
    Several food trucks can't operate and people are getting frustrated. 
    The backup generators don't seem to be working either. 
    Can someone please fix this? It's affecting a lot of vendors.
    """
    
    print("⚡ Processing Infrastructure Complaint...")
    print(f"User Input: {user_complaint}")
    print("\n" + "="*50)
    
    try:
        result = await user_input_app.query(input_text=user_complaint)
        
        print("🔍 User Input Analysis Results:")
        print(f"📊 Validation Status: {result.get('validation_status', 'N/A')}")
        print(f"🎯 Confidence Score: {result.get('confidence_score', 'N/A')}")
        
        if result.get('incident_details'):
            details = result['incident_details']
            print(f"\n📋 Incident Classification:")
            print(f"   Category: {details.get('category', 'N/A')}")
            print(f"   Urgency Level: {details.get('urgency_level', 'N/A')}")
            print(f"   Description: {details.get('description', 'N/A')}")
        
        if result.get('routing_decision'):
            routing = result['routing_decision']
            print(f"\n🎯 Routing Decision:")
            print(f"   Target Agent: {routing.get('target_agent', 'N/A')}")
            print(f"   Priority Level: {routing.get('priority_level', 'N/A')}/10")
        
        if result.get('validation_issues'):
            issues = result['validation_issues']
            if issues.get('missing_information'):
                print(f"\n⚠️ Missing Information: {issues['missing_information']}")
            if issues.get('follow_up_questions'):
                print(f"❓ Follow-up Questions: {issues['follow_up_questions']}")
                
    except Exception as e:
        print(f"❌ Error processing infrastructure complaint: {e}")

async def process_multilingual_input():
    """Example: Process input in non-English language"""
    
    spanish_input = """
    ¡Ayuda! Hay una multitud muy grande cerca del escenario principal. 
    La gente está empujando y no puedo moverme. Estoy preocupado por mi seguridad. 
    ¿Pueden enviar más seguridad por favor?
    """
    
    print("🌍 Processing Multilingual Input (Spanish)...")
    print(f"User Input: {spanish_input}")
    print("\n" + "="*50)
    
    try:
        result = await user_input_app.query(input_text=spanish_input)
        
        print("🔍 Multilingual Analysis Results:")
        print(f"📊 Validation Status: {result.get('validation_status', 'N/A')}")
        print(f"🎯 Confidence Score: {result.get('confidence_score', 'N/A')}")
        
        if result.get('extracted_data'):
            extracted = result['extracted_data']
            print(f"\n🌐 Language Processing:")
            print(f"   Language Detected: {extracted.get('language_detected', 'N/A')}")
            print(f"   Sentiment: {extracted.get('sentiment', 'N/A')}")
            print(f"   Keywords: {extracted.get('key_keywords', 'N/A')}")
        
        if result.get('processing_metadata'):
            metadata = result['processing_metadata']
            print(f"\n📊 Processing Metadata:")
            print(f"   Language Processing: {metadata.get('language_processing', 'N/A')}")
            print(f"   Quality Score: {metadata.get('quality_score', 'N/A')}")
        
        if result.get('routing_decision'):
            routing = result['routing_decision']
            print(f"\n🎯 Routing Decision:")
            print(f"   Target Agent: {routing.get('target_agent', 'N/A')}")
            print(f"   Routing Reason: {routing.get('routing_reason', 'N/A')}")
                
    except Exception as e:
        print(f"❌ Error processing multilingual input: {e}")

async def process_ambiguous_input():
    """Example: Process vague or incomplete input"""
    
    vague_input = """
    Something's wrong near the bathrooms. Not sure what exactly but it looks bad.
    """
    
    print("❓ Processing Ambiguous Input...")
    print(f"User Input: {vague_input}")
    print("\n" + "="*50)
    
    try:
        result = await user_input_app.query(input_text=vague_input)
        
        print("🔍 Ambiguous Input Analysis:")
        print(f"📊 Validation Status: {result.get('validation_status', 'N/A')}")
        print(f"🎯 Confidence Score: {result.get('confidence_score', 'N/A')}")
        
        if result.get('validation_issues'):
            issues = result['validation_issues']
            print(f"\n⚠️ Validation Issues:")
            if issues.get('missing_information'):
                print(f"   Missing Information: {issues['missing_information']}")
            if issues.get('clarification_needed'):
                print(f"   Clarification Needed: {issues['clarification_needed']}")
            if issues.get('follow_up_questions'):
                print(f"   Follow-up Questions: {issues['follow_up_questions']}")
        
        if result.get('routing_decision'):
            routing = result['routing_decision']
            print(f"\n🎯 Preliminary Routing:")
            print(f"   Target Agent: {routing.get('target_agent', 'N/A')}")
            print(f"   Routing Reason: {routing.get('routing_reason', 'N/A')}")
        
        print(f"\n💡 Input Summary: {result.get('input_summary', 'N/A')}")
                
    except Exception as e:
        print(f"❌ Error processing ambiguous input: {e}")

async def test_input_categorization():
    """Test various input types and categorization"""
    
    test_inputs = [
        {
            "name": "Security Threat",
            "input": "I saw someone with a weapon near the entrance gate. Very suspicious behavior.",
            "expected_category": "security",
            "expected_agent": "security_agent"
        },
        {
            "name": "Medical Emergency",
            "input": "Person having seizure in the VIP area. Need medical help urgently!",
            "expected_category": "medical",
            "expected_agent": "medassist_agent"
        },
        {
            "name": "Crowd Issues",
            "input": "It's getting really crowded near the stage and people are getting crushed.",
            "expected_category": "crowd",
            "expected_agent": "crowdflow_agent"
        },
        {
            "name": "Queue Problems",
            "input": "The line for food is taking forever and people are cutting in line.",
            "expected_category": "crowd",
            "expected_agent": "queue_management_agent"
        },
        {
            "name": "Lost Person",
            "input": "I can't find my friend. We got separated in the crowd. Can you help?",
            "expected_category": "communication",
            "expected_agent": "comms_resources_agent"
        },
        {
            "name": "Weather Concern",
            "input": "It's starting to rain and there's lightning. Is the event still safe?",
            "expected_category": "environmental",
            "expected_agent": "comms_resources_agent"
        }
    ]
    
    for test_case in test_inputs:
        print(f"\n🧪 Testing: {test_case['name']}")
        print("="*60)
        
        try:
            result = await user_input_app.query(input_text=test_case['input'])
            
            category = result.get('incident_details', {}).get('category', 'unknown')
            target_agent = result.get('routing_decision', {}).get('target_agent', 'unknown')
            urgency = result.get('incident_details', {}).get('urgency_level', 'unknown')
            confidence = result.get('confidence_score', 0)
            
            print(f"📊 Category: {category} (Expected: {test_case['expected_category']})")
            print(f"🎯 Target Agent: {target_agent} (Expected: {test_case['expected_agent']})")
            print(f"⚡ Urgency: {urgency}")
            print(f"🎯 Confidence: {confidence}")
            
            # Check if categorization is correct
            category_match = "✅" if category == test_case['expected_category'] else "⚠️"
            agent_match = "✅" if target_agent == test_case['expected_agent'] else "⚠️"
            
            print(f"{category_match} Category Match | {agent_match} Agent Match")
            
        except Exception as e:
            print(f"❌ Error: {e}")

async def test_multimodal_scenarios():
    """Test scenarios with multiple input types"""
    
    print("\n📱 Testing Multimodal Input Scenarios")
    print("="*60)
    
    multimodal_scenarios = [
        {
            "name": "Text + Image Reference",
            "input": "There's a problem with the stage lighting - see attached photo",
            "has_image": True
        },
        {
            "name": "Voice Message Description", 
            "input": "This would be processed as a voice message about a medical emergency",
            "input_type": "voice"
        },
        {
            "name": "Text + Location Data",
            "input": "Need help at Section C, Row 15. Person feeling sick.",
            "has_location": True
        },
        {
            "name": "Emergency with Multiple Media",
            "input": "EMERGENCY: Fire in kitchen area! See photo and voice message for details.",
            "multimodal": True
        }
    ]
    
    for scenario in multimodal_scenarios:
        print(f"\n📱 Scenario: {scenario['name']}")
        print("-" * 40)
        
        try:
            result = await user_input_app.query(input_text=scenario['input'])
            
            print(f"📊 Validation: {result.get('validation_status', 'N/A')}")
            print(f"🎯 Confidence: {result.get('confidence_score', 'N/A')}")
            
            if result.get('processing_metadata'):
                metadata = result['processing_metadata']
                print(f"📱 Input Type: {metadata.get('input_type', 'N/A')}")
                print(f"⚡ Processing Time: {metadata.get('processing_time', 'N/A')}")
            
            if result.get('routing_decision'):
                routing = result['routing_decision']
                print(f"🎯 Target Agent: {routing.get('target_agent', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Error analyzing multimodal scenario: {e}")

async def main():
    """Main example function"""
    print("📱 User Input Analysis Agent Usage Examples")
    print("="*60)
    
    # Test emergency text processing
    await process_text_emergency_report()
    print("\n" + "="*60)
    
    # Test infrastructure complaint
    await process_infrastructure_complaint()
    print("\n" + "="*60)
    
    # Test multilingual input
    await process_multilingual_input()
    print("\n" + "="*60)
    
    # Test ambiguous input handling
    await process_ambiguous_input()
    print("\n" + "="*60)
    
    # Test input categorization
    await test_input_categorization()
    print("\n" + "="*60)
    
    # Test multimodal scenarios
    await test_multimodal_scenarios()
    
    print("\n✅ All user input analysis examples completed!")
    print("\n📱 Intelligent input processing and routing capabilities ready!")

if __name__ == "__main__":
    # Run the examples
    asyncio.run(main()) 