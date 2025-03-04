import streamlit as st
from time import sleep
import os
from fake_useragent import UserAgent

from langchain_community.document_loaders import (WebBaseLoader,
                                                  YoutubeLoader,
                                                  PyPDFLoader,
                                                  CSVLoader,
                                                  TextLoader)

# Define a pasta local onde os arquivos serão salvos
OUTPUT_DIR = "/Users/leonardomota/Desktop/PatrimoniAI/Dev_/patrimoni-agent/backend/memory/files"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Website loader
def website_loader(url, file_name):
    final_document = ''
    for i in range(10):
        try:
            os.environ['USER_AGENT'] = UserAgent().random
            loader = WebBaseLoader(url, raise_for_status=True)
            list_documents = loader.load()
            final_document = '\n\n'.join([doc.page_content for doc in list_documents])
            break
        except:
            print(f'Erro ao carregar a página {url}. Tentativa {i + 1} de 10.')
            sleep(3)
    if final_document == '':
        st.error(f'Não foi possivel carregar a página {url}.')
        st.stop()
    # Salvar o final_document em um arquivo
    output_file_path = os.path.join(OUTPUT_DIR, file_name)
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(final_document)
    return final_document

# Youtube loader
def youtube_loader(video_id, file_name):
    loader = YoutubeLoader(video_id, add_video_info=False, language='pt')
    list_documents = loader.load()
    final_document = '\n\n'.join([doc.page_content for doc in list_documents])
    # Salvar o final_document em um arquivo
    output_file_path = os.path.join(OUTPUT_DIR, file_name)
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(final_document)
    return final_document

# PDF loader
def pdf_loader(file_path, file_name):
    loader = PyPDFLoader(file_path)
    list_documents = loader.load()
    final_document = '\n\n'.join([doc.page_content for doc in list_documents])
    # Salvar o final_document em um arquivo
    output_file_path = os.path.join(OUTPUT_DIR, file_name)
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(final_document)
    return final_document

# CSV loader
def csv_loader(file_path, file_name):
    loader = CSVLoader(file_path)
    list_documents = loader.load()
    final_document = '\n\n'.join([doc.page_content for doc in list_documents])
    # Salvar o final_document em um arquivo
    output_file_path = os.path.join(OUTPUT_DIR, file_name)
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(final_document)
    return final_document

# Text loader
def text_loader(file_path, file_name):
    loader = TextLoader(file_path)
    list_documents = loader.load()
    final_document = '\n\n'.join([doc.page_content for doc in list_documents])
    # Salvar o final_document em um arquivo
    output_file_path = os.path.join(OUTPUT_DIR, file_name)
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(final_document)
    return final_document