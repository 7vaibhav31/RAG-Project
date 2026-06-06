from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from config import CONFIG

def build_rag_chain(vectorstore):
    # --- RETRIEVER ---
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": CONFIG["top_k_chunks"]}
    )

    # --- PROMPT TEMPLATE ---
    system_template = """You are an expert, highly professional question-answering assistant.
Your task is to answer the user's question STRICTLY based on the provided context.

RULES:
1. If the answer is NOT in the context, say EXACTLY: "This information is not available in the provided document."
2. Never hallucinate or use outside knowledge.
3. If the answer IS in the context, you MUST format your response beautifully:
   - Provide a brief introductory sentence.
   - Use clear, detailed bullet points (using `*` or `-`) for ALL facts and details.
   - Break down complex paragraphs into easy-to-read bulleted lists.
   - End by mentioning the relevant context.

CONTEXT:
{context}"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("human", "{question}")
    ])

    # --- LLM ---
    # Upgrading to ChatOllama to use the model's native system/user instruction formatting
    llm = ChatOllama(
        model=CONFIG["llm_model"],
        temperature=CONFIG["temperature"]
    )

    # --- RAG CHAIN ---
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )

    return chain
