import os
import requests
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

url = (
    f"https://api.adzuna.com/v1/api/jobs/in/search/1"
    f"?app_id={APP_ID}"
    f"&app_key={APP_KEY}"
    f"&what=Machine Learning Engineer"
)

response = requests.get(url)

print("Status Code:", response.status_code)

data = response.json()

print("Results Found:", len(data.get("results", [])))

if data.get("results"):
    print("\nSample Job Title:")
    print(data["results"][0]["title"])