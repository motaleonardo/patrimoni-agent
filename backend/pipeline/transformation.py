import nest_asyncio

from llama_index.core import SimpleDirectoryReader

nest_asyncio.apply()

# Transforma os dados do texto na pasta em um dicionário com as chaves sendo o nome do arquivo e o valor sendo o texto do arquivo
# Exemplo: {'arquivo1.txt': 'texto do arquivo 1', 'arquivo2.txt': 'texto do arquivo 2'}
def transformation_data(filepath: str):
    # Carrega todos os documentos da pasta
    docs = SimpleDirectoryReader(input_dir=filepath).load_data()
    
    for doc in docs:
        # define o template do conteudo/metadata
        docs.text_template = "Metadata:\n{metadata_str}\n-----\nContent: {content}"

        # exclui o 'page_label' do embedding
        if "page_label" not in docs.excluded_embed_metadata_keys:
            docs.excluded_embed_metadata_keys.append("page_label")

    # Cria um dicionário onde as chaves são os nomes dos arquivos e os valores são o conteúdo do documento
    docs_dict = {}
    for doc in docs:
        # Tenta obter o nome do arquivo a partir dos metadata (pode ser 'file_name' ou 'source', conforme seu loader)
        file_name = doc.metadata.get("file_name", doc.metadata.get("source", "unknown"))
        docs_dict[file_name] = doc.page_content

    return docs_dict
