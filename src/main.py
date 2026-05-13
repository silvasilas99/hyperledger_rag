import os
import sys
import argparse

# Adiciona o diretório raiz ao sys.path para permitir importações do pacote 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.infrastructure.scraper import BeautifulSoupScraper
from src.infrastructure.vector_store import FAISSVectorStore
from src.infrastructure.llm import TinyLlamaModel, RAGChain
from src.application.services import CrawlerService, IngestionService

def get_args():
    parser = argparse.ArgumentParser(description="Hyperledger RAG CLI")
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")

    # Comando Crawl
    crawl_parser = subparsers.add_parser("crawl", help="Executa o crawler e gera o índice")
    crawl_parser.add_argument("--pages", type=int, default=10, help="Máximo de páginas")

    # Comando Ask
    ask_parser = subparsers.add_parser("ask", help="Faz uma pergunta ao RAG")
    ask_parser.add_argument("question", type=str, help="Sua pergunta")

    return parser.parse_args()

def main():
    args = get_args()
    TARGET_URL = "https://hyperledger-fabric.readthedocs.io/en/latest/"
    VECTOR_DB_PATH = "faiss_index_v2"
    
    scraper = BeautifulSoupScraper()
    vector_store = FAISSVectorStore()

    if args.command == "crawl":
        print(f"[i] Iniciando Crawling (máx {args.pages} páginas)...")
        crawler = CrawlerService(scraper, TARGET_URL)
        docs = crawler.execute(max_pages=args.pages)
        
        if not docs:
            print("[!] Erro: Nenhum documento foi coletado. Verifique sua conexão ou se a URL está acessível.")
            return

        ingestion = IngestionService(vector_store)
        ingestion.execute(docs)
        vector_store.save(VECTOR_DB_PATH)
        print("[v] Crawling e Ingestão concluídos.")

    elif args.command == "ask":
        if not os.path.exists(VECTOR_DB_PATH):
            print("[!] Erro: Índice vetorial não encontrado. Rode o comando 'crawl' primeiro.")
            return

        print("[i] Carregando banco vetorial e LLM...")
        vector_store.load(VECTOR_DB_PATH)
        llm_model = TinyLlamaModel()
        rag = RAGChain(llm_model, vector_store)

        print(f"\nPergunta: {args.question}")
        resposta = rag.ask(args.question)
        print(f"\nResposta: {resposta}")

    else:
        print("Use -h para ver os comandos. Ex: python src/main.py ask 'O que é Fabric?'")

if __name__ == "__main__":
    main()
