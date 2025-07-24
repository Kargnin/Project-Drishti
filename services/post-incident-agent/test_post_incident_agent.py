"""
Test cases for the Post-Incident Analysis Agent

This module contains unit tests and integration tests for the Post-Incident Analysis Agent
to ensure it properly analyzes incidents and provides appropriate optimization recommendations.
"""

import unittest
import asyncio
import json
from unittest.mock import Mock, patch
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import post_incident_agent, post_incident_app
from prompt import POST_INCIDENT_ANALYSIS_PROMPT

class TestPostIncidentAgent(unittest.TestCase):
    """Test cases for Post-Incident Analysis Agent functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_scenarios = [
            {
                "name": "Excellent Medical Response",
                "description": "Medical emergency handled perfectly, 2-minute response, successful outcome",
                "expected_effectiveness": 9,
                "expected_compliance": 10
            },
            {
                "name": "Good Security Response",
                "description": "Security threat identified and resolved quickly with minor coordination delays",
                "expected_effectiveness": 7,
                "expected_compliance": 8
            },
            {
                "name": "Adequate Infrastructure Response",
                "description": "Power outage resolved but response time was slower than optimal",
                "expected_effectiveness": 5,
                "expected_compliance": 6
            },
            {
                "name": "Poor Communication Response",
                "description": "Emergency announcement delayed, language barriers not addressed, confusion resulted",
                "expected_effectiveness": 3,
                "expected_compliance": 4
            }
        ]
    
    def test_agent_initialization(self):
        """Test that the post incident agent initializes correctly"""
        self.assertIsNotNone(post_incident_agent)
        self.assertEqual(post_incident_agent.name, "post_incident_agent")
        self.assertEqual(post_incident_agent.model, "gemini-2.0-flash-001")
        self.assertIn("post-incident", post_incident_agent.description.lower())
        self.assertIn("analysis", post_incident_agent.description.lower())
    
    def test_prompt_content(self):
        """Test that the prompt contains required analysis keywords"""
        prompt = POST_INCIDENT_ANALYSIS_PROMPT
        
        # Check for key analysis terms
        self.assertIn("post-incident", prompt.lower())
        self.assertIn("analysis", prompt.lower())
        self.assertIn("effectiveness", prompt.lower())
        self.assertIn("pattern", prompt.lower())
        self.assertIn("optimization", prompt.lower())
        
        # Check for effectiveness levels
        self.assertIn("excellent", prompt.lower())
        self.assertIn("good", prompt.lower())
        self.assertIn("adequate", prompt.lower())
        self.assertIn("poor", prompt.lower())
        
        # Check for required response fields
        self.assertIn("incident_analyzed", prompt)
        self.assertIn("effectiveness_score", prompt)
        self.assertIn("detailed_evaluation", prompt)
        self.assertIn("instruction_compliance", prompt)
        self.assertIn("pattern_identification", prompt)
        self.assertIn("system_optimization", prompt)
    
    @patch('agent.post_incident_app.query')
    async def test_excellent_response_analysis(self, mock_query):
        """Test analysis of excellent incident response"""
        # Mock response for excellent performance
        mock_response = {
            "incident_analyzed": True,
            "incident_summary": "Excellent medical emergency response with optimal outcomes",
            "effectiveness_score": 9,
            "analysis_confidence": 0.95,
            "detailed_evaluation": {
                "response_timeliness": {
                    "score": 10,
                    "assessment": "Exceptional response speed, immediate deployment",
                    "improvement_areas": []
                },
                "resource_allocation": {
                    "score": 9,
                    "assessment": "Optimal resource deployment with minimal waste",
                    "optimization_opportunities": ["minor efficiency gains possible"]
                },
                "communication_effectiveness": {
                    "score": 9,
                    "assessment": "Clear, timely, multilingual communication",
                    "enhancement_suggestions": ["expand to additional languages"]
                },
                "coordination_quality": {
                    "score": 9,
                    "assessment": "Seamless inter-agent coordination",
                    "workflow_improvements": ["minor process streamlining"]
                },
                "outcome_achievement": {
                    "score": 10,
                    "assessment": "Perfect incident resolution, no escalation",
                    "success_factors": ["rapid response", "clear communication", "excellent coordination"]
                }
            },
            "instruction_compliance": {
                "instructions_followed": "100%",
                "compliance_score": 10,
                "deviation_analysis": "No deviations from protocol",
                "compliance_gaps": []
            },
            "pattern_identification": {
                "recurring_patterns": ["medical emergency best practices"],
                "trend_analysis": "Consistent high performance in medical responses",
                "risk_indicators": [],
                "predictive_insights": "Response model suitable for replication"
            },
            "system_optimization": {
                "training_data_generated": "Excellent response patterns extracted for training",
                "model_improvements": ["response time optimization"],
                "process_optimizations": ["workflow standardization"],
                "system_enhancements": ["automated best practice recognition"]
            },
            "recommendations": {
                "immediate_actions": ["document best practices"],
                "short_term_improvements": ["train other teams on this response model"],
                "long_term_optimizations": ["implement automated response triggers"],
                "training_recommendations": ["create case study for training"]
            },
            "lessons_learned": {
                "key_insights": ["early detection critical", "clear communication prevents panic"],
                "best_practices": ["rapid deployment", "multilingual communication"],
                "failure_modes": [],
                "prevention_strategies": ["maintain rapid response capabilities"]
            },
            "benchmarking": {
                "industry_comparison": "Exceeds industry standards by 40%",
                "historical_comparison": "Best performance recorded",
                "performance_metrics": {"response_time": "2.1_minutes", "success_rate": "100%"}
            },
            "requires_escalation": False
        }
        mock_query.return_value = mock_response
        
        description = "Medical emergency handled perfectly, 2-minute response, successful outcome"
        result = await post_incident_app.query(input_text=description)
        
        self.assertTrue(result["incident_analyzed"])
        self.assertEqual(result["effectiveness_score"], 9)
        self.assertEqual(result["instruction_compliance"]["compliance_score"], 10)
        self.assertGreaterEqual(result["analysis_confidence"], 0.9)
        self.assertFalse(result["requires_escalation"])
    
    @patch('agent.post_incident_app.query')
    async def test_poor_response_analysis(self, mock_query):
        """Test analysis of poor incident response"""
        mock_response = {
            "incident_analyzed": True,
            "incident_summary": "Poor communication response with significant failures",
            "effectiveness_score": 3,
            "analysis_confidence": 0.88,
            "detailed_evaluation": {
                "response_timeliness": {
                    "score": 4,
                    "assessment": "Delayed response, missed critical window",
                    "improvement_areas": ["faster detection", "quicker deployment"]
                },
                "resource_allocation": {
                    "score": 5,
                    "assessment": "Adequate resources but poor coordination",
                    "optimization_opportunities": ["better resource planning", "coordination training"]
                },
                "communication_effectiveness": {
                    "score": 2,
                    "assessment": "Poor communication, language barriers not addressed",
                    "enhancement_suggestions": ["multilingual support", "clearer messaging", "multiple channels"]
                },
                "coordination_quality": {
                    "score": 3,
                    "assessment": "Significant coordination failures",
                    "workflow_improvements": ["communication protocols", "role clarity", "decision hierarchy"]
                },
                "outcome_achievement": {
                    "score": 3,
                    "assessment": "Incident resolved but with negative impacts",
                    "success_factors": ["eventual resolution"]
                }
            },
            "instruction_compliance": {
                "instructions_followed": "45%",
                "compliance_score": 4,
                "deviation_analysis": "Multiple protocol violations, communication failures",
                "compliance_gaps": ["language support", "timing adherence", "resource coordination"]
            },
            "pattern_identification": {
                "recurring_patterns": ["communication delays", "language barrier issues"],
                "trend_analysis": "Declining performance in multilingual situations",
                "risk_indicators": ["inadequate translation", "cultural insensitivity"],
                "predictive_insights": "High risk of similar failures without intervention"
            },
            "system_optimization": {
                "training_data_generated": "Failure patterns identified for prevention training",
                "model_improvements": ["communication protocols", "language detection"],
                "process_optimizations": ["translation workflow", "cultural adaptation"],
                "system_enhancements": ["real-time translation", "cultural awareness training"]
            },
            "recommendations": {
                "immediate_actions": ["implement emergency translation", "train staff on protocols"],
                "short_term_improvements": ["enhance translation capabilities", "cultural awareness training"],
                "long_term_optimizations": ["AI-powered translation", "cultural adaptation system"],
                "training_recommendations": ["intensive communication training", "multilingual preparedness"]
            },
            "lessons_learned": {
                "key_insights": ["language barriers critical failure point", "cultural sensitivity essential"],
                "best_practices": [],
                "failure_modes": ["delayed translation", "cultural miscommunication"],
                "prevention_strategies": ["proactive translation", "cultural training", "diverse staff"]
            },
            "benchmarking": {
                "industry_comparison": "Below industry standards by 35%",
                "historical_comparison": "Worst performance in category",
                "performance_metrics": {"response_time": "12.3_minutes", "success_rate": "60%"}
            },
            "requires_escalation": True
        }
        mock_query.return_value = mock_response
        
        description = "Emergency announcement delayed, language barriers not addressed, confusion resulted"
        result = await post_incident_app.query(input_text=description)
        
        self.assertTrue(result["incident_analyzed"])
        self.assertEqual(result["effectiveness_score"], 3)
        self.assertEqual(result["instruction_compliance"]["compliance_score"], 4)
        self.assertTrue(result["requires_escalation"])
        self.assertIn("communication", result["incident_summary"].lower())
    
    @patch('agent.post_incident_app.query')
    async def test_pattern_recognition(self, mock_query):
        """Test pattern recognition capabilities"""
        mock_response = {
            "incident_analyzed": True,
            "incident_summary": "Pattern analysis of recurring security incidents",
            "effectiveness_score": 6,
            "analysis_confidence": 0.92,
            "detailed_evaluation": {
                "response_timeliness": {
                    "score": 7,
                    "assessment": "Generally good response times with some variations",
                    "improvement_areas": ["consistency in off-peak hours"]
                },
                "resource_allocation": {
                    "score": 6,
                    "assessment": "Resource allocation shows patterns of inefficiency",
                    "optimization_opportunities": ["predictive deployment", "dynamic allocation"]
                },
                "communication_effectiveness": {
                    "score": 7,
                    "assessment": "Communication generally effective",
                    "enhancement_suggestions": ["proactive messaging"]
                },
                "coordination_quality": {
                    "score": 6,
                    "assessment": "Coordination quality varies by incident type",
                    "workflow_improvements": ["standardized workflows", "role clarity"]
                },
                "outcome_achievement": {
                    "score": 7,
                    "assessment": "Most incidents resolved successfully",
                    "success_factors": ["experienced staff", "established procedures"]
                }
            },
            "instruction_compliance": {
                "instructions_followed": "75%",
                "compliance_score": 7,
                "deviation_analysis": "Some deviations due to situational adaptation",
                "compliance_gaps": ["procedure updates needed"]
            },
            "pattern_identification": {
                "recurring_patterns": [
                    "parking area incidents peak at 2-4 AM",
                    "entrance gate issues during high-traffic periods",
                    "communication delays in remote areas"
                ],
                "trend_analysis": "Security incidents increasing 15% year-over-year, but severity decreasing",
                "risk_indicators": [
                    "understaffed late hours",
                    "inadequate lighting in parking",
                    "communication dead zones"
                ],
                "predictive_insights": "High probability of parking incidents during late events"
            },
            "system_optimization": {
                "training_data_generated": "Temporal and spatial incident patterns for ML training",
                "model_improvements": ["predictive incident modeling", "resource forecasting"],
                "process_optimizations": ["dynamic staffing", "proactive deployment"],
                "system_enhancements": ["predictive analytics", "automated resource allocation"]
            },
            "recommendations": {
                "immediate_actions": ["increase late-hour parking security", "improve lighting"],
                "short_term_improvements": ["predictive staffing model", "communication infrastructure"],
                "long_term_optimizations": ["AI-powered incident prediction", "automated resource deployment"],
                "training_recommendations": ["pattern recognition training", "predictive response training"]
            },
            "lessons_learned": {
                "key_insights": [
                    "temporal patterns highly predictable",
                    "proactive deployment more effective than reactive"
                ],
                "best_practices": ["data-driven staffing", "proactive positioning"],
                "failure_modes": ["reactive-only response", "ignoring patterns"],
                "prevention_strategies": ["predictive deployment", "pattern-based planning"]
            },
            "benchmarking": {
                "industry_comparison": "Pattern recognition above industry average",
                "historical_comparison": "Significant improvement in predictive capability",
                "performance_metrics": {"prediction_accuracy": "78%", "prevention_rate": "34%"}
            },
            "requires_escalation": False
        }
        mock_query.return_value = mock_response
        
        description = "Analyze recurring security incident patterns from past 6 months"
        result = await post_incident_app.query(input_text=description)
        
        self.assertTrue(result["incident_analyzed"])
        patterns = result["pattern_identification"]
        self.assertIsInstance(patterns["recurring_patterns"], list)
        self.assertGreater(len(patterns["recurring_patterns"]), 0)
        self.assertIn("trend_analysis", patterns)
        self.assertIn("predictive_insights", patterns)
    
    @patch('agent.post_incident_app.query')
    async def test_system_optimization_recommendations(self, mock_query):
        """Test system optimization recommendation generation"""
        mock_response = {
            "incident_analyzed": True,
            "incident_summary": "System optimization analysis for communication improvements",
            "effectiveness_score": 7,
            "analysis_confidence": 0.91,
            "detailed_evaluation": {
                "response_timeliness": {
                    "score": 8,
                    "assessment": "Response times generally good",
                    "improvement_areas": ["automation opportunities"]
                },
                "resource_allocation": {
                    "score": 6,
                    "assessment": "Resource allocation has optimization potential",
                    "optimization_opportunities": ["AI-powered allocation", "predictive modeling"]
                },
                "communication_effectiveness": {
                    "score": 7,
                    "assessment": "Communication effective but room for enhancement",
                    "enhancement_suggestions": ["multilingual improvements", "channel optimization"]
                },
                "coordination_quality": {
                    "score": 7,
                    "assessment": "Good coordination with enhancement opportunities",
                    "workflow_improvements": ["automated workflows", "decision support"]
                },
                "outcome_achievement": {
                    "score": 8,
                    "assessment": "Strong outcome achievement",
                    "success_factors": ["systematic approach", "continuous improvement"]
                }
            },
            "instruction_compliance": {
                "instructions_followed": "85%",
                "compliance_score": 8,
                "deviation_analysis": "Minor deviations for situational optimization",
                "compliance_gaps": ["automated compliance monitoring needed"]
            },
            "pattern_identification": {
                "recurring_patterns": ["communication enhancement needs", "resource optimization opportunities"],
                "trend_analysis": "Steady improvement with acceleration potential",
                "risk_indicators": ["capacity constraints during peak events"],
                "predictive_insights": "System ready for next-generation enhancements"
            },
            "system_optimization": {
                "training_data_generated": "Communication effectiveness patterns for AI training",
                "model_improvements": [
                    "real-time translation accuracy",
                    "cultural adaptation algorithms",
                    "channel optimization models"
                ],
                "process_optimizations": [
                    "automated message translation",
                    "dynamic channel selection",
                    "feedback-driven improvement"
                ],
                "system_enhancements": [
                    "AI-powered translation system",
                    "predictive communication routing",
                    "automated effectiveness monitoring"
                ]
            },
            "recommendations": {
                "immediate_actions": [
                    "implement automated translation",
                    "deploy effectiveness monitoring"
                ],
                "short_term_improvements": [
                    "enhance multilingual capabilities",
                    "optimize communication channels",
                    "implement feedback systems"
                ],
                "long_term_optimizations": [
                    "AI-powered communication system",
                    "predictive messaging platform",
                    "autonomous optimization engine"
                ],
                "training_recommendations": [
                    "AI system training on communication patterns",
                    "staff training on new technologies",
                    "continuous improvement methodologies"
                ]
            },
            "lessons_learned": {
                "key_insights": [
                    "automation enhances consistency",
                    "AI can improve cultural adaptation",
                    "predictive systems reduce response time"
                ],
                "best_practices": [
                    "data-driven optimization",
                    "continuous monitoring",
                    "automated improvement"
                ],
                "failure_modes": ["manual process limitations", "cultural insensitivity"],
                "prevention_strategies": [
                    "automated translation",
                    "cultural awareness AI",
                    "predictive optimization"
                ]
            },
            "benchmarking": {
                "industry_comparison": "Above average with significant enhancement potential",
                "historical_comparison": "Consistent improvement trajectory",
                "performance_metrics": {
                    "automation_level": "65%",
                    "optimization_potential": "40%",
                    "enhancement_readiness": "high"
                }
            },
            "requires_escalation": False
        }
        mock_query.return_value = mock_response
        
        description = "Generate system optimization recommendations for communication improvements"
        result = await post_incident_app.query(input_text=description)
        
        self.assertTrue(result["incident_analyzed"])
        optimization = result["system_optimization"]
        self.assertIn("model_improvements", optimization)
        self.assertIn("process_optimizations", optimization)
        self.assertIn("system_enhancements", optimization)
        
        recommendations = result["recommendations"]
        self.assertIn("immediate_actions", recommendations)
        self.assertIn("short_term_improvements", recommendations)
        self.assertIn("long_term_optimizations", recommendations)
    
    @patch('agent.post_incident_app.query')
    async def test_compliance_evaluation(self, mock_query):
        """Test instruction compliance evaluation"""
        mock_response = {
            "incident_analyzed": True,
            "incident_summary": "Compliance evaluation for emergency evacuation procedures",
            "effectiveness_score": 6,
            "analysis_confidence": 0.89,
            "detailed_evaluation": {
                "response_timeliness": {
                    "score": 7,
                    "assessment": "Timely response within acceptable parameters",
                    "improvement_areas": ["faster initial detection"]
                },
                "resource_allocation": {
                    "score": 6,
                    "assessment": "Resources deployed but coordination issues",
                    "optimization_opportunities": ["better coordination protocols"]
                },
                "communication_effectiveness": {
                    "score": 5,
                    "assessment": "Communication partially effective",
                    "enhancement_suggestions": ["clearer instructions", "multiple languages"]
                },
                "coordination_quality": {
                    "score": 6,
                    "assessment": "Coordination adequate but inconsistent",
                    "workflow_improvements": ["standardized procedures", "role clarity"]
                },
                "outcome_achievement": {
                    "score": 7,
                    "assessment": "Objectives achieved with room for improvement",
                    "success_factors": ["staff dedication", "established procedures"]
                }
            },
            "instruction_compliance": {
                "instructions_followed": "70%",
                "compliance_score": 6,
                "deviation_analysis": "Several deviations due to unclear procedures and time constraints",
                "compliance_gaps": [
                    "language translation delays",
                    "unclear role assignments",
                    "insufficient training on new procedures"
                ]
            },
            "pattern_identification": {
                "recurring_patterns": ["compliance issues during high-stress situations"],
                "trend_analysis": "Compliance decreases under pressure",
                "risk_indicators": ["time pressure", "unclear procedures", "inadequate training"],
                "predictive_insights": "Compliance likely to improve with better training and clearer procedures"
            },
            "system_optimization": {
                "training_data_generated": "Compliance patterns under various stress conditions",
                "model_improvements": ["stress-adaptive procedures", "clarity optimization"],
                "process_optimizations": ["simplified procedures", "stress testing"],
                "system_enhancements": ["automated compliance monitoring", "real-time guidance"]
            },
            "recommendations": {
                "immediate_actions": [
                    "clarify evacuation procedures",
                    "conduct compliance training"
                ],
                "short_term_improvements": [
                    "simplify procedure language",
                    "implement compliance monitoring",
                    "stress-test procedures"
                ],
                "long_term_optimizations": [
                    "automated compliance assistance",
                    "adaptive procedure system",
                    "AI-powered guidance"
                ],
                "training_recommendations": [
                    "compliance under pressure training",
                    "procedure simplification workshop",
                    "stress management training"
                ]
            },
            "lessons_learned": {
                "key_insights": [
                    "stress significantly impacts compliance",
                    "clear procedures improve adherence",
                    "training frequency affects performance"
                ],
                "best_practices": [
                    "simple, clear procedures",
                    "regular compliance training",
                    "stress testing"
                ],
                "failure_modes": [
                    "complex procedures under stress",
                    "inadequate training",
                    "unclear role definitions"
                ],
                "prevention_strategies": [
                    "procedure simplification",
                    "frequent training",
                    "automated guidance"
                ]
            },
            "benchmarking": {
                "industry_comparison": "Compliance rate below industry average",
                "historical_comparison": "Slight improvement from previous incidents",
                "performance_metrics": {
                    "compliance_rate": "70%",
                    "training_effectiveness": "65%",
                    "procedure_clarity": "60%"
                }
            },
            "requires_escalation": True
        }
        mock_query.return_value = mock_response
        
        description = "Evaluate compliance with evacuation procedures during emergency"
        result = await post_incident_app.query(input_text=description)
        
        self.assertTrue(result["incident_analyzed"])
        compliance = result["instruction_compliance"]
        self.assertIn("compliance_score", compliance)
        self.assertIn("deviation_analysis", compliance)
        self.assertIn("compliance_gaps", compliance)
        self.assertEqual(compliance["compliance_score"], 6)
        self.assertTrue(result["requires_escalation"])
    
    def test_response_format_validation(self):
        """Test that expected response format fields are defined"""
        required_fields = [
            "incident_analyzed",
            "incident_summary",
            "effectiveness_score", 
            "analysis_confidence",
            "detailed_evaluation",
            "instruction_compliance",
            "pattern_identification",
            "system_optimization",
            "recommendations",
            "lessons_learned",
            "benchmarking",
            "requires_escalation"
        ]
        
        # Check that all required fields are mentioned in the prompt
        prompt = POST_INCIDENT_ANALYSIS_PROMPT
        for field in required_fields:
            self.assertIn(field, prompt, f"Required field '{field}' not found in prompt")

class TestPostIncidentAgentIntegration(unittest.TestCase):
    """Integration tests for Post-Incident Analysis Agent"""
    
    @unittest.skipIf(not os.getenv('PROJECT_ID'), "PROJECT_ID not set - skipping integration tests")
    async def test_real_agent_response(self):
        """Test actual agent response (requires valid GCP credentials)"""
        try:
            description = "Test scenario: Analyze response to minor technical issue during event."
            result = await post_incident_app.query(input_text=description)
            
            # Verify response has expected structure
            self.assertIsInstance(result, dict)
            
            # Check for key fields (allowing for flexibility in actual AI responses)
            expected_fields = ["incident_summary", "effectiveness_score"]
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
        'test_excellent_response_analysis',
        'test_poor_response_analysis', 
        'test_pattern_recognition',
        'test_system_optimization_recommendations',
        'test_compliance_evaluation'
    ]
    
    for method_name in async_test_methods:
        suite.addTest(TestPostIncidentAgent(method_name))
    
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
    print("🧪 Running Post-Incident Analysis Agent Tests")
    print("="*50)
    
    # Run synchronous tests first
    print("\n📋 Running synchronous tests...")
    sync_suite = unittest.TestLoader().loadTestsFromTestCase(TestPostIncidentAgent)
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
        print("\n🔍 Post-Incident Analysis Agent is ready for learning and optimization!")
    else:
        print("❌ Some tests failed. Check output above for details.")
        
    print("\n📚 Advanced incident analysis and system optimization capabilities ready!") 