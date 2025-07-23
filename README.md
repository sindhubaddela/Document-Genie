#  Document-Genie  
**Intelligent Document Processing Suite — Analyze, Summarize, and Transform**

![Python](https://img.shields.io/badge/Python-3.9+-brightgreen.svg)  
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-ff69b4.svg)  
![LLM](https://img.shields.io/badge/LLM-Groq%20Llama%203-8A2BE2.svg)  
![Embeddings](https://img.shields.io/badge/Embeddings-Hugging%20Face-yellow.svg)

🔗 **Project Link**: [Document Genie Web App](https://document-genie-313ftvxc.streamlit.app/)

---

An intelligent document processing suite that transforms your static documents into dynamic, interactive assets.  
**Analyze, summarize, chat with, and even create podcasts** from your files, all powered by a cutting-edge **RAG pipeline** and the speed of **Llama 3 on Groq**.

---

## Key Features

- 📄 **Multi-Format Document Processor**  
  Upload and process `.pdf`, `.docx`, and `.txt` files effortlessly.
- 🧠 **AI-Powered Summarizer**  
  Extracts key insights and presents a concise summary.
- 💬 **Conversational Q&A (Chat with your Docs)**  
  Ask natural language questions and receive accurate, contextual answers.
- 🎙️ **Dual-Voice Podcast Generator**  
  Generates a podcast script from your documents and produces an audio file with two distinct voices.
  

---


## Detailed Process
**Ingestion & Chunking**
Uploaded documents are split into smaller segments using RecursiveCharacterTextSplitter.

**Embedding & Indexing**
Chunks are embedded into vector representations using Hugging Face’s all-MiniLM-L6-v2 and stored in FAISS for efficient retrieval.

**Retrieval**
When a user asks a question, FAISS retrieves relevant chunks that serve as context for the LLM.

**Generation**
Contextual chunks are injected into a prompt and passed to the Llama 3 8B model (via Groq API) to generate accurate responses, summaries, or scripts.

**Voice Synthesis**
The podcast script is parsed into two speakers — Alex and Ben. The gTTS library synthesizes speech with domain-specific voices (.com and .co.uk), producing a conversational-style audio file.

---

## 🛠️ Tech Stack

| Component                | Technology                        |
| ------------------------ | --------------------------------- |
| **LLM & API**            | Groq (Llama 3 - 8B)               |
| **AI Orchestration**     | LangChain                         |
| **Frontend**             | Streamlit                         |
| **Embeddings**           | Hugging Face (`all-MiniLM-L6-v2`) |
| **Vector Store**         | FAISS (in-memory)                 |
| **Document Loading**     | `PyPDFLoader`, `Docx2txtLoader`   |
| **Voice Synthesis**      | gTTS (Google Text-to-Speech)      |
| **Programming Language** | Python                            |


```mermaid
graph TD
    %% Phase 1: Ingestion & Storage
    A["📤 Upload (.pdf / .docx / .txt)"] --> B["🧹 Preprocess & Embed"];
    B --> C["🧠 FAISS Vector Store"];
    B --> D["📄 Documents"];

    %% Feature A: Chat with Document
    E["💬 User Query"] --> F["🔍 Retrieval Chain"];
    C --> F;
    F --> G["🧠 Llama 3 (via Groq)"];
    G --> H["📝 Generated Answer"];

    %% Feature B: Summarization & Podcast
    I["🧾 User Request"] --> J["🧠 Generation Chain"];
    D --> J;
    J --> G;
    G --> K["📚 Summary / Script"];
    K -->|Podcast Option| L["🔊 Text-to-Speech (gTTS)"];
    L --> M["🎧 MP3 Output"];

    %% Node Styling
    style C fill:#ec4899,color:#fff,stroke-width:1.5px
    style D fill:#f9a8d4,color:#000,stroke-width:1.5px
    style G fill:#8A2BE2,color:#fff,stroke-width:1.5px
    style H fill:#a5b4fc,color:#000




