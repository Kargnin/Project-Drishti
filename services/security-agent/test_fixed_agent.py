"""
Simple test script to verify the fixed security agent works correctly
"""

import asyncio
import os
from pathlib import Path

# Set environment variables if not already set
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "TRUE")
os.environ.setdefault("PROJECT_ID", "noted-throne-466513-v6")
os.environ.setdefault("LOCATION", "us-central1")
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "noted-throne-466513-v6")
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")

def test_agent_import():
    """Test that we can import the security agent without errors"""
    try:
        from agent import security_app, security_agent
        print("✅ Successfully imported security_app and security_agent")
        print(f"   - Agent name: {security_agent.name}")
        print(f"   - Agent model: {security_agent.model}")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error importing agent: {e}")
        return False

def test_simple_query():
    """Test a simple query to the security agent"""
    try:
        from agent import security_app
        
        print("\n🔍 Testing simple security query...")
        
        test_message = "Someone reported a suspicious person near the main entrance with a large backpack"
        
        # Get response from agent
        response_text = ""
        for event in security_app.stream_query(
            user_id="test_user",
            message=test_message
        ):
            if hasattr(event, 'content') and hasattr(event.content, 'parts'):
                for part in event.content.parts:
                    if hasattr(part, 'text'):
                        response_text += part.text
        
        if response_text:
            print(f"✅ Agent responded successfully")
            print(f"   Query: {test_message}")
            print(f"   Response: {response_text[:200]}...")
            return True
        else:
            print("❌ Agent returned empty response")
            return False
            
    except Exception as e:
        print(f"❌ Error testing query: {e}")
        return False

async def main():
    """Run all tests"""
    print("🛡️ Testing Fixed Security Agent")
    print("=" * 50)
    
    # Test 1: Import
    import_success = test_agent_import()
    
    if import_success:
        # Test 2: Simple query
        query_success = test_simple_query()
        
        if query_success:
            print("\n✅ All tests passed! The security agent is working correctly.")
            print("\n📋 Summary of fixes:")
            print("  ✓ Updated agent.py to use AdkApp wrapper")
            print("  ✓ Fixed usage_example.py to use stream_query instead of generate_async")
            print("  ✓ Added necessary imports and environment setup")
            print("  ✓ Updated dependencies in pyproject.toml")
        else:
            print("\n⚠️ Agent import successful but query failed")
    else:
        print("\n❌ Agent import failed - check dependencies and environment")

if __name__ == "__main__":
    asyncio.run(main()) 