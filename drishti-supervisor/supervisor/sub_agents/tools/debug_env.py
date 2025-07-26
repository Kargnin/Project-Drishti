#!/usr/bin/env python3
"""
Debug script to check environment variables and identify Google Cloud vs Google AI Studio conflicts.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_environment():
    """Check for problematic environment variables."""
    print("🔍 Environment Variable Debug Report")
    print("=" * 60)
    
    # Required variables for Google AI Studio
    required_vars = {
        'LLM_API_KEY': 'Gemini API key',
        'EMBEDDING_API_KEY': 'Gemini API key for embeddings'
    }
    
    # Variables that should NOT be set for Google AI Studio
    problematic_vars = {
        'LLM_BASE_URL': 'Should not be set for Google AI Studio',
        'GOOGLE_CLOUD_PROJECT': 'Only needed for Vertex AI',
        'GOOGLE_CLOUD_LOCATION': 'Only needed for Vertex AI', 
        'GOOGLE_APPLICATION_CREDENTIALS': 'Only needed for Vertex AI',
        'GENERATE_CONTENT_API': 'Only needed for Vertex AI'
    }
    
    # Optional variables
    optional_vars = {
        'LLM_CHOICE': 'gemini-2.5-flash',
        'EMBEDDING_MODEL': 'text-embedding-004',
        'VECTOR_DIMENSION': '768',
        'NEO4J_URI': 'bolt://localhost:7687',
        'NEO4J_USER': 'neo4j',
        'NEO4J_PASSWORD': 'Required for Neo4j'
    }
    
    print("\n✅ REQUIRED Variables (for Google AI Studio):")
    missing_required = []
    for var, desc in required_vars.items():
        value = os.getenv(var)
        if value:
            print(f"  ✅ {var}: Set (length: {len(value)} chars)")
        else:
            print(f"  ❌ {var}: NOT SET - {desc}")
            missing_required.append(var)
    
    print("\n❌ PROBLEMATIC Variables (should NOT be set for Google AI Studio):")
    found_problematic = []
    for var, desc in problematic_vars.items():
        value = os.getenv(var)
        if value:
            print(f"  ⚠️  {var}: SET TO '{value}' - {desc}")
            found_problematic.append((var, value))
        else:
            print(f"  ✅ {var}: Not set (correct)")
    
    print("\n📋 OPTIONAL Variables:")
    for var, default in optional_vars.items():
        value = os.getenv(var, default)
        status = "set" if os.getenv(var) else f"default ({default})"
        print(f"  ℹ️  {var}: {value} ({status})")
    
    print("\n" + "=" * 60)
    print("🔍 DIAGNOSIS:")
    print("=" * 60)
    
    if missing_required:
        print(f"❌ Missing required variables: {', '.join(missing_required)}")
    
    if found_problematic:
        print("⚠️  FOUND PROBLEMATIC VARIABLES - These are causing the Vertex AI connection attempt:")
        for var, value in found_problematic:
            print(f"   - {var}={value}")
        print("\n🔧 TO FIX: Remove these from your .env file or unset them:")
        for var, _ in found_problematic:
            print(f"   unset {var}")
            
        print(f"\n📝 Your .env file should ONLY contain:")
        print("   NEO4J_URI=bolt://localhost:7687")
        print("   NEO4J_USER=neo4j") 
        print("   NEO4J_PASSWORD=your_password")
        print("   LLM_API_KEY=your_gemini_api_key")
        print("   EMBEDDING_API_KEY=your_gemini_api_key")
        print("   LLM_CHOICE=gemini-2.5-flash")
        print("   EMBEDDING_MODEL=text-embedding-004")
        
    else:
        if not missing_required:
            print("✅ Environment looks good for Google AI Studio!")
        else:
            print("⚠️  Need to set the missing required variables")
    
    # Check for any environment variables that contain 'aiplatform' or 'vertex'
    print("\n🔍 Checking for Google Cloud/Vertex AI variables:")
    all_env_vars = dict(os.environ)
    vertex_vars = {k: v for k, v in all_env_vars.items() 
                   if 'aiplatform' in v.lower() or 'vertex' in v.lower() or 'googleapis' in v.lower()}
    
    if vertex_vars:
        print("⚠️  Found variables containing Google Cloud references:")
        for var, value in vertex_vars.items():
            print(f"   {var}={value}")
    else:
        print("✅ No Google Cloud/Vertex AI references found")

if __name__ == "__main__":
    check_environment() 