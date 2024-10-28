import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
import os
from email.mime.text import MIMEText
import smtplib
import re
import linkedin_api # for authenticated LinkedIn access

class EnhancedJobChecker:
    def __init__(self):
        self.seen_jobs = set()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Enhanced keywords list
        self.keywords = [
            'energy',
            'renewable',
            'sustainability',
            'power',
            'utilities',
            'grid',
            'electrical',
            'sustainable',
            'clean energy',
            'smart grid',
            'ev charging',
            'electric vehicle',
            'EV infrastructure',
            'charging station',
            'senior product manager',
            'senior product management',
            'sr. product manager',
            'sr product manager',
            'principal product manager'
        ]
        
        # Initialize LinkedIn API
        self.linkedin = linkedin_api.Linkedin(
            os.getenv('LINKEDIN_EMAIL'),
            os.getenv('LINKEDIN_PASSWORD')
        )

    def find_linkedin_job_post(self, company_name, job_title):
        """Find matching job on LinkedIn and get hiring manager info"""
        try:
            # Search for the job on LinkedIn
            search_params = {
                'keywords': job_title,
                'companies': ['amazon'],
                'time_posted': 'past_week'
            }
            
            jobs = self.linkedin.search_jobs(
                search_params=search_params
            )
            
            for job in jobs:
                # Get detailed job info
                job_detail = self.linkedin.get_job(job['job_id'])
                
                # Get job poster info if available
                if 'poster' in job_detail:
                    poster_info = self.linkedin.get_profile(job_detail['poster']['public_id'])
                    return {
                        'linkedin_url': f"https://www.linkedin.com/jobs/view/{job['job_id']}",
                        'hiring_manager': {
                            'name': poster_info.get('full_name', 'N/A'),
                            'title': poster_info.get('headline', 'N/A'),
                            'profile_url': f"https://www.linkedin.com/in/{poster_info.get('public_id')}",
                        }
                    }
            
            return None
            
        except Exception as e:
            print(f"LinkedIn search error: {str(e)}")
            return None

    def check_amazon_jobs(self):
        jobs = []
        base_urls = [
            "https://www.amazon.jobs/en/search?base_query=product+manager&loc_query=United+States",
            "https://www.amazon.jobs/en/search?base_query=energy&loc_query=United+States",
            "https://www.amazon.jobs/en/search?base_query=ev+charging&loc_query=United+States",
            "https://www.amazon.jobs/en/search?base_query=senior+product+manager&loc_query=United+States"
        ]
        
        for url in base_urls:
            try:
                response = requests.get(url, headers=self.headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                jobs_list = soup.find_all('div', class_='job-tile')
                
                for job in jobs_list:
                    title = job.find('h3', class_='job-title').text.strip()
                    location = job.find('p', class_='location-and-id').text.strip()
                    link = 'https://www.amazon.jobs' + job.find('a')['href']
                    team = job.find('p', class_='department-and-category').text.strip()
                    
                    # Enhanced keyword matching
                    if any(keyword.lower() in title.lower() or keyword.lower() in team.lower() 
                           for keyword in self.keywords):
                        if link not in self.seen_jobs:
                            # Get job details
                            job_response = requests.get(link, headers=self.headers)
                            job_soup = BeautifulSoup(job_response.text, 'html.parser')
                            
                            # Get full job description
                            description = job_soup.find('div', class_='job-description').text.strip()
                            
                            # Find matching LinkedIn post
                            linkedin_info = self.find_linkedin_job_post('Amazon', title)
                            
                            jobs.append({
                                'title': title,
                                'location': location,
                                'team': team,
                                'amazon_link': link,
                                'description': description[:500] + "...",  # First 500 chars
                                'linkedin_info': linkedin_info,
                                'date_found': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            })
                            self.seen_jobs.add(link)
                
                time.sleep(2)  # Respectful delay between requests
                
            except Exception as e:
                print(f"Error checking Amazon jobs: {str(e)}")
                
        return jobs

    def send_email(self, jobs):
        if not jobs:
            return
            
        email = os.getenv('EMAIL_ADDRESS')
        password = os.getenv('EMAIL_PASSWORD')
        
        msg_text = "New Amazon Energy/EV/Senior PM Jobs Found:\n\n"
        msg_text += f"Total New Jobs Found: {len(jobs)}\n"
        msg_text += "=" * 70 + "\n\n"
        
        for job in jobs:
            msg_text += f"Title: {job['title']}\n"
            msg_text += f"Location: {job['location']}\n"
            msg_text += f"Team: {job['team']}\n"
            msg_text += f"Amazon Link: {job['amazon_link']}\n"
            
            if job['linkedin_info']:
                msg_text += "\nLinkedIn Information:\n"
                msg_text += f"LinkedIn Job URL: {job['linkedin_info']['linkedin_url']}\n"
                msg_text += f"Hiring Manager: {job['linkedin_info']['hiring_manager']['name']}\n"
                msg_text += f"Manager Title: {job['linkedin_info']['hiring_manager']['title']}\n"
                msg_text += f"Manager Profile: {job['linkedin_info']['hiring_manager']['profile_url']}\n"
            
            msg_text += f"\nJob Description Preview:\n{job['description']}\n"
            msg_text += f"\nFound: {job['date_found']}\n"
            msg_text += "-" * 70 + "\n\n"
            
        msg = MIMEText(msg_text)
        msg['Subject'] = f"New Amazon Energy/EV/Senior PM Jobs - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        msg['From'] = email
        msg['To'] = email
        
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(email, password)
                server.send_message(msg)
                print(f"Email sent with {len(jobs)} new jobs")
        except Exception as e:
            print(f"Email error: {str(e)}")

    def run(self):
        print(f"Starting Enhanced Job Checker at {datetime.now()}")
        while True:
            print(f"Checking for new jobs at {datetime.now()}")
            new_jobs = self.check_amazon_jobs()
            
            if new_jobs:
                print(f"Found {len(new_jobs)} new jobs")
                self.send_email(new_jobs)
            else:
                print("No new jobs found")
                
            # Wait for 30 minutes before next check
            print(f"Sleeping until next check at {datetime.now() + timedelta(minutes=30)}")
            time.sleep(1800)  # 30 minutes

if __name__ == "__main__":
    checker = EnhancedJobChecker()
    checker.run()
