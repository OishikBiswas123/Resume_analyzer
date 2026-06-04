import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv("GROQ_API_KEY"))
print(os.getenv("ADZUNA_APP_ID"))
print(os.getenv("ADZUNA_APP_KEY"))