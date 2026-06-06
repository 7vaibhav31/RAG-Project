# rag_project/config.py

CONFIG = {
    "document_path"  : "document/knowledge_base.txt",  # Knowledge base document
    "llm_model"      : "phi3",                         # LLM for answering
    "embed_model"    : "nomic-embed-text",             # Model for embeddings
    "chunk_size"     : 600,    # Characters per chunk
    "chunk_overlap"  : 80,     # Overlap between chunks
    "top_k_chunks"   : 3,      # How many chunks to retrieve per query
    "temperature"    : 0.7,    # Increased for better formatting flexibility
    "faiss_index_dir": "code/faiss_index",             # Where to save vector DB
}
