import streamlit as st
import os
import hashlib
import pickle
import pandas as pd
from load_paper import load_pdf
from text_splitter import split_text
from embeddings import create_embeddings
from vector_store import create_vector_store, save_index, load_index
from search import search
from llm import generate_answer

# Page configuration
st.set_page_config(
    page_title="InsightPaper - Research Paper Analyzer",
    page_icon="📄",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .analysis-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #007bff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if "paper_data" not in st.session_state:
    st.session_state.paper_data = {
        "chunks": None,
        "index": None,
        "filename": None,
        "analysis": None,
        "metadata": None
    }

if "messages" not in st.session_state:
    st.session_state.messages = []

def get_file_hash(file_content):
    return hashlib.sha256(file_content).hexdigest()

def process_paper(file):
    """Pipeline to process the uploaded PDF and generate initial analysis."""
    file_content = file.read()
    file_hash = get_file_hash(file_content)

    # Cache setup
    cache_dir = "cache"
    os.makedirs(cache_dir, exist_ok=True)
    index_path = os.path.join(cache_dir, f"{file_hash}.index")
    chunks_path = os.path.join(cache_dir, f"{file_hash}.chunks")
    analysis_path = os.path.join(cache_dir, f"{file_hash}.analysis")

    # Check if cached version exists
    if os.path.exists(index_path) and os.path.exists(chunks_path) and os.path.exists(analysis_path):
        st.info("⚡ Loading processed version from cache...")
        with open(chunks_path, "rb") as f:
            chunks = pickle.load(f)
        index = load_index(index_path)
        with open(analysis_path, "rb") as f:
            analysis = pickle.load(f)

        # We still need to load PDF for metadata
        temp_file_path = os.path.join("temp_uploads", file.name)
        os.makedirs("temp_uploads", exist_ok=True)
        with open(temp_file_path, "wb") as f:
            f.write(file_content)
        _, metadata = load_pdf(temp_file_path)
        os.remove(temp_file_path)

        return {
            "chunks": chunks,
            "index": index,
            "filename": file.name,
            "analysis": analysis,
            "metadata": metadata
        }

    # Save file temporarily for load_pdf
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, file.name)

    with open(file_path, "wb") as f:
        f.write(file_content)

    try:
        with st.status("Analyzing research paper...", expanded=True) as status:
            st.write("📖 Extracting text and metadata from PDF...")
            paper_text, metadata = load_pdf(file_path)

            if not paper_text or len(paper_text.strip()) < 50:
                st.error("Could not extract enough text from this PDF. It may be a scanned image.")
                return None

            st.write("✂️ Splitting text into chunks...")
            chunks = split_text(paper_text)

            st.write(f"🧬 Creating embeddings for {len(chunks)} chunks...")
            embeddings = create_embeddings(chunks)
            index = create_vector_store(embeddings)

            st.write("🤖 Generating automated analysis...")
            analysis = {}
            prompts = {
                "Summary": "Provide a comprehensive summary of this research paper in 3-4 sentences. What is the paper about?",
                "Key Findings": "What are the key findings and contributions of this research paper? List the most important 3-4 points.",
                "Methodology": "What methodology or approach does this paper use? Describe the techniques, datasets, or frameworks used.",
                "Conclusion": "What are the main conclusions and future directions suggested by this paper?"
            }

            for section, question in prompts.items():
                st.write(f"Analyzing {section}...")
                results = search(question, index, chunks)
                context = " ".join(results)
                answer = generate_answer(context, question)
                analysis[section] = answer

            status.update(label="Analysis Complete!", state="complete")

        # Save to cache
        save_index(index, index_path)
        with open(chunks_path, "wb") as f:
            pickle.dump(chunks, f)
        with open(analysis_path, "wb") as f:
            pickle.dump(analysis, f)

        return {
            "chunks": chunks,
            "index": index,
            "filename": file.name,
            "analysis": analysis,
            "metadata": metadata
        }
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

# Header
st.title("📄 InsightPaper")
st.subheader("AI-Powered Research Paper Analysis")
st.markdown("---")

# Sidebar for upload and settings
with st.sidebar:
    st.header("Upload Section")
    uploaded_file = st.file_uploader("Choose a research paper (PDF)", type="pdf")

    if uploaded_file:
        if st.button("Analyze Paper"):
            result = process_paper(uploaded_file)
            if result:
                st.session_state.paper_data = result
                # Clear chat history for a new paper
                st.session_state.messages = []
                st.rerun()

    if st.session_state.paper_data["filename"]:
        st.success(f"📄 Current paper: {st.session_state.paper_data['filename']}")
        if st.button("🗑️ Clear Analysis"):
            st.session_state.paper_data = {"chunks": None, "index": None, "filename": None, "analysis": None, "metadata": None}
            st.session_state.messages = []
            st.rerun()

    if "messages" in st.session_state and len(st.session_state.messages) > 0:
        if st.button("💬 Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

# Main Content
if st.session_state.paper_data["analysis"]:
    # Metadata View
    metadata = st.session_state.paper_data["metadata"]
    if metadata:
        st.markdown(f"""
        <div style="background-color: #e9ecef; padding: 15px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #6c757d;">
            <strong>Title:</strong> {metadata['Title']} | <strong>Author:</strong> {metadata['Author']}
        </div>
        """, unsafe_allow_html=True)

    # Analysis View
    st.header("🔍 Automated Analysis")

    # View toggle
    view_mode = st.radio("Choose view mode:", ["Cards", "Table"], horizontal=True)

    analysis = st.session_state.paper_data["analysis"]

    if view_mode == "Cards":
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="analysis-card"><h4>📝 Summary</h4><p>{analysis["Summary"]}</p></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="analysis-card"><h4>🛠️ Methodology</h4><p>{analysis["Methodology"]}</p></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="analysis-card"><h4>💡 Key Findings</h4><p>{analysis["Key Findings"]}</p></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="analysis-card"><h4>🏁 Conclusion</h4><p>{analysis["Conclusion"]}</p></div>', unsafe_allow_html=True)
    else:
        df = pd.DataFrame(list(analysis.items()), columns=["Section", "Analysis"])
        st.table(df)

    st.markdown("---")

    # Chat Interface
    st.header("💬 Ask Follow-up Questions")

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "sources" in message:
                with st.expander("View Sources"):
                    for i, source in enumerate(message["sources"]):
                        st.markdown(f"**Source {i+1}:**\n{source}")

    # Chat input
    if prompt := st.chat_input("What would you like to know about this paper?"):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    results = search(prompt, st.session_state.paper_data["index"], st.session_state.paper_data["chunks"])
                    context = " ".join(results)
                    answer = generate_answer(context, prompt)
                    st.markdown(answer)

                    # Add response and sources to session state
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": results
                    })

                    # Show sources for the current response immediately
                    with st.expander("View Sources"):
                        for i, source in enumerate(results):
                            st.markdown(f"**Source {i+1}:**\n{source}")

                except Exception as e:
                    st.error(f"Error generating answer: {e}")

else:
    # Empty State
    st.info("👈 Please upload a PDF research paper in the sidebar to get started!")

    # Show an example of what the tool does
    st.image("https://via.placeholder.com/800x400?text=Upload+a+PDF+to+get+AI+Analysis", use_column_width=True)

    st.markdown("""
    ### How it works:
    1. **Upload**: You provide a research paper in PDF format.
    2. **Analysis**: The AI extracts text, creates vector embeddings, and generates a structured analysis.
    3. **Query**: You can ask specific questions about the methodology, results, or conclusions using a RAG-based chat.
    """)
