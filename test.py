import requests
import time
from datetime import datetime

print("Starting job check...")

# Test Amazon jobs website
url = "https://www.amazon.jobs/en/search?base_query=energy&loc_query=United+States"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

try:
    print("Attempting to fetch jobs...")
    response = requests.get(url, headers=headers)
    print(f"Response status: {response.status_code}")
    print(f"Response length: {len(response.text)}")
    print("Job check completed successfully!")
except Exception as e:
    print(f"Error occurred: {str(e)}")
