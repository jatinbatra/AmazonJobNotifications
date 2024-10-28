import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import os
import sys

def log_message(message):
    # Print to console and file
    print(message, flush=True)
    with open('job_scan.log', 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] {message}\n")

class AmazonJobScanner:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.search_terms = [
            'energy',
            'ev charging',
            'electric vehicle',
            'senior product management',
            'senior product manager',
            'sr. product manager'
        ]

    def scan_jobs(self):
        log_message("\nStarting Amazon job scan...")
        jobs_found = []
        
        for term in self.search_terms:
            log_message(f"\nSearching for: {term}")
            url = f"https://www.amazon.jobs/en/search?base_query={term.replace(' ', '+')}&loc_query=United+States"
            
            try:
                log_message(f"Fetching URL: {url}")
                response = requests.get(url, headers=self.headers)
                log_message(f"Response status: {response.status_code}")
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    job_cards = soup.find_all('div', class_='job-tile')
                    
                    log_message(f"Found {len(job_cards)} job cards")
                    
                    for job in job_cards:
                        title = job.find('h3', class_='job-title')
                        location = job.find('p', class_='location-and-id')
                        
                        if title and location:
                            job_info = {
                                'title': title.text.strip(),
                                'location': location.text.strip(),
                                'url': 'https://www.amazon.jobs' + job.find('a')['href'],
                                'search_term': term
                            }
                            jobs_found.append(job_info)
                            log_message(f"Found job: {job_info['title']} in {job_info['location']}")
                
                time.sleep(2)  # Pause between searches
                
            except Exception as e:
                log_message(f"Error searching for {term}: {str(e)}")
        
        return jobs_found

def main():
    log_message("=== Amazon Job Scanner Started ===")
    log_message(f"Start time: {datetime.now()}")
    
    scanner = AmazonJobScanner()
    jobs = scanner.scan_jobs()
    
    log_message(f"\nTotal jobs found: {len(jobs)}")
    
    # Write detailed results to file
    with open('jobs_found.txt', 'w') as f:
        f.write(f"Amazon Jobs Scan Results - {datetime.now()}\n")
        f.write("=" * 50 + "\n\n")
        
        for job in jobs:
            f.write(f"Title: {job['title']}\n")
            f.write(f"Location: {job['location']}\n")
            f.write(f"URL: {job['url']}\n")
            f.write(f"Search Term: {job['search_term']}\n")
            f.write("-" * 50 + "\n")
    
    log_message("\n=== Scan Complete ===")

if __name__ == "__main__":
    main()
