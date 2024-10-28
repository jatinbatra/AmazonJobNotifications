import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import os
import sys
import json

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
        # Testing with just one URL first
        self.search_urls = [
            "https://www.amazon.jobs/en/search?base_query=product+manager&loc_query=United+States"
        ]

    def get_page_content(self, url):
        """Get and save page content for debugging"""
        try:
            response = requests.get(url, headers=self.headers)
            log_message(f"URL: {url}")
            log_message(f"Status Code: {response.status_code}")
            
            # Save raw HTML for debugging
            with open('debug_page.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            log_message("Saved raw HTML to debug_page.html")
            return response.text
        except Exception as e:
            log_message(f"Error fetching URL: {str(e)}")
            return None

    def scan_jobs(self):
        log_message("\nStarting debug job scan...")
        jobs_found = []
        
        for url in self.search_urls:
            log_message(f"\nProcessing URL: {url}")
            
            html_content = self.get_page_content(url)
            if not html_content:
                continue
                
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Debug: Print all div classes found
            log_message("\nAll div classes found:")
            all_divs = soup.find_all('div', class_=True)
            div_classes = set(div['class'][0] for div in all_divs if div.get('class'))
            log_message(str(div_classes))
            
            # Try to find job listings
            log_message("\nLooking for job listings...")
            
            # Method 1: Look for job-tile class
            job_tiles = soup.find_all('div', class_='job-tile')
            log_message(f"Found {len(job_tiles)} job-tile elements")
            
            # Method 2: Look for job cards with data attributes
            job_cards = soup.find_all('div', attrs={'data-job-id': True})
            log_message(f"Found {len(job_cards)} job cards with data-job-id")
            
            # Method 3: Look for any job-related links
            job_links = soup.find_all('a', href=lambda x: x and '/jobs/' in x)
            log_message(f"Found {len(job_links)} job-related links")
            
            # Try to extract from either method
            for job in (job_tiles or job_cards or []):
                try:
                    # Debug: Print the entire job element
                    log_message("\nJob HTML structure:")
                    log_message(str(job)[:500])  # First 500 chars
                    
                    # Try multiple ways to get title
                    title = None
                    title_elem = (job.find('h3', class_='job-title') or 
                                job.find('h3', class_='title') or
                                job.find('a', class_='job-link'))
                    
                    if title_elem:
                        title = title_elem.text.strip()
                        log_message(f"Found job title: {title}")
                        
                        # Get all text from this job element
                        full_text = job.get_text(separator=' ', strip=True)
                        log_message(f"Full job text: {full_text[:200]}...")
                        
                        job_info = {
                            'title': title,
                            'full_text': full_text,
                            'html': str(job)[:500]
                        }
                        jobs_found.append(job_info)
                
                except Exception as e:
                    log_message(f"Error processing job element: {str(e)}")
                    continue
        
        return jobs_found

def main():
    log_message("=== Debug Amazon Job Scanner Started ===")
    scanner = AmazonJobScanner()
    jobs = scanner.scan_jobs()
    
    # Save all debug info
    with open('debug_results.txt', 'w') as f:
        f.write(f"Debug Scan Results - {datetime.now()}\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total elements found: {len(jobs)}\n\n")
        
        for i, job in enumerate(jobs, 1):
            f.write(f"Item {i}:\n")
            f.write(f"Title: {job.get('title', 'No title found')}\n")
            f.write(f"Full text: {job.get('full_text', 'No text found')}\n")
            f.write(f"HTML: {job.get('html', 'No HTML found')}\n")
            f.write("-" * 50 + "\n\n")
    
    log_message("\n=== Debug Scan Complete ===")
    log_message(f"Found {len(jobs)} potential job elements")
    log_message("Check debug_results.txt and debug_page.html for details")

if __name__ == "__main__":
    main()
