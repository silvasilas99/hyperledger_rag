from typing import List, Set
from collections import deque
from src.core.interfaces import Scraper, Document, VectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

class CrawlerService:
    def __init__(self, scraper: Scraper, base_url: str):
        self.scraper = scraper
        self.base_url = base_url
        self.visited: Set[str] = set()
        self.queue = deque([base_url])

    def execute(self, max_pages: int = 10) -> List[Document]:
        documents = []
        count = 0
        while self.queue and count < max_pages:
            url = self.queue.popleft()
            if url in self.visited or not url.startswith(self.base_url):
                continue
            
            html = self.scraper.fetch_content(url)
            if not html:
                continue
                
            self.visited.add(url)
            content = self.scraper.parse_main_content(html)
            documents.append(Document(content=content, metadata={"url": url}))
            
            links = self.scraper.extract_links(url, html)
            for link in links:
                if link not in self.visited:
                    self.queue.append(link)
            
            count += 1
            print(f"[*] Processado ({count}/{max_pages}): {url}")
        return documents

class IngestionService:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    def execute(self, documents: List[Document]):
        # Converte documentos para chunks menores
        chunked_docs = []
        for doc in documents:
            texts = self.splitter.split_text(doc.content)
            for t in texts:
                chunked_docs.append(Document(content=t, metadata=doc.metadata))
        
        self.vector_store.add_documents(chunked_docs)
        print(f"[+] {len(chunked_docs)} chunks ingeridos no banco vetorial.")
