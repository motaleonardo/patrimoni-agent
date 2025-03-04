import os
import sys

# Adicionando o diretório do backend ao path do sistema
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from backend.configs.general_configs import CONFIG_MODELOS, TIPOS_ARQUIVOS_VALIDOS
from backend.loader.document_loader import *

from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate

MEMORIA = ConversationBufferMemory()

def load_file(file_type, file):
    pass

def model_loader(provider, model, api_key, back, inteligence):
    
    document = ''

    system_message = """""
    Você é um assistente virtual amigavel, com uma inteligência treinada para responder perguntas sobre o Grupo Luiz Höhl.
    Você possui acesso as seguintes informações vindas de um documento: {}:
    
    ###
    {}
    ###
    
    Utilize as informações fornecidas para basear suas respostas.

    Sempre que houver $ na saída, substitua por S.

    Se a informação do documento for algo como 'Just a moment...Enable JavaScript and cookies to continue' sugira ao usuário carregar novamente o assistente.
    
    """.format(back, inteligence)

    template = ChatPromptTemplate([
        ('system', system_message),
        ('user', '{input}')
    ])

    chat = CONFIG_MODELOS[provider]['chat'](model=model, 
                                            api_key=api_key)
    
    chain = template | chat

    st.session_state['chain'] = chain

def chat_page():
    st.header('Bem vindo ao assistente virtual!', divider=True)

    chain = st.session_state.get('chain')

    memory = st.session_state.get('memory', MEMORIA)
    for message in memory.buffer_as_messages:
        chat = st.chat_message(message.type)
        chat.markdown(message.content)

    input_message = st.chat_input('Fale com o assistente virtual:')
    if input_message:
        chat = st.chat_message('human')
        chat.markdown(input_message)

        response = chain.invoke({
            'input': input_message,
            'chat_history': memory.buffer_as_messages
        }).content

        chat = st.chat_message('ai')
        chat.markdown(response)

        memory.chat_memory.add_user_message(input_message)
        memory.chat_memory.add_ai_message(response)
        
        st.session_state['memory'] = memory

def sidebar():
    tabs = st.tabs('Upload de arquivos', 'Selecione o modelo')

    with tabs[0]: # Upload de arquivos
        st.subheader('Upload de arquivos')
        file_type = st.selectbox('Selecione o tipo de arquivo para upload:', TIPOS_ARQUIVOS_VALIDOS)
        if file_type == 'SITE':
            file = st.text_input('URL do site')
        if file_type == 'YOUTUBE':
            file = st.text_input('URL do vídeo')
        if file_type == 'PDF':
            file = st.file_uploader('Selecione o arquivo PDF', type=['.pdf'])
        if file_type == 'CSV':
            file = st.file_uploader('Selecione o arquivo CSV', type=['.csv'])
        if file_type == 'TXT':
            file = st.file_uploader('Selecione o arquivo TXT', type=['.txt'])
        
    with tabs[1]:
        st.subheader('Selecione o modelo')
        provider = st.selectbox('Selecione o modelo LLM:', CONFIG_MODELOS.keys())
        model = st.selectbox('Selecione o modelo para o assistente:', CONFIG_MODELOS[provider]['modelos'])
        env_key = CONFIG_MODELOS[provider]['env_keys'][model]
        api_key = os.getenv(env_key)

        if api_key:
            st.success(f'Chave de API carregada para {model}!')
        else:
            st.warning(f'Chave de API não encontrada para {model}. Favor contactar o Admin do Sistema!')
    
    if st.button('Carregar Modelo'):
        model_loader(provider, model, api_key, file_type, file)
    if st.button('Limpar Memória'):
        st.session_state['memory'] = MEMORIA

def main():
    with st.sidebar:
        sidebar()
    chat_page()

if __name__ == '__main__':
    main()