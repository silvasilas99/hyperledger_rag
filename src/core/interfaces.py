from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

class Document:
    def __init__(self, content: str, metadata: Dict[str, Any]):
        self.content = content
        self.metadata = metadata

class Scraper(ABC):
    @abstractmethod
    def fetch_content(self, url: str) -> Optional[str]:
        pass

    @abstractmethod
    def extract_links(self, url: str, html: str) -> List[str]:
        pass

    @abstractmethod
    def parse_main_content(self, html: str) -> str:
        pass

class VectorStore(ABC):
    @abstractmethod
    def add_documents(self, documents: List[Document]):
        pass

    @abstractmethod
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        pass

    @abstractmethod
    def save(self, path: str):
        pass

    @abstractmethod
    def load(self, path: str):
        pass

class LanguageModel(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass
