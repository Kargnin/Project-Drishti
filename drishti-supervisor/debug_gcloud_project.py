#!/usr/bin/env python3
"""
Debug script to identify which Google Cloud project is being used and why.
"""
import os
import subprocess
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_project_sources():
    """Check all possible sources of Google Cloud project configuration."""
    print("🔍 Google Cloud Project Debug Report")
    print("=" * 60)
    
    # 1. Check .env file
    env_project = os.getenv("GOOGLE_CLOUD_PROJECT")
    print(f"1. GOOGLE_CLOUD_PROJECT in .env: {env_project}")
    
    # 2. Check gcloud config
    try:
        result = subprocess.run(['gcloud', 'config', 'get-value', 'project'], 
                              capture_output=True, text=True, check=True)
        gcloud_project = result.stdout.strip()
        print(f"2. gcloud config project: {gcloud_project}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("2. gcloud config project: NOT SET or gcloud not found")
        gcloud_project = None
    
    # 3. Check application default credentials
    try:
        result = subprocess.run(['gcloud', 'auth', 'application-default', 'print-access-token'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("3. Application Default Credentials: ✅ ACTIVE")
            
            # Try to get project from ADC
            try:
                result = subprocess.run(['gcloud', 'config', 'list', '--format=json'], 
                                      capture_output=True, text=True, check=True)
                config_data = json.loads(result.stdout)
                adc_project = None
                for account in config_data.get('credentialed_accounts', []):
                    if account.get('status') == 'ACTIVE':
                        adc_project = account.get('project')
                        break
                print(f"   ADC active project: {adc_project}")
            except:
                print("   ADC project: Could not determine")
        else:
            print("3. Application Default Credentials: ❌ NOT SET")
    except FileNotFoundError:
        print("3. Application Default Credentials: gcloud not found")
    
    # 4. Check GOOGLE_APPLICATION_CREDENTIALS
    cred_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if cred_file:
        print(f"4. GOOGLE_APPLICATION_CREDENTIALS: {cred_file}")
        if os.path.exists(cred_file):
            try:
                with open(cred_file, 'r') as f:
                    cred_data = json.load(f)
                    sa_project = cred_data.get('project_id')
                    print(f"   Service Account project: {sa_project}")
            except Exception as e:
                print(f"   Error reading credentials: {e}")
        else:
            print("   ❌ File does not exist!")
    else:
        print("4. GOOGLE_APPLICATION_CREDENTIALS: Not set")
    
    # 5. Check current active account
    try:
        result = subprocess.run(['gcloud', 'auth', 'list', '--filter=status:ACTIVE', '--format=value(account)'], 
                              capture_output=True, text=True, check=True)
        active_account = result.stdout.strip()
        print(f"5. Active gcloud account: {active_account}")
    except:
        print("5. Active gcloud account: Could not determine")
    
    print("\n" + "=" * 60)
    print("🔍 ISSUE ANALYSIS:")
    
    if env_project and gcloud_project and env_project != gcloud_project:
        print(f"❌ MISMATCH: .env has '{env_project}' but gcloud config has '{gcloud_project}'")
        print("   Solution: Run 'gcloud config set project YOUR_PROJECT_ID'")
    elif not env_project:
        print("❌ GOOGLE_CLOUD_PROJECT not set in .env file")
    elif not gcloud_project:
        print("❌ gcloud project not configured")
        print("   Solution: Run 'gcloud config set project YOUR_PROJECT_ID'")
    else:
        print("✅ Project settings appear consistent")
    
    print("\n📋 RECOMMENDED FIX:")
    if env_project:
        print(f"Run this command: gcloud config set project {env_project}")
    else:
        print("1. Set GOOGLE_CLOUD_PROJECT in your .env file")
        print("2. Run: gcloud config set project YOUR_PROJECT_ID")

if __name__ == "__main__":
    check_project_sources() 