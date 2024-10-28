import requests
import time
from datetime import datetime
import sys

# Force Python to flush print statements immediately
sys.stdout.reconfigure(line_buffering=True)

print("==========================================")
print(f"Script started at: {datetime.now()}")
print("==========================================")

# Test Amazon jobs website
print("\n1. Setting up request...")
url = "https://www.amazon.jobs/en/search?base_query=energy&loc_query=United+States"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

try:
    print("\n2. Making request to Amazon jobs...")
    print(f"URL: {url}")
    
    response = requests.get(url, headers=headers)
    
    print("\n3. Response received:")
    print(f"Status code: {response.status_code}")
    print(f"Response size: {len(response.text)} characters")
    
    if response.status_code == 200:
        print("\n4. Successfully connected to Amazon jobs!")
        
        # Look for job listings in the response
        if 'energy' in response.text.lower():
            print("Found 'energy' keyword in response!")
        else:
            print("Keyword 'energy' not found in response")
            
        if 'job-title' in response.text.lower():
            print("Found job listings in response!")
        else:
            print("No job listings found in response")
    else:
        print(f"\nError: Received status code {response.status_code}")
        
    print("\n5. Saving sample of response:")
    print("First 500 characters of response:")
    print("-" * 50)
    print(response.text[:500])
    print("-" * 50)

except Exception as e:
    print("\nERROR OCCURRED:")
    print(f"Type: {type(e).__name__}")
    print(f"Message: {str(e)}")

print("\n==========================================")
print(f"Script finished at: {datetime.now()}")
print("==========================================")
