from langchain_core.prompts import ChatPromptTemplate


skill_extraction_prompt = ChatPromptTemplate.from_template(
    """
You are an expert resume analyzer.

Extract technical and soft skills from the given text.

Return ONLY valid JSON in this format:
{{
  "skills": ["skill1", "skill2", "skill3"]
}}

Text:
{text}
"""
)


match_explanation_prompt = ChatPromptTemplate.from_template(
    """
You are an expert ATS resume analyzer.

Explain the resume-job match result.

Final Score: {final_score}/100

Matched Skills:
{matched_skills}

Missing Skills:
{missing_skills}

Resume:
{resume_text}

Job Description:
{job_description}

Give output in this format:

Match Summary:
...

Strengths:
- ...

Missing Skills:
- ...

Improvement Suggestions:
- ...
"""
)


rag_prompt = ChatPromptTemplate.from_template(
    """
You are a resume assistant.

Answer the question only using the resume context below.

If the answer is not available in the resume, say:
"Not found in the resume."

Resume Context:
{context}

Question:
{question}
"""
)