#pdf and docx file handling and text extraction using pypdf and python-docx libraries
import streamlit as st
from pypdf import PdfReader
from docx import Document

st.set_page_config(page_title="Resume Analyzer", page_icon="📄")

st.title("AI Resume Analyzer")
st.write("Upload your resume and extract the text.")


def extract_text_from_pdf(uploaded_file): # Extract text from PDF file
    pdf_reader = PdfReader(uploaded_file)
    text = ""   # Initialize an empty string to store the extracted text

    for page in pdf_reader.pages: # Iterate through each page and extract text
        page_text = page.extract_text()     # Extract text from the current page

        if page_text:
            text += page_text + "\n" # Add a newline after each page's text

    return text


def extract_text_from_docx(uploaded_file): # Extract text from DOCX file
    doc = Document(uploaded_file)

    text = ""

    for para in doc.paragraphs:  # Iterate through each paragraph and extract text
        text += para.text + "\n"    # Add a newline after each paragraph's text

    return text