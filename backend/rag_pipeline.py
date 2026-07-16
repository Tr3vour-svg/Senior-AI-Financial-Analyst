import os
import time
import pickle
import hashlib
from typing import List, Dict, Any, Optional

try:
    from langchain_openai import OpenAIEmbeddings, ChatOpenAI
except Exception:
    OpenAIEmbeddings = None
    ChatOpenAI = None

try:
    from langchain_pinecone import PineconeVectorStore
except Exception:
    PineconeVectorStore = None

try:
    from pinecone import Pinecone, ServerlessSpec
except Exception:
    Pinecone = None
    ServerlessSpec = None

try:
    from langchain_community.retrievers import PineconeHybridSearchRetriever
except Exception:
    PineconeHybridSearchRetriever = None

try:
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
except Exception:
    ChatPromptTemplate = None
    StrOutputParser = None

# --- CONFIGURATION ---
INDEX_NAME = "big-tech-rag-2026"
NAMESPACE = "financial-reports"

# Simple Mock or In-Memory Cache Replacement for Notebook Persistent State
class LocalCache:
    def __init__(self):
        self.data = {}
    def get(self, key): return self.data.get(key)
    def set(self, key, val): self.data[key] = val

cache = LocalCache()

def get_llm(model_name: str = "gpt-4o-mini", temperature: float = 0.0) -> ChatOpenAI:
    """Initialize OpenRouter/OpenAI Compatible Interface"""
    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
        openai_api_key=os.environ.get("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        max_tokens=1024,
        timeout=60
    )

def extract_structured_data(all_raw_elements: List[Any]) -> List[Dict[str, Any]]:
    """Processes Unstructured elements, preserving tables and images metadata"""
    processed_chunks = []
    for element in all_raw_elements:
        el_type = getattr(element, "category", "Text")
        metadata = getattr(element, "metadata", LocalCache())
        
        chunk_data = {
            "text": str(element),
            "metadata": {
                "source": getattr(metadata, "filename", "Unknown"),
                "page_number": getattr(metadata, "page_number", 1),
                "has_tables": el_type == "Table"
            }
        }
        
        if el_type == "Table":
            chunk_data["metadata"]["table_html"] = getattr(metadata, "text_as_html", "")
            
        processed_chunks.append(chunk_data)
    return processed_chunks

def get_hybrid_retriever(bm25_encoder: Any):
    """Initializes standard Pinecone Hybrid Index Connection"""
    if Pinecone is None or OpenAIEmbeddings is None or PineconeHybridSearchRetriever is None:
        raise RuntimeError("Required RAG dependencies are not installed")

    pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
    index = pc.Index(INDEX_NAME)
    
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.environ.get("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1"
    )
    
    retriever = PineconeHybridSearchRetriever(
        embeddings=embeddings, 
        sparse_encoder=bm25_encoder, 
        index=index,
        namespace=NAMESPACE
    )
    return retriever

def generate_final_answer(query: str, retrieved_docs: List[Any]) -> str:
    """Core RAG Generation with Advanced Reasoning Models (Claude-3.5/GPT-4o)"""
    if ChatOpenAI is None or ChatPromptTemplate is None or StrOutputParser is None:
        raise RuntimeError("Required LLM dependencies are not installed")

    llm = get_llm(model_name="gpt-4o", temperature=0.0) # Swappable with target models
    
    context_block = "\n\n".join([
        f"Source: {doc.metadata.get('source')} (Page {doc.metadata.get('page_number')})\nContent: {doc.page_content}"
        for doc in retrieved_docs
    ])
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an Expert Financial Analyst. Review the 10-K document contexts provided and synthesize a highly accurate precision analysis."),
        ("human", "Contexts:\n{context_block}\n\nQuestion: {query}")
    ])
    
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"context_block": context_block, "query": query})