import time
from datetime import datetime
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def log_message(message):
    print(message, flush=True)
    with open('job_scan.log', 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] {message}\n")

class AmazonJobScanner:
    def __init__(self):
        # Set up Chrome options for headless running
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        
        self.search_urls = [
            "https://www.amazon.jobs/en/search?base_query=senior+product+manager&loc_query=United+States",
            "https://www.amazon.jobs/en/search?base_query=energy+manager&loc_query=United+States",
            "https://www.amazon.jobs/en/search?base_query=sustainability&loc_query=United+States"
        ]

    def scan_jobs(self):
        log_message("\nStarting Amazon job scan with Selenium...")
        jobs_found = []
        
        for url in self.search_urls:
            try:
                log_message(f"\nAccessing URL: {url}")
                self.driver.get(url)
                
                # Wait for jobs to load
                time.sleep(5)  # Give time for JavaScript to load content
                
                # Wait for job cards to appear
                log_message("Waiting for job listings to load...")
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "job-tile"))
                )
                
                # Get all job listings
                job_cards = self.driver.find_elements(By.CLASS_NAME, "job-tile")
                log_message(f"Found {len(job_cards)} job listings")
                
                for job in job_cards:
                    try:
                        # Get job details
                        title = job.find_element(By.CLASS_NAME, "job-title").text
                        location = job.find_element(By.CLASS_NAME, "location-and-id").text
                        link = job.find_element(By.TAG_NAME, "a").get_attribute("href")
                        
                        log_message(f"Found job: {title} in {location}")
                        
                        jobs_found.append({
                            'title': title,
                            'location': location,
                            'url': link,
                            'found_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                        
                    except Exception as e:
                        log_message(f"Error processing job card: {str(e)}")
                        continue
                
            except Exception as e:
                log_message(f"Error with URL {url}: {str(e)}")
        
        return jobs_found

    def close(self):
        self.driver.quit()

def main():
    log_message("=== Amazon Job Scanner Started ===")
    scanner = AmazonJobScanner()
    
    try:
        jobs = scanner.scan_jobs()
        
        log_message(f"\nTotal jobs found: {len(jobs)}")
        
        # Write results to file
        with open('jobs_found.txt', 'w') as f:
            f.write(f"Amazon Jobs Scan Results - {datetime.now()}\n")
            f.write("=" * 50 + "\n\n")
            
            for job in jobs:
                f.write(f"Title: {job['title']}\n")
                f.write(f"Location: {job['location']}\n")
                f.write(f"URL: {job['url']}\n")
                f.write(f"Found: {job['found_time']}\n")
                f.write("-" * 50 + "\n\n")
    
    finally:
        scanner.close()
        log_message("\n=== Scan Complete ===")

if __name__ == "__main__":
    main()
