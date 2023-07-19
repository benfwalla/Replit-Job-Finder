# Replit Job Finder

A simple Selenium script that checks [Replit's careers page](https://replit.com/site/careers) for new job postings.

The scripts is designed to run on a scheduled cadence. Upon invocation, the script will bring in "the known jobs" that
were found in the last run located in [jobs.csv](jobs.csv). Then, a Selenium sequence gets all current job openings. 
Finally, the current jobs are checked against the known jobs, and all new jobs are printed out.

### ✅ TODO 
- Ensure jobs.csv is up to date by noting jobs that are no longer available
- When a new job is found, click into it and use GPT to summarize the new role
- Send an email or SMS on the new job

### 💡 Idea
Build similar scripts for the most innovative companies (Apple, Google, Meta, Nvidia) and get job alerts on their senior
roles. Make a blog called "Job Drop" that summarizes companies' newest job openings, as it's a key indicator of the 
strategic direction these companies would like to go.