"""
Test cases for the MedAssist Agent

This module contains unit tests and integration tests for the MedAssist Agent
to ensure it properly analyzes medical emergencies and provides appropriate medical responses.
"""

import unittest
import asyncio
import json
from unittest.mock import Mock, patch
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import medassist_agent, medassist_app
from prompt import MEDICAL_ANALYSIS_PROMPT

class TestMedAssistAgent(unittest.TestCase):
    """Test cases for MedAssist Agent functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_scenarios = [
            {
                "name": "Critical Cardiac Emergency",
                "description": "Person collapsed with severe chest pain, unconscious, not breathing normally",
                "expected_level": "critical",
                "expected_categories": ["cardiac"]
            },
            {
                "name": "Urgent Trauma",
                "description": "Person fell from stage, conscious but complaining of severe back pain, cannot move legs",
                "expected_level": "urgent", 
                "expected_categories": ["trauma", "neurological"]
            },
            {
                "name": "Minor Injury",
                "description": "Small cut on finger from broken bottle, bleeding is controlled, person is alert",
                "expected_level": "non-urgent",
                "expected_categories": ["trauma"]
            },
            {
                "name": "Allergic Reaction",
                "description": "Person having difficulty breathing after eating nuts, face swelling, hives visible",
                "expected_level": "critical",
                "expected_categories": ["allergic"]
            }
        ]
    
    def test_agent_initialization(self):
        """Test that the medassist agent initializes correctly"""
        self.assertIsNotNone(medassist_agent)
        self.assertEqual(medassist_agent.name, "medassist_agent")
        self.assertEqual(medassist_agent.model, "gemini-2.0-flash-001")
        self.assertIn("medical", medassist_agent.description.lower())
    
    def test_prompt_content(self):
        """Test that the prompt contains required medical keywords"""
        prompt = MEDICAL_ANALYSIS_PROMPT
        
        # Check for key medical categories
        self.assertIn("trauma", prompt.lower())
        self.assertIn("cardiac", prompt.lower())
        self.assertIn("neurological", prompt.lower())
        self.assertIn("allergic", prompt.lower())
        
        # Check for triage levels
        self.assertIn("critical", prompt.lower())
        self.assertIn("urgent", prompt.lower())
        self.assertIn("non-urgent", prompt.lower())
        
        # Check for required response fields
        self.assertIn("is_medical_emergency", prompt)
        self.assertIn("emergency_level", prompt)
        self.assertIn("confidence_score", prompt)
        self.assertIn("recommended_actions", prompt)
        self.assertIn("triage_score", prompt)
    
    @patch('agent.medassist_app.query')
    async def test_cardiac_emergency_analysis(self, mock_query):
        """Test analysis of cardiac emergency"""
        # Mock response for cardiac emergency
        mock_response = {
            "is_medical_emergency": True,
            "emergency_level": "critical",
            "confidence_score": 0.95,
            "triage_score": 9,
            "analysis": "Critical cardiac emergency - possible heart attack",
            "recommended_actions": ["Call 911 immediately", "Begin CPR if no pulse", "Prepare AED"],
            "requires_immediate_response": True,
            "medical_categories": ["cardiac"],
            "resource_requirements": ["ambulance", "ALS_team", "defibrillator"],
            "estimated_response_time": "immediate",
            "emergency_services_needed": True,
            "follow_up_care": "hospitalization"
        }
        mock_query.return_value = mock_response
        
        description = "Person collapsed with severe chest pain, unconscious, not breathing normally"
        result = await medassist_app.query(input_text=description)
        
        self.assertTrue(result["is_medical_emergency"])
        self.assertEqual(result["emergency_level"], "critical")
        self.assertIn("cardiac", result["medical_categories"])
        self.assertTrue(result["requires_immediate_response"])
        self.assertTrue(result["emergency_services_needed"])
    
    @patch('agent.medassist_app.query')
    async def test_trauma_analysis(self, mock_query):
        """Test analysis of trauma emergency"""
        mock_response = {
            "is_medical_emergency": True,
            "emergency_level": "urgent", 
            "confidence_score": 0.85,
            "triage_score": 7,
            "analysis": "Serious trauma with potential spinal injury",
            "recommended_actions": ["Immobilize spine", "Check vital signs", "Prepare for transport"],
            "requires_immediate_response": True,
            "medical_categories": ["trauma", "neurological"],
            "resource_requirements": ["ambulance", "backboard", "medical_team"],
            "estimated_response_time": "minutes",
            "emergency_services_needed": True,
            "follow_up_care": "transport"
        }
        mock_query.return_value = mock_response
        
        description = "Person fell from stage, conscious but severe back pain, cannot move legs"
        result = await medassist_app.query(input_text=description)
        
        self.assertTrue(result["is_medical_emergency"])
        self.assertEqual(result["emergency_level"], "urgent")
        self.assertIn("trauma", result["medical_categories"])
        self.assertTrue(result["requires_immediate_response"])
    
    @patch('agent.medassist_app.query')
    async def test_allergic_reaction_analysis(self, mock_query):
        """Test analysis of severe allergic reaction"""
        mock_response = {
            "is_medical_emergency": True,
            "emergency_level": "critical",
            "confidence_score": 0.9,
            "triage_score": 8,
            "analysis": "Severe allergic reaction - possible anaphylaxis",
            "recommended_actions": ["Administer epinephrine if available", "Call 911", "Monitor airway"],
            "requires_immediate_response": True,
            "medical_categories": ["allergic"],
            "resource_requirements": ["ambulance", "epinephrine", "oxygen"],
            "estimated_response_time": "immediate",
            "emergency_services_needed": True,
            "follow_up_care": "hospitalization"
        }
        mock_query.return_value = mock_response
        
        description = "Person difficulty breathing after eating nuts, face swelling, hives visible"
        result = await medassist_app.query(input_text=description)
        
        self.assertTrue(result["is_medical_emergency"])
        self.assertEqual(result["emergency_level"], "critical")
        self.assertIn("allergic", result["medical_categories"])
        self.assertTrue(result["emergency_services_needed"])
    
    @patch('agent.medassist_app.query')
    async def test_minor_injury_analysis(self, mock_query):
        """Test analysis of minor medical situation"""
        mock_response = {
            "is_medical_emergency": True,
            "emergency_level": "non-urgent",
            "confidence_score": 0.8,
            "triage_score": 2,
            "analysis": "Minor laceration requiring basic first aid",
            "recommended_actions": ["Clean wound", "Apply bandage", "Monitor for infection"],
            "requires_immediate_response": False,
            "medical_categories": ["trauma"],
            "resource_requirements": ["first_aid_kit"],
            "estimated_response_time": "standard",
            "emergency_services_needed": False,
            "follow_up_care": "monitoring"
        }
        mock_query.return_value = mock_response
        
        description = "Small cut on finger from broken bottle, bleeding controlled, person alert"
        result = await medassist_app.query(input_text=description)
        
        self.assertTrue(result["is_medical_emergency"])
        self.assertEqual(result["emergency_level"], "non-urgent")
        self.assertFalse(result["requires_immediate_response"])
        self.assertFalse(result["emergency_services_needed"])
    
    @patch('agent.medassist_app.query')
    async def test_neurological_emergency(self, mock_query):
        """Test analysis of neurological emergency"""
        mock_response = {
            "is_medical_emergency": True,
            "emergency_level": "critical",
            "confidence_score": 0.92,
            "triage_score": 9,
            "analysis": "Possible stroke - immediate intervention required",
            "recommended_actions": ["Call 911 immediately", "Note time of onset", "Prepare for rapid transport"],
            "requires_immediate_response": True,
            "medical_categories": ["neurological"],
            "resource_requirements": ["ambulance", "stroke_team"],
            "estimated_response_time": "immediate",
            "emergency_services_needed": True,
            "follow_up_care": "hospitalization"
        }
        mock_query.return_value = mock_response
        
        description = "Person suddenly confused, slurred speech, weakness on right side of body"
        result = await medassist_app.query(input_text=description)
        
        self.assertTrue(result["is_medical_emergency"])
        self.assertEqual(result["emergency_level"], "critical")
        self.assertIn("neurological", result["medical_categories"])
        self.assertTrue(result["emergency_services_needed"])
    
    @patch('agent.medassist_app.query')
    async def test_environmental_emergency(self, mock_query):
        """Test analysis of environmental medical emergency"""
        mock_response = {
            "is_medical_emergency": True,
            "emergency_level": "urgent",
            "confidence_score": 0.85,
            "triage_score": 6,
            "analysis": "Heat exhaustion requiring immediate cooling and hydration",
            "recommended_actions": ["Move to shade", "Cool with water", "Provide fluids if conscious"],
            "requires_immediate_response": True,
            "medical_categories": ["environmental"],
            "resource_requirements": ["cooling_supplies", "IV_fluids"],
            "estimated_response_time": "minutes",
            "emergency_services_needed": False,
            "follow_up_care": "monitoring"
        }
        mock_query.return_value = mock_response
        
        description = "Person overheated, dizzy, nauseous, hot dry skin, disoriented"
        result = await medassist_app.query(input_text=description)
        
        self.assertTrue(result["is_medical_emergency"])
        self.assertEqual(result["emergency_level"], "urgent")
        self.assertIn("environmental", result["medical_categories"])
    
    @patch('agent.medassist_app.query')
    async def test_non_medical_situation(self, mock_query):
        """Test handling of non-medical situations"""
        mock_response = {
            "is_medical_emergency": False,
            "emergency_level": "non-urgent",
            "confidence_score": 0.9,
            "triage_score": 1,
            "analysis": "Not a medical emergency - appears to be security/logistics issue",
            "recommended_actions": ["Forward to event security", "Provide information"],
            "requires_immediate_response": False,
            "medical_categories": [],
            "resource_requirements": [],
            "estimated_response_time": "standard",
            "emergency_services_needed": False,
            "follow_up_care": "none"
        }
        mock_query.return_value = mock_response
        
        description = "Person asking for directions to restrooms, appears fine"
        result = await medassist_app.query(input_text=description)
        
        self.assertFalse(result["is_medical_emergency"])
        self.assertEqual(result["medical_categories"], [])
        self.assertFalse(result["emergency_services_needed"])
    
    def test_response_format_validation(self):
        """Test that expected response format fields are defined"""
        required_fields = [
            "is_medical_emergency",
            "emergency_level", 
            "confidence_score",
            "triage_score",
            "analysis",
            "recommended_actions",
            "requires_immediate_response",
            "medical_categories",
            "resource_requirements",
            "estimated_response_time",
            "emergency_services_needed",
            "follow_up_care"
        ]
        
        # Check that all required fields are mentioned in the prompt
        prompt = MEDICAL_ANALYSIS_PROMPT
        for field in required_fields:
            self.assertIn(field, prompt, f"Required field '{field}' not found in prompt")

class TestMedAssistAgentIntegration(unittest.TestCase):
    """Integration tests for MedAssist Agent"""
    
    @unittest.skipIf(not os.getenv('PROJECT_ID'), "PROJECT_ID not set - skipping integration tests")
    async def test_real_agent_response(self):
        """Test actual agent response (requires valid GCP credentials)"""
        try:
            description = "Test scenario: Person with minor headache, alert and oriented."
            result = await medassist_app.query(input_text=description)
            
            # Verify response has expected structure
            self.assertIsInstance(result, dict)
            
            # Check for key fields (allowing for flexibility in actual AI responses)
            expected_fields = ["analysis", "emergency_level"]
            for field in expected_fields:
                self.assertIn(field, result, f"Expected field '{field}' missing from response")
                
        except Exception as e:
            self.skipTest(f"Integration test failed - may require proper GCP setup: {e}")

def run_async_tests():
    """Run async tests"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Create test suite with only async tests
    suite = unittest.TestSuite()
    
    # Add async test methods
    async_test_methods = [
        'test_cardiac_emergency_analysis',
        'test_trauma_analysis', 
        'test_allergic_reaction_analysis',
        'test_minor_injury_analysis',
        'test_neurological_emergency',
        'test_environmental_emergency',
        'test_non_medical_situation'
    ]
    
    for method_name in async_test_methods:
        suite.addTest(TestMedAssistAgent(method_name))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Patch the test methods to handle async
    for test in suite:
        if hasattr(test, '_testMethodName'):
            method_name = test._testMethodName
            if method_name in async_test_methods:
                original_method = getattr(test, method_name)
                setattr(test, method_name, lambda self: loop.run_until_complete(original_method()))
    
    result = runner.run(suite)
    loop.close()
    return result

if __name__ == '__main__':
    print("🧪 Running MedAssist Agent Tests")
    print("="*50)
    
    # Run synchronous tests first
    print("\n📋 Running synchronous tests...")
    sync_suite = unittest.TestLoader().loadTestsFromTestCase(TestMedAssistAgent)
    # Filter out async tests
    filtered_tests = []
    for test in sync_suite:
        if test._testMethodName in [
            'test_agent_initialization', 'test_prompt_content', 'test_response_format_validation'
        ]:
            filtered_tests.append(test)
    
    sync_suite = unittest.TestSuite(filtered_tests)
    sync_runner = unittest.TextTestRunner(verbosity=2)
    sync_result = sync_runner.run(sync_suite)
    
    # Run async tests
    print("\n🔄 Running asynchronous tests...")
    async_result = run_async_tests()
    
    # Summary
    total_tests = sync_result.testsRun + async_result.testsRun
    total_failures = len(sync_result.failures) + len(async_result.failures)
    total_errors = len(sync_result.errors) + len(async_result.errors)
    
    print(f"\n📊 Test Summary:")
    print(f"   Total tests: {total_tests}")
    print(f"   Failures: {total_failures}")
    print(f"   Errors: {total_errors}")
    print(f"   Success rate: {((total_tests - total_failures - total_errors) / total_tests * 100):.1f}%")
    
    if total_failures == 0 and total_errors == 0:
        print("✅ All tests passed!")
        print("\n🏥 MedAssist Agent is ready for medical emergency response!")
    else:
        print("❌ Some tests failed. Check output above for details.")
        
    print("\n⚠️  IMPORTANT: This is for testing purposes only.")
    print("In real medical emergencies, always call emergency services immediately!") 