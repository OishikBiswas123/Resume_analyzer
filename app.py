import streamlit as st

from utils import (
    extract_text_from_pdf,
    extract_text_from_docx
)

from llm import extract_skills_list, generate_match_explanation,  predict_career_field
from rag import create_vector_store, answer_resume_question

from matcher import (
    calculate_skill_match,
    calculate_semantic_similarity,
    calculate_final_score
)

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
    - FAISS vector search
    """)

st.title("📄 AI Resume Analyzer")
st.write("Upload a resume, compare it with a job description, and ask questions using RAG.")

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

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

    tab1, tab2, tab3, tab4 = st.tabs([
    "📄 Resume Text",
    "🎯 Job Match",
    "💬 Resume Q&A",
    "🚀 Career Path Predictor"
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

        if st.button("Predict Best Career Path"):
            with st.spinner("Analyzing resume and predicting career path..."):
                career_result = predict_career_field(resume_text)

                st.subheader("AI Career Path Analysis")
                st.write(career_result)

else:
    st.info("Please upload a PDF or DOCX resume to begin.")