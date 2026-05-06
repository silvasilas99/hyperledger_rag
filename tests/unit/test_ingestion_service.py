import pytest
from unittest.mock import MagicMock
from src.application.services import IngestionService
from src.core.interfaces import Document, VectorStore

def test_ingestion_service_chunks_documents():
    # Arrange
    mock_vs = MagicMock(spec=VectorStore)
    service = IngestionService(mock_vs)
    
    # Conteúdo longo para forçar split (chunk_size=1000)
    long_content = "A" * 1500
    docs = [Document(content=long_content, metadata={"url": "test"})]
    
    # Act
    service.execute(docs)
    
    # Assert
    # Deve chamar add_documents com uma lista de pelo menos 2 chunks
    args, _ = mock_vs.add_documents.call_args
    ingested_docs = args[0]
    
    assert len(ingested_docs) >= 2
    assert ingested_docs[0].metadata["url"] == "test"
    mock_vs.add_documents.assert_called_once()
