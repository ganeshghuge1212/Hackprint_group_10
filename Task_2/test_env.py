import torch
import faiss
from sentence_transformers import SentenceTransformer

print("Torch:", torch.__version__)
print("FAISS OK")
print("MiniLM test:", SentenceTransformer("all-MiniLM-L6-v2"))
