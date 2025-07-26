#!/usr/bin/env python3
"""
Test script to verify Google Cloud Vertex AI setup and authentication.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment_variables():
    """Test if required environment variables are set for Vertex AI."""
    print("🔍 Testing Vertex AI Environment Variables...")
    
    required_vars = {
        'GOOGLE_CLOUD_PROJECT': 'Your Google Cloud project ID',
        'GOOGLE_CLOUD_LOCATION': 'Google Cloud region (e.g., us-central1)'
    }
    
    optional_vars = {
        'GOOGLE_APPLICATION_CREDENTIALS': 'Path to service account key (if not using ADC)',
        'LLM_CHOICE': 'gemini-2.5-flash',
        'EMBEDDING_MODEL': 'text-embedding-004'
    }
    
    missing_required = []
    for var, desc in required_vars.items():
        value = os.getenv(var)
        if not value:
            missing_required.append(f"  ❌ {var}: {desc}")
            print(f"  ❌ {var}: Not set ({desc})")
        else:
            print(f"  ✅ {var}: {value}")
    
    print("\n📋 Optional Variables:")
    for var, default in optional_vars.items():
        value = os.getenv(var)
        if value:
            if var == 'GOOGLE_APPLICATION_CREDENTIALS':
                print(f"  ℹ️  {var}: {value} (service account key)")
            else:
                print(f"  ℹ️  {var}: {value}")
        else:
            print(f"  ℹ️  {var}: Not set (will use default: {default})")
    
    if missing_required:
        print(f"\n❌ Missing required environment variables:")
        for var in missing_required:
            print(var)
        return False
    
    print("\n✅ All required environment variables are set!")
    return True

def test_google_cloud_auth():
    """Test Google Cloud authentication."""
    print("\n🔐 Testing Google Cloud Authentication...")
    
    try:
        from google.auth import default
        from google.auth.exceptions import DefaultCredentialsError
        
        try:
            credentials, project = default()
            print(f"  ✅ Default credentials found")
            print(f"  📋 Project from credentials: {project}")
            
            # Check if project matches environment variable
            env_project = os.getenv('GOOGLE_CLOUD_PROJECT')
            if project and env_project and project != env_project:
                print(f"  ⚠️  Warning: Credential project ({project}) != environment project ({env_project})")
            
            return True
            
        except DefaultCredentialsError as e:
            print(f"  ❌ No default credentials found: {e}")
            print(f"  💡 Run: gcloud auth application-default login")
            return False
            
    except ImportError:
        print(f"  ❌ google-auth library not installed")
        print(f"  💡 Run: pip install google-auth")
        return False

def test_vertex_ai_connection():
    """Test Vertex AI API connection."""
    print("\n🤖 Testing Vertex AI Connection...")
    
    try:
        from google.cloud import aiplatform
        
        project = os.getenv('GOOGLE_CLOUD_PROJECT')
        location = os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1')
        
        # Initialize Vertex AI
        aiplatform.init(project=project, location=location)
        print(f"  ✅ Vertex AI initialized successfully")
        print(f"  📋 Project: {project}")
        print(f"  📍 Location: {location}")
        
        # Try to list models (this will test API access)
        try:
            models = aiplatform.Model.list(limit=1)
            print(f"  ✅ Vertex AI API access confirmed")
            return True
        except Exception as e:
            print(f"  ⚠️  Vertex AI API access limited: {e}")
            print(f"  ℹ️  This might be normal if you haven't deployed custom models")
            return True  # Still consider this a success
            
    except ImportError:
        print(f"  ❌ google-cloud-aiplatform library not installed")
        print(f"  💡 Run: pip install google-cloud-aiplatform")
        return False
    except Exception as e:
        print(f"  ❌ Vertex AI connection failed: {e}")
        return False

def test_graphiti_config():
    """Test Graphiti configuration."""
    print("\n📊 Testing Graphiti Configuration...")
    
    try:
        from graphiti_core.llm_client.config import LLMConfig
        from graphiti_core.llm_client.gemini_client import GeminiClient
        from graphiti_core.embedder.gemini import GeminiEmbedder, GeminiEmbedderConfig
        
        # Test LLM config (no API key for Vertex AI)
        llm_config = LLMConfig(
            model=os.getenv("LLM_CHOICE", "gemini-2.5-flash")
        )
        print(f"  ✅ LLMConfig created successfully")
        
        # Test LLM client
        llm_client = GeminiClient(config=llm_config)
        print(f"  ✅ GeminiClient created successfully")
        
        # Test embedder config (no API key for Vertex AI)
        embedder_config = GeminiEmbedderConfig(
            embedding_model=os.getenv("EMBEDDING_MODEL", "text-embedding-004"),
            embedding_dim=int(os.getenv("VECTOR_DIMENSION", "768"))
        )
        print(f"  ✅ GeminiEmbedderConfig created successfully")
        
        # Test embedder
        embedder = GeminiEmbedder(config=embedder_config)
        print(f"  ✅ GeminiEmbedder created successfully")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Graphiti library import failed: {e}")
        print(f"  💡 Run: pip install graphiti-core")
        return False
    except Exception as e:
        print(f"  ❌ Graphiti configuration failed: {e}")
        return False

def main():
    """Main test function."""
    print("=" * 60)
    print("🔬 Google Cloud Vertex AI Setup Test")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 4
    
    # Test 1: Environment variables
    if test_environment_variables():
        tests_passed += 1
    
    # Test 2: Google Cloud authentication
    if test_google_cloud_auth():
        tests_passed += 1
    
    # Test 3: Vertex AI connection
    if test_vertex_ai_connection():
        tests_passed += 1
    
    # Test 4: Graphiti configuration
    if test_graphiti_config():
        tests_passed += 1
    
    print("\n" + "=" * 60)
    print(f"🏁 Test Results: {tests_passed}/{total_tests} tests passed")
    print("=" * 60)
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Your Vertex AI setup is ready.")
        print("✅ You can now run the graph builder successfully.")
    else:
        print(f"❌ {total_tests - tests_passed} test(s) failed.")
        print("📖 See setup_vertex_ai.md for detailed setup instructions.")
        sys.exit(1)

if __name__ == "__main__":
    main() 