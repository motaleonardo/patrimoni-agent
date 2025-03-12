import os
import tempfile
import nest_asyncio

from llama_index.core import SimpleDirectoryReader

nest_asyncio.apply()

def transformation_data(input_source: any):
    """
    Recebe como input:
      - Um caminho para um diretório (string).
      - Ou um objeto de arquivo (por exemplo, o resultado de st.file_uploader).
      - Ou até mesmo um texto bruto.
    
    O input é salvo em arquivo temporário (se necessário) e lido pelo SimpleDirectoryReader.
    Retorna um dicionário onde as chaves são os nomes dos arquivos e os valores o conteúdo dos documentos.
    """
    # Se for um diretório válido, use-o diretamente
    if isinstance(input_source, str) and os.path.isdir(input_source):
        temp_dir = input_source
    else:
        # Cria um diretório temporário
        temp_dir = tempfile.mkdtemp()
        # Define o nome do arquivo; se input_source tiver atributo 'name' (como o UploadedFile), use-o
        filename = getattr(input_source, "name", "temp_file.txt")
        file_path = os.path.join(temp_dir, filename)
        
        # Se o input_source tiver método de leitura (por exemplo, um objeto UploadedFile)
        if hasattr(input_source, "read"):
            # Lê os bytes e converte para string (assumindo utf-8)
            content = input_source.read()
            try:
                content = content.decode("utf-8")
            except (AttributeError, UnicodeDecodeError):
                content = str(content)
        else:
            # Se for apenas um texto bruto
            content = input_source

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    # Carrega os documentos usando o SimpleDirectoryReader
    docs = SimpleDirectoryReader(input_dir=temp_dir).load_data()

    # Configura o template e define metadados a serem excluídos
    for doc in docs:
        doc.text_template = "Metadata:\n{metadata_str}\n-----\nContent: {content}"
        # Inicializa a lista se não existir e adiciona 'page_label' se ainda não estiver presente
        if not hasattr(doc, "excluded_embed_metadata_keys") or doc.excluded_embed_metadata_keys is None:
            doc.excluded_embed_metadata_keys = []
        if "page_label" not in doc.excluded_embed_metadata_keys:
            doc.excluded_embed_metadata_keys.append("page_label")
    
    # Cria um dicionário com o nome do arquivo como chave e o conteúdo como valor
    docs_dict = {}
    for doc in docs:
        file_name = doc.metadata.get("file_name", doc.metadata.get("source", "unknown"))
        docs_dict[file_name] = doc.page_content

    return docs_dict
