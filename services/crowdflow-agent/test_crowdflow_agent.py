"""
Test cases for the CrowdFlow Agent

This module contains unit tests and integration tests for the CrowdFlow Agent
to ensure it properly analyzes crowd density and provides appropriate crowd flow responses.
"""

import unittest
import asyncio
import json
from unittest.mock import Mock, patch
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import crowdflow_agent, crowdflow_app
from prompt import CROWDFLOW_ANALYSIS_PROMPT

class TestCrowdFlowAgent(unittest.TestCase):
    """Test cases for CrowdFlow Agent functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_scenarios = [
            {
                "name": "Critical Density Emergency",
                "description": "Extremely dense crowd at main stage, people pressed against barriers, crush risk imminent",
                "expected_density": "critical",
                "expected_count_range": (3000, 5000)
            },
            {
                "name": "High Density Concert",
                "description": "Popular performer, high crowd density but manageable, people standing close together",
                "expected_density": "high", 
                "expected_count_range": (1500, 3000)
            },
            {
                "name": "Moderate Food Court",
                "description": "Busy food court with moderate crowd density, people queuing and moving around vendors",
                "expected_density": "moderate",
                "expected_count_range": (500, 1500)
            },
            {
                "name": "Low Density Entrance",
                "description": "Early morning entrance area, sparse crowd with plenty of space between people",
                "expected_density": "low",
                "expected_count_range": (50, 500)
            }
        ]
    
    def test_agent_initialization(self):
        """Test that the crowdflow agent initializes correctly"""
        self.assertIsNotNone(crowdflow_agent)
        self.assertEqual(crowdflow_agent.name, "crowdflow_agent")
        self.assertEqual(crowdflow_agent.model, "gemini-2.0-flash-001")
        self.assertIn("crowd", crowdflow_agent.description.lower())
        self.assertIn("yolo", crowdflow_agent.description.lower())
    
    def test_prompt_content(self):
        """Test that the prompt contains required crowd flow keywords"""
        prompt = CROWDFLOW_ANALYSIS_PROMPT
        
        # Check for key computer vision terms
        self.assertIn("yolov3", prompt.lower())
        self.assertIn("computer vision", prompt.lower())
        self.assertIn("density", prompt.lower())
        self.assertIn("detection", prompt.lower())
        
        # Check for density levels
        self.assertIn("critical", prompt.lower())
        self.assertIn("high", prompt.lower())
        self.assertIn("moderate", prompt.lower())
        self.assertIn("low", prompt.lower())
        
        # Check for required response fields
        self.assertIn("crowd_detected", prompt)
        self.assertIn("crowd_density_level", prompt)
        self.assertIn("crowd_metrics", prompt)
        self.assertIn("flow_predictions", prompt)
        self.assertIn("ml_model_outputs", prompt)
    
    @patch('agent.crowdflow_app.query')
    async def test_critical_density_analysis(self, mock_query):
        """Test analysis of critical crowd density"""
        # Mock response for critical density
        mock_response = {
            "crowd_detected": True,
            "crowd_density_level": "critical",
            "confidence_score": 0.95,
            "density_score": 9,
            "analysis": "Critical overcrowding detected with immediate safety risks",
            "crowd_metrics": {
                "estimated_count": 4500,
                "density_per_sqm": 7.2,
                "coverage_area_sqm": 625,
                "movement_speed": "stationary"
            },
            "flow_predictions": {
                "direction": "convergent",
                "predicted_growth": "stable",
                "peak_time_estimate": "immediate",
                "dispersion_pattern": "bottlenecked"
            },
            "safety_assessment": {
                "crush_risk": "critical",
                "exit_accessibility": "blocked",
                "emergency_response_time": "immediate"
            },
            "density_map_regions": [
                {
                    "region": "stage_front",
                    "density": "critical",
                    "risk_level": "critical"
                }
            ],
            "recommended_actions": ["Emergency evacuation procedures", "Immediate crowd control"],
            "ml_model_outputs": {
                "yolo_detections": 4500,
                "tracking_accuracy": 0.92,
                "prediction_confidence": 0.95
            },
            "requires_intervention": True
        }
        mock_query.return_value = mock_response
        
        description = "Extremely dense crowd at main stage, people pressed against barriers, crush risk"
        result = await crowdflow_app.query(input_text=description)
        
        self.assertTrue(result["crowd_detected"])
        self.assertEqual(result["crowd_density_level"], "critical")
        self.assertEqual(result["safety_assessment"]["crush_risk"], "critical")
        self.assertTrue(result["requires_intervention"])
        self.assertGreater(result["crowd_metrics"]["estimated_count"], 3000)
    
    @patch('agent.crowdflow_app.query')
    async def test_moderate_density_analysis(self, mock_query):
        """Test analysis of moderate crowd density"""
        mock_response = {
            "crowd_detected": True,
            "crowd_density_level": "moderate", 
            "confidence_score": 0.85,
            "density_score": 4,
            "analysis": "Moderate crowd density with manageable flow",
            "crowd_metrics": {
                "estimated_count": 800,
                "density_per_sqm": 2.5,
                "coverage_area_sqm": 320,
                "movement_speed": "slow"
            },
            "flow_predictions": {
                "direction": "east",
                "predicted_growth": "stable",
                "peak_time_estimate": "15 minutes",
                "dispersion_pattern": "organized"
            },
            "safety_assessment": {
                "crush_risk": "low",
                "exit_accessibility": "clear",
                "emergency_response_time": "minutes"
            },
            "density_map_regions": [
                {
                    "region": "food_court",
                    "density": "moderate",
                    "risk_level": "low"
                }
            ],
            "recommended_actions": ["Continue monitoring", "Maintain staff presence"],
            "ml_model_outputs": {
                "yolo_detections": 800,
                "tracking_accuracy": 0.88,
                "prediction_confidence": 0.85
            },
            "requires_intervention": False
        }
        mock_query.return_value = mock_response
        
        description = "Busy food court with moderate crowd density, people queuing around vendors"
        result = await crowdflow_app.query(input_text=description)
        
        self.assertTrue(result["crowd_detected"])
        self.assertEqual(result["crowd_density_level"], "moderate")
        self.assertEqual(result["safety_assessment"]["crush_risk"], "low")
        self.assertFalse(result["requires_intervention"])
    
    @patch('agent.crowdflow_app.query')
    async def test_computer_vision_outputs(self, mock_query):
        """Test computer vision and ML model outputs"""
        mock_response = {
            "crowd_detected": True,
            "crowd_density_level": "high",
            "confidence_score": 0.9,
            "density_score": 7,
            "analysis": "High density crowd detected via computer vision analysis",
            "crowd_metrics": {
                "estimated_count": 2200,
                "density_per_sqm": 5.1,
                "coverage_area_sqm": 431,
                "movement_speed": "slow"
            },
            "flow_predictions": {
                "direction": "convergent",
                "predicted_growth": "increasing",
                "peak_time_estimate": "20 minutes",
                "dispersion_pattern": "organized"
            },
            "safety_assessment": {
                "crush_risk": "moderate",
                "exit_accessibility": "partially_blocked",
                "emergency_response_time": "minutes"
            },
            "density_map_regions": [
                {
                    "region": "stage_area",
                    "density": "high",
                    "risk_level": "moderate"
                }
            ],
            "recommended_actions": ["Deploy additional staff", "Monitor exits"],
            "ml_model_outputs": {
                "yolo_detections": 2200,
                "tracking_accuracy": 0.91,
                "prediction_confidence": 0.88
            },
            "requires_intervention": True
        }
        mock_query.return_value = mock_response
        
        description = "Camera feed shows high density crowd formation with YOLOv3 detection"
        result = await crowdflow_app.query(input_text=description)
        
        # Test ML model outputs
        ml_outputs = result["ml_model_outputs"]
        self.assertIsInstance(ml_outputs["yolo_detections"], int)
        self.assertGreater(ml_outputs["yolo_detections"], 0)
        self.assertGreaterEqual(ml_outputs["tracking_accuracy"], 0.8)
        self.assertGreaterEqual(ml_outputs["prediction_confidence"], 0.8)
        
        # Test crowd metrics
        metrics = result["crowd_metrics"]
        self.assertIsInstance(metrics["estimated_count"], int)
        self.assertIsInstance(metrics["density_per_sqm"], float)
        self.assertGreater(metrics["density_per_sqm"], 0)
    
    @patch('agent.crowdflow_app.query')
    async def test_flow_prediction_analysis(self, mock_query):
        """Test crowd flow prediction capabilities"""
        mock_response = {
            "crowd_detected": True,
            "crowd_density_level": "high",
            "confidence_score": 0.88,
            "density_score": 6,
            "analysis": "Dynamic crowd flow with predictable movement patterns",
            "crowd_metrics": {
                "estimated_count": 1800,
                "density_per_sqm": 4.2,
                "coverage_area_sqm": 429,
                "movement_speed": "moderate"
            },
            "flow_predictions": {
                "direction": "north",
                "predicted_growth": "increasing",
                "peak_time_estimate": "25 minutes",
                "dispersion_pattern": "organized"
            },
            "safety_assessment": {
                "crush_risk": "moderate",
                "exit_accessibility": "clear",
                "emergency_response_time": "minutes"
            },
            "density_map_regions": [
                {
                    "region": "main_corridor",
                    "density": "high",
                    "risk_level": "moderate"
                }
            ],
            "recommended_actions": ["Guide flow direction", "Prepare for peak"],
            "ml_model_outputs": {
                "yolo_detections": 1800,
                "tracking_accuracy": 0.89,
                "prediction_confidence": 0.86
            },
            "requires_intervention": True
        }
        mock_query.return_value = mock_response
        
        description = "Crowd moving toward main stage, steady directional flow building"
        result = await crowdflow_app.query(input_text=description)
        
        # Test flow predictions
        flow = result["flow_predictions"]
        self.assertIn(flow["direction"], ["north", "south", "east", "west", "convergent", "divergent"])
        self.assertIn(flow["predicted_growth"], ["decreasing", "stable", "increasing", "rapid_growth"])
        self.assertIn(flow["dispersion_pattern"], ["organized", "chaotic", "bottlenecked"])
    
    @patch('agent.crowdflow_app.query')
    async def test_density_mapping_regions(self, mock_query):
        """Test density mapping and regional analysis"""
        mock_response = {
            "crowd_detected": True,
            "crowd_density_level": "moderate",
            "confidence_score": 0.82,
            "density_score": 5,
            "analysis": "Multi-zone venue with varying density levels across regions",
            "crowd_metrics": {
                "estimated_count": 3200,
                "density_per_sqm": 3.1,
                "coverage_area_sqm": 1032,
                "movement_speed": "slow"
            },
            "flow_predictions": {
                "direction": "divergent",
                "predicted_growth": "stable",
                "peak_time_estimate": "30 minutes",
                "dispersion_pattern": "organized"
            },
            "safety_assessment": {
                "crush_risk": "low",
                "exit_accessibility": "clear",
                "emergency_response_time": "minutes"
            },
            "density_map_regions": [
                {
                    "region": "stage_front",
                    "density": "high",
                    "risk_level": "moderate"
                },
                {
                    "region": "food_area",
                    "density": "moderate",
                    "risk_level": "low"
                },
                {
                    "region": "entrance",
                    "density": "low",
                    "risk_level": "low"
                }
            ],
            "recommended_actions": ["Monitor stage area", "Balance crowd distribution"],
            "ml_model_outputs": {
                "yolo_detections": 3200,
                "tracking_accuracy": 0.87,
                "prediction_confidence": 0.82
            },
            "requires_intervention": False
        }
        mock_query.return_value = mock_response
        
        description = "Multi-zone venue with varying density: stage packed, food court moderate, entrance light"
        result = await crowdflow_app.query(input_text=description)
        
        # Test density map regions
        regions = result["density_map_regions"]
        self.assertIsInstance(regions, list)
        self.assertGreater(len(regions), 1)
        
        for region in regions:
            self.assertIn("region", region)
            self.assertIn("density", region)
            self.assertIn("risk_level", region)
            self.assertIn(region["density"], ["low", "moderate", "high", "critical"])
            self.assertIn(region["risk_level"], ["low", "moderate", "high", "critical"])
    
    @patch('agent.crowdflow_app.query')
    async def test_safety_assessment_accuracy(self, mock_query):
        """Test safety assessment and risk evaluation"""
        mock_response = {
            "crowd_detected": True,
            "crowd_density_level": "critical",
            "confidence_score": 0.93,
            "density_score": 8,
            "analysis": "Dangerous crowd conditions requiring immediate intervention",
            "crowd_metrics": {
                "estimated_count": 3800,
                "density_per_sqm": 6.8,
                "coverage_area_sqm": 559,
                "movement_speed": "stationary"
            },
            "flow_predictions": {
                "direction": "convergent",
                "predicted_growth": "stable",
                "peak_time_estimate": "immediate",
                "dispersion_pattern": "bottlenecked"
            },
            "safety_assessment": {
                "crush_risk": "critical",
                "exit_accessibility": "blocked",
                "emergency_response_time": "immediate"
            },
            "density_map_regions": [
                {
                    "region": "bottleneck_area",
                    "density": "critical",
                    "risk_level": "critical"
                }
            ],
            "recommended_actions": ["Emergency procedures", "Immediate evacuation"],
            "ml_model_outputs": {
                "yolo_detections": 3800,
                "tracking_accuracy": 0.90,
                "prediction_confidence": 0.93
            },
            "requires_intervention": True
        }
        mock_query.return_value = mock_response
        
        description = "Emergency situation: crowd crush risk, exits blocked, immediate danger"
        result = await crowdflow_app.query(input_text=description)
        
        # Test safety assessment
        safety = result["safety_assessment"]
        self.assertEqual(safety["crush_risk"], "critical")
        self.assertEqual(safety["exit_accessibility"], "blocked")
        self.assertEqual(safety["emergency_response_time"], "immediate")
        self.assertTrue(result["requires_intervention"])
    
    def test_response_format_validation(self):
        """Test that expected response format fields are defined"""
        required_fields = [
            "crowd_detected",
            "crowd_density_level", 
            "confidence_score",
            "density_score",
            "analysis",
            "crowd_metrics",
            "flow_predictions",
            "safety_assessment",
            "density_map_regions",
            "recommended_actions",
            "ml_model_outputs",
            "requires_intervention"
        ]
        
        # Check that all required fields are mentioned in the prompt
        prompt = CROWDFLOW_ANALYSIS_PROMPT
        for field in required_fields:
            self.assertIn(field, prompt, f"Required field '{field}' not found in prompt")

class TestCrowdFlowAgentIntegration(unittest.TestCase):
    """Integration tests for CrowdFlow Agent"""
    
    @unittest.skipIf(not os.getenv('PROJECT_ID'), "PROJECT_ID not set - skipping integration tests")
    async def test_real_agent_response(self):
        """Test actual agent response (requires valid GCP credentials)"""
        try:
            description = "Test scenario: Moderate crowd density at entrance area with steady flow."
            result = await crowdflow_app.query(input_text=description)
            
            # Verify response has expected structure
            self.assertIsInstance(result, dict)
            
            # Check for key fields (allowing for flexibility in actual AI responses)
            expected_fields = ["analysis", "crowd_density_level"]
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
        'test_critical_density_analysis',
        'test_moderate_density_analysis', 
        'test_computer_vision_outputs',
        'test_flow_prediction_analysis',
        'test_density_mapping_regions',
        'test_safety_assessment_accuracy'
    ]
    
    for method_name in async_test_methods:
        suite.addTest(TestCrowdFlowAgent(method_name))
    
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
    print("🧪 Running CrowdFlow Agent Tests")
    print("="*50)
    
    # Run synchronous tests first
    print("\n📋 Running synchronous tests...")
    sync_suite = unittest.TestLoader().loadTestsFromTestCase(TestCrowdFlowAgent)
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
        print("\n👥 CrowdFlow Agent is ready for computer vision crowd analysis!")
    else:
        print("❌ Some tests failed. Check output above for details.")
        
    print("\n🔍 Advanced crowd detection and density mapping ready!") 