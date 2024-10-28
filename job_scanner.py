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
        # Base searches - we'll check these first
        self.search_urls = [
            "https://www.amazon.jobs/en/search?base_query=product+manager&loc_query=United+States",
            "https://www.amazon.jobs/en/search?base_query=product+management&loc_query=United+States",
            "https://www.amazon.jobs/en/search?base_query=senior+product+manager&loc_query=United+States",
            "https://www.amazon.jobs/en/search?base_query=energy&loc_query=United+States",
            "https://www.amazon.jobs/en/search?base_query=ev+charging&loc_query=United+States"
        ]
        
        # Keywords to look for in titles
        self.keywords = [
            'senior',
            'sr',
            'lead',
            'energy',
            'ev',
            'electric vehicle',
            'charging',
            'renewable',
            'sustainability',
            'product'
        ]

    def is_relevant_job(self, title):
        """Check if job matches our criteria"""
        title_lower = title.lower()
        return any(keyword.lower() in title_lower for keyword in self.keywords)

    def scan_jobs(self):
        log_message("\nStarting Amazon job scan...")
        jobs_found = []
        seen_urls = set()

        for url in self.search_urls:
            log_message(f"\nChecking URL: {url}")
            
            try:
                response = requests.get(url, headers=self.headers)
                log_message(f"Response status: {response.status_code}")
                
                if response.status_code == 200:
                    # Print first 500 characters of response to debug
                    log_message(f"Response preview: {response.text[:500]}")
                    
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Print the HTML structure we're finding
                    log_message("Looking for job cards...")
                    
                    # Try different possible class names
                    job_cards = (
                        soup.find_all('div', class_='job-tile') or 
                        soup.find_all('div', class_='jobs-list') or
                        soup.find_all('div', attrs={'data-job-id': True})
                    )
                    
                    log_message(f"Found {len(job_cards)} potential job cards")
                    
                    for job in job_cards:
                        try:
                            # Try different possible selectors
                            title = (
                                job.find('h3', class_='job-title') or
                                job.find('h3', class_='title') or
                                job.find('h2', class_='job-title') or
                                job.find('a', class_='job-link')
                            )
                            
                            if title:
                                title_text = title.text.strip()
                                log_message(f"Found job title: {title_text}")
                                
                                # Try to get the URL
                                job_link = job.find('a')
                                if job_link and 'href' in job_link.attrs:
                                    job_url = 'https://www.amazon.jobs' + job_link['href']
                                    
                                    if job_url not in seen_urls and self.is_relevant_job(title_text):
                                        # Try to get location
                                        location = (
                                            job.find('p', class_='location-and-id') or
                                            job.find('span', class_='location') or
                                            job.find('div', class_='location')
                                        )
                                        location_text = location.text.strip() if location else "Location not specified"
                                        
                                        job_info = {
                                            'title': title_text,
                                            'location': location_text,
                                            'url': job_url,
                                            'found_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                        }
                                        
                                        jobs_found.append(job_info)
                                        seen_urls.add(job_url)
                                        log_message(f"Added job: {title_text} in {location_text}")
                        
                        except Exception as e:
                            log_message(f"Error processing job card: {str(e)}")
                            continue
                
                time.sleep(2)  # Pause between searches
                
            except Exception as e:
                log_message(f"Error with URL {url}: {str(e)}")
        
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
            f.write("-" * 50 + "\n\n")
    
    log_message("\n=== Scan Complete ===")

if __name__ == "__main__":
    main()
