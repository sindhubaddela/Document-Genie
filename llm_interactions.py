# llm_interactions.py

import streamlit as st
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from groq._exceptions import APIStatusError, APIConnectionError
import json
from config import GROQ_API_KEY, MODEL_NAME

def get_groq_client():
    """Initializes and returns the Groq client."""
    return ChatGroq(model_name=MODEL_NAME, groq_api_key=GROQ_API_KEY)

def generate_summary(docs):
    """Generates a summary of the provided documents."""
    if not docs:
        st.warning("Please process your documents first.")
        return

    groq = get_groq_client()
    all_text = " ".join([doc.page_content for doc in docs])
    prompt = ChatPromptTemplate.from_template("""
        You are a highly skilled summarizer with expertise in distilling complex content into clear, impactful summaries.
        Your task is to generate a professional, well-structured summary of the following text. Ensure the summary has all the important details and is concise.
        make it in paragraph format and bullet points if needed and bold the important key words.
        Text to summarize:
        {text}
    """)
    chain = prompt | groq

    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
    chunks = splitter.split_text(all_text)
    
    summaries = []
    progress = st.progress(0)
    for i, chunk in enumerate(chunks):
        try:
            partial_summary = chain.invoke({"text": chunk}).content
            summaries.append(partial_summary)
            progress.progress((i + 1) / len(chunks))
        except APIStatusError as e:
            st.error(f"API Error: {e}")
            break

    final_summary = "\n\n".join(summaries)
    st.success("Summary Generated!")
    st.write(final_summary)

def get_chatbot_response(vector_store, user_question):
    """Gets a response from the chatbot based on the user's question."""
    if not vector_store:
        st.warning("Please process your documents to enable the chatbot.")
        return

    groq = get_groq_client()
    prompt = ChatPromptTemplate.from_template("""
        Answer the user's question based on the provided context.
        If the answer is not in the context, say "I couldn't find the answer in the documents."
        <context>
        {context}
        </context>
        Question: {input}
    """)
    document_chain = create_stuff_documents_chain(groq, prompt)
    retriever = vector_store.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
    response = retrieval_chain.invoke({"input": user_question})
    st.write(response["answer"])

def generate_podcast_script(docs):
    """Generates a podcast script from the provided documents."""
    if not docs:
        st.warning("Please process your documents first.")
        return

    groq = get_groq_client()
    all_text = " ".join([doc.page_content for doc in docs])
    prompt = ChatPromptTemplate.from_template("""
        You are a creative podcast scriptwriter. 
        Generate a conversational podcast script between two hosts, 'Alex' and 'Ben'.
        Alex is the curious host who asks questions, and Ben is the expert who provides answers based on the provided text.
        The conversation should be engaging, natural, and based entirely on the following content.
        Content:
        {text}
    """)
    chain = prompt | groq

    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
    chunks = splitter.split_text(all_text)
    
    script_chunks = []
    progress = st.progress(0)
    for i, chunk in enumerate(chunks):
        try:
            part = chain.invoke({"text": chunk}).content
            script_chunks.append(part)
            progress.progress((i + 1) / len(chunks))
        except APIConnectionError:
            st.error("Connection Error: Please check your internet connection.")
            break

    if script_chunks:
        final_script = "\n\n".join(script_chunks)
        st.session_state.script = final_script
        st.success("Podcast script generated!")
        st.text_area("Generated Script", final_script, height=300)