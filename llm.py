import json
import re

from langchain_core.output_parsers import StrOutputParser

from config import get_llm
from prompts import (
    skill_extraction_prompt,
    match_explanation_prompt,
    career_prediction_prompt,
    market_skill_extraction_prompt
)


def parse_json_response(response):
    try:
        return json.loads(response)

    except json.JSONDecodeError:
        json_match = re.search(r"\{.*\}", response, re.DOTALL)

        if json_match:
            return json.loads(json_match.group())

        return {"skills": []}


def extract_skills_list(text):
    llm = get_llm()

    chain = skill_extraction_prompt | llm | StrOutputParser()

    response = chain.invoke({
        "text": text
    })

    data = parse_json_response(response)

    return [skill.lower().strip() for skill in data.get("skills", [])]


def predict_career_field(resume_text):
    llm = get_llm()

    chain = career_prediction_prompt | llm | StrOutputParser()

    response = chain.invoke({
        "resume_text": resume_text
    })

    return response

def extract_market_skills(text):
    llm = get_llm()

    chain = market_skill_extraction_prompt | llm | StrOutputParser()

    response = chain.invoke({
        "text": text
    })

    data = parse_json_response(response)

    return [skill.lower().strip() for skill in data.get("skills", [])]


def generate_match_explanation(
    resume_text,
    job_description,
    final_score,
    matched_skills,
    missing_skills
):
    llm = get_llm()

    chain = match_explanation_prompt | llm | StrOutputParser()

    response = chain.invoke({
        "resume_text": resume_text,
        "job_description": job_description,
        "final_score": final_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    })

    return response