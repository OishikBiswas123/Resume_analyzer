# AI Resume Analyzer

AI Resume Analyzer is a Streamlit-based NLP and RAG application that analyzes resumes, extracts skills, compares them with a job description, calculates a job match score, and allows users to ask questions about the resume using FAISS-based retrieval.

## Features

- Upload resume in PDF or DOCX format
- Extract text from resumes
- Extract skills using Groq LLM
- Compare resume with job description
- Calculate hybrid job match score
- Semantic skill matching
- Missing skill detection
- AI-generated improvement suggestions
- FAISS vector database
- Resume question-answering using RAG

## Tech Stack

- Python
- Streamlit
- LangChain
- Groq LLM
- FAISS
- HuggingFace Embeddings
- Sentence Transformers
- PyPDF
- python-docx
- Scikit-learn

## Project Structure

```text
resume-analyzer/
│
├── app.py
├── utils.py
├── llm.py
├── matcher.py
├── rag.py
├── prompts.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
