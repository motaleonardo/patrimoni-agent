import os
import nest_asyncio
from llama_index.core import SimpleDirectoryReader
from llama_index.core import Document
from llama_index.core.schema import MetadataMode


nest_asyncio.apply()

# Transforma os dados do texto na pasta em um dicionário com as chaves sendo o nome do arquivo e o valor sendo o texto do arquivo
# Exemplo: {'arquivo1.txt': 'texto do arquivo 1', 'arquivo2.txt': 'texto do arquivo 2'}
def transformation_data(filepath: str):
    for docs in os.listdir(filepath):
        docs = SimpleDirectoryReader(input_dir=filepath).load_data()

        # define o template do conteudo/metadata
        docs.text_template = "Metadata:\n{metadata_str}\n-----\nContent: {content}"

        # exclui o 'page_label' do embedding
        if "page_label" not in docs.excluded_embed_metadata_keys:
            docs.excluded_embed_metadata_keys.append("page_label")
    return docs

