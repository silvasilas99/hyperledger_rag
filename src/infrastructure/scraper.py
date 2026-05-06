import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag
from typing import List, Optional
from src.core.interfaces import Scraper

class BeautifulSoupScraper(Scraper):
    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def fetch_content(self, url: str) -> Optional[str]:
        try:
            response = requests.get(url, timeout=self.timeout)
            if 'text/html' not in response.headers.get('Content-Type', ''):
                return None
            response.raise_for_status()
            return response.text
        except requests.RequestException:
            return None

    def extract_links(self, url: str, html: str) -> List[str]:
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        for link in soup.find_all('a', href=True):
            absolute_url = urljoin(url, link['href'])
            clean_url, _ = urldefrag(absolute_url)
            links.append(clean_url)
        return links

    def parse_main_content(self, html: str) -> str:
        soup = BeautifulSoup(html, 'html.parser')
        main_content = soup.find(attrs={"itemprop": "articleBody"}) or soup.find(attrs={"role": "main"})
        if main_content:
            return main_content.get_text(separator='\n', strip=True)
        return soup.get_text(separator='\n', strip=True)
