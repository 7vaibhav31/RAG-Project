# Local RAG Chatbot

A **Retrieval-Augmented Generation (RAG)** chatbot that runs entirely on your local machine. Upload any text document and ask questions about it — powered by Ollama, LangChain, and FAISS.

---

## 📁 Project Structure

```
Intern_Project/
│
├── code/                       ← All Python source files
│   ├── app.py                  # Streamlit web UI (main entry point)
│   ├── config.py               # Central configuration (models, paths, settings)
│   ├── document_loader.py      # Loads and chunks documents
│   ├── vector_store.py         # Builds and loads FAISS vector store
│   ├── rag_chain.py            # Builds the LangChain RAG pipeline
│   ├── requirements.txt        # Python dependencies
│   ├── faiss_index/            # Auto-generated vector DB (gitignored)
│   └── .streamlit/
│       └── config.toml         # Streamlit theme (yellow)
│
├── document/                   ← Knowledge base
│   └── knowledge_base.txt      # Machine Learning reference guide
│
├── output/                     ← Q&A test results (screenshots)
│   ├── output_log.md           # Markdown file with embedded screenshots
│   └── *.jpg                   # 5 Q&A test result screenshots
│
├── notes/                      ← Project notes
│   └── out_of_scope_note.md    # How out-of-scope questions are handled
│
└── README.md                   ← This file
```

---

## 🛠️ Tech Stack

| Component      | Technology                          |
|----------------|-------------------------------------|
| **Frontend**   | Streamlit                           |
| **LLM**        | Phi-3 (via Ollama — runs locally)   |
| **Embeddings** | nomic-embed-text (via Ollama)       |
| **Vector DB**  | FAISS (local, no cloud needed)      |
| **Framework**  | LangChain                           |
| **Language**   | Python 3.10+                        |

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com) installed and running

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd Intern_Project
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

### 3. Install Python Dependencies
```bash
pip install -r code/requirements.txt
```

### 4. Pull the Required Ollama Models
```bash
ollama pull phi3
ollama pull nomic-embed-text
```

### 5. Run the App
```bash
streamlit run code/app.py
```

Then open your browser at: **http://localhost:8501**

---

## 💡 How It Works

```
User uploads a document
        ↓
Document is split into overlapping chunks (600 chars each)
        ↓
Each chunk is embedded into a vector using nomic-embed-text
        ↓
Vectors are stored in a local FAISS index
        ↓
User asks a question
        ↓
The most relevant chunks are retrieved from FAISS (top 3)
        ↓
Retrieved chunks + question are passed to Phi-3 via a strict prompt
        ↓
Phi-3 answers ONLY from the retrieved context
```

---

## 🚫 Out-of-Scope Question Handling

See [`notes/out_of_scope_note.md`](./notes/out_of_scope_note.md) for a full explanation.

The system uses a **strict prompt template** and **temperature = 0** to force the LLM to answer only from the provided document context. If the answer is not in the document, it refuses to answer rather than hallucinating.
