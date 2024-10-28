import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import os
import sys

def check_environment_variables():
    """Check if all required environment variables are set"""
    required_vars = ['EMAIL_ADDRESS', 'EMAIL_PASSWORD', 'LINKEDIN_EMAIL', 'LINKEDIN_PASSWORD']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        print(f"ERROR: Missing required environment variables: {', '.join(missing_vars)}")
        return False
    return True

def simple_test():
    """Run a simple test of core functionality"""
    print("Starting simple test...")
    
    # Test environment variables
    if not check_environment_variables():
        sys.exit(1)
    
    # Test web request
    try:
        print("Testing connection to Amazon jobs...")
        url = "https://www.amazon.jobs/en/search?base_query=product+manager&loc_query=United+States"
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        print(f"Amazon jobs response status: {response.status_code}")
        
        if response.status_code != 200:
            print("ERROR: Failed to connect to Amazon jobs website")
            sys.exit(1)
            
        # Test BeautifulSoup parsing
        soup = BeautifulSoup(response.text, 'html.parser')
        jobs = soup.find_all('div', class_='job-tile')
        print(f"Found {len(jobs)} job listings in test search")
        
        # Test email setup
        import smtplib
        print("Testing email connection...")
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            try:
                server.login(os.getenv('EMAIL_ADDRESS'), os.getenv('EMAIL_PASSWORD'))
                print("Email login successful")
            except Exception as e:
                print(f"ERROR: Email login failed: {str(e)}")
                sys.exit(1)
                
        print("All basic tests passed successfully!")
        return True
        
    except Exception as e:
        print(f"ERROR during testing: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    print("Starting job scanner with diagnostic mode...")
    print(f"Python version: {sys.version}")
    print(f"Current working directory: {os.getcwd()}")
    print("Checking for required packages...")
    
    try:
        import requests
        import beautifulsoup4
        print("All required packages found")
    except ImportError as e:
        print(f"ERROR: Missing required package: {str(e)}")
        sys.exit(1)
    
    if simple_test():
        print("Initial tests passed, proceeding with main script...")
        # [Rest of your original script here]
