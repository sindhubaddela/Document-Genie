# Document-Genie
Intelligent Document Processing Suite - Analyze, Summarize, and Transform
![alt text](https://img.shields.io/badge/Python-3.9+-brightgreen.svg)
![alt text](https://img.shields.io/badge/Framework-Streamlit-ff69b4.svg)
![alt text](https://img.shields.io/badge/LLM-Groq%20Llama%203-8A2BE2.svg)
![alt text](https://img.shields.io/badge/Embeddings-Hugging%20Face-yellow.svg)

An intelligent document processing suite that transforms your static documents into dynamic, interactive assets. Analyze, summarize, chat with, and even create podcasts from your files, all powered by a cutting-edge RAG pipeline and the speed of Llama 3 on Groq.

<br>

✨ Key Features

📄 Multi-Format Document Processor: Seamlessly upload and process .pdf, .docx, and .txt files.

🧠 AI-Powered Summarizer: Distills lengthy documents into concise, well-structured summaries, highlighting key terms and concepts using Llama 3.

💬 Conversational Q&A (Chat with your Docs): Ask questions in natural language and receive context-aware answers sourced directly from your documents.

🎙️ Dual-Voice Podcast Generator: Automatically transforms your content into an engaging, two-host podcast script and generates the corresponding audio file.

⚡ Blazing Fast & Responsive: Built with the high-performance Groq API for near-instantaneous LLM responses and a sleek, modern UI created with Streamlit.

🏛️ Architecture & How It Works

Document Genie is built on a powerful Retrieval-Augmented Generation (RAG) architecture. This approach enhances the Large Language Model's capabilities by providing it with relevant, external information sourced directly from your documents.

Here's a breakdown of the workflow:

Generated mermaid
graph TD
    subgraph "1. Document Ingestion & Processing"
        A[User Uploads Files <br> (.pdf, .docx, .txt)] --> B{Load & Chunk Documents};
        B --> C[RecursiveCharacterTextSplitter];
    end

    subgraph "2. Indexing: Creating the Knowledge Base"
        C --> D{Generate Embeddings <br> (Hugging Face 'all-MiniLM-L6-v2')};
        D --> E[Store in FAISS Vector Store <br> (In-Memory)];
    end

    subgraph "3. RAG Pipeline: Chat & Q&A"
        F[User Asks a Question] --> G{FAISS Retriever};
        G -- Fetches Relevant Chunks --> H{LangChain Stuff Chain};
        E -- Provides Context --> G;
        I[Groq Llama 3 LLM] --> H;
        H -- Injects Context into Prompt --> I;
        I --> J[Generated Answer];
    end

    subgraph "4. Advanced Content Generation"
        K[User requests Summary or Podcast] --> L{LangChain Prompt Engineering};
        L -- Creative Prompt --> M[Groq Llama 3 LLM];
        M --> N[Generates Summary / Podcast Script];
        N --> O{gTTS Voice Synthesis};
        O --> P[Dual-Voice MP3 Audio];
    end

    style A fill:#4f46e5,color:#fff
    style J fill:#a5b4fc,color:#000
    style P fill:#a5b4fc,color:#000
    style E fill:#ec4899,color:#fff


Ingestion & Chunking: Uploaded documents are loaded and broken down into smaller, manageable chunks using RecursiveCharacterTextSplitter.

Embedding & Indexing: Each chunk is converted into a numerical vector (an embedding) using a Hugging Face model. These vectors are stored in a FAISS vector store, creating a searchable knowledge base.

Retrieval: When you ask a question, the FAISS retriever scans the vector store to find the document chunks most relevant to your query.

Generation: The retrieved chunks are injected as context into a prompt, which is then sent to the Llama 3 8B model via the Groq API. This allows the LLM to generate a highly accurate and context-aware answer, summary, or podcast script.

Voice Synthesis: For podcasts, the generated script is parsed to identify two speakers ('Alex' and 'Ben'). The gTTS library then synthesizes the dialogue using different top-level domains (co.uk and .com) to simulate distinct voices.

🛠️ Tech Stack

LLM & API: Groq for Llama 3 8B model inference

AI & Orchestration: LangChain

Frontend: Streamlit

Embeddings: Hugging Face Sentence Transformers (all-MiniLM-L6-v2)

Vector Store: FAISS (in-memory)

Document Loading: PyPDFLoader, Docx2txtLoader

Voice Synthesis: gTTS (Google Text-to-Speech)

Language: Python

🚀 Getting Started

Follow these instructions to set up and run Document Genie on your local machine.

Prerequisites

Python 3.9 or higher

A Groq API Key

Installation

Clone the repository:

Generated sh
git clone https://github.com/sindhubaddela/Document-Genie.git
cd Document-Genie
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Sh
IGNORE_WHEN_COPYING_END

Create and activate a virtual environment (recommended):

Generated sh
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Sh
IGNORE_WHEN_COPYING_END

Install the required dependencies:

Generated sh
pip install -r requirements.txt
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Sh
IGNORE_WHEN_COPYING_END

Set up your API key:

Create a folder named .streamlit in the root of your project directory.

Inside the .streamlit folder, create a file named secrets.toml.

Add your Groq API key to the secrets.toml file like this:

Generated toml
GROQ_API_KEY = "your_groq_api_key_here"
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Toml
IGNORE_WHEN_COPYING_END
Running the Application

Launch the Streamlit app with the following command:

Generated sh
streamlit run app.py
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Sh
IGNORE_WHEN_COPYING_END

Your browser should automatically open to the application, ready for you to use!

📖 Usage Guide

Upload Documents: Use the sidebar to upload one or more files (.pdf, .docx, .txt).

Process Documents: Click the Process Documents button. This will create the vector store needed for all other features.

Generate a Summary: Navigate to the 📄 Summarizer tab and click Generate Summary.

Chat with Docs: Go to the 💬 Chat with Docs tab, type your question into the input box, and press Enter.

Create a Podcast:

In the 🎙️ Podcast Generator tab, first click Generate Podcast Script.

Once the script appears, click 🔊 Generate Audio to synthesize the MP3 file. You can then listen to it directly or download it.


Project Link: https://github.com/sindhubaddela/Document-Genie
