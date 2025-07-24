"""
Post-Incident Analysis Agent Usage Example

This example demonstrates how to use the Post-Incident Analysis Agent to analyze
past incidents, evaluate response effectiveness, and generate system optimization
recommendations in the Drishti Event Management System.
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Import the post incident agent
from agent import post_incident_app

async def analyze_medical_emergency_response():
    """Example: Analyze a past medical emergency response"""
    
    incident_description = """
    Analyze the medical emergency response from July 15th at main stage area.
    
    Incident Details:
    - Time: 3:45 PM during peak attendance
    - Type: Person collapsed, unconscious, possible cardiac arrest
    - Location: Front of main stage, high crowd density
    - Initial Response: Medical team deployed in 4 minutes
    - Resources Used: 2 paramedics, 1 ambulance, 4 security staff, crowd barriers
    - Communications: PA announcements in English and Spanish, area evacuation
    - Outcome: Patient stabilized and transported, area cleared successfully
    - Duration: 18 minutes total from incident to area normalization
    
    Evaluate effectiveness and identify improvement opportunities.
    """
    
    print("🔍 Analyzing Medical Emergency Response...")
    print(f"Incident: {incident_description}")
    print("\n" + "="*50)
    
    try:
        result = await post_incident_app.query(input_text=incident_description)
        
        print("📊 Post-Incident Analysis Results:")
        print(f"✅ Incident Analyzed: {result.get('incident_analyzed', 'N/A')}")
        print(f"⭐ Effectiveness Score: {result.get('effectiveness_score', 'N/A')}/10")
        print(f"🎯 Analysis Confidence: {result.get('analysis_confidence', 'N/A')}")
        print(f"🚨 Requires Escalation: {result.get('requires_escalation', 'N/A')}")
        
        print(f"\n📝 Incident Summary: {result.get('incident_summary', 'N/A')}")
        
        if result.get('detailed_evaluation'):
            eval_data = result['detailed_evaluation']
            print(f"\n🔍 Detailed Evaluation:")
            
            categories = ['response_timeliness', 'resource_allocation', 'communication_effectiveness', 
                         'coordination_quality', 'outcome_achievement']
            
            for category in categories:
                if category in eval_data:
                    cat_data = eval_data[category]
                    print(f"\n  📈 {category.replace('_', ' ').title()}:")
                    print(f"     Score: {cat_data.get('score', 'N/A')}/10")
                    print(f"     Assessment: {cat_data.get('assessment', 'N/A')}")
                    
                    improvements = cat_data.get('improvement_areas') or cat_data.get('optimization_opportunities') or cat_data.get('enhancement_suggestions') or cat_data.get('workflow_improvements') or cat_data.get('success_factors', [])
                    if improvements:
                        print(f"     Improvements: {improvements}")
        
        if result.get('instruction_compliance'):
            compliance = result['instruction_compliance']
            print(f"\n📋 Instruction Compliance:")
            print(f"   Instructions Followed: {compliance.get('instructions_followed', 'N/A')}")
            print(f"   Compliance Score: {compliance.get('compliance_score', 'N/A')}/10")
            print(f"   Deviation Analysis: {compliance.get('deviation_analysis', 'N/A')}")
            if compliance.get('compliance_gaps'):
                print(f"   Compliance Gaps: {compliance['compliance_gaps']}")
        
        if result.get('recommendations'):
            recommendations = result['recommendations']
            print(f"\n💡 Recommendations:")
            for rec_type, actions in recommendations.items():
                if actions:
                    print(f"   {rec_type.replace('_', ' ').title()}: {actions}")
                
    except Exception as e:
        print(f"❌ Error analyzing medical emergency: {e}")

async def analyze_security_incident_patterns():
    """Example: Analyze patterns in security incidents"""
    
    pattern_analysis_request = """
    Analyze security incident patterns from the past 6 months of events.
    
    Historical Data Summary:
    - Total Security Incidents: 45 across 12 events
    - Types: Unauthorized access (15), disturbances (12), threats (8), theft (7), other (3)
    - Peak Times: 8-10 PM during main performances, 2-4 AM during late events
    - Common Locations: Parking areas (18), entrance gates (12), backstage (8), vendor areas (7)
    - Response Times: Average 6.2 minutes, Range 2-15 minutes
    - Resolution Success: 89% successfully resolved without escalation
    - Resource Usage: Security teams, local police coordination, communication systems
    
    Identify patterns, predict future risks, and recommend optimizations.
    """
    
    print("🔍 Analyzing Security Incident Patterns...")
    print(f"Analysis Request: {pattern_analysis_request}")
    print("\n" + "="*50)
    
    try:
        result = await post_incident_app.query(input_text=pattern_analysis_request)
        
        print("📈 Pattern Recognition Analysis:")
        print(f"⭐ Effectiveness Score: {result.get('effectiveness_score', 'N/A')}/10")
        print(f"🎯 Analysis Confidence: {result.get('analysis_confidence', 'N/A')}")
        
        if result.get('pattern_identification'):
            patterns = result['pattern_identification']
            print(f"\n🔍 Pattern Identification:")
            print(f"   Recurring Patterns: {patterns.get('recurring_patterns', 'N/A')}")
            print(f"   Trend Analysis: {patterns.get('trend_analysis', 'N/A')}")
            print(f"   Risk Indicators: {patterns.get('risk_indicators', 'N/A')}")
            print(f"   Predictive Insights: {patterns.get('predictive_insights', 'N/A')}")
        
        if result.get('system_optimization'):
            optimization = result['system_optimization']
            print(f"\n⚙️ System Optimization:")
            print(f"   Training Data: {optimization.get('training_data_generated', 'N/A')}")
            print(f"   Model Improvements: {optimization.get('model_improvements', 'N/A')}")
            print(f"   Process Optimizations: {optimization.get('process_optimizations', 'N/A')}")
            print(f"   System Enhancements: {optimization.get('system_enhancements', 'N/A')}")
        
        if result.get('lessons_learned'):
            lessons = result['lessons_learned']
            print(f"\n📚 Lessons Learned:")
            print(f"   Key Insights: {lessons.get('key_insights', 'N/A')}")
            print(f"   Best Practices: {lessons.get('best_practices', 'N/A')}")
            print(f"   Failure Modes: {lessons.get('failure_modes', 'N/A')}")
            print(f"   Prevention Strategies: {lessons.get('prevention_strategies', 'N/A')}")
                
    except Exception as e:
        print(f"❌ Error analyzing security patterns: {e}")

async def evaluate_communication_effectiveness():
    """Example: Evaluate communication effectiveness across incidents"""
    
    communication_evaluation = """
    Evaluate communication effectiveness during weather emergency evacuation on August 22nd.
    
    Communication Details:
    - Incident: Severe thunderstorm warning, 30-minute advance notice
    - Languages Used: English, Spanish, French (primary event languages)
    - Channels: PA system, mobile app, digital displays, staff radios
    - Messages Sent: 12 announcements over 25 minutes
    - Target Audience: 15,000 attendees across festival grounds
    - Response Measured: 85% moved to covered areas within 20 minutes
    - Compliance Issues: Some confusion at remote food vendor areas
    - Staff Coordination: 90% of staff followed evacuation procedures
    - Technology Performance: PA system had intermittent issues in Zone C
    
    Assess instruction compliance and communication clarity effectiveness.
    """
    
    print("📢 Evaluating Communication Effectiveness...")
    print(f"Evaluation Request: {communication_evaluation}")
    print("\n" + "="*50)
    
    try:
        result = await post_incident_app.query(input_text=communication_evaluation)
        
        print("📊 Communication Effectiveness Analysis:")
        print(f"⭐ Effectiveness Score: {result.get('effectiveness_score', 'N/A')}/10")
        print(f"🎯 Analysis Confidence: {result.get('analysis_confidence', 'N/A')}")
        
        if result.get('detailed_evaluation') and result['detailed_evaluation'].get('communication_effectiveness'):
            comm_eval = result['detailed_evaluation']['communication_effectiveness']
            print(f"\n📢 Communication Assessment:")
            print(f"   Score: {comm_eval.get('score', 'N/A')}/10")
            print(f"   Assessment: {comm_eval.get('assessment', 'N/A')}")
            print(f"   Enhancement Suggestions: {comm_eval.get('enhancement_suggestions', 'N/A')}")
        
        if result.get('instruction_compliance'):
            compliance = result['instruction_compliance']
            print(f"\n📋 Instruction Compliance Analysis:")
            print(f"   Instructions Followed: {compliance.get('instructions_followed', 'N/A')}")
            print(f"   Compliance Score: {compliance.get('compliance_score', 'N/A')}/10")
            print(f"   Deviation Analysis: {compliance.get('deviation_analysis', 'N/A')}")
        
        if result.get('benchmarking'):
            benchmark = result['benchmarking']
            print(f"\n📊 Benchmarking Results:")
            print(f"   Industry Comparison: {benchmark.get('industry_comparison', 'N/A')}")
            print(f"   Historical Comparison: {benchmark.get('historical_comparison', 'N/A')}")
            print(f"   Performance Metrics: {benchmark.get('performance_metrics', 'N/A')}")
                
    except Exception as e:
        print(f"❌ Error evaluating communication: {e}")

async def test_analysis_scenarios():
    """Test different post-incident analysis scenarios"""
    
    scenarios = [
        {
            "name": "Infrastructure Failure Analysis",
            "description": "Power outage affected vendor area for 45 minutes. Backup generators deployed in 8 minutes. Vendors lost estimated $3,000 in sales. Communication sent to attendees about temporary disruption.",
            "expected_score_range": (6, 8)
        },
        {
            "name": "Crowd Control Success",
            "description": "VIP arrival caused crowd surge at entrance. Security quickly deployed barriers and redirected flow. No injuries, minimal delays, excellent crowd management and communication.",
            "expected_score_range": (8, 10)
        },
        {
            "name": "Food Safety Incident",
            "description": "Food poisoning reports from vendor. Health department notified, vendor closed within 30 minutes. 15 people affected, all treated. Clear communication prevented panic.",
            "expected_score_range": (7, 9)
        },
        {
            "name": "Weather Response Delay",
            "description": "Rain started before evacuation completed. Delayed weather monitoring caused 10-minute response delay. Some attendees got wet, minor equipment damage occurred.",
            "expected_score_range": (4, 6)
        },
        {
            "name": "Lost Child Resolution",
            "description": "Child lost for 90 minutes during peak hours. Security and PA announcements used. Family reunited safely. Took longer than optimal due to crowd density.",
            "expected_score_range": (5, 7)
        }
    ]
    
    for scenario in scenarios:
        print(f"\n🧪 Testing Analysis Scenario: {scenario['name']}")
        print("="*60)
        
        try:
            result = await post_incident_app.query(input_text=scenario['description'])
            
            effectiveness_score = result.get('effectiveness_score', 0)
            print(f"⭐ Effectiveness Score: {effectiveness_score}/10")
            print(f"🎯 Analysis Confidence: {result.get('analysis_confidence', 'N/A')}")
            print(f"✅ Incident Analyzed: {result.get('incident_analyzed', 'N/A')}")
            
            # Check if score is in expected range
            expected_min, expected_max = scenario['expected_score_range']
            if expected_min <= effectiveness_score <= expected_max:
                print(f"✅ Score within expected range ({expected_min}-{expected_max})")
            else:
                print(f"⚠️ Score outside expected range ({expected_min}-{expected_max})")
            
            # Show key recommendations
            if result.get('recommendations') and result['recommendations'].get('immediate_actions'):
                print(f"💡 Immediate Actions: {result['recommendations']['immediate_actions']}")
            
            # Show compliance score
            if result.get('instruction_compliance'):
                compliance_score = result['instruction_compliance'].get('compliance_score', 'N/A')
                print(f"📋 Compliance Score: {compliance_score}/10")
            
        except Exception as e:
            print(f"❌ Error: {e}")

async def generate_optimization_recommendations():
    """Example: Generate system optimization recommendations"""
    
    print("\n⚙️ Testing System Optimization Scenarios")
    print("="*60)
    
    optimization_scenarios = [
        "Analyze overall system performance for the past quarter. Response times have improved 15% but resource utilization shows inefficiencies in staff deployment.",
        "Multiple incidents show communication delays in non-English speaking areas. Pattern suggests need for enhanced translation capabilities and cultural adaptation.",
        "Emergency medical responses are consistently effective, but resource allocation could be optimized based on event type and expected attendance.",
        "Security incident prevention has improved, but post-incident coordination between agents shows room for workflow optimization."
    ]
    
    for i, scenario in enumerate(optimization_scenarios, 1):
        print(f"\n⚙️ Optimization Scenario {i}: {scenario}")
        print("-" * 40)
        
        try:
            result = await post_incident_app.query(input_text=scenario)
            
            print(f"⭐ Effectiveness: {result.get('effectiveness_score', 'N/A')}/10")
            
            if result.get('system_optimization'):
                optimization = result['system_optimization']
                print(f"🔧 Process Optimizations: {optimization.get('process_optimizations', 'N/A')}")
                print(f"💡 System Enhancements: {optimization.get('system_enhancements', 'N/A')}")
            
            if result.get('recommendations'):
                recommendations = result['recommendations']
                if recommendations.get('short_term_improvements'):
                    print(f"📅 Short-term Improvements: {recommendations['short_term_improvements']}")
                if recommendations.get('long_term_optimizations'):
                    print(f"🎯 Long-term Optimizations: {recommendations['long_term_optimizations']}")
            
        except Exception as e:
            print(f"❌ Error analyzing optimization scenario: {e}")

async def benchmark_performance():
    """Example: Benchmark system performance"""
    
    benchmarking_request = """
    Benchmark our event management system performance against industry standards.
    
    Current Performance:
    - Average Response Time: 5.2 minutes (Emergency: 3.1 min, Non-emergency: 7.3 min)
    - Resolution Success Rate: 92%
    - Resource Utilization Efficiency: 78%
    - Communication Reach: 89% of target audience
    - Staff Instruction Compliance: 85%
    - Incident Prevention Rate: 67% (proactive identification)
    - Stakeholder Satisfaction: 4.2/5.0
    
    Compare against industry best practices and provide improvement roadmap.
    """
    
    print("\n📊 Benchmarking System Performance...")
    print(f"Benchmarking Request: {benchmarking_request}")
    print("\n" + "="*50)
    
    try:
        result = await post_incident_app.query(input_text=benchmarking_request)
        
        print("📊 Performance Benchmarking Results:")
        print(f"⭐ Effectiveness Score: {result.get('effectiveness_score', 'N/A')}/10")
        
        if result.get('benchmarking'):
            benchmark = result['benchmarking']
            print(f"\n📈 Benchmarking Analysis:")
            print(f"   Industry Comparison: {benchmark.get('industry_comparison', 'N/A')}")
            print(f"   Historical Comparison: {benchmark.get('historical_comparison', 'N/A')}")
            print(f"   Performance Metrics: {benchmark.get('performance_metrics', 'N/A')}")
        
        if result.get('recommendations'):
            recommendations = result['recommendations']
            print(f"\n🎯 Improvement Roadmap:")
            for rec_category, actions in recommendations.items():
                if actions and rec_category != 'training_recommendations':
                    print(f"   {rec_category.replace('_', ' ').title()}: {actions}")
                    
    except Exception as e:
        print(f"❌ Error benchmarking performance: {e}")

async def main():
    """Main example function"""
    print("🔍 Post-Incident Analysis Agent Usage Examples")
    print("="*60)
    
    # Test medical emergency analysis
    await analyze_medical_emergency_response()
    print("\n" + "="*60)
    
    # Test security pattern analysis
    await analyze_security_incident_patterns()
    print("\n" + "="*60)
    
    # Test communication effectiveness
    await evaluate_communication_effectiveness()
    print("\n" + "="*60)
    
    # Test different analysis scenarios
    await test_analysis_scenarios()
    print("\n" + "="*60)
    
    # Test optimization recommendations
    await generate_optimization_recommendations()
    print("\n" + "="*60)
    
    # Test performance benchmarking
    await benchmark_performance()
    
    print("\n✅ All post-incident analysis examples completed!")
    print("\n🔍 Advanced learning and optimization capabilities ready!")

if __name__ == "__main__":
    # Run the examples
    asyncio.run(main()) 