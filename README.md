# Hyperledger Crawler & RAG

Este projeto implementa um sistema de **RAG (Retrieval-Augmented Generation)** local e gratuito para consultar a documentação do Hyperledger Fabric. Ele utiliza uma arquitetura limpa (**Clean Architecture**) e segue os princípios **SOLID**.

## 🚀 Funcionalidades

- **Crawler:** Coleta automática da documentação oficial do Hyperledger Fabric.
- **RAG Local:** Sistema de perguntas e respostas usando modelos de linguagem locais.
- **Modelos Utilizados:**
  - **Embeddings:** `sentence-transformers/all-MiniLM-l6-v2` (Local)
  - **LLM:** `TinyLlama/TinyLlama-1.1B-Chat-v1.0` (Local/Gratuito)
- **Banco Vetorial:** FAISS.

## 📋 Pré-requisitos

- Python 3.10 ou superior.
- Ambiente virtual configurado.

## 🛠️ Instalação

1. Clone o repositório e acesse a pasta do projeto.
2. Crie e ative o ambiente virtual:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-mock
   ```

## 📖 Como usar

O projeto utiliza uma interface de linha de comando (CLI) única através do arquivo `src/main.py`.

### 1. Coleta de Dados (Crawling)
Para baixar a documentação e gerar o índice vetorial:
```bash
python3 src/main.py crawl --pages 50
```
*O índice será salvo na pasta `faiss_index_v2`. O sistema agora gerencia automaticamente o caminho de execução e utiliza headers de navegador para evitar bloqueios.*

### 2. Consulta (Ask)
Para fazer perguntas ao sistema RAG (requer que o passo de crawling tenha sido executado ao menos uma vez):
```bash
python3 src/main.py ask "Como configurar um serviço de ordenação BFT no Fabric v3.0?"
```

## 🧪 Testes

O projeto utiliza `pytest` para testes de unidade e integração.

Para rodar todos os testes:
```bash
python -m pytest
```

Os testes estão divididos em:
- **Unidade:** Testam a lógica do Crawler e Ingestão isoladamente com Mocks.
- **Integração:** Testam a persistência e busca no banco vetorial FAISS.

## 🏗️ Estrutura do Projeto

```text
src/
├── core/           # Abstrações e Interfaces (Domínio)
├── application/    # Casos de uso e Serviços
├── infrastructure/ # Implementações concretas (Scraper, LLM, VectorStore)
└── main.py         # Ponto de entrada CLI
tests/              # Suite de testes
```

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.
