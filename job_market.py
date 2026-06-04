import os
import requests

from dotenv import load_dotenv
from matcher import calculate_skill_match
load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")


def fetch_jobs(role, location="india", results=20):

    url = (
        f"https://api.adzuna.com/v1/api/jobs/in/search/1"
        f"?app_id={APP_ID}"
        f"&app_key={APP_KEY}"
        f"&what={role}"
        f"&results_per_page={results}"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()

    return data.get("results", [])

def combine_job_descriptions(jobs):

    combined_text = ""

    for job in jobs:

        description = job.get("description", "")

        combined_text += description + "\n\n"

    return combined_text



def calculate_market_fit(resume_skills, market_skills):
    score, matched, missing = calculate_skill_match(
        resume_skills,
        market_skills,
        threshold=0.70
    )

    return score, matched, missing