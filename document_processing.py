# document_processing.py

import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from config import EMBEDDINGS_MODEL_NAME

def load_documents(files):
    """
    Loads and extracts text from uploaded files (PDF, DOCX, TXT).
    """
    documents = []
    for file in files:
        file_extension = os.path.splitext(file.name)[1]

        # Create a temporary file to handle uploads
        with open(file.name, "wb") as f:
            f.write(file.getbuffer())

        if file_extension == ".pdf":
            loader = PyPDFLoader(file.name)
            documents.extend(loader.load())
        elif file_extension == ".docx":
            loader = Docx2txtLoader(file.name)
            documents.extend(loader.load())
        elif file_extension == ".txt":
            with open(file.name, "r", encoding="utf-8") as f:
                text = f.read()
                documents.append(Document(page_content=text, metadata={"source": file.name}))

        # Clean up the temporary file
        os.remove(file.name)
    return documents

def create_vector_store(documents):
    """
    Creates an in-memory vector store from the document chunks.
    """
    if not documents:
        return None, None

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL_NAME)
    vector_store = FAISS.from_documents(docs, embeddings)
    return vector_store, docs