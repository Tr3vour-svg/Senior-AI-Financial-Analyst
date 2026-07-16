import streamlit as st
import requests
import uuid

st.set_page_config(
    page_title="Agentic 10-K Financial Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS matching the polished presentation theme visible in code buffers
st.markdown("""
<style>
    .status-box { background-color: #f0f2f6; border-radius: 5px; padding: 15px; margin-bottom: 10px; }
    .source-tag { background-color: #e1f5fe; color: #0288d1; border-radius: 3px; padding: 2px 6px; font-size: 0.85em; }
</style>
""", unsafe_allow_html=True)

# Backend service address tracking via internal network endpoints
API_URL = st.sidebar.text_input("FastAPI Backend URL", value="http://backend:8000")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("📊 Senior AI Financial Analyst")
st.caption("Agentic 10-K Analysis, Risk Factor Mapping, & Cross-Enterprise Visualizations")

# Sidebar quick query samples
st.sidebar.subheader("Quick Example Targets")
examples = [
    "What are the specific risk factors Broadcom listed regarding dependence on a limited supply chain?",
    "Map the cascading supply chain dependencies between ASML, TSMC, and NVIDIA."
]
for ex in examples:
    if st.sidebar.button(ex, key=ex[:30]):
        st.session_state.current_query = ex

# Chat container execution loop
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "sources" in msg and msg["sources"]:
            st.markdown(f"**Sources Evaluated:** " + " ".join([f"<span class='source-tag'>{s}</span>" for s in msg['sources']]), unsafe_allow_html=True)

user_input = st.chat_input("Query financial filings...")
if "current_query" in st.session_state and st.session_state.current_query:
    user_input = st.session_state.current_query
    del st.session_state.current_query

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
        
    with st.chat_message("assistant"):
        with st.spinner("Searching 10-K Documents & Appending Agent Context..."):
            try:
                response = requests.post(
                    f"{API_URL}/analyze/stream",
                    json={"query": user_input, "thread_id": st.session_state.thread_id},
                    timeout=120
                )
                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    sources = data["sources"]
                    
                    st.markdown(answer)
                    if sources:
                        st.markdown(f"**Sources Evaluated:** " + " ".join([f"<span class='source-tag'>{s}</span>" for s in msg['sources']]), unsafe_allow_html=True)
                    
                    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
                else:
                    st.error(f"Error returned from engine backend: {response.text}")
            except Exception as e:
                st.error(f"Failed to communicate with back-end pipeline architecture: {e}")