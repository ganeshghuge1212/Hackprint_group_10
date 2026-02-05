import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pandas as pd
from typing import Dict, List, Any
import numpy as np

# ===== RAG IMPORTS =====
from sentence_transformers import SentenceTransformer
import faiss

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Web Scraper",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# CUSTOM CSS (UNCHANGED LOOK)
# ===============================
st.markdown("""
<style>
.stat-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 1rem;
    color: white;
    text-align: center;
}
.stat-value {
    font-size: 2.5rem;
    font-weight: bold;
}
.stat-label {
    font-size: 0.875rem;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# LOAD EMBEDDING MODEL (RAG)
# ===============================
@st.cache_resource
def load_rag_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

rag_model = load_rag_model()

# ===============================
# ORIGINAL SCRAPER (UNCHANGED)
# ===============================
class WebScraper:
    def __init__(self, url: str):
        self.url = url
        self.soup = None
        self.base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"

    def fetch_page(self):
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(self.url, headers=headers, timeout=10)
        response.raise_for_status()
        self.soup = BeautifulSoup(response.content, "html.parser")

    def extract_metadata(self):
        return {
            "title": self.soup.title.string if self.soup.title else "",
            "description": (self.soup.find("meta", {"name": "description"}) or {}).get("content", ""),
            "author": (self.soup.find("meta", {"name": "author"}) or {}).get("content", "")
        }

    def extract_text(self):
        for tag in self.soup(["script", "style", "noscript"]):
            tag.decompose()
        paragraphs = [p.get_text(strip=True) for p in self.soup.find_all("p")]
        return {
            "paragraphs": paragraphs,
            "all_text": " ".join(paragraphs)
        }

    def extract_images(self):
        imgs = []
        for img in self.soup.find_all("img"):
            src = img.get("src")
            if src:
                imgs.append({"url": urljoin(self.base_url, src), "alt": img.get("alt", "")})
        return imgs

    def extract_links(self):
        internal, external = [], []
        for a in self.soup.find_all("a", href=True):
            url = urljoin(self.base_url, a["href"])
            if urlparse(url).netloc == urlparse(self.base_url).netloc:
                internal.append(url)
            else:
                external.append(url)
        return {"internal": internal, "external": external}

    def scrape_all(self):
        self.fetch_page()
        text = self.extract_text()
        images = self.extract_images()
        links = self.extract_links()

        return {
            "metadata": self.extract_metadata(),
            "text": text,
            "images": images,
            "links": links,
            "stats": {
                "headings": len(self.soup.find_all(["h1","h2","h3","h4","h5","h6"])),
                "paragraphs": len(text["paragraphs"]),
                "images": len(images),
                "links": len(links["internal"]) + len(links["external"]),
                "tables": len(self.soup.find_all("table"))
            }
        }

# ===============================
# RAG FUNCTIONS (ADD ONLY)
# ===============================
def chunk_text(text, chunk_size=500, overlap=100):
    words = text.split()
    chunks, start = [], 0
    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))
        start = end - overlap
    return chunks

def build_faiss_index(chunks):
    embeddings = rag_model.encode(chunks)
    embeddings = np.array(embeddings).astype("float32")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index

def retrieve_chunks(question, chunks, index, top_k=3):
    q_emb = rag_model.encode([question])
    q_emb = np.array(q_emb).astype("float32")
    _, idx = index.search(q_emb, top_k)
    return [chunks[i] for i in idx[0]]

# ===============================
# MAIN APP
# ===============================
def main():
    st.title("🌐 Web Scraper")
    st.markdown("### Extract all data from any website instantly")

    url = st.text_input("Enter Website URL", placeholder="https://example.com")

    if st.button("🔍 Scrape Website"):
        scraper = WebScraper(url)
        data = scraper.scrape_all()
        st.session_state.data = data
        st.success("Scraping completed successfully!")

    if "data" in st.session_state:
        data = st.session_state.data

        st.subheader("📊 Statistics")
        c1, c2, c3, c4, c5 = st.columns(5)
        stats = data["stats"]

        for col, label in zip(
            [c1,c2,c3,c4,c5],
            ["Headings","Paragraphs","Images","Links","Tables"]
        ):
            with col:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{stats[label.lower()]}</div>
                    <div class="stat-label">{label}</div>
                </div>
                """, unsafe_allow_html=True)

        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "📝 Metadata",
            "📄 Paragraphs",
            "🖼️ Images",
            "🔗 Links",
            "📊 Tables",
            "📄 Full Text",
            "🤖 Q&A (RAG)"
        ])

        with tab1:
            st.json(data["metadata"])

        with tab2:
            for p in data["text"]["paragraphs"][:50]:
                st.write(p)

        with tab3:
            for img in data["images"]:
                st.image(img["url"], caption=img["alt"], use_container_width=True)

        with tab4:
            st.write("Internal Links:", len(data["links"]["internal"]))
            st.write("External Links:", len(data["links"]["external"]))

        with tab5:
            st.write("Tables detected:", stats["tables"])

        with tab6:
            st.write(data["text"]["all_text"])

        # ===============================
        # RAG TAB (YOUR REQUIREMENT)
        # ===============================
        with tab7:
            st.subheader("🤖 Ask Questions from this Website")

            question = st.text_input(
                "Ask a question",
                placeholder="What is this page about?"
            )

            if st.button("Get Answer using RAG"):
                full_text = data["text"]["all_text"]

                chunks = chunk_text(full_text)
                index = build_faiss_index(chunks)
                retrieved = retrieve_chunks(question, chunks, index)

                st.success("Answer")
                st.write(" ".join(retrieved))

# ===============================
# ENTRY POINT
# ===============================
if __name__ == "__main__":
    main()
