#!/usr/bin/env python3
"""
Quick check for problematic environment variables that cause Vertex AI connections.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_problematic_vars():
    """Check for variables that cause Vertex AI connection attempts."""
    problematic_vars = [
        'LLM_BASE_URL',
        'GOOGLE_CLOUD_PROJECT', 
        'GOOGLE_CLOUD_LOCATION',
        'GOOGLE_APPLICATION_CREDENTIALS',
        'GENERATE_CONTENT_API'
    ]
    
    found_problematic = []
    for var in problematic_vars:
        value = os.getenv(var)
        if value:
            found_problematic.append(f"{var}={value}")
    
    if found_problematic:
        print("❌ FOUND PROBLEMATIC VARIABLES - Remove these from your .env file:")
        for var in found_problematic:
            print(f"   {var}")
        print("\n🔧 To fix: Comment out or remove these lines from your .env file")
        return False
    else:
        print("✅ No problematic variables found!")
        return True

if __name__ == "__main__":
    print("🔍 Checking for variables that cause Vertex AI connection attempts...")
    check_problematic_vars() 