import pytest
from unittest.mock import MagicMock
from src.application.services import CrawlerService
from src.core.interfaces import Scraper

def test_crawler_service_executes_correctly():
    # Arrange
    mock_scraper = MagicMock(spec=Scraper)
    mock_scraper.fetch_content.side_effect = [
        "<html><body><a href='/page1'>Link</a></body></html>",
        "<html><body>Content of Page 1</body></html>"
    ]
    mock_scraper.extract_links.side_effect = [
        ["https://base.com/page1"],
        []
    ]
    mock_scraper.parse_main_content.side_effect = ["Index", "Page 1 Content"]
    
    service = CrawlerService(mock_scraper, "https://base.com/")
    
    # Act
    docs = service.execute(max_pages=2)
    
    # Assert
    assert len(docs) == 2
    assert docs[0].content == "Index"
    assert docs[1].metadata["url"] == "https://base.com/page1"
    assert mock_scraper.fetch_content.call_count == 2
