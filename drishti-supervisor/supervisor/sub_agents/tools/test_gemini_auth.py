#!/usr/bin/env python3
"""
Simple test script to verify Gemini authentication and configuration.
"""
import os
import sys
from dotenv import load_dotenv
from graphiti_core.llm_client.config import LLMConfig
from graphiti_core.llm_client.gemini_client import GeminiClient
from graphiti_core.embedder.gemini import GeminiEmbedder, GeminiEmbedderConfig

# Load environment variables
load_dotenv()

def test_environment_variables():
    """Test if all required environment variables are set."""
    print("🔍 Testing environment variables...")
    
    required_vars = {
        'LLM_API_KEY': 'Gemini API key for LLM',
        'EMBEDDING_API_KEY': 'Gemini API key for embeddings'
    }
    
    missing_vars = []
    for var, description in required_vars.items():
        value = os.getenv(var)
        if not value:
            missing_vars.append(f"  ❌ {var}: {description}")
            print(f"  ❌ {var}: Not set ({description})")
        else:
            print(f"  ✅ {var}: Set (length: {len(value)} chars)")
    
    if missing_vars:
        print(f"\n❌ Missing required environment variables:")
        for var in missing_vars:
            print(var)
        return False
    
    print("\n✅ All required environment variables are set!")
    return True

def test_llm_config():
    """Test LLM configuration."""
    print("\n🤖 Testing LLM configuration...")
    
    try:
        llm_config = LLMConfig(
            api_key=os.getenv("LLM_API_KEY"),
            model=os.getenv("LLM_CHOICE", "gemini-2.5-flash"),
        )
        print(f"  ✅ LLMConfig created successfully")
        print(f"  📝 Model: {llm_config.model}")
        return llm_config
    except Exception as e:
        print(f"  ❌ Failed to create LLMConfig: {e}")
        return None

def test_llm_client(llm_config):
    """Test LLM client creation."""
    print("\n🚀 Testing LLM client...")
    
    try:
        llm_client = GeminiClient(config=llm_config)
        print(f"  ✅ GeminiClient created successfully")
        return llm_client
    except Exception as e:
        print(f"  ❌ Failed to create GeminiClient: {e}")
        return None

def test_embedder_config():
    """Test embedding configuration."""
    print("\n🔤 Testing embedding configuration...")
    
    try:
        embedder_config = GeminiEmbedderConfig(
            api_key=os.getenv("EMBEDDING_API_KEY"),
            embedding_model=os.getenv("EMBEDDING_MODEL", "text-embedding-004"),
            embedding_dim=int(os.getenv("VECTOR_DIMENSION", "768")),
        )
        print(f"  ✅ GeminiEmbedderConfig created successfully")
        print(f"  📝 Model: {embedder_config.embedding_model}")
        print(f"  📏 Dimensions: {embedder_config.embedding_dim}")
        return embedder_config
    except Exception as e:
        print(f"  ❌ Failed to create GeminiEmbedderConfig: {e}")
        return None

def test_embedder(embedder_config):
    """Test embedder creation."""
    print("\n🎯 Testing embedder...")
    
    try:
        embedder = GeminiEmbedder(config=embedder_config)
        print(f"  ✅ GeminiEmbedder created successfully")
        return embedder
    except Exception as e:
        print(f"  ❌ Failed to create GeminiEmbedder: {e}")
        return None

def main():
    """Main test function."""
    print("=" * 60)
    print("🔬 Gemini Authentication Test")
    print("=" * 60)
    
    # Test environment variables
    if not test_environment_variables():
        print("\n❌ Environment variable test failed!")
        sys.exit(1)
    
    # Test LLM configuration
    llm_config = test_llm_config()
    if not llm_config:
        print("\n❌ LLM configuration test failed!")
        sys.exit(1)
    
    # Test LLM client
    llm_client = test_llm_client(llm_config)
    if not llm_client:
        print("\n❌ LLM client test failed!")
        sys.exit(1)
    
    # Test embedder configuration
    embedder_config = test_embedder_config()
    if not embedder_config:
        print("\n❌ Embedder configuration test failed!")
        sys.exit(1)
    
    # Test embedder
    embedder = test_embedder(embedder_config)
    if not embedder:
        print("\n❌ Embedder test failed!")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 All tests passed! Your Gemini configuration is working correctly.")
    print("✅ You should now be able to use the GraphitiClient successfully.")
    print("=" * 60)

if __name__ == "__main__":
    main() 