import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import os
import sys

def log_message(message):
    print(message, flush=True)
    with open('job_scan.log', 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] {message}\n")

class AmazonJobScanner:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        # Broader search terms to cast a wider net
        self.base_searches = [
            'product manager',
            'product management',
            'program manager'
        ]
        
        # Keywords to filter results
        self.keywords = [
            'senior',
            'sr',
            'lead',
            'energy',
            'ev',
            'electric vehicle',
            'charging',
            'renewable',
            'sustainability'
        ]

    def is_relevant_job(self, title, description):
        """Check if job matches our criteria"""
        title_lower = title.lower()
        desc_lower = description.lower()
        
        # Check if it's a senior/lead role
        is_senior = any(word in title_lower for word in ['senior', 'sr', 'sr.', 'lead', 'principal'])
        
        # Check if it's related to energy/EV
        is_energy_related = any(word in title_lower or word in desc_lower for word in 
            ['energy', 'ev', 'electric vehicle', 'charging', 'renewable', 'sustainability'])
        
        return is_senior or is_energy_related

    def scan_jobs(self):
        log_message("\nStarting Amazon job scan...")
        jobs_found = []
        seen_urls = set()  # To avoid duplicates
        
        for search_term in self.base_searches:
            log_message(f"\nSearching for: {search_term}")
            url = f"https://www.amazon.jobs/en/search?base_query={search_term.replace(' ', '+')}&loc_query=United+States"
            
            try:
                log_message(f"Fetching URL: {url}")
                response = requests.get(url, headers=self.headers)
                log_message(f"Response status: {response.status_code}")
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    job_cards = soup.find_all('div', class_='job-tile')
                    
                    log_message(f"Found {len(job_cards)} job cards to analyze")
                    
                    for job in job_cards:
                        try:
                            title_elem = job.find('h3', class_='job-title')
                            location_elem = job.find('p', class_='location-and-id')
                            description_elem = job.find('p', class_='description')
                            
                            if title_elem and location_elem:
                                title = title_elem.text.strip()
                                location = location_elem.text.strip()
                                description = description_elem.text.strip() if description_elem else ""
                                job_url = 'https://www.amazon.jobs' + job.find('a')['href']
                                
                                # Only process if we haven't seen this URL
                                if job_url not in seen_urls:
                                    if self.is_relevant_job(title, description):
                                        job_info = {
                                            'title': title,
                                            'location': location,
                                            'url': job_url,
                                            'description': description,
                                            'found_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                        }
                                        jobs_found.append(job_info)
                                        seen_urls.add(job_url)
                                        log_message(f"Found relevant job: {title} in {location}")
                        
                        except Exception as e:
                            log_message(f"Error processing job card: {str(e)}")
                            continue
                
                time.sleep(2)  # Pause between searches
                
            except Exception as e:
                log_message(f"Error searching for {search_term}: {str(e)}")
        
        return jobs_found

def main():
    log_message("=== Amazon Job Scanner Started ===")
    log_message(f"Start time: {datetime.now()}")
    
    scanner = AmazonJobScanner()
    jobs = scanner.scan_jobs()
    
    log_message(f"\nTotal relevant jobs found: {len(jobs)}")
    
    # Write detailed results to file
    with open('jobs_found.txt', 'w') as f:
        f.write(f"Amazon Jobs Scan Results - {datetime.now()}\n")
        f.write("=" * 50 + "\n\n")
        
        for job in jobs:
            f.write(f"Title: {job['title']}\n")
            f.write(f"Location: {job['location']}\n")
            f.write(f"URL: {job['url']}\n")
            f.write(f"Found: {job['found_time']}\n")
            if job['description']:
                f.write(f"Description Preview: {job['description'][:200]}...\n")
            f.write("-" * 50 + "\n\n")
    
    log_message("\n=== Scan Complete ===")

if __name__ == "__main__":
    main()
