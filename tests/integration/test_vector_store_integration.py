import os
import shutil
import pytest
from src.infrastructure.vector_store import FAISSVectorStore
from src.core.interfaces import Document

def test_faiss_vector_store_save_and_load(tmp_path):
    # Arrange
    db_path = str(tmp_path / "test_faiss")
    vs = FAISSVectorStore()
    docs = [
        Document(content="Hyperledger Fabric is a blockchain", metadata={"id": 1}),
        Document(content="Ethereum is another blockchain", metadata={"id": 2})
    ]
    
    # Act
    vs.add_documents(docs)
    vs.save(db_path)
    
    # Novo objeto para carregar
    new_vs = FAISSVectorStore()
    new_vs.load(db_path)
    
    results = new_vs.similarity_search("What is Fabric?", k=1)
    
    # Assert
    assert len(results) == 1
    assert "Hyperledger" in results[0].content
    assert results[0].metadata["id"] == 1
