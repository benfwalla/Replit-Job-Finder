from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import os
import time


def read_existing_jobs(file_path='jobs.csv'):
    """Return a set of existing job IDs from the given file"""
    existing_job_ids = set()
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                existing_job_ids.add(row[0])
    return existing_job_ids


def write_new_jobs(new_jobs, file_path='jobs.csv'):
    """Write new job IDs to the given csv file"""
    if len(new_jobs) > 0:
        with open(file_path, 'a') as f:
            writer = csv.writer(f)
            for job in new_jobs:
                writer.writerow(job)


def get_webpage_html(url):
    """Return the HTML content of the given URL using Selenium"""
    driver = webdriver.Chrome()
    driver.get(url)

    time.sleep(2)

    # Get the page source (HTML) after JavaScript has run
    html = driver.page_source

    # Quit the driver
    driver.quit()

    return html


def check_new_replit_jobs(existing_job_ids, html):
    """Return a list of new job IDs on the given HTML page relative to the existing job IDs in the csv file"""

    # Create a BeautifulSoup object from the HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Find the container for the open positions
    job_container = soup.find('div', {'id': 'open-positions'})

    # Find all divs that contain an <a> tag and a <span> tag
    # We should only collect the deepest divs that have those tags. No parent divs that will cause duplicates
    job_divs = [div for div in job_container.find_all('div')
                if div.find('a') and div.find('span') and not any(
            subdiv.find('a') and subdiv.find('span') for subdiv in div.find_all('div'))]
    print(f"There are {len(job_divs)} active job openings on Replit's careers page.")

    # Create a list to store new jobs
    new_jobs = []

    # Iterate over job divs
    for job_div in job_divs:

        job_link = job_div.find('a')
        job_location = job_div.find('span')

        # Store the job ID, job title, job location, and job URL
        job_id = job_link['href'].split('/')[-1]
        job_title = job_link.text
        job_location = job_location.text
        job_url = job_link['href']

        # If this job ID is not in the existing set, print it and add it to new_jobs
        if job_id not in existing_job_ids:
            print(f"New Job Posting: {job_title}")
            new_jobs.append([job_id, job_title, job_location, job_url])

    if len(new_jobs) > 0:
        print(f"{len(new_jobs)} new jobs found!")
    else:
        print("No new jobs found.")

    return new_jobs


existing_jobs = read_existing_jobs()
html = get_webpage_html('https://replit.com/site/careers')
new_jobs = check_new_replit_jobs(existing_jobs, html)
write_new_jobs(new_jobs)
