import streamlit as st
import time
from document_processing import load_documents, create_vector_store
from llm_interactions import generate_summary, get_chatbot_response, generate_podcast_script
from voice_gen import synthesize_dual_voice

def main():
    st.set_page_config(
        page_title="Document Genie",
        layout="wide",
        page_icon="🧞‍♂️",
        initial_sidebar_state="expanded"
    )

    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
        }

        .stApp {
            background: linear-gradient(135deg, #0f172a, #1e293b);
            color: #e2e8f0;
        }

        /* Header */
        .main-header {
            background: linear-gradient(135deg, #4f46e5, #7c3aed, #ec4899);
            color: white;
            padding: 2.5rem 2rem;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }

        .main-header h1 {
            font-size: 2.6rem;
            font-weight: 900;
            margin-bottom: 0.5rem;
        }

        .main-header p {
            font-size: 1.1rem;
            font-weight: 400;
            margin-top: 0;
        }

        /* Feature Card */
        .feature-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(12px);
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1.2rem 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #f1f5f9;
        }

        .feature-card h3 {
            color: #a5b4fc;
            margin-bottom: 0.5rem;
        }

        .feature-card p {
            color: #cbd5e1;
        }

        /* Buttons */
        .stButton > button {
            background: linear-gradient(to right, #6366f1, #8b5cf6);
            color: white;
            padding: 0.7rem 2rem;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            font-size: 1rem;
            margin-top: 1rem;
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            background: linear-gradient(to right, #8b5cf6, #ec4899);
            transform: translateY(-2px);
            box-shadow: 0 4px 14px rgba(236, 72, 153, 0.3);
        }

        /* Inputs */
        .stTextInput input, .stFileUploader > div {
            background-color: #1e293b;
            color: #f1f5f9;
            border-radius: 10px;
            padding: 0.75rem;
            border: 1px solid #334155;
        }

        .stTextInput input:focus {
            border: 1px solid #818cf8;
            box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.2);
        }

        /* Audio Player */
        .stAudio {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 1rem;
            margin-top: 1rem;
        }

        /* Download Button */
        .stDownloadButton > button {
            background: linear-gradient(to right, #ec4899, #f97316);
            color: white;
            border-radius: 10px;
            padding: 0.7rem 2rem;
            font-weight: 600;
            border: none;
            margin-top: 1rem;
            transition: all 0.2s ease;
        }

        .stDownloadButton > button:hover {
            background: linear-gradient(to right, #f97316, #ec4899);
            box-shadow: 0 4px 14px rgba(249, 115, 22, 0.3);
            transform: scale(1.02);
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            background: #1e293b;
            border-radius: 12px;
            padding: 0.5rem;
        }

        .stTabs [data-baseweb="tab"] {
            color: #cbd5e1;
            font-weight: 500;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            transition: background 0.2s ease;
        }

        .stTabs [aria-selected="true"] {
            background: #4f46e5;
            color: white;
        }

        /* Progress bar */
        .stProgress > div > div {
            background: linear-gradient(to right, #8b5cf6, #f43f5e);
            border-radius: 8px;
        }

        /* Status box */
        .stStatus {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 1rem;
            color: #f1f5f9;
        }

        /* Footer */
        .footer {
            text-align: center;
            font-size: 0.9rem;
            color: #94a3b8;
            margin-top: 3rem;
        }
        </style>
    """, unsafe_allow_html=True)


    # Header
    st.markdown("""
        <div class="main-header">
            <h1>🧞‍♂️ Document Genie</h1>
            <p>Intelligent Document Processing Suite - Analyze, Summarize, and Transform</p>
        </div>
    """, unsafe_allow_html=True)

    # Initialize session state
    if "vector" not in st.session_state:
        st.session_state.vector = None
    if "docs" not in st.session_state:
        st.session_state.docs = None
    if "script" not in st.session_state:
        st.session_state.script = None

    # Sidebar
    with st.sidebar:
        st.header("📁 Upload Documents")
        uploaded_files = st.file_uploader("Upload PDF, DOCX, or TXT files", accept_multiple_files=True, type=["pdf", "docx", "txt"])

        if st.button("🔄 Process Documents"):
            if uploaded_files:
                with st.spinner("Processing documents..."):
                    documents = load_documents(uploaded_files)
                    st.session_state.vector, st.session_state.docs = create_vector_store(documents)
                st.success("✅ Documents processed successfully!")
            else:
                st.warning("⚠️ Please upload at least one document.")

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📄 Summarizer", "💬 Chat with Docs", "🎙️ Podcast Generator"])

    # --- Summarizer ---
    with tab1:
        st.markdown("""
            <div class="feature-card">
                <h3>📄 Document Summarizer</h3>
                <p>Generate concise summaries from your documents highlighting key insights.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🧠 Generate Summary"):
            if st.session_state.docs:
                generate_summary(st.session_state.docs)
            else:
                st.warning("⚠️ Please upload and process documents first.")

    # --- Chat ---
    with tab2:
        st.markdown("""
            <div class="feature-card">
                <h3>💬 Ask Anything</h3>
                <p>Interact with your documents.</p>
            </div>
        """, unsafe_allow_html=True)

        if st.session_state.vector:
            user_question = st.text_input("🔍 Ask your question:")
            if user_question:
                start_time = time.time()
                get_chatbot_response(st.session_state.vector, user_question)
                end_time = time.time()
                st.info(f"⚡ Response in {end_time - start_time:.2f} seconds.")
        else:
            st.warning("🛑 Please process your documents to use chat.")

    # --- Podcast ---
    with tab3:
        st.markdown("""
            <div class="feature-card">
                <h3>🎙️ Generate Podcast</h3>
                <p>Create a podcast-style audio summary of your documents.</p>
            </div>
        """, unsafe_allow_html=True)

        if st.button("📝 Generate Podcast Script"):
            if st.session_state.docs:
                generate_podcast_script(st.session_state.docs)
            else:
                st.warning("⚠️ Please process documents first.")

        if st.session_state.script:
            if st.button("🔊 Generate Audio"):
                with st.status("🎙️ Generating podcast audio...", expanded=True) as status:
                    try:
                        progress = st.progress(0.0)

                        def update_progress(pct):
                            progress.progress(pct)

                        audio_fp = synthesize_dual_voice(
                            st.session_state.script,
                            progress_callback=update_progress
                        )
                        audio_fp.seek(0)  # Ensure it's readable

                        st.audio(audio_fp, format='audio/mp3')
                        st.download_button(
                            label="📥 Download Podcast",
                            data=audio_fp,
                            file_name="podcast_dual_voice.mp3",
                            mime="audio/mpeg"
                        )
                        status.update(label="✅ Audio generated!", state="complete")
                    except Exception as e:
                        status.update(label="❌ Audio generation failed.", state="error")
                        st.error(f"Error: {e}")

    # Footer
    st.markdown("""---""")
    st.markdown("""
        <div style='text-align: center; color: #94a3b8; padding: 1.5rem 0;'>
            Made with ❤️ | © 2025 Document Genie
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
