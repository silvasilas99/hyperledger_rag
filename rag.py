import os
from transformers import pipeline
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFacePipeline
from langchain_classic.chains import RetrievalQA

# 1. Carregar documentos de texto
loader = DirectoryLoader('./dados_hyperledger', glob="*.txt", loader_cls=TextLoader)
documents = loader.load()

# 2. Dividir documentos em partes (Chunking) - Crucial para RAG
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(documents)

# 3. Criar Embeddings com Hugging Face (local)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-l6-v2")

# 4. Criar o Banco Vetorial FAISS
db = FAISS.from_documents(docs, embeddings)
db.save_local("faiss_index")

# 5. Carregar o banco vetorial
db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

# 6. Configurar o LLM localmente (TinyLlama é leve e excelente para rodar localmente)
model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
pipe = pipeline(
    "text-generation", 
    model=model_id, 
    max_new_tokens=512, 
    do_sample=True, 
    temperature=0.7, 
    top_k=50, 
    top_p=0.95
)
llm = HuggingFacePipeline(pipeline=pipe)

# 7. Criar a Cadeia de RAG
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=db.as_retriever(search_kwargs={"k": 2}) # Recupera os top 2
)

# 8. Fazer uma pergunta
pergunta = "O que é Hyperledger?"
resposta = qa_chain.invoke(pergunta)
print(resposta['result'])