#!/usr/bin/env python3
"""
Test script to verify graph database connection and environment setup.
"""
import asyncio
import os
import sys
from pathlib import Path

# Add the supervisor directory to path
sys.path.append(str(Path(__file__).parent / "supervisor" / "sub_agents" / "tools"))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_environment_variables():
    """Check if all required environment variables are set."""
    required_vars = {
        'NEO4J_PASSWORD': 'Neo4j database password',
        'LLM_API_KEY': 'LLM API key (Gemini)',
        'EMBEDDING_API_KEY': 'Embedding API key (Gemini)'
    }
    
    optional_vars = {
        'NEO4J_URI': 'bolt://localhost:7687',
        'NEO4J_USER': 'neo4j',
        'LLM_BASE_URL': 'https://api.openai.com/v1',
        'LLM_CHOICE': 'gemini-2.0-flash-exp',
        'EMBEDDING_MODEL': 'text-embedding-3-small',
        'VECTOR_DIMENSION': '768'
    }
    
    print("🔍 Checking environment variables...")
    
    missing_required = []
    for var, description in required_vars.items():
        value = os.getenv(var)
        if not value:
            missing_required.append(f"  ❌ {var}: {description}")
            print(f"  ❌ {var}: Not set ({description})")
        else:
            print(f"  ✅ {var}: Set")
    
    print("\n📋 Optional variables (with defaults):")
    for var, default in optional_vars.items():
        value = os.getenv(var, default)
        print(f"  ℹ️  {var}: {value}")
    
    if missing_required:
        print(f"\n❌ Missing required environment variables:")
        for var in missing_required:
            print(var)
        return False
    
    print("\n✅ All required environment variables are set!")
    return True

async def test_graph_connection():
    """Test the graph database connection."""
    try:
        print("\n🔌 Testing graph database connection...")
        
        # Import graph utilities
        from graph_utils import GraphitiClient
        
        # Create client
        client = GraphitiClient()
        
        # Test initialization
        print("  📡 Initializing Graphiti client...")
        await client.initialize()
        print("  ✅ Graphiti client initialized successfully!")
        
        # Test basic operations
        print("  📊 Getting graph statistics...")
        stats = await client.get_graph_statistics()
        print(f"  ✅ Graph statistics: {stats}")
        
        # Test search (should work even with empty graph)
        print("  🔍 Testing search functionality...")
        results = await client.search("test query")
        print(f"  ✅ Search completed, found {len(results)} results")
        
        # Close connection
        await client.close()
        print("  ✅ Connection closed successfully")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Graph connection failed: {e}")
        print(f"     Error type: {type(e).__name__}")
        
        # Provide specific guidance based on error type
        if "Unable to retrieve routing information" in str(e):
            print("\n💡 This error suggests Neo4j is not running or not accessible.")
            print("   Solutions:")
            print("   1. Start Neo4j database (see instructions above)")
            print("   2. Check NEO4J_URI in .env file")
            print("   3. Verify Neo4j is running on the specified port")
        elif "authentication" in str(e).lower():
            print("\n💡 Authentication error - check your Neo4j credentials")
            print("   - Verify NEO4J_USER and NEO4J_PASSWORD in .env file")
        elif "api" in str(e).lower() or "key" in str(e).lower():
            print("\n💡 API key error - check your LLM/Embedding API keys")
            print("   - Verify LLM_API_KEY and EMBEDDING_API_KEY in .env file")
        
        return False

async def main():
    """Main test function."""
    print("🧪 Graph Connection Test")
    print("=" * 50)
    
    # Check environment variables first
    env_ok = check_environment_variables()
    
    if not env_ok:
        print("\n❌ Environment setup incomplete. Please set missing variables.")
        return False
    
    # Test graph connection
    connection_ok = await test_graph_connection()
    
    if connection_ok:
        print("\n🎉 All tests passed! Graph builder should work now.")
        return True
    else:
        print("\n❌ Connection test failed. Please address the issues above.")
        return False

if __name__ == "__main__":
    asyncio.run(main()) 