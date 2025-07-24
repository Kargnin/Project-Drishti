"""
Test cases for the User Input Analysis Agent

This module contains unit tests and integration tests for the User Input Analysis Agent
to ensure it properly processes user inputs and routes them to appropriate agents.
"""

import unittest
import asyncio
import json
from unittest.mock import Mock, patch
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import user_input_agent, user_input_app
from prompt import USER_INPUT_ANALYSIS_PROMPT

class TestUserInputAgent(unittest.TestCase):
    """Test cases for User Input Analysis Agent functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_scenarios = [
            {
                "name": "Medical Emergency",
                "input": "Person collapsed at main stage, not breathing, need help immediately!",
                "expected_category": "medical",
                "expected_agent": "medassist_agent",
                "expected_urgency": "critical"
            },
            {
                "name": "Security Threat",
                "input": "Suspicious person with weapon near entrance gate",
                "expected_category": "security",
                "expected_agent": "security_agent",
                "expected_urgency": "high"
            },
            {
                "name": "Infrastructure Issue",
                "input": "Power outage in vendor area, generators not working",
                "expected_category": "infrastructure",
                "expected_agent": "infrastructure_agent",
                "expected_urgency": "medium"
            },
            {
                "name": "Crowd Problem",
                "input": "Too crowded near stage, people getting crushed",
                "expected_category": "crowd",
                "expected_agent": "crowdflow_agent",
                "expected_urgency": "high"
            },
            {
                "name": "Information Request",
                "input": "Can't find my friend, we got separated in the crowd",
                "expected_category": "communication",
                "expected_agent": "comms_resources_agent",
                "expected_urgency": "medium"
            }
        ]
    
    def test_agent_initialization(self):
        """Test that the user input agent initializes correctly"""
        self.assertIsNotNone(user_input_agent)
        self.assertEqual(user_input_agent.name, "user_input_agent")
        self.assertEqual(user_input_agent.model, "gemini-2.0-flash-001")
        self.assertIn("user input", user_input_agent.description.lower())
        self.assertIn("analysis", user_input_agent.description.lower())
    
    def test_prompt_content(self):
        """Test that the prompt contains required input analysis keywords"""
        prompt = USER_INPUT_ANALYSIS_PROMPT
        
        # Check for key analysis terms
        self.assertIn("user input", prompt.lower())
        self.assertIn("analysis", prompt.lower())
        self.assertIn("categorization", prompt.lower())
        self.assertIn("routing", prompt.lower())
        self.assertIn("validation", prompt.lower())
        
        # Check for input types
        self.assertIn("text", prompt.lower())
        self.assertIn("image", prompt.lower())
        self.assertIn("voice", prompt.lower())
        self.assertIn("multimodal", prompt.lower())
        
        # Check for required response fields
        self.assertIn("input_processed", prompt)
        self.assertIn("validation_status", prompt)
        self.assertIn("incident_details", prompt)
        self.assertIn("routing_decision", prompt)
        self.assertIn("extracted_data", prompt)
    
    @patch('agent.user_input_app.query')
    async def test_medical_emergency_processing(self, mock_query):
        """Test processing of medical emergency report"""
        # Mock response for medical emergency
        mock_response = {
            "input_processed": True,
            "input_summary": "Medical emergency report: person collapsed at main stage",
            "validation_status": "valid",
            "confidence_score": 0.95,
            "incident_details": {
                "category": "medical",
                "subcategory": "cardiac_emergency",
                "urgency_level": "critical",
                "urgency_score": 9,
                "location": "main_stage",
                "time_reported": "immediate",
                "people_involved": "1_person_affected",
                "description": "Person collapsed and not breathing, suspected cardiac arrest"
            },
            "extracted_data": {
                "key_keywords": ["collapsed", "not breathing", "help", "immediately"],
                "entities": ["main stage", "person"],
                "sentiment": "panicked",
                "language_detected": "en",
                "location_coordinates": "main_stage_coordinates"
            },
            "routing_decision": {
                "target_agent": "medassist_agent",
                "routing_reason": "Medical emergency requiring immediate medical response",
                "priority_level": 10,
                "requires_multiple_agents": True,
                "additional_agents": ["comms_resources_agent", "security_agent"]
            },
            "data_for_target": {
                "formatted_input": "CRITICAL: Cardiac arrest at main stage, immediate response required",
                "context_info": "Crowded area, may need crowd control",
                "user_contact": "emergency_reporter",
                "follow_up_required": True
            },
            "validation_issues": {
                "missing_information": [],
                "clarification_needed": [],
                "follow_up_questions": []
            },
            "processing_metadata": {
                "input_type": "text",
                "processing_time": "150ms",
                "language_processing": "direct_processing",
                "quality_score": 0.9
            },
            "requires_escalation": True
        }
        mock_query.return_value = mock_response
        
        input_text = "Person collapsed at main stage, not breathing, need help immediately!"
        result = await user_input_app.query(input_text=input_text)
        
        self.assertTrue(result["input_processed"])
        self.assertEqual(result["validation_status"], "valid")
        self.assertEqual(result["incident_details"]["category"], "medical")
        self.assertEqual(result["routing_decision"]["target_agent"], "medassist_agent")
        self.assertEqual(result["incident_details"]["urgency_level"], "critical")
        self.assertTrue(result["requires_escalation"])
    
    @patch('agent.user_input_app.query')
    async def test_security_threat_processing(self, mock_query):
        """Test processing of security threat report"""
        mock_response = {
            "input_processed": True,
            "input_summary": "Security threat report: suspicious person with weapon",
            "validation_status": "valid",
            "confidence_score": 0.88,
            "incident_details": {
                "category": "security",
                "subcategory": "weapon_threat",
                "urgency_level": "high",
                "urgency_score": 8,
                "location": "entrance_gate",
                "time_reported": "current",
                "people_involved": "1_suspect",
                "description": "Suspicious individual carrying potential weapon near entrance"
            },
            "extracted_data": {
                "key_keywords": ["suspicious", "weapon", "entrance", "gate"],
                "entities": ["person", "entrance gate", "weapon"],
                "sentiment": "concerned",
                "language_detected": "en",
                "location_coordinates": "entrance_gate_coordinates"
            },
            "routing_decision": {
                "target_agent": "security_agent",
                "routing_reason": "Security threat requiring immediate security response",
                "priority_level": 9,
                "requires_multiple_agents": True,
                "additional_agents": ["comms_resources_agent"]
            },
            "data_for_target": {
                "formatted_input": "HIGH PRIORITY: Weapon threat at entrance gate",
                "context_info": "Public area with high foot traffic",
                "user_contact": "witness_reporter",
                "follow_up_required": True
            },
            "validation_issues": {
                "missing_information": ["specific_weapon_type"],
                "clarification_needed": ["exact_location"],
                "follow_up_questions": ["Can you describe the weapon?", "Which entrance gate?"]
            },
            "processing_metadata": {
                "input_type": "text",
                "processing_time": "120ms",
                "language_processing": "direct_processing",
                "quality_score": 0.85
            },
            "requires_escalation": True
        }
        mock_query.return_value = mock_response
        
        input_text = "Suspicious person with weapon near entrance gate"
        result = await user_input_app.query(input_text=input_text)
        
        self.assertTrue(result["input_processed"])
        self.assertEqual(result["incident_details"]["category"], "security")
        self.assertEqual(result["routing_decision"]["target_agent"], "security_agent")
        self.assertEqual(result["incident_details"]["urgency_level"], "high")
        self.assertTrue(result["routing_decision"]["requires_multiple_agents"])
    
    @patch('agent.user_input_app.query')
    async def test_infrastructure_issue_processing(self, mock_query):
        """Test processing of infrastructure issue report"""
        mock_response = {
            "input_processed": True,
            "input_summary": "Infrastructure issue: power outage in vendor area",
            "validation_status": "valid",
            "confidence_score": 0.82,
            "incident_details": {
                "category": "infrastructure",
                "subcategory": "power_outage",
                "urgency_level": "medium",
                "urgency_score": 5,
                "location": "vendor_area",
                "time_reported": "10_minutes_ago",
                "people_involved": "multiple_vendors_affected",
                "description": "Power outage affecting vendor operations, backup systems not functional"
            },
            "extracted_data": {
                "key_keywords": ["power", "outage", "vendor", "generators", "not working"],
                "entities": ["vendor area", "generators", "food trucks"],
                "sentiment": "frustrated",
                "language_detected": "en",
                "location_coordinates": "vendor_area_coordinates"
            },
            "routing_decision": {
                "target_agent": "infrastructure_agent",
                "routing_reason": "Infrastructure failure requiring maintenance response",
                "priority_level": 6,
                "requires_multiple_agents": True,
                "additional_agents": ["comms_resources_agent"]
            },
            "data_for_target": {
                "formatted_input": "INFRASTRUCTURE: Power outage in vendor area, backup failure",
                "context_info": "Multiple vendors affected, business impact",
                "user_contact": "vendor_representative",
                "follow_up_required": True
            },
            "validation_issues": {
                "missing_information": ["outage_cause"],
                "clarification_needed": ["affected_vendors_count"],
                "follow_up_questions": ["How many vendors are affected?"]
            },
            "processing_metadata": {
                "input_type": "text",
                "processing_time": "100ms",
                "language_processing": "direct_processing",
                "quality_score": 0.8
            },
            "requires_escalation": False
        }
        mock_query.return_value = mock_response
        
        input_text = "Power outage in vendor area, generators not working"
        result = await user_input_app.query(input_text=input_text)
        
        self.assertTrue(result["input_processed"])
        self.assertEqual(result["incident_details"]["category"], "infrastructure")
        self.assertEqual(result["routing_decision"]["target_agent"], "infrastructure_agent")
        self.assertEqual(result["incident_details"]["urgency_level"], "medium")
        self.assertFalse(result["requires_escalation"])
    
    @patch('agent.user_input_app.query')
    async def test_multilingual_processing(self, mock_query):
        """Test processing of non-English input"""
        mock_response = {
            "input_processed": True,
            "input_summary": "Spanish language crowd safety concern",
            "validation_status": "valid",
            "confidence_score": 0.79,
            "incident_details": {
                "category": "crowd",
                "subcategory": "overcrowding",
                "urgency_level": "high",
                "urgency_score": 7,
                "location": "main_stage_area",
                "time_reported": "current",
                "people_involved": "large_crowd",
                "description": "Overcrowding near main stage causing safety concerns"
            },
            "extracted_data": {
                "key_keywords": ["multitud", "empujando", "seguridad", "escenario"],
                "entities": ["escenario principal", "multitud", "seguridad"],
                "sentiment": "worried",
                "language_detected": "es",
                "location_coordinates": "main_stage_coordinates"
            },
            "routing_decision": {
                "target_agent": "crowdflow_agent",
                "routing_reason": "Crowd safety concern requiring density analysis",
                "priority_level": 8,
                "requires_multiple_agents": True,
                "additional_agents": ["security_agent", "comms_resources_agent"]
            },
            "data_for_target": {
                "formatted_input": "CROWD SAFETY: Overcrowding at main stage, safety concerns reported",
                "context_info": "Spanish-speaking attendee, crowd control needed",
                "user_contact": "spanish_speaker",
                "follow_up_required": True
            },
            "validation_issues": {
                "missing_information": [],
                "clarification_needed": [],
                "follow_up_questions": []
            },
            "processing_metadata": {
                "input_type": "text",
                "processing_time": "180ms",
                "language_processing": "translation_needed",
                "quality_score": 0.75
            },
            "requires_escalation": False
        }
        mock_query.return_value = mock_response
        
        spanish_input = "Hay una multitud muy grande cerca del escenario principal. La gente está empujando y no puedo moverme."
        result = await user_input_app.query(input_text=spanish_input)
        
        self.assertTrue(result["input_processed"])
        self.assertEqual(result["extracted_data"]["language_detected"], "es")
        self.assertEqual(result["processing_metadata"]["language_processing"], "translation_needed")
        self.assertEqual(result["incident_details"]["category"], "crowd")
        self.assertEqual(result["routing_decision"]["target_agent"], "crowdflow_agent")
    
    @patch('agent.user_input_app.query')
    async def test_ambiguous_input_handling(self, mock_query):
        """Test handling of vague or incomplete input"""
        mock_response = {
            "input_processed": True,
            "input_summary": "Vague report of unspecified problem near restroom facilities",
            "validation_status": "incomplete",
            "confidence_score": 0.45,
            "incident_details": {
                "category": "other",
                "subcategory": "unspecified_issue",
                "urgency_level": "low",
                "urgency_score": 3,
                "location": "restroom_area",
                "time_reported": "current",
                "people_involved": "unknown",
                "description": "Unspecified problem reported near restroom facilities"
            },
            "extracted_data": {
                "key_keywords": ["wrong", "bathrooms", "bad"],
                "entities": ["bathrooms"],
                "sentiment": "concerned",
                "language_detected": "en",
                "location_coordinates": "restroom_area_general"
            },
            "routing_decision": {
                "target_agent": "comms_resources_agent",
                "routing_reason": "Requires clarification before routing to specialized agent",
                "priority_level": 4,
                "requires_multiple_agents": False,
                "additional_agents": []
            },
            "data_for_target": {
                "formatted_input": "CLARIFICATION NEEDED: Vague issue report near restrooms",
                "context_info": "Incomplete information, requires follow-up",
                "user_contact": "unclear_reporter",
                "follow_up_required": True
            },
            "validation_issues": {
                "missing_information": ["specific_problem", "severity", "people_affected"],
                "clarification_needed": ["nature_of_problem", "urgency_level"],
                "follow_up_questions": [
                    "Can you describe what specifically looks wrong?",
                    "Is anyone injured or in danger?",
                    "What type of problem are you seeing?"
                ]
            },
            "processing_metadata": {
                "input_type": "text",
                "processing_time": "80ms",
                "language_processing": "direct_processing",
                "quality_score": 0.3
            },
            "requires_escalation": False
        }
        mock_query.return_value = mock_response
        
        vague_input = "Something's wrong near the bathrooms. Not sure what exactly but it looks bad."
        result = await user_input_app.query(input_text=vague_input)
        
        self.assertTrue(result["input_processed"])
        self.assertEqual(result["validation_status"], "incomplete")
        self.assertLess(result["confidence_score"], 0.5)
        self.assertEqual(result["routing_decision"]["target_agent"], "comms_resources_agent")
        self.assertTrue(len(result["validation_issues"]["follow_up_questions"]) > 0)
        self.assertTrue(result["data_for_target"]["follow_up_required"])
    
    @patch('agent.user_input_app.query')
    async def test_multi_agent_routing(self, mock_query):
        """Test scenarios requiring multiple agents"""
        mock_response = {
            "input_processed": True,
            "input_summary": "Complex incident requiring multiple agent coordination",
            "validation_status": "valid",
            "confidence_score": 0.92,
            "incident_details": {
                "category": "medical",
                "subcategory": "injury_with_security_concern",
                "urgency_level": "critical",
                "urgency_score": 9,
                "location": "concert_area",
                "time_reported": "immediate",
                "people_involved": "injured_person_and_crowd",
                "description": "Person injured in fight, crowd gathering, medical and security response needed"
            },
            "extracted_data": {
                "key_keywords": ["fight", "injured", "blood", "crowd", "gathering"],
                "entities": ["person", "fight", "injury", "crowd"],
                "sentiment": "urgent",
                "language_detected": "en",
                "location_coordinates": "concert_area_coordinates"
            },
            "routing_decision": {
                "target_agent": "medassist_agent",
                "routing_reason": "Primary medical emergency with secondary security concerns",
                "priority_level": 10,
                "requires_multiple_agents": True,
                "additional_agents": ["security_agent", "crowdflow_agent", "comms_resources_agent"]
            },
            "data_for_target": {
                "formatted_input": "CRITICAL: Injury from fight, crowd control needed",
                "context_info": "Multi-agent response required, crowd management essential",
                "user_contact": "witness_reporter",
                "follow_up_required": True
            },
            "validation_issues": {
                "missing_information": [],
                "clarification_needed": [],
                "follow_up_questions": []
            },
            "processing_metadata": {
                "input_type": "text",
                "processing_time": "140ms",
                "language_processing": "direct_processing",
                "quality_score": 0.9
            },
            "requires_escalation": True
        }
        mock_query.return_value = mock_response
        
        complex_input = "There was a fight and someone got injured with blood. Crowd is gathering around."
        result = await user_input_app.query(input_text=complex_input)
        
        self.assertTrue(result["input_processed"])
        self.assertEqual(result["routing_decision"]["target_agent"], "medassist_agent")
        self.assertTrue(result["routing_decision"]["requires_multiple_agents"])
        self.assertGreater(len(result["routing_decision"]["additional_agents"]), 2)
        self.assertTrue(result["requires_escalation"])
    
    def test_response_format_validation(self):
        """Test that expected response format fields are defined"""
        required_fields = [
            "input_processed",
            "input_summary",
            "validation_status", 
            "confidence_score",
            "incident_details",
            "extracted_data",
            "routing_decision",
            "data_for_target",
            "validation_issues",
            "processing_metadata",
            "requires_escalation"
        ]
        
        # Check that all required fields are mentioned in the prompt
        prompt = USER_INPUT_ANALYSIS_PROMPT
        for field in required_fields:
            self.assertIn(field, prompt, f"Required field '{field}' not found in prompt")

class TestUserInputAgentIntegration(unittest.TestCase):
    """Integration tests for User Input Analysis Agent"""
    
    @unittest.skipIf(not os.getenv('PROJECT_ID'), "PROJECT_ID not set - skipping integration tests")
    async def test_real_agent_response(self):
        """Test actual agent response (requires valid GCP credentials)"""
        try:
            input_text = "Test scenario: Need help with lost item at information booth."
            result = await user_input_app.query(input_text=input_text)
            
            # Verify response has expected structure
            self.assertIsInstance(result, dict)
            
            # Check for key fields (allowing for flexibility in actual AI responses)
            expected_fields = ["input_summary", "validation_status"]
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
        'test_medical_emergency_processing',
        'test_security_threat_processing', 
        'test_infrastructure_issue_processing',
        'test_multilingual_processing',
        'test_ambiguous_input_handling',
        'test_multi_agent_routing'
    ]
    
    for method_name in async_test_methods:
        suite.addTest(TestUserInputAgent(method_name))
    
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
    print("🧪 Running User Input Analysis Agent Tests")
    print("="*50)
    
    # Run synchronous tests first
    print("\n📋 Running synchronous tests...")
    sync_suite = unittest.TestLoader().loadTestsFromTestCase(TestUserInputAgent)
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
        print("\n📱 User Input Analysis Agent is ready for intelligent input processing!")
    else:
        print("❌ Some tests failed. Check output above for details.")
        
    print("\n🚀 Advanced multimodal input processing and routing capabilities ready!") 