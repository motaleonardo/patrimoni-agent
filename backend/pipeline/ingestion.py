import os
from dotenv import load_dotenv, find_dotenv
import sys

from llama_index.llms.openai import OpenAI
from llama_index.core.extractors import TitleExtractor, QuestionsAnsweredExtractor
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex

# Adicionando o diretório do backend ao path do sistema
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.configs.general_configs import CONFIG_MODELOS, TIPOS_ARQUIVOS_VALIDOS

# Load the environment variables
_ = load_dotenv(find_dotenv())




def llm_transformation(docs, model=CONFIG_MODELOS['modelos'][1], api_key=os.getenv("OPENAI_API_KEY")):

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

    nodes = pipeline.run(
        documents=docs,
        in_place=True,
        show_progress=True
    )
    return nodes

def llm_embeddings(nodes, model="text-embedding-3-small", api_key=os.getenv("OPENAI_API_KEY")):
    hf_embedding = OpenAIEmbedding(model=model, api_key=api_key)

    index = VectorStoreIndex(nodes=nodes, embed_model=hf_embedding)

    