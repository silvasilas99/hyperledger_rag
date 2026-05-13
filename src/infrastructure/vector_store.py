import os
from typing import List
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document as LCDocument
from src.core.interfaces import VectorStore, Document

class FAISSVectorStore(VectorStore):
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-l6-v2"):
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
        self.db = None

    def add_documents(self, documents: List[Document]):
        if not documents:
            print("[!] Aviso: Tentativa de adicionar uma lista vazia de documentos ao banco vetorial.")
            return
        lc_docs = [LCDocument(page_content=d.content, metadata=d.metadata) for d in documents]
        if self.db is None:
            self.db = FAISS.from_documents(lc_docs, self.embeddings)
        else:
            self.db.add_documents(lc_docs)

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        if not self.db:
            return []
        results = self.db.similarity_search(query, k=k)
        return [Document(content=r.page_content, metadata=r.metadata) for r in results]

    def save(self, path: str):
        if self.db:
            self.db.save_local(path)

    def load(self, path: str):
        if os.path.exists(path):
            self.db = FAISS.load_local(path, self.embeddings, allow_dangerous_deserialization=True)
