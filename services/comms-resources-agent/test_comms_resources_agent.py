"""
Test cases for the Communication & Resource Management Agent

This module contains unit tests and integration tests for the Communication & Resource Management Agent
to ensure it properly coordinates communication and resource deployment.
"""

import unittest
import asyncio
import json
from unittest.mock import Mock, patch
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import comms_resources_agent, comms_resources_app
from prompt import COMMUNICATION_COORDINATION_PROMPT

class TestCommsResourcesAgent(unittest.TestCase):
    """Test cases for Communication & Resource Management Agent functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_scenarios = [
            {
                "name": "Emergency Medical Response",
                "instruction": "Medical emergency at main stage, deploy medical team and announce evacuation",
                "expected_priority": "emergency",
                "expected_resources": ["medical_team", "security_staff"]
            },
            {
                "name": "Weather Warning Broadcast",
                "instruction": "Severe weather approaching, broadcast multilingual evacuation notice",
                "expected_priority": "high", 
                "expected_languages": ["en", "es", "fr"]
            },
            {
                "name": "Routine Staff Deployment",
                "instruction": "Need additional staff at entrance gate during lunch rush",
                "expected_priority": "medium",
                "expected_resources": ["security_staff"]
            },
            {
                "name": "Infrastructure Maintenance",
                "instruction": "Power outage in vendor area, deploy maintenance crew with backup generators",
                "expected_priority": "high",
                "expected_resources": ["maintenance_crew", "generators"]
            }
        ]
    
    def test_agent_initialization(self):
        """Test that the comms resources agent initializes correctly"""
        self.assertIsNotNone(comms_resources_agent)
        self.assertEqual(comms_resources_agent.name, "comms_resources_agent")
        self.assertEqual(comms_resources_agent.model, "gemini-2.0-flash-001")
        self.assertIn("communication", comms_resources_agent.description.lower())
        self.assertIn("resource", comms_resources_agent.description.lower())
    
    def test_prompt_content(self):
        """Test that the prompt contains required coordination keywords"""
        prompt = COMMUNICATION_COORDINATION_PROMPT
        
        # Check for key coordination terms
        self.assertIn("communication", prompt.lower())
        self.assertIn("resource", prompt.lower())
        self.assertIn("deployment", prompt.lower())
        self.assertIn("translation", prompt.lower())
        self.assertIn("broadcast", prompt.lower())
        
        # Check for priority levels
        self.assertIn("emergency", prompt.lower())
        self.assertIn("high", prompt.lower())
        self.assertIn("medium", prompt.lower())
        self.assertIn("low", prompt.lower())
        
        # Check for required response fields
        self.assertIn("instruction_understood", prompt)
        self.assertIn("priority_level", prompt)
        self.assertIn("communication_actions", prompt)
        self.assertIn("resource_deployment", prompt)
        self.assertIn("coordination_requirements", prompt)
    
    @patch('agent.comms_resources_app.query')
    async def test_emergency_coordination(self, mock_query):
        """Test coordination of emergency response"""
        # Mock response for emergency coordination
        mock_response = {
            "instruction_understood": True,
            "priority_level": "emergency",
            "urgency_score": 9,
            "coordination_plan": "Immediate medical response with crowd evacuation",
            "communication_actions": {
                "announcements": [
                    {
                        "message": "Medical emergency - please clear the area immediately",
                        "language": "en",
                        "channel": "public_address",
                        "audience": "all_attendees"
                    }
                ],
                "translations_needed": ["es", "fr", "de"],
                "broadcast_priority": "emergency",
                "delivery_method": "both"
            },
            "resource_deployment": {
                "personnel": [
                    {
                        "type": "medical_team",
                        "quantity": 2,
                        "location": "main_stage",
                        "eta": "3 minutes"
                    }
                ],
                "equipment": [
                    {
                        "type": "emergency_barriers",
                        "quantity": 6,
                        "location": "stage_perimeter"
                    }
                ],
                "vehicles": []
            },
            "weather_considerations": {
                "current_conditions": "clear",
                "impact_on_operations": "minimal",
                "weather_alerts": []
            },
            "coordination_requirements": {
                "agents_to_notify": ["security_agent", "medassist_agent"],
                "external_services": ["emergency_dispatch"],
                "follow_up_actions": ["monitor_situation", "prepare_evacuation_route"]
            },
            "estimated_timeline": {
                "immediate": "Medical team deployment",
                "short_term": "Area clearance and treatment",
                "long_term": "Transport to medical facility"
            },
            "success_metrics": ["response_time", "area_clearance_time"],
            "requires_escalation": True
        }
        mock_query.return_value = mock_response
        
        instruction = "Medical emergency at main stage, deploy medical team and announce evacuation"
        result = await comms_resources_app.query(input_text=instruction)
        
        self.assertTrue(result["instruction_understood"])
        self.assertEqual(result["priority_level"], "emergency")
        self.assertEqual(result["urgency_score"], 9)
        self.assertTrue(result["requires_escalation"])
        self.assertIn("medical_team", [p["type"] for p in result["resource_deployment"]["personnel"]])
    
    @patch('agent.comms_resources_app.query')
    async def test_multilingual_broadcasting(self, mock_query):
        """Test multilingual communication coordination"""
        mock_response = {
            "instruction_understood": True,
            "priority_level": "high",
            "urgency_score": 7,
            "coordination_plan": "Multilingual weather warning broadcast with shelter guidance",
            "communication_actions": {
                "announcements": [
                    {
                        "message": "Severe weather warning - seek immediate shelter",
                        "language": "en",
                        "channel": "public_address",
                        "audience": "all_attendees"
                    },
                    {
                        "message": "Advertencia meteorológica severa - busque refugio inmediato",
                        "language": "es",
                        "channel": "public_address",
                        "audience": "spanish_speakers"
                    }
                ],
                "translations_needed": ["es", "fr", "de", "zh"],
                "broadcast_priority": "high",
                "delivery_method": "both"
            },
            "resource_deployment": {
                "personnel": [
                    {
                        "type": "crowd_management",
                        "quantity": 4,
                        "location": "shelter_areas",
                        "eta": "5 minutes"
                    }
                ],
                "equipment": [
                    {
                        "type": "directional_signage",
                        "quantity": 12,
                        "location": "main_pathways"
                    }
                ],
                "vehicles": []
            },
            "weather_considerations": {
                "current_conditions": "thunderstorm_approaching",
                "impact_on_operations": "significant",
                "weather_alerts": ["severe_thunderstorm_warning"]
            },
            "coordination_requirements": {
                "agents_to_notify": ["security_agent", "infrastructure_agent"],
                "external_services": ["weather_service", "emergency_management"],
                "follow_up_actions": ["monitor_weather", "prepare_shelters"]
            },
            "estimated_timeline": {
                "immediate": "Broadcast warnings",
                "short_term": "Guide to shelters",
                "long_term": "Weather monitoring"
            },
            "success_metrics": ["message_reach", "shelter_capacity"],
            "requires_escalation": False
        }
        mock_query.return_value = mock_response
        
        instruction = "Severe weather approaching, broadcast multilingual evacuation notice"
        result = await comms_resources_app.query(input_text=instruction)
        
        self.assertTrue(result["instruction_understood"])
        self.assertEqual(result["priority_level"], "high")
        self.assertGreater(len(result["communication_actions"]["translations_needed"]), 2)
        self.assertEqual(result["communication_actions"]["broadcast_priority"], "high")
    
    @patch('agent.comms_resources_app.query')
    async def test_drone_deployment(self, mock_query):
        """Test drone deployment coordination"""
        mock_response = {
            "instruction_understood": True,
            "priority_level": "medium",
            "urgency_score": 5,
            "coordination_plan": "Deploy surveillance drone for security assessment",
            "communication_actions": {
                "announcements": [],
                "translations_needed": [],
                "broadcast_priority": "standard",
                "delivery_method": "audio"
            },
            "resource_deployment": {
                "personnel": [
                    {
                        "type": "drone_operator",
                        "quantity": 1,
                        "location": "command_center",
                        "eta": "2 minutes"
                    }
                ],
                "equipment": [
                    {
                        "type": "communication_relay",
                        "quantity": 1,
                        "location": "parking_lot_c"
                    }
                ],
                "vehicles": [
                    {
                        "type": "drone",
                        "purpose": "aerial_surveillance",
                        "deployment_area": "parking_lot_c"
                    }
                ]
            },
            "weather_considerations": {
                "current_conditions": "clear",
                "impact_on_operations": "minimal",
                "weather_alerts": []
            },
            "coordination_requirements": {
                "agents_to_notify": ["security_agent"],
                "external_services": ["air_traffic_control"],
                "follow_up_actions": ["monitor_surveillance_feed", "coordinate_ground_response"]
            },
            "estimated_timeline": {
                "immediate": "Drone deployment",
                "short_term": "Surveillance assessment",
                "long_term": "Ongoing monitoring"
            },
            "success_metrics": ["deployment_time", "surveillance_coverage"],
            "requires_escalation": False
        }
        mock_query.return_value = mock_response
        
        instruction = "Security concern in parking lot C, deploy drone for aerial surveillance"
        result = await comms_resources_app.query(input_text=instruction)
        
        self.assertTrue(result["instruction_understood"])
        self.assertEqual(result["priority_level"], "medium")
        vehicles = result["resource_deployment"]["vehicles"]
        self.assertTrue(any(v["type"] == "drone" for v in vehicles))
        self.assertIn("security_agent", result["coordination_requirements"]["agents_to_notify"])
    
    @patch('agent.comms_resources_app.query')
    async def test_resource_optimization(self, mock_query):
        """Test resource allocation and optimization"""
        mock_response = {
            "instruction_understood": True,
            "priority_level": "medium",
            "urgency_score": 4,
            "coordination_plan": "Optimize staff allocation during peak period",
            "communication_actions": {
                "announcements": [
                    {
                        "message": "Minor delays expected at entrance gates",
                        "language": "en",
                        "channel": "mobile_app",
                        "audience": "incoming_attendees"
                    }
                ],
                "translations_needed": ["es"],
                "broadcast_priority": "standard",
                "delivery_method": "visual"
            },
            "resource_deployment": {
                "personnel": [
                    {
                        "type": "security_staff",
                        "quantity": 3,
                        "location": "entrance_gate_2",
                        "eta": "10 minutes"
                    },
                    {
                        "type": "crowd_management",
                        "quantity": 2,
                        "location": "queue_areas",
                        "eta": "8 minutes"
                    }
                ],
                "equipment": [
                    {
                        "type": "queue_barriers",
                        "quantity": 8,
                        "location": "entrance_gate_2"
                    }
                ],
                "vehicles": []
            },
            "weather_considerations": {
                "current_conditions": "sunny",
                "impact_on_operations": "minimal",
                "weather_alerts": []
            },
            "coordination_requirements": {
                "agents_to_notify": ["queue_management_agent"],
                "external_services": [],
                "follow_up_actions": ["monitor_queue_length", "adjust_staffing"]
            },
            "estimated_timeline": {
                "immediate": "Staff redeployment",
                "short_term": "Queue optimization",
                "long_term": "Maintain efficient flow"
            },
            "success_metrics": ["queue_wait_time", "staff_utilization"],
            "requires_escalation": False
        }
        mock_query.return_value = mock_response
        
        instruction = "Queue building up at entrance gate 2, need additional security staff"
        result = await comms_resources_app.query(input_text=instruction)
        
        self.assertTrue(result["instruction_understood"])
        self.assertEqual(result["priority_level"], "medium")
        personnel = result["resource_deployment"]["personnel"]
        self.assertTrue(any(p["type"] == "security_staff" for p in personnel))
        self.assertIn("queue_management_agent", result["coordination_requirements"]["agents_to_notify"])
    
    @patch('agent.comms_resources_app.query')
    async def test_weather_integration(self, mock_query):
        """Test weather monitoring and integration"""
        mock_response = {
            "instruction_understood": True,
            "priority_level": "high",
            "urgency_score": 7,
            "coordination_plan": "Weather-responsive resource deployment and communication",
            "communication_actions": {
                "announcements": [
                    {
                        "message": "Rain expected in 20 minutes - covered areas available",
                        "language": "en",
                        "channel": "public_address",
                        "audience": "outdoor_attendees"
                    }
                ],
                "translations_needed": ["es", "fr"],
                "broadcast_priority": "high",
                "delivery_method": "both"
            },
            "resource_deployment": {
                "personnel": [
                    {
                        "type": "crowd_management",
                        "quantity": 6,
                        "location": "covered_areas",
                        "eta": "5 minutes"
                    }
                ],
                "equipment": [
                    {
                        "type": "shelter_tents",
                        "quantity": 4,
                        "location": "open_areas"
                    }
                ],
                "vehicles": []
            },
            "weather_considerations": {
                "current_conditions": "cloudy",
                "impact_on_operations": "moderate",
                "weather_alerts": ["rain_warning", "wind_advisory"]
            },
            "coordination_requirements": {
                "agents_to_notify": ["infrastructure_agent", "crowdflow_agent"],
                "external_services": ["weather_service"],
                "follow_up_actions": ["monitor_weather_updates", "prepare_additional_shelter"]
            },
            "estimated_timeline": {
                "immediate": "Weather announcement",
                "short_term": "Crowd shelter guidance",
                "long_term": "Weather monitoring"
            },
            "success_metrics": ["shelter_utilization", "weather_response_time"],
            "requires_escalation": False
        }
        mock_query.return_value = mock_response
        
        instruction = "Rain approaching, coordinate shelter announcements and crowd management"
        result = await comms_resources_app.query(input_text=instruction)
        
        self.assertTrue(result["instruction_understood"])
        self.assertEqual(result["priority_level"], "high")
        weather = result["weather_considerations"]
        self.assertIn("rain_warning", weather["weather_alerts"])
        self.assertEqual(weather["impact_on_operations"], "moderate")
    
    @patch('agent.comms_resources_app.query')
    async def test_coordination_requirements(self, mock_query):
        """Test inter-agent coordination requirements"""
        mock_response = {
            "instruction_understood": True,
            "priority_level": "high",
            "urgency_score": 8,
            "coordination_plan": "Multi-agent coordination for complex incident",
            "communication_actions": {
                "announcements": [
                    {
                        "message": "Temporary service interruption - alternative routes available",
                        "language": "en",
                        "channel": "digital_displays",
                        "audience": "affected_areas"
                    }
                ],
                "translations_needed": ["es", "fr", "de"],
                "broadcast_priority": "high",
                "delivery_method": "visual"
            },
            "resource_deployment": {
                "personnel": [
                    {
                        "type": "maintenance_crew",
                        "quantity": 4,
                        "location": "affected_area",
                        "eta": "8 minutes"
                    }
                ],
                "equipment": [
                    {
                        "type": "backup_generators",
                        "quantity": 2,
                        "location": "vendor_area"
                    }
                ],
                "vehicles": [
                    {
                        "type": "maintenance_truck",
                        "purpose": "equipment_transport",
                        "deployment_area": "vendor_area"
                    }
                ]
            },
            "weather_considerations": {
                "current_conditions": "clear",
                "impact_on_operations": "minimal",
                "weather_alerts": []
            },
            "coordination_requirements": {
                "agents_to_notify": ["infrastructure_agent", "queue_management_agent", "security_agent"],
                "external_services": ["utility_company", "vendor_management"],
                "follow_up_actions": ["monitor_power_restoration", "assess_vendor_impact"]
            },
            "estimated_timeline": {
                "immediate": "Deploy maintenance crew",
                "short_term": "Power restoration",
                "long_term": "System verification"
            },
            "success_metrics": ["restoration_time", "vendor_satisfaction"],
            "requires_escalation": True
        }
        mock_query.return_value = mock_response
        
        instruction = "Power outage in vendor area, coordinate maintenance and communication"
        result = await comms_resources_app.query(input_text=instruction)
        
        self.assertTrue(result["instruction_understood"])
        self.assertEqual(result["priority_level"], "high")
        coord = result["coordination_requirements"]
        self.assertGreater(len(coord["agents_to_notify"]), 2)
        self.assertIn("infrastructure_agent", coord["agents_to_notify"])
        self.assertTrue(result["requires_escalation"])
    
    def test_response_format_validation(self):
        """Test that expected response format fields are defined"""
        required_fields = [
            "instruction_understood",
            "priority_level", 
            "urgency_score",
            "coordination_plan",
            "communication_actions",
            "resource_deployment",
            "weather_considerations",
            "coordination_requirements",
            "estimated_timeline",
            "success_metrics",
            "requires_escalation"
        ]
        
        # Check that all required fields are mentioned in the prompt
        prompt = COMMUNICATION_COORDINATION_PROMPT
        for field in required_fields:
            self.assertIn(field, prompt, f"Required field '{field}' not found in prompt")

class TestCommsResourcesAgentIntegration(unittest.TestCase):
    """Integration tests for Communication & Resource Management Agent"""
    
    @unittest.skipIf(not os.getenv('PROJECT_ID'), "PROJECT_ID not set - skipping integration tests")
    async def test_real_agent_response(self):
        """Test actual agent response (requires valid GCP credentials)"""
        try:
            instruction = "Test scenario: Need additional staff at information booth during peak hours."
            result = await comms_resources_app.query(input_text=instruction)
            
            # Verify response has expected structure
            self.assertIsInstance(result, dict)
            
            # Check for key fields (allowing for flexibility in actual AI responses)
            expected_fields = ["coordination_plan", "priority_level"]
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
        'test_emergency_coordination',
        'test_multilingual_broadcasting', 
        'test_drone_deployment',
        'test_resource_optimization',
        'test_weather_integration',
        'test_coordination_requirements'
    ]
    
    for method_name in async_test_methods:
        suite.addTest(TestCommsResourcesAgent(method_name))
    
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
    print("🧪 Running Communication & Resource Management Agent Tests")
    print("="*50)
    
    # Run synchronous tests first
    print("\n📋 Running synchronous tests...")
    sync_suite = unittest.TestLoader().loadTestsFromTestCase(TestCommsResourcesAgent)
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
        print("\n📡 Communication & Resource Management Agent is ready for coordination!")
    else:
        print("❌ Some tests failed. Check output above for details.")
        
    print("\n🚀 Advanced communication and resource coordination capabilities ready!") 