import time
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from config import CONFIG

def build_vectorstore(chunks):
    start = time.time()

    embeddings = OllamaEmbeddings(model=CONFIG["embed_model"])

    # For EACH chunk → calls Ollama API → gets 768-dim vector → stores in FAISS
    vectorstore = FAISS.from_documents(chunks, embeddings)

    elapsed = time.time() - start

    # Save locally — next time you can load instead of re-embedding
    vectorstore.save_local(CONFIG["faiss_index_dir"])

    return vectorstore

def load_vectorstore():
    embeddings = OllamaEmbeddings(model=CONFIG["embed_model"])
    vectorstore = FAISS.load_local(CONFIG["faiss_index_dir"], embeddings, allow_dangerous_deserialization=True)
    return vectorstore
