"""
MedAssist Agent Usage Example

This example demonstrates how to use the MedAssist Agent to analyze
medical emergencies and coordinate medical response in the Drishti Event Management System.
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()

# Import the medassist agent
from agent import medassist_app

async def analyze_medical_emergency():
    """Example: Analyze medical emergency from text description"""
    
    text_description = """
    A person has collapsed near the main stage and appears to be unconscious. 
    Bystanders report the person was complaining of chest pain moments before 
    collapsing. They are not responding to verbal stimuli and appear to have 
    difficulty breathing.
    """
    
    print("🚑 Analyzing medical emergency from text description...")
    print(f"Description: {text_description}")
    print("\n" + "="*50)
    
    try:
        result = await medassist_app.query(input_text=text_description)
        
        print("🏥 Medical Emergency Analysis Results:")
        print(f"🚨 Medical Emergency: {result.get('is_medical_emergency', 'N/A')}")
        print(f"⚡ Emergency Level: {result.get('emergency_level', 'N/A')}")
        print(f"🎯 Confidence Score: {result.get('confidence_score', 'N/A')}")
        print(f"📊 Triage Score: {result.get('triage_score', 'N/A')}/10")
        print(f"🚨 Immediate Response Required: {result.get('requires_immediate_response', 'N/A')}")
        print(f"🩺 Medical Categories: {result.get('medical_categories', 'N/A')}")
        print(f"🚑 Emergency Services Needed: {result.get('emergency_services_needed', 'N/A')}")
        print(f"⏱️  Response Time: {result.get('estimated_response_time', 'N/A')}")
        print(f"🏥 Follow-up Care: {result.get('follow_up_care', 'N/A')}")
        
        if result.get('resource_requirements'):
            print(f"📋 Required Resources: {result.get('resource_requirements', 'N/A')}")
        
        print(f"\n📝 Medical Analysis: {result.get('analysis', 'N/A')}")
        
        if result.get('recommended_actions'):
            print(f"\n🩺 Recommended Actions:")
            for i, action in enumerate(result['recommended_actions'], 1):
                print(f"   {i}. {action}")
                
    except Exception as e:
        print(f"❌ Error analyzing medical emergency: {e}")

async def analyze_with_visual_evidence():
    """Example: Analyze medical situation with both text and image"""
    
    # This is a placeholder - in real usage, you'd load an actual medical emergency image
    image_path = "../images/normal1.jfif"  # Using existing image as example
    
    text_description = """
    Person appears to have fallen and is lying motionless on the ground. 
    There's visible bleeding from what appears to be a head injury. 
    The person is not responding to people trying to help.
    """
    
    print("🚑 Analyzing medical emergency with text and visual evidence...")
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
            result = await medassist_app.query(
                input_text=text_description,
                # Note: Actual image handling may vary based on ADK implementation
                image_data=image_data
            )
        else:
            print("⚠️  Image not found, analyzing text only...")
            result = await medassist_app.query(input_text=text_description)
        
        print("🏥 Medical Emergency Analysis Results:")
        print(f"🚨 Medical Emergency: {result.get('is_medical_emergency', 'N/A')}")
        print(f"⚡ Emergency Level: {result.get('emergency_level', 'N/A')}")
        print(f"🎯 Confidence Score: {result.get('confidence_score', 'N/A')}")
        print(f"📊 Triage Score: {result.get('triage_score', 'N/A')}/10")
        print(f"🚨 Immediate Response Required: {result.get('requires_immediate_response', 'N/A')}")
        print(f"🩺 Medical Categories: {result.get('medical_categories', 'N/A')}")
        print(f"📋 Required Resources: {result.get('resource_requirements', 'N/A')}")
        
        if result.get('visual_signs_detected'):
            print(f"👁️  Visual Signs Detected: {result.get('visual_signs_detected', 'N/A')}")
        
        print(f"\n📝 Medical Analysis: {result.get('analysis', 'N/A')}")
        
        if result.get('recommended_actions'):
            print(f"\n🩺 Recommended Actions:")
            for i, action in enumerate(result['recommended_actions'], 1):
                print(f"   {i}. {action}")
                
    except Exception as e:
        print(f"❌ Error analyzing medical emergency: {e}")

async def test_medical_scenarios():
    """Test different medical emergency scenarios"""
    
    scenarios = [
        {
            "name": "Cardiac Emergency",
            "description": "Middle-aged person clutching chest, complaining of severe chest pain radiating to left arm. Appears sweaty and short of breath.",
            "expected_level": "critical"
        },
        {
            "name": "Severe Allergic Reaction",
            "description": "Person having difficulty breathing after eating. Face appears swollen and they have a rash. Complaining they can't breathe properly.",
            "expected_level": "critical"
        },
        {
            "name": "Heat Exhaustion",
            "description": "Concert-goer feeling dizzy and nauseous. Appears overheated and disoriented. Skin is hot and dry.",
            "expected_level": "urgent"
        },
        {
            "name": "Minor Cut",
            "description": "Person has a small cut on their hand from broken glass. Bleeding is minimal and they are alert and oriented.",
            "expected_level": "non-urgent"
        },
        {
            "name": "Seizure",
            "description": "Person suddenly collapsed and is having convulsions. Bystanders report jerking movements and loss of consciousness.",
            "expected_level": "critical"
        },
        {
            "name": "Sprained Ankle", 
            "description": "Person twisted ankle while dancing. Ankle is swollen and painful but they can bear some weight. No other injuries.",
            "expected_level": "urgent"
        },
        {
            "name": "Panic Attack",
            "description": "Person hyperventilating and expressing fear. Says they feel like they're having a heart attack but vital signs appear stable.",
            "expected_level": "urgent"
        },
        {
            "name": "Intoxication",
            "description": "Heavily intoxicated person vomiting and barely conscious. Friends report excessive alcohol consumption.",
            "expected_level": "urgent"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n🧪 Testing Medical Scenario: {scenario['name']}")
        print("="*60)
        
        try:
            result = await medassist_app.query(input_text=scenario['description'])
            
            print(f"⚡ Emergency Level: {result.get('emergency_level', 'N/A')}")
            print(f"📊 Triage Score: {result.get('triage_score', 'N/A')}/10")
            print(f"🚨 Immediate Response: {result.get('requires_immediate_response', 'N/A')}")
            print(f"🩺 Medical Categories: {result.get('medical_categories', 'N/A')}")
            print(f"📋 Resources Needed: {result.get('resource_requirements', 'N/A')}")
            print(f"⏱️  Response Time: {result.get('estimated_response_time', 'N/A')}")
            
            # Check if assessment matches expected level
            expected = scenario.get('expected_level', 'unknown')
            actual = result.get('emergency_level', 'unknown')
            match_indicator = "✅" if expected == actual else "⚠️"
            print(f"{match_indicator} Expected: {expected}, Got: {actual}")
            
        except Exception as e:
            print(f"❌ Error: {e}")

async def test_symptom_analysis():
    """Test symptom analysis capabilities"""
    
    print("\n🔬 Testing Symptom Analysis Capabilities")
    print("="*60)
    
    symptom_cases = [
        "Severe chest pain, shortness of breath, nausea, sweating",
        "High fever, severe headache, stiff neck, sensitivity to light", 
        "Sudden severe abdominal pain, vomiting, unable to stand straight",
        "Difficulty swallowing, swollen throat, hives on skin",
        "Confusion, slurred speech, weakness on one side of body"
    ]
    
    for i, symptoms in enumerate(symptom_cases, 1):
        print(f"\n📋 Symptom Case {i}: {symptoms}")
        print("-" * 40)
        
        try:
            # Create a detailed symptom description
            symptom_description = f"Patient presenting with: {symptoms}"
            result = await medassist_app.query(input_text=symptom_description)
            
            print(f"📊 Triage Assessment: {result.get('emergency_level', 'N/A')}")
            print(f"🩺 Medical Categories: {result.get('medical_categories', 'N/A')}")
            print(f"⏱️  Response Priority: {result.get('estimated_response_time', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Error analyzing symptoms: {e}")

async def main():
    """Main example function"""
    print("🏥 MedAssist Agent Usage Examples")
    print("="*60)
    
    # Test basic medical emergency analysis
    await analyze_medical_emergency()
    print("\n" + "="*60)
    
    # Test with visual evidence (if available)
    await analyze_with_visual_evidence()
    print("\n" + "="*60)
    
    # Test different medical scenarios
    await test_medical_scenarios()
    print("\n" + "="*60)
    
    # Test symptom analysis
    await test_symptom_analysis()
    
    print("\n✅ All medical analysis examples completed!")
    print("\n🚑 Remember: This is for demonstration purposes only.")
    print("In real emergencies, always call emergency services immediately!")

if __name__ == "__main__":
    # Run the examples
    asyncio.run(main()) 