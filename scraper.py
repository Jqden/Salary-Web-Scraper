import requests
from bs4 import BeautifulSoup

# Jobs to scrape salary quartiles
jobs = ("Chemist I", "Chemist II", "Software Engineer I", "Software Engineer III", "Physicist II")
job_salaries = {}

for job in jobs:
    print("Processing", job)
    # Create website link
    job_url = job.lower().replace(" ", "-")
    URL = "https://www.salary.com/tools/salary-calculator/" + job_url + "/billerica-ma"
    
    # Get website HTML
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    # Scrape the salary quartiles from HTML
    quartile_ids = ("left_salary_value_2", "top_salary_value", "right_salary_value_1") # locations in HTML where values of interest are
    quartiles = (soup.find(id=e) for e in quartile_ids) # soup finds the locations
    salaries = [quart.text.strip().replace("$", "").replace(",", "") for quart in quartiles] # remove the whitespace, $, and , from salary

    # Record result
    job_salaries[job] = salaries

# Record the results to salary_quartiles.csv
with open("salary_quartiles.csv", "w") as f:
    f.write("Job, 25% Salary, 50% Salary, 75% Salary\n")
    for job in job_salaries:
        f.write(job + ", " + ", ".join(job_salaries[job]) + "\n")