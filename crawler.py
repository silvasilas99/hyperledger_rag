import os
import time
import requests
from urllib.parse import urljoin, urldefrag
from bs4 import BeautifulSoup
from collections import deque

class HyperledgerCrawler:
    def __init__(self, base_url, output_dir="hyperledger_docs"):
        self.base_url = base_url
        self.output_dir = output_dir
        self.visited_urls = set()
        self.queue = deque([base_url])

        # Cria o diretório de saída se não existir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def is_valid_url(self, url):
        """Verifica se a URL pertence à documentação base e não é um link externo."""
        return url.startswith(self.base_url)

    def extract_main_content(self, soup):
        """
        Extrai apenas o conteúdo útil da página do Read the Docs.
        O RTD geralmente encapsula o conteúdo principal em uma div com atributo 'itemprop="articleBody"' ou role='main'.
        """
        main_content = soup.find(attrs={"itemprop": "articleBody"})
        if not main_content:
            main_content = soup.find(attrs={"role": "main"})

        if main_content:
            return main_content.get_text(separator='\n', strip=True)
        return soup.get_text(separator='\n', strip=True) # Fallback

    def save_content(self, url, text):
        """Salva o texto extraído em um arquivo local, usando a rota da URL como nome."""
        # Cria um nome de arquivo seguro baseado na URL
        relative_path = url.replace(self.base_url, "").strip("/")
        if not relative_path:
            relative_path = "index"

        filename = relative_path.replace("/", "_").replace(".html", "") + ".txt"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"URL Original: {url}\n")
            f.write("="*50 + "\n\n")
            f.write(text)

        print(f"[+] Salvo: {filename}")

    def crawl(self):
        """Inicia o processo de crawling usando busca em largura (BFS)."""
        print(f"Iniciando crawling em: {self.base_url}")

        while self.queue:
            current_url = self.queue.popleft()

            # Remove fragmentos da URL (ex: #secao-1) para evitar duplicatas
            current_url, _ = urldefrag(current_url)

            if current_url in self.visited_urls:
                continue

            self.visited_urls.add(current_url)

            try:
                # Faz a requisição
                response = requests.get(current_url, timeout=10)
                # Verifica se o Content-Type é HTML
                if 'text/html' not in response.headers.get('Content-Type', ''):
                    continue

                response.raise_for_status()

                # Faz o parse da página
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extrai e salva o conteúdo
                content_text = self.extract_main_content(soup)
                if content_text:
                    self.save_content(current_url, content_text)

                # Encontra todos os links da página para continuar o crawling
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    absolute_url = urljoin(current_url, href)
                    clean_url, _ = urldefrag(absolute_url)

                    # Adiciona à fila se for uma URL válida e não visitada
                    if self.is_valid_url(clean_url) and clean_url not in self.visited_urls:
                        self.queue.append(clean_url)

                # Politeness policy: atraso de 0.5s para não sobrecarregar o servidor
                time.sleep(0.5)

            except requests.RequestException as e:
                print(f"[-] Erro ao acessar {current_url}: {e}")

        print(f"\nCrawling finalizado! {len(self.visited_urls)} páginas processadas.")

if __name__ == "__main__":
    # URL base do Hyperledger Fabric (substitua pela versão ou projeto desejado)
    # Certifique-se de manter a barra (/) no final para delimitar o escopo corretamente.
    TARGET_URL = "https://hyperledger-fabric.readthedocs.io/en/latest/"

    crawler = HyperledgerCrawler(base_url=TARGET_URL, output_dir="dados_hyperledger")
    crawler.crawl()
