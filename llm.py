import json

from langchain_core.output_parsers import StrOutputParser

from config import get_llm
from prompts import skill_extraction_prompt, match_explanation_prompt


def extract_skills_list(text):
    llm = get_llm()

    chain = skill_extraction_prompt | llm | StrOutputParser()

    response = chain.invoke({
        "text": text
    })

    data = json.loads(response)

    return [skill.lower().strip() for skill in data["skills"]]


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