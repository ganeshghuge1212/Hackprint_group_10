# ui.py
import streamlit as st
from rag_system import HybridRAGSystem
import config

# ===================== Initialize RAG system =====================
@st.cache_resource
def load_rag():
    return HybridRAGSystem(
        mongodb_uri=config.MONGODB_URI,
        database_name=config.DATABASE_NAME,
        gemini_api_key=config.GEMINI_API_KEY
    )

rag = load_rag()

# ===================== Page Config =====================
st.set_page_config(
    page_title="Helix HR RAG System",
    page_icon="🧠",
    layout="wide"
)

# ===================== Title =====================
st.title("🧠 Helix HR RAG System")
st.markdown(
    """
    Ask any question related to **Employees, Attendance, Leave, or HR Policies**.
    The system will use structured and semantic search to provide answers.
    """
)

# ===================== Sidebar =====================
with st.sidebar:
    st.header("💡 Example Questions")
    examples = [
        "What is the designation of emp101?",
        "Show attendance for emp205 last month",
        "How many leave days does emp101 have left?",
        "Explain the work-from-home policy",
        "Who was absent on 2026-01-15?",
        "List employees with low attendance in December"
    ]
    for q in examples:
        if st.button(q):
            st.session_state.query = q

# ===================== Query Input =====================
query = st.text_input("Enter your HR question:", key="query")

# ===================== Search Button =====================
if st.button("Search") and query.strip():
    with st.spinner("Searching... 🔍"):
        result = rag.query(query)

    # ===================== Answer =====================
    st.subheader("✅ Answer")
    st.success(result["answer"])

    # ===================== Sources =====================
    st.subheader("📄 Sources")
    if result["sources"]:
        for i, src in enumerate(result["sources"], start=1):
            st.write(f"{i}. {src}")
    else:
        st.info("No sources found for this query.")

    # ===================== Metadata =====================
    st.subheader("ℹ️ Details")
    st.write(f"- Confidence: {result.get('confidence', 0):.2f}")
    st.write(f"- Search Method: {result.get('search_method', 'semantic')}")

# ===================== Footer =====================
st.markdown("---")
st.markdown(
    "Developed for **Helix HR RAG System**. Supports structured queries with employee IDs and semantic search for HR policies."
)
