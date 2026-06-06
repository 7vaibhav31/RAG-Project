import os
import sys
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import CONFIG

def load_document(path: str):
    if not os.path.exists(path):
        print(f"❌ File not found: {path}")
        sys.exit(1)

    loader = TextLoader(path, encoding="utf-8")
    documents = loader.load()

    return documents

def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CONFIG["chunk_size"],
        chunk_overlap=CONFIG["chunk_overlap"],
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )

    chunks = splitter.split_documents(documents)

    return chunks
