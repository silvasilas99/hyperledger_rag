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
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.google.com/'
            }
            response = requests.get(url, headers=headers, timeout=self.timeout)
            if 'text/html' not in response.headers.get('Content-Type', ''):
                print(f"[!] Erro: Content-Type inválido ({response.headers.get('Content-Type')}) para {url}")
                return None
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"[!] Erro ao buscar {url}: {e}")
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
