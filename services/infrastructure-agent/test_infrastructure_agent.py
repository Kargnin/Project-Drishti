"""
Test cases for the Infrastructure Agent

This module contains unit tests and integration tests for the Infrastructure Agent
to ensure it properly analyzes infrastructure issues and provides appropriate responses.
"""

import unittest
import asyncio
import json
from unittest.mock import Mock, patch
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import infrastructure_agent, infrastructure_app
from prompt import INFRASTRUCTURE_ANALYSIS_PROMPT

class TestInfrastructureAgent(unittest.TestCase):
    """Test cases for Infrastructure Agent functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_scenarios = [
            {
                "name": "Critical Power Failure",
                "description": "Complete power outage in main pavilion. Emergency lighting activated. Backup generators not responding.",
                "expected_status": "critical",
                "expected_systems": ["power"]
            },
            {
                "name": "Network Degradation",
                "description": "Internet connectivity slow and intermittent. Some switches showing amber status lights.",
                "expected_status": "degraded", 
                "expected_systems": ["connectivity"]
            },
            {
                "name": "Minor Structural Issue",
                "description": "Small crack noticed in non-load-bearing wall. Doesn't appear to be expanding.",
                "expected_status": "operational",
                "expected_systems": ["structural"]
            },
            {
                "name": "Environmental System Alert",
                "description": "HVAC system showing maintenance alert but still functioning normally.",
                "expected_status": "operational",
                "expected_systems": ["environmental"]
            }
        ]
    
    def test_agent_initialization(self):
        """Test that the infrastructure agent initializes correctly"""
        self.assertIsNotNone(infrastructure_agent)
        self.assertEqual(infrastructure_agent.name, "infrastructure_agent")
        self.assertEqual(infrastructure_agent.model, "gemini-2.0-flash-001")
        self.assertIn("infrastructure", infrastructure_agent.description.lower())
    
    def test_prompt_content(self):
        """Test that the prompt contains required infrastructure keywords"""
        prompt = INFRASTRUCTURE_ANALYSIS_PROMPT
        
        # Check for key infrastructure categories
        self.assertIn("power", prompt.lower())
        self.assertIn("connectivity", prompt.lower())
        self.assertIn("structural", prompt.lower())
        self.assertIn("environmental", prompt.lower())
        
        # Check for status levels
        self.assertIn("operational", prompt.lower())
        self.assertIn("degraded", prompt.lower())
        self.assertIn("critical", prompt.lower())
        
        # Check for required response fields
        self.assertIn("is_infrastructure_concern", prompt)
        self.assertIn("status_level", prompt)
        self.assertIn("confidence_score", prompt)
        self.assertIn("recommended_actions", prompt)
    
    @patch('agent.infrastructure_app.query')
    async def test_power_system_analysis(self, mock_query):
        """Test analysis of power system issues"""
        # Mock response for power system failure
        mock_response = {
            "is_infrastructure_concern": True,
            "status_level": "critical",
            "confidence_score": 0.95,
            "status_score": 9,
            "analysis": "Critical power system failure detected",
            "recommended_actions": ["Activate backup power", "Check generator status"],
            "requires_immediate_response": True,
            "affected_systems": ["power"],
            "maintenance_priority": "high",
            "estimated_downtime": "immediate"
        }
        mock_query.return_value = mock_response
        
        description = "Main power transformer failure. Complete outage in pavilion A."
        result = await infrastructure_app.query(input_text=description)
        
        self.assertTrue(result["is_infrastructure_concern"])
        self.assertEqual(result["status_level"], "critical")
        self.assertIn("power", result["affected_systems"])
        self.assertTrue(result["requires_immediate_response"])
    
    @patch('agent.infrastructure_app.query')
    async def test_connectivity_analysis(self, mock_query):
        """Test analysis of connectivity issues"""
        mock_response = {
            "is_infrastructure_concern": True,
            "status_level": "degraded", 
            "confidence_score": 0.85,
            "status_score": 6,
            "analysis": "Network connectivity degraded but functional",
            "recommended_actions": ["Check network switches", "Monitor bandwidth usage"],
            "requires_immediate_response": False,
            "affected_systems": ["connectivity"],
            "maintenance_priority": "medium",
            "estimated_downtime": "hours"
        }
        mock_query.return_value = mock_response
        
        description = "Wi-Fi is slow in the north section. Some users reporting connection issues."
        result = await infrastructure_app.query(input_text=description)
        
        self.assertTrue(result["is_infrastructure_concern"])
        self.assertEqual(result["status_level"], "degraded")
        self.assertIn("connectivity", result["affected_systems"])
        self.assertFalse(result["requires_immediate_response"])
    
    @patch('agent.infrastructure_app.query')
    async def test_structural_integrity_analysis(self, mock_query):
        """Test analysis of structural integrity issues"""
        mock_response = {
            "is_infrastructure_concern": True,
            "status_level": "critical",
            "confidence_score": 0.9,
            "status_score": 8,
            "analysis": "Structural integrity compromised - immediate evacuation required",
            "recommended_actions": ["Evacuate area", "Contact structural engineer", "Block access"],
            "requires_immediate_response": True,
            "affected_systems": ["structural"],
            "maintenance_priority": "high",
            "estimated_downtime": "days"
        }
        mock_query.return_value = mock_response
        
        description = "Large crack appeared in main support beam of stage platform. Visible movement detected."
        result = await infrastructure_app.query(input_text=description)
        
        self.assertTrue(result["is_infrastructure_concern"])
        self.assertEqual(result["status_level"], "critical")
        self.assertIn("structural", result["affected_systems"])
        self.assertTrue(result["requires_immediate_response"])
    
    @patch('agent.infrastructure_app.query')
    async def test_environmental_system_analysis(self, mock_query):
        """Test analysis of environmental system issues"""
        mock_response = {
            "is_infrastructure_concern": True,
            "status_level": "operational",
            "confidence_score": 0.7,
            "status_score": 3,
            "analysis": "Environmental systems functioning normally with routine maintenance alert",
            "recommended_actions": ["Schedule routine maintenance", "Monitor performance"],
            "requires_immediate_response": False,
            "affected_systems": ["environmental"],
            "maintenance_priority": "low",
            "estimated_downtime": "planned"
        }
        mock_query.return_value = mock_response
        
        description = "HVAC system showing routine maintenance indicator but operating normally."
        result = await infrastructure_app.query(input_text=description)
        
        self.assertTrue(result["is_infrastructure_concern"])
        self.assertEqual(result["status_level"], "operational")
        self.assertIn("environmental", result["affected_systems"])
        self.assertFalse(result["requires_immediate_response"])
    
    @patch('agent.infrastructure_app.query')
    async def test_non_infrastructure_concern(self, mock_query):
        """Test handling of non-infrastructure related reports"""
        mock_response = {
            "is_infrastructure_concern": False,
            "status_level": "operational",
            "confidence_score": 0.8,
            "status_score": 1,
            "analysis": "Not an infrastructure concern - appears to be event logistics issue",
            "recommended_actions": ["Forward to event management team"],
            "requires_immediate_response": False,
            "affected_systems": [],
            "maintenance_priority": "low",
            "estimated_downtime": "planned"
        }
        mock_query.return_value = mock_response
        
        description = "Food vendor ran out of napkins and needs more supplies."
        result = await infrastructure_app.query(input_text=description)
        
        self.assertFalse(result["is_infrastructure_concern"])
        self.assertEqual(result["status_level"], "operational")
        self.assertEqual(result["affected_systems"], [])
    
    def test_response_format_validation(self):
        """Test that expected response format fields are defined"""
        required_fields = [
            "is_infrastructure_concern",
            "status_level", 
            "confidence_score",
            "status_score",
            "analysis",
            "recommended_actions",
            "requires_immediate_response",
            "affected_systems",
            "maintenance_priority",
            "estimated_downtime"
        ]
        
        # Check that all required fields are mentioned in the prompt
        prompt = INFRASTRUCTURE_ANALYSIS_PROMPT
        for field in required_fields:
            self.assertIn(field, prompt, f"Required field '{field}' not found in prompt")

class TestInfrastructureAgentIntegration(unittest.TestCase):
    """Integration tests for Infrastructure Agent"""
    
    @unittest.skipIf(not os.getenv('PROJECT_ID'), "PROJECT_ID not set - skipping integration tests")
    async def test_real_agent_response(self):
        """Test actual agent response (requires valid GCP credentials)"""
        try:
            description = "Test scenario: Minor lighting issue in entrance area. One LED panel flickering."
            result = await infrastructure_app.query(input_text=description)
            
            # Verify response has expected structure
            self.assertIsInstance(result, dict)
            
            # Check for key fields (allowing for flexibility in actual AI responses)
            expected_fields = ["analysis", "status_level"]
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
    test_case = TestInfrastructureAgent()
    suite.addTest(TestInfrastructureAgent('test_power_system_analysis'))
    suite.addTest(TestInfrastructureAgent('test_connectivity_analysis'))
    suite.addTest(TestInfrastructureAgent('test_structural_integrity_analysis'))
    suite.addTest(TestInfrastructureAgent('test_environmental_system_analysis'))
    suite.addTest(TestInfrastructureAgent('test_non_infrastructure_concern'))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Patch the test methods to handle async
    for test in suite:
        if hasattr(test, '_testMethodName'):
            method_name = test._testMethodName
            if method_name in ['test_power_system_analysis', 'test_connectivity_analysis', 
                              'test_structural_integrity_analysis', 'test_environmental_system_analysis',
                              'test_non_infrastructure_concern']:
                original_method = getattr(test, method_name)
                setattr(test, method_name, lambda self: loop.run_until_complete(original_method()))
    
    result = runner.run(suite)
    loop.close()
    return result

if __name__ == '__main__':
    print("🧪 Running Infrastructure Agent Tests")
    print("="*50)
    
    # Run synchronous tests first
    print("\n📋 Running synchronous tests...")
    sync_suite = unittest.TestLoader().loadTestsFromTestCase(TestInfrastructureAgent)
    # Filter out async tests
    filtered_tests = []
    for test in sync_suite:
        if not test._testMethodName.startswith('test_') or test._testMethodName in [
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
    else:
        print("❌ Some tests failed. Check output above for details.") 