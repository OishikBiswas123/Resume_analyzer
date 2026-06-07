import streamlit as st
import re

from utils import (
    extract_text_from_pdf,
    extract_text_from_docx
)

from llm import (
    extract_skills_list,
    generate_match_explanation,
    predict_career_field,
    extract_market_skills
)

from rag import create_vector_store, answer_resume_question

from matcher import (
    calculate_skill_match,
    calculate_semantic_similarity,
    calculate_final_score
)

from job_market import (
    fetch_jobs,
    combine_job_descriptions,
    calculate_market_fit
)


def extract_best_target_role(career_result):
    text = career_result.replace("*", "").strip()

    match = re.search(
        r"Best\s+Target\s+Role\s*:\s*([^\n\r]+)",
        text,
        re.IGNORECASE
    )

    if match:
        role = match.group(1).strip()
        role = role.replace('"', "").replace("'", "")
        return role

    return ""


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

with st.sidebar:
    st.title("📄 Resume Analyzer")
    st.markdown("""
    ### Features
    - Resume PDF/DOCX parsing
    - AI skill extraction
    - Job match scoring
    - Semantic similarity
    - Missing skill detection
    - Resume Q&A using RAG
    - Career path prediction
    - Live job market analysis
    - FAISS vector search
    """)

st.title("📄 AI Resume Analyzer")
st.write(
    "Upload a resume, compare it with a job description, ask questions using RAG, and analyze live job market demand."
)

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "predicted_role" not in st.session_state:
    st.session_state.predicted_role = ""

if "career_result" not in st.session_state:
    st.session_state.career_result = ""

uploaded_resume = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx"]
)

if uploaded_resume:

    file_extension = uploaded_resume.name.split(".")[-1].lower()

    if file_extension == "pdf":
        resume_text = extract_text_from_pdf(uploaded_resume)
    else:
        resume_text = extract_text_from_docx(uploaded_resume)

    st.session_state.resume_text = resume_text

    st.success("Resume uploaded and text extracted successfully.")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📄 Resume Text",
        "🎯 Job Match",
        "💬 Resume Q&A",
        "🚀 Career Path Predictor",
        "📈 Market Analysis"
    ])

    with tab1:
        st.subheader("Extracted Resume Text")

        st.text_area(
            "Resume Content",
            resume_text,
            height=350
        )

        if st.button("Extract Skills"):
            with st.spinner("Extracting skills..."):
                skills = extract_skills_list(resume_text)

            st.subheader("Extracted Skills")

            cols = st.columns(3)

            for index, skill in enumerate(skills):
                with cols[index % 3]:
                    st.markdown(f"✅ **{skill.title()}**")

    with tab2:
        st.subheader("Job Description")

        job_description = st.text_area(
            "Paste Job Description",
            height=250
        )

        if st.button("Analyze Job Match"):

            if not job_description.strip():
                st.warning("Please paste a job description.")
                st.stop()

            with st.spinner("Analyzing job match..."):

                resume_skills = extract_skills_list(resume_text)
                jd_skills = extract_skills_list(job_description)

                skill_score, matched_skills, missing_skills = calculate_skill_match(
                    resume_skills,
                    jd_skills
                )

                semantic_score = calculate_semantic_similarity(
                    resume_text,
                    job_description
                )

                final_score = calculate_final_score(
                    skill_score,
                    semantic_score
                )

                explanation = generate_match_explanation(
                    resume_text,
                    job_description,
                    final_score,
                    matched_skills,
                    missing_skills
                )

            st.subheader("Job Match Result")

            col1, col2, col3 = st.columns(3)

            col1.metric("Final Match Score", f"{final_score}%")
            col2.metric("Skill Match Score", f"{skill_score}%")
            col3.metric("Semantic Similarity", f"{semantic_score}%")

            st.divider()

            col4, col5 = st.columns(2)

            with col4:
                st.subheader("Matched Skills")
                if matched_skills:
                    for skill in matched_skills:
                        st.success(skill)
                else:
                    st.info("No matched skills found.")

            with col5:
                st.subheader("Missing Skills")
                if missing_skills:
                    for skill in missing_skills:
                        st.error(skill)
                else:
                    st.success("No missing skills found.")

            st.divider()

            st.subheader("AI Explanation")
            st.write(explanation)

    with tab3:
        st.subheader("Ask Questions About Resume")

        if st.button("Create Resume Vector Database"):
            with st.spinner("Creating FAISS vector database..."):
                st.session_state.vector_store = create_vector_store(resume_text)

            st.success("Vector database created successfully.")

        question = st.text_input(
            "Ask a question about the resume"
        )

        if st.button("Get Answer"):

            if st.session_state.vector_store is None:
                st.warning("Please create the vector database first.")

            elif not question.strip():
                st.warning("Please enter a question.")

            else:
                with st.spinner("Searching resume and generating answer..."):
                    answer = answer_resume_question(
                        st.session_state.vector_store,
                        question
                    )

                st.subheader("Answer")
                st.write(answer)

    with tab4:
        st.subheader("Career Path Predictor")

        st.write(
            "Use this if you do not have a job description and want AI to suggest the best career direction based on your resume."
        )

        if st.session_state.career_result:
            st.subheader("Last Career Analysis")
            st.write(st.session_state.career_result)

            if st.session_state.predicted_role:
                st.success(
                    f"Current Suggested Role: {st.session_state.predicted_role}"
                )

        if st.button("Predict Best Career Path"):

            with st.spinner("Analyzing resume and predicting career path..."):
                career_result = predict_career_field(resume_text)

            predicted_role = extract_best_target_role(career_result)

            st.session_state.career_result = career_result
            st.session_state.predicted_role = predicted_role

            st.subheader("AI Career Path Analysis")
            st.write(career_result)

            if predicted_role:
                st.success(
                    f"Suggested Role: {predicted_role}"
                )
            else:
                st.warning(
                    "Could not extract a target role from the AI response. You can still type a role manually in Market Analysis."
                )

    with tab5:
        st.subheader("Live Job Market Analysis")

        st.write(
            "Use the predicted role from Career Path Predictor or enter a target role manually."
        )

        role = st.text_input(
            "Target Role",
            value=st.session_state.predicted_role,
            placeholder="Example: Machine Learning Engineer"
        )

        if not role.strip():
            st.info(
                "No target role selected yet. Go to Career Path Predictor first or type a role manually."
            )

        if st.button("Analyze Market Demand"):

            if not role.strip():
                st.warning(
                    "Please enter a target role or generate one from the Career Path Predictor."
                )
                st.stop()

            with st.spinner("Fetching current job market data..."):

                jobs = fetch_jobs(role)

                if not jobs:
                    st.error("Could not fetch job data.")
                    st.stop()

                job_text = combine_job_descriptions(jobs)

                market_skills = extract_market_skills(job_text)
                market_skills = market_skills[:30]

                resume_skills = extract_skills_list(resume_text)

                market_score, matched, missing = calculate_market_fit(
                    resume_skills,
                    market_skills
                )

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Market Fit Score",
                    f"{market_score}%"
                )

            with col2:
                st.metric(
                    "Matched Skills",
                    f"{len(matched)}/{len(market_skills)}"
                )

            st.write(
                f"You match **{len(matched)} out of {len(market_skills)}** current market skills for **{role}**."
            )

            st.subheader("Top Skills To Learn Next")

            if missing:
                for skill in missing[:5]:
                    st.warning(skill)
            else:
                st.success("You have covered all major market skills.")

            st.divider()

            col3, col4 = st.columns(2)

            with col3:
                st.subheader("Skills You Already Have")

                if matched:
                    for skill in matched:
                        display_skill = skill.split("↔")[0].strip()
                        st.success(display_skill)
                else:
                    st.warning("No matching skills found.")

            with col4:
                st.subheader("Skills Missing In Current Market")

                if missing:
                    for skill in missing[:10]:
                        st.error(skill)

                    if len(missing) > 10:
                        st.info(f"+ {len(missing) - 10} more skills not shown.")
                else:
                    st.success("No missing skills found.")

            with st.expander("View Current Market Skills"):
                for skill in market_skills:
                    st.info(skill)

else:
    st.info("Please upload a PDF or DOCX resume to begin.")