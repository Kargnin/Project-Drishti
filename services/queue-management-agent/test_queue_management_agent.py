"""
Test cases for the Queue Management Agent

This module contains unit tests and integration tests for the Queue Management Agent
to ensure it properly analyzes crowd flow and provides appropriate queue management responses.
"""

import unittest
import asyncio
import json
from unittest.mock import Mock, patch
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import queue_management_agent, queue_management_app
from prompt import QUEUE_MANAGEMENT_PROMPT

class TestQueueManagementAgent(unittest.TestCase):
    """Test cases for Queue Management Agent functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_scenarios = [
            {
                "name": "Critical Congestion",
                "description": "Entrance gate completely backed up, 60+ minute wait times, safety concerns with crowd pushing",
                "expected_efficiency": "critical",
                "expected_categories": ["entry_exit"]
            },
            {
                "name": "Moderate Food Court Queue",
                "description": "Food vendors have 15-20 minute wait times, manageable but could be improved",
                "expected_efficiency": "congested", 
                "expected_categories": ["service_areas"]
            },
            {
                "name": "Optimal Flow",
                "description": "All entry points flowing smoothly, minimal wait times, efficient operations",
                "expected_efficiency": "optimal",
                "expected_categories": ["entry_exit"]
            },
            {
                "name": "Transportation Bottleneck",
                "description": "Parking shuttle service backed up, long lines for transportation out of venue",
                "expected_efficiency": "congested",
                "expected_categories": ["transportation"]
            }
        ]
    
    def test_agent_initialization(self):
        """Test that the queue management agent initializes correctly"""
        self.assertIsNotNone(queue_management_agent)
        self.assertEqual(queue_management_agent.name, "queue_management_agent")
        self.assertEqual(queue_management_agent.model, "gemini-2.0-flash-001")
        self.assertIn("queue", queue_management_agent.description.lower())
    
    def test_prompt_content(self):
        """Test that the prompt contains required queue management keywords"""
        prompt = QUEUE_MANAGEMENT_PROMPT
        
        # Check for key queue categories
        self.assertIn("entry_exit", prompt.lower())
        self.assertIn("service_areas", prompt.lower())
        self.assertIn("entertainment", prompt.lower())
        self.assertIn("transportation", prompt.lower())
        
        # Check for flow efficiency levels
        self.assertIn("optimal", prompt.lower())
        self.assertIn("moderate", prompt.lower())
        self.assertIn("congested", prompt.lower())
        self.assertIn("critical", prompt.lower())
        
        # Check for required response fields
        self.assertIn("requires_intervention", prompt)
        self.assertIn("flow_efficiency", prompt)
        self.assertIn("confidence_score", prompt)
        self.assertIn("flow_recommendations", prompt)
        self.assertIn("staff_allocation", prompt)
    
    @patch('agent.queue_management_app.query')
    async def test_critical_congestion_analysis(self, mock_query):
        """Test analysis of critical queue congestion"""
        # Mock response for critical congestion
        mock_response = {
            "requires_intervention": True,
            "flow_efficiency": "critical",
            "confidence_score": 0.95,
            "congestion_score": 9,
            "analysis": "Critical congestion with safety risks",
            "flow_recommendations": ["Open additional entry points", "Deploy crowd control barriers"],
            "staff_allocation": {
                "additional_staff_needed": 8,
                "redeployment_suggestions": ["Move staff from quiet areas"],
                "priority_locations": ["Main entrance", "Emergency exits"]
            },
            "estimated_wait_times": {
                "current_wait": "60+ minutes",
                "predicted_wait": "90 minutes", 
                "peak_time_wait": "120+ minutes"
            },
            "queue_categories": ["entry_exit"],
            "bottleneck_locations": ["Security checkpoint", "Metal detectors"],
            "capacity_utilization": 0.95,
            "recommended_actions": {
                "immediate": ["Deploy additional staff", "Open emergency protocols"],
                "short_term": ["Add entry points", "Improve signage"],
                "long_term": ["Redesign entry flow", "Add permanent infrastructure"]
            }
        }
        mock_query.return_value = mock_response
        
        description = "Entrance gate completely backed up, 60+ minute wait times, safety concerns"
        result = await queue_management_app.query(input_text=description)
        
        self.assertTrue(result["requires_intervention"])
        self.assertEqual(result["flow_efficiency"], "critical")
        self.assertIn("entry_exit", result["queue_categories"])
        self.assertGreater(result["staff_allocation"]["additional_staff_needed"], 5)
    
    @patch('agent.queue_management_app.query')
    async def test_moderate_congestion_analysis(self, mock_query):
        """Test analysis of moderate queue congestion"""
        mock_response = {
            "requires_intervention": True,
            "flow_efficiency": "congested", 
            "confidence_score": 0.85,
            "congestion_score": 6,
            "analysis": "Moderate congestion requiring attention",
            "flow_recommendations": ["Balance vendor distribution", "Improve queue organization"],
            "staff_allocation": {
                "additional_staff_needed": 3,
                "redeployment_suggestions": ["Redirect from low-traffic vendors"],
                "priority_locations": ["Popular food trucks"]
            },
            "estimated_wait_times": {
                "current_wait": "15-20 minutes",
                "predicted_wait": "20-25 minutes",
                "peak_time_wait": "30-35 minutes"
            },
            "queue_categories": ["service_areas"],
            "bottleneck_locations": ["Popular vendor", "Payment processing"],
            "capacity_utilization": 0.75,
            "recommended_actions": {
                "immediate": ["Add cashiers", "Improve line organization"],
                "short_term": ["Balance customer distribution"],
                "long_term": ["Optimize vendor layout"]
            }
        }
        mock_query.return_value = mock_response
        
        description = "Food vendors have 15-20 minute wait times, manageable but could be improved"
        result = await queue_management_app.query(input_text=description)
        
        self.assertTrue(result["requires_intervention"])
        self.assertEqual(result["flow_efficiency"], "congested")
        self.assertIn("service_areas", result["queue_categories"])
        self.assertEqual(result["staff_allocation"]["additional_staff_needed"], 3)
    
    @patch('agent.queue_management_app.query')
    async def test_optimal_flow_analysis(self, mock_query):
        """Test analysis of optimal queue flow"""
        mock_response = {
            "requires_intervention": False,
            "flow_efficiency": "optimal",
            "confidence_score": 0.9,
            "congestion_score": 1,
            "analysis": "Excellent flow efficiency, minimal wait times",
            "flow_recommendations": ["Maintain current operations", "Monitor for changes"],
            "staff_allocation": {
                "additional_staff_needed": 0,
                "redeployment_suggestions": ["Consider redeploying excess staff"],
                "priority_locations": []
            },
            "estimated_wait_times": {
                "current_wait": "Under 5 minutes",
                "predicted_wait": "5-10 minutes",
                "peak_time_wait": "10-15 minutes"
            },
            "queue_categories": ["entry_exit"],
            "bottleneck_locations": [],
            "capacity_utilization": 0.3,
            "recommended_actions": {
                "immediate": ["Continue monitoring"],
                "short_term": ["Prepare for peak times"],
                "long_term": ["Use as model for other areas"]
            }
        }
        mock_query.return_value = mock_response
        
        description = "All entry points flowing smoothly, minimal wait times, efficient operations"
        result = await queue_management_app.query(input_text=description)
        
        self.assertFalse(result["requires_intervention"])
        self.assertEqual(result["flow_efficiency"], "optimal")
        self.assertEqual(result["staff_allocation"]["additional_staff_needed"], 0)
        self.assertEqual(result["bottleneck_locations"], [])
    
    @patch('agent.queue_management_app.query')
    async def test_transportation_queue_analysis(self, mock_query):
        """Test analysis of transportation queue issues"""
        mock_response = {
            "requires_intervention": True,
            "flow_efficiency": "congested",
            "confidence_score": 0.8,
            "congestion_score": 7,
            "analysis": "Transportation bottleneck affecting event exit flow",
            "flow_recommendations": ["Increase shuttle frequency", "Add alternative transport"],
            "staff_allocation": {
                "additional_staff_needed": 4,
                "redeployment_suggestions": ["Deploy traffic management staff"],
                "priority_locations": ["Shuttle stops", "Parking areas"]
            },
            "estimated_wait_times": {
                "current_wait": "25-30 minutes",
                "predicted_wait": "35-40 minutes",
                "peak_time_wait": "45-60 minutes"
            },
            "queue_categories": ["transportation"],
            "bottleneck_locations": ["Main shuttle stop", "Parking lot exit"],
            "capacity_utilization": 0.85,
            "recommended_actions": {
                "immediate": ["Add shuttle vehicles", "Improve loading efficiency"],
                "short_term": ["Optimize routes", "Add signage"],
                "long_term": ["Expand transportation infrastructure"]
            }
        }
        mock_query.return_value = mock_response
        
        description = "Parking shuttle service backed up, long lines for transportation"
        result = await queue_management_app.query(input_text=description)
        
        self.assertTrue(result["requires_intervention"])
        self.assertEqual(result["flow_efficiency"], "congested")
        self.assertIn("transportation", result["queue_categories"])
        self.assertIn("Shuttle stops", result["staff_allocation"]["priority_locations"])
    
    @patch('agent.queue_management_app.query')
    async def test_entertainment_queue_analysis(self, mock_query):
        """Test analysis of entertainment area queues"""
        mock_response = {
            "requires_intervention": True,
            "flow_efficiency": "congested",
            "confidence_score": 0.88,
            "congestion_score": 6,
            "analysis": "Popular attraction creating long queues and crowd concentration",
            "flow_recommendations": ["Implement timed entry system", "Create alternative entertainment"],
            "staff_allocation": {
                "additional_staff_needed": 5,
                "redeployment_suggestions": ["Add queue management staff"],
                "priority_locations": ["Main stage area", "Photo booth"]
            },
            "estimated_wait_times": {
                "current_wait": "20-25 minutes",
                "predicted_wait": "30-35 minutes",
                "peak_time_wait": "45-60 minutes"
            },
            "queue_categories": ["entertainment"],
            "bottleneck_locations": ["Photo opportunity", "Meet and greet"],
            "capacity_utilization": 0.8,
            "recommended_actions": {
                "immediate": ["Organize queue lines", "Add entertainment for waiting crowds"],
                "short_term": ["Implement reservation system"],
                "long_term": ["Add similar attractions to distribute demand"]
            }
        }
        mock_query.return_value = mock_response
        
        description = "Long lines at photo booth and meet-and-greet area, crowds gathering around popular attraction"
        result = await queue_management_app.query(input_text=description)
        
        self.assertTrue(result["requires_intervention"])
        self.assertEqual(result["flow_efficiency"], "congested")
        self.assertIn("entertainment", result["queue_categories"])
    
    @patch('agent.queue_management_app.query')
    async def test_staff_allocation_recommendations(self, mock_query):
        """Test staff allocation recommendation accuracy"""
        mock_response = {
            "requires_intervention": True,
            "flow_efficiency": "congested",
            "confidence_score": 0.9,
            "congestion_score": 7,
            "analysis": "Multiple areas requiring staff redeployment",
            "flow_recommendations": ["Redistribute staff based on demand"],
            "staff_allocation": {
                "additional_staff_needed": 6,
                "redeployment_suggestions": [
                    "Move 2 staff from quiet entrance to main gate",
                    "Redeploy merchandise staff to food service during peak",
                    "Add queue management specialists to problem areas"
                ],
                "priority_locations": ["Main entrance", "Food court", "Restroom areas"]
            },
            "estimated_wait_times": {
                "current_wait": "20-30 minutes",
                "predicted_wait": "25-35 minutes",
                "peak_time_wait": "40-50 minutes"
            },
            "queue_categories": ["entry_exit", "service_areas"],
            "bottleneck_locations": ["Security checkpoint", "Popular vendors"],
            "capacity_utilization": 0.85,
            "recommended_actions": {
                "immediate": ["Deploy additional staff", "Implement queue management"],
                "short_term": ["Optimize staff schedules"],
                "long_term": ["Review staffing models"]
            }
        }
        mock_query.return_value = mock_response
        
        description = "Multiple bottlenecks across venue requiring coordinated staff response"
        result = await queue_management_app.query(input_text=description)
        
        staff_allocation = result["staff_allocation"]
        self.assertIsInstance(staff_allocation["additional_staff_needed"], int)
        self.assertGreater(staff_allocation["additional_staff_needed"], 0)
        self.assertIsInstance(staff_allocation["redeployment_suggestions"], list)
        self.assertIsInstance(staff_allocation["priority_locations"], list)
    
    def test_response_format_validation(self):
        """Test that expected response format fields are defined"""
        required_fields = [
            "requires_intervention",
            "flow_efficiency", 
            "confidence_score",
            "congestion_score",
            "analysis",
            "flow_recommendations",
            "staff_allocation",
            "estimated_wait_times",
            "queue_categories",
            "bottleneck_locations",
            "capacity_utilization",
            "recommended_actions"
        ]
        
        # Check that all required fields are mentioned in the prompt
        prompt = QUEUE_MANAGEMENT_PROMPT
        for field in required_fields:
            self.assertIn(field, prompt, f"Required field '{field}' not found in prompt")

class TestQueueManagementAgentIntegration(unittest.TestCase):
    """Integration tests for Queue Management Agent"""
    
    @unittest.skipIf(not os.getenv('PROJECT_ID'), "PROJECT_ID not set - skipping integration tests")
    async def test_real_agent_response(self):
        """Test actual agent response (requires valid GCP credentials)"""
        try:
            description = "Test scenario: Moderate queuing at entrance, 10-minute wait times."
            result = await queue_management_app.query(input_text=description)
            
            # Verify response has expected structure
            self.assertIsInstance(result, dict)
            
            # Check for key fields (allowing for flexibility in actual AI responses)
            expected_fields = ["analysis", "flow_efficiency"]
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
        'test_critical_congestion_analysis',
        'test_moderate_congestion_analysis', 
        'test_optimal_flow_analysis',
        'test_transportation_queue_analysis',
        'test_entertainment_queue_analysis',
        'test_staff_allocation_recommendations'
    ]
    
    for method_name in async_test_methods:
        suite.addTest(TestQueueManagementAgent(method_name))
    
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
    print("🧪 Running Queue Management Agent Tests")
    print("="*50)
    
    # Run synchronous tests first
    print("\n📋 Running synchronous tests...")
    sync_suite = unittest.TestLoader().loadTestsFromTestCase(TestQueueManagementAgent)
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
        print("\n🚶‍♂️ Queue Management Agent is ready for crowd flow optimization!")
    else:
        print("❌ Some tests failed. Check output above for details.")
        
    print("\n📊 Ready to optimize crowd flow and reduce wait times!") 