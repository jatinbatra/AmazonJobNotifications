import os
import sys
print("=== Starting Debug Script ===")

# 1. Check Python version
print(f"Python Version: {sys.version}")

# 2. Check current directory
print(f"Current Directory: {os.getcwd()}")
print("Directory contents:")
print(os.listdir())

# 3. Check environment variables
print("\nChecking environment variables:")
email = os.getenv('EMAIL_ADDRESS')
password = os.getenv('EMAIL_PASSWORD')

if not email:
    print("ERROR: EMAIL_ADDRESS is not set")
    sys.exit(1)
if not password:
    print("ERROR: EMAIL_PASSWORD is not set")
    sys.exit(1)

print("Environment variables are set correctly")

# 4. Test imports
print("\nTesting imports:")
try:
    import requests
    print("✓ requests imported")
    import beautifulsoup4
    print("✓ beautifulsoup4 imported")
except ImportError as e:
    print(f"ERROR importing: {str(e)}")
    sys.exit(1)

# 5. Test basic request
print("\nTesting web request:")
try:
    response = requests.get('https://www.amazon.jobs')
    print(f"Response status code: {response.status_code}")
except Exception as e:
    print(f"ERROR making request: {str(e)}")
    sys.exit(1)

print("\n=== Debug Script Completed Successfully ===")
