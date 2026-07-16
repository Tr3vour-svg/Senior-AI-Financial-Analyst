# Senior-AI-Financial-Analyst
An Agentic RAG Platform for Multimodal 10-K Analysis & Cross-Enterprise Intelligence
💡 Overview
The Junior AI Financial Analyst is an advanced, production-grade Hybrid RAG (Retrieval-Augmented Generation) pipeline designed to ingest, process, and analyze complex financial documents (like 10-K and 10-Q filings) with expert-level precision.

By combining hierarchical document layout parsing, hybrid dense/sparse vector search, agentic routing, and stateful memory, this system goes beyond basic keyword matching. It handles tricky multi-step financial reasoning—such as mapping supply chain vulnerabilities between suppliers (like ASML) and chipmakers (like TSMC and NVIDIA)—with strict data integrity and source tracking.

🧠 System Architecture & Key Features
               +--------------------------------------------------+
               |  Unstructured.io PDF Layout-Aware Partitioning   |
               +-----------------------+--------------------------+
                                       |
                                       v
               +--------------------------------------------------+
               |   Parent/Child Hierarchical Semantic Chunking   |
               +-----------------------+--------------------------+
                                       |
                                       v
               +--------------------------------------------------+
               |       Pinecone Hybrid Vector & Sparse Index      |
               |     (Dense: OpenAI v3  |  Sparse: BM25/SPLADE)    |
               +-----------------------+--------------------------+
                                       |
                                       v
               +--------------------------------------------------+
               |  LangGraph Agentic Flow with Reranking (Flash)   |
               +-----------------------+--------------------------+
                                       |
                                       v
               +--------------------------------------------------+
               |     OpenRouter Orchestration (GPT-4o & Claude)   |
               +--------------------------------------------------+
1. Advanced Document Partitioning
Layout-Aware Processing: Uses model-based layout detection (via unstructured) to cleanly separate running text, complex tables, and narrative blocks.

Hierarchical Chunking: Aggressively groups related financial sections while maintaining parent-child metadata relationships to preserve table formats and avoid fragmented data.

2. Hybrid Retrieval Engine
Dense + Sparse Vector Search: Combines semantic embeddings (OpenAI text-embedding-3-small) with keyword-matching sparse vectors (via Pinecone's BM25 hybrid search) to capture both high-level context and specific financial figures.

FlashRerank Integration: Compresses the retrieved context block to feed only the highest-quality, most-relevant chunks into the LLM, maintaining low latency and avoiding context window dilution.

3. Agentic Orchestration & Logic
Stateful Memory with LangGraph: Holds conversation context and tracks complex historical threads.

Intelligent Reasoning Gateways: Utilizes specialized prompt templates and reasoning configurations to prevent hallucinations, strictly enforcing source attribution (Filename, Page Number) in every analyst response.

🛠️ Project Structure
Plaintext
Junior_AI_Financial_Analyst/
├── backend/
│   ├── Dockerfile             # Multi-stage image build for FastAPI
│   ├── main.py                # FastAPI endpoints & streaming logic
│   ├── rag_pipeline.py        # Core RAG, LangGraph, & Pinecone retrieval
│   └── requirements.txt       # Backend Python dependencies
├── frontend/
│   ├── Dockerfile             # Lightweight Streamlit environment
│   └── app.py                 # Streamlit UI with conversation state
├── .env                       # Environment variables (API Keys)
└── docker-compose.yml         # Container orchestration configuration
🚀 Quick Start (Docker Deployment)
Deploying the entire ecosystem is streamlined into a resource-optimized, multi-container Docker compose orchestration.

1. Prerequisites
Make sure you have Docker and Docker Compose installed on your machine.

2. Clone and Setup Environment
Clone your repository and create a .env file in the root directory:

Bash
# Clone your repo
git clone https://github.com/yourusername/Junior-AI-Financial-Analyst.git
cd Junior-AI-Financial-Analyst

# Create your .env file
touch .env
Populate the .env file with your credentials:

Code snippet
OPENROUTER_API_KEY=your_openrouter_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here

# LangChain Tracing (Optional but highly recommended)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langchain_api_key_here
LANGCHAIN_PROJECT=big-tech-rag-2026
3. Run the Multi-Stage Build
To prevent out-of-memory or running out of disk space during concurrent builds, build and launch the services sequentially:

Bash
# 1. Clean any old build cache
docker system prune -f

# 2. Build and start the backend
docker compose up -d --build backend

# 3. Clean intermediate build steps to free disk space
docker builder prune -f

# 4. Build and start the frontend
docker compose up -d --build frontend
4. Access the Services
Streamlit UI (Interactive Dashboard): Open http://localhost:8501

FastAPI backend (Interactive Docs): Open http://localhost:8000/docs

📈 Example Queries to Try
Test the platform's ability to handle complex cross-document context synthesis:

🔍 "What are the specific risk factors Broadcom listed regarding dependence on a limited supply chain?"

🔍 "Map the cascading supply chain dependencies between ASML, TSMC, and NVIDIA based on their 10-K reports."
