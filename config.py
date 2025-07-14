#import os
#from dotenv import load_dotenv
#load_dotenv()
#GROQ_API_KEY = os.getenv("GROQ_API_KEY")
#MODEL_NAME = "llama3-8b-8192"
#EMBEDDINGS_MODEL_NAME = "all-MiniLM-L6-v2"


import os
import streamlit as st
GROQ_API_KEY = st.secrets["GROQ_API_KEY"] 
MODEL_NAME = "llama3-8b-8192"
EMBEDDINGS_MODEL_NAME = "all-MiniLM-L6-v2"