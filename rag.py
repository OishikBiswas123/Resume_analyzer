from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser

from config import get_llm
from prompts import rag_prompt


def create_vector_store(resume_text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100
    )

    chunks = text_splitter.split_text(resume_text)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = FAISS.from_texts(
        texts=chunks,
        embedding=embeddings
    )

    return vector_store


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def answer_resume_question(vector_store, question):
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

    docs = retriever.invoke(question)

    context = format_docs(docs)

    llm = get_llm()

    chain = rag_prompt | llm | StrOutputParser()

    answer = chain.invoke({
        "context": context,
        "question": question
    })

    return answer