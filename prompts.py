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


career_prediction_prompt = ChatPromptTemplate.from_template(
    """
You are an expert AI career advisor.

Analyze the candidate's resume and predict the most suitable career paths.

Use the candidate's:
- Skills
- Projects
- Experience
- Tools
- Education

Identify the TOP 3 most suitable career fields and rank them.

Choose from these categories:

1. Machine Learning / AI
2. Data Science / Analytics
3. Web Development
4. Backend Development
5. Frontend Development
6. Cloud / DevOps
7. Cybersecurity
8. Mobile App Development
9. UI/UX Design
10. General Software Engineering

11. Electronics & Embedded Systems
12. IoT & Smart Systems
13. VLSI Design & Semiconductor Engineering
14. Robotics & Automation
15. Telecommunications & Networking

16. Electrical Engineering
17. Mechanical Engineering
18. Civil Engineering

19. Product Management
20. Business Analysis
21. Marketing & Digital Marketing
22. Finance & Investment Analysis
23. Human Resources (HR)

24. Research & Development
25. Teaching & Academia
26. Entrepreneurship & Startups

Resume:
{resume_text}

Give output in this format:

Top Career Fields:

Rank 1:
Field: ...
Confidence: ...%

Rank 2:
Field: ...
Confidence: ...%

Rank 3:
Field: ...
Confidence: ...%

Best Target Role:
...

Other Suitable Roles:
- ...
- ...
- ...

Recommended Roles:
- ...
- ...
- ...

Why These Fields Fit:
- ...
- ...
- ...

Skill Gaps:
- ...
- ...
- ...

Next Learning Steps:
- ...
- ...
- ...

Best Project To Build Next:
...
"""
)

market_skill_extraction_prompt = ChatPromptTemplate.from_template(
    """
You are an expert job market analyst.

Extract the most important technical skills, tools, frameworks, libraries, platforms, and qualifications from these job descriptions.

Return ONLY valid JSON in this format:
{{
  "skills": ["skill1", "skill2", "skill3"]
}}

Rules:
- Focus only on job-required skills.
- Ignore company descriptions, benefits, HR text, salary, location, and generic soft skills.
- Normalize abbreviations:
  ML = Machine Learning
  DL = Deep Learning
  AI = Artificial Intelligence
- Keep only unique skills.
- Return maximum 30 skills.

Job Descriptions:
{text}
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