#!/usr/bin/env python3
"""
Debug script to show what environment variables are being loaded.
"""
import os
print("🔍 BEFORE loading .env:")
print(f"GOOGLE_CLOUD_PROJECT: {os.getenv('GOOGLE_CLOUD_PROJECT', 'NOT SET')}")
print(f"LLM_CHOICE: {os.getenv('LLM_CHOICE', 'NOT SET')}")

# Load .env file
from dotenv import load_dotenv
load_dotenv()

print("\n🔍 AFTER loading .env:")
print(f"GOOGLE_CLOUD_PROJECT: {os.getenv('GOOGLE_CLOUD_PROJECT', 'NOT SET')}")
print(f"LLM_CHOICE: {os.getenv('LLM_CHOICE', 'NOT SET')}")
print(f"GOOGLE_CLOUD_LOCATION: {os.getenv('GOOGLE_CLOUD_LOCATION', 'NOT SET')}")

print("\n📂 .env file location:")
if os.path.exists('.env'):
    print("✅ .env file found in current directory")
else:
    print("❌ .env file NOT found in current directory")

print("\n🚨 THE ISSUE:")
project = os.getenv('GOOGLE_CLOUD_PROJECT')
if project == 'profound-jet-466507-a1':
    print("❌ FOUND THE PROBLEM: .env file contains wrong project!")
    print("   Your .env file has: GOOGLE_CLOUD_PROJECT=profound-jet-466507-a1")
    print("   Should be: GOOGLE_CLOUD_PROJECT=eventide-intel-jn8fi")
elif project == 'eventide-intel-jn8fi':
    print("✅ Project is correct in .env")
else:
    print(f"⚠️  Unexpected project: {project}")

model = os.getenv('LLM_CHOICE')
if model == 'gemini-2.5-flash':
    print("❌ FOUND THE PROBLEM: .env file contains wrong model!")
    print("   Your .env file has: LLM_CHOICE=gemini-2.5-flash")
    print("   Should be: LLM_CHOICE=gemini-1.5-flash")
elif model == 'gemini-1.5-flash':
    print("✅ Model is correct in .env")
else:
    print(f"⚠️  Model in .env: {model}") 