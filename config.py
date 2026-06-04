import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def get_api_key():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY not found. Check your .env or Streamlit secrets.")

    return api_key


def get_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        api_key=get_api_key()
    )