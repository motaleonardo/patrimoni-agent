import os
from dotenv import load_dotenv, find_dotenv
import sys

from llama_index.llms.openai import OpenAI
from llama_index.core.extractors import TitleExtractor, QuestionsAnsweredExtractor
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

# Adicionando o diretório do backend ao path do sistema
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.configs.general_configs import CONFIG_MODELOS, TIPOS_ARQUIVOS_VALIDOS

# Load the environment variables
_ = load_dotenv(find_dotenv())


def llm_transformation(docs, model=CONFIG_MODELOS['modelos'][1], api_key=os.getenv("OPENAI_API_KEY")):
    """
    Aplica transformações (split, extração de título, Q&A) nos documentos
    usando o pipeline do llama_index.
    """

    llm_transformation = OpenAI(model=model, api_key=api_key)

    text_splitter = SentenceSplitter(separator=" ",
                                 chunk_size=1024,
                                 chunk_overlap=128)
    title_extractor = TitleExtractor(llm=llm_transformation, nodes=5)
    qa_extractor = QuestionsAnsweredExtractor(llm=llm_transformation, questions=3)

    pipeline = IngestionPipeline(
        transformations= [
            text_splitter,
            title_extractor,
            qa_extractor
        ]
    )

    # 'docs' deve ser uma lista de documentos ou algo compatível
    # com a pipeline. Você obteve esses docs do transformation_data
    # (transformação.py) ou diretamente de outro lugar.
    nodes = pipeline.run(
        documents=docs,
        in_place=True,
        show_progress=True
    )
    return nodes

def llm_embeddings(
        nodes, 
        model="text-embedding-3-small", 
        api_key=os.getenv("OPENAI_API_KEY"),
        qdrant_url="",
        collection_name="",):
    """
    Cria embeddings usando OpenAIEmbedding e envia os dados para o Qdrant.
    Retorna um objeto VectorStoreIndex que pode ser consultado posteriormente.
    """

    # Cria o embedding com OpenAI
    embedding_model = OpenAIEmbedding(model=model, api_key=api_key)

    # Conecta ao Qdrant (local ou remoto)
    client = QdrantClient(
        url=qdrant_url,
        collection_name=collection_name,
        embedding=embedding_model
    )

    # Define o vector store
    vector_store = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embedding_model
    )

    # Cria o índice que armazena os embeddings no Qdrant
    index = VectorStoreIndex(nodes, storage=vector_store)

    # (Opcional) persistir no disco local
    # index.storage_context.persist(persist_dir="./storage")

    return index

def ingest_docs_into_qdrant(docs):
    """
    Função de alto nível que faz todo o processo:
    1) Aplica transformações LLM
    2) Gera embeddings e indexa no Qdrant
    """

    openai_key = os.getenv("OPENAI_API_KEY")

    # Exemplo de uso de um modelo LLM
    nodes = llm_transformation(docs, model="text-embedding-3-small", api_key=openai_key)

    # Envia pro Qdrant (use o nome de collection que desejar)
    index = llm_embeddings(
        nodes,
        model="text-embedding-3-small",
        api_key=openai_key,
        qdrant_url="http://localhost:6333",
        qdrante_api_key=None,
        collection_name="llm_collection"
    )

    return index