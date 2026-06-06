import os
import tempfile
import streamlit as st
from config import CONFIG
from document_loader import load_document, chunk_documents
from vector_store import build_vectorstore, load_vectorstore
from rag_chain import build_rag_chain

st.set_page_config(page_title="Local RAG Chatbot", page_icon="🤖", layout="wide")

# ─── Sidebar: Project Info Only ────────────────────────────────────────────────
st.sidebar.title("📌 Project Details")
st.sidebar.info("""
**Local RAG Chatbot**
This application uses Retrieval-Augmented Generation (RAG) to let you chat with your documents locally.

**Tech Stack:**
- **Frontend:** Streamlit
- **LLM:** Phi-3 (via Ollama)
- **Embeddings:** Nomic Embed Text
- **Vector Store:** FAISS
- **Framework:** LangChain
""")

st.sidebar.markdown("---")
st.sidebar.title("💡 How it Works")
st.sidebar.markdown("""
1. **Upload:** You upload a document.
2. **Chunk:** The document is split into smaller pieces.
3. **Embed:** Each piece is converted into a vector.
4. **Retrieve:** When you ask a question, the most relevant pieces are found.
5. **Generate:** Phi-3 reads those pieces and answers your question!
""")

# ─── Main Header ───────────────────────────────────────────────────────────────
st.title("🤖 Local RAG Chatbot")

# ─── Upload Bar (alongside chat area, at the top of main content) ──────────────
upload_col, status_col = st.columns([2, 3])

with upload_col:
    # File uploader placed inline in the main content area
    uploaded_file = st.file_uploader(
        "📎 Upload a document to chat with it",
        type=["txt", "md"],
        label_visibility="collapsed",
        help="Upload a .txt or .md file"
    )

with status_col:
    if uploaded_file:
        st.success(f"✅ Loaded: **{uploaded_file.name}**")
    else:
        st.info("📂 No file uploaded — using default knowledge base")

st.divider()

# ─── RAG System Initialization ─────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def process_uploaded_file(file_content, filename):
    """Process an uploaded file: chunk, embed, and build RAG chain."""
    # Save uploaded content to a temporary .txt file on disk
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
        tmp_file.write(file_content)
        tmp_file_path = tmp_file.name

    with st.spinner(f"⏳ Processing **{filename}**..."):
        documents = load_document(tmp_file_path)
        chunks = chunk_documents(documents)
        vectorstore = build_vectorstore(chunks)
        chain = build_rag_chain(vectorstore)

    # Clean up the temporary file after processing
    os.remove(tmp_file_path)
    return chain

@st.cache_resource(show_spinner=False)
def initialize_default_system():
    """Load the default knowledge base if no file is uploaded."""
    # If a pre-built FAISS index exists, load it directly (faster)
    if os.path.exists(CONFIG["faiss_index_dir"]):
        vectorstore = load_vectorstore()
        return build_rag_chain(vectorstore)
    # Otherwise build fresh from the default document
    elif os.path.exists(CONFIG["document_path"]):
        with st.spinner("⏳ Building vector store from default document..."):
            documents = load_document(CONFIG["document_path"])
            chunks = chunk_documents(documents)
            vectorstore = build_vectorstore(chunks)
            return build_rag_chain(vectorstore)
    return None

# Determine which chain to use
chain = None
if uploaded_file is not None:
    content = uploaded_file.read()
    chain = process_uploaded_file(content, uploaded_file.name)
else:
    chain = initialize_default_system()
    if not chain:
        st.warning("⚠️ Please upload a document above to get started!")

# ─── Chat Interface ─────────────────────────────────────────────────────────────
if chain:
    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display all previous chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input box — pinned to the bottom by Streamlit automatically
    if prompt := st.chat_input("Ask a question about the document..."):
        # Show user message immediately
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generate and display the assistant's response
        with st.spinner("🤔 Thinking..."):
            result = chain.invoke({"query": prompt})
            answer = result["result"]

            with st.chat_message("assistant"):
                st.markdown(answer)

        # Save assistant message to history
        st.session_state.messages.append({"role": "assistant", "content": answer})
