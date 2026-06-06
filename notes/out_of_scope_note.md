# Brief Note: Handling Out-of-Scope Questions

The system is strictly designed to prevent hallucination when asked questions outside the scope of the provided knowledge base. It achieves this through a two-step process:

### 1. Vector Search (FAISS)
When a user asks a question, the local FAISS database searches for the top 3 most mathematically similar text chunks in the document. Even if the question is completely unrelated (e.g., *"Who is the CEO of Google?"*), FAISS will still return 3 chunks.

### 2. Strict LangChain Prompting
To prevent the LLM from trying to answer the unrelated question using the retrieved chunks or its own internal knowledge, we use a heavily engineered `ChatPromptTemplate` in LangChain. 

The system prompt explicitly commands the model:
> *"If the answer is NOT in the context, say EXACTLY: 'This information is not available in the provided document.' Never hallucinate or use outside knowledge."*

### Conclusion
Because the retrieved chunks will not contain the answer to the out-of-scope question, the LLM obeys the strict system prompt and safely refuses to answer. This guarantees a highly reliable, document-faithful RAG application.
