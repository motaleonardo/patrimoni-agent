from llama_index.llms.openai import OpenAI
from llama_index.llms.groq import Groq


CONFIG_MODELOS = {
    'Groq': {
        'modelos': ['gemma2-9b-it', 'llama-3.3-70b-versatile', 'mixtral-8x7b-32768'],
        'chat': Groq,
        'env_keys': {
            'llama-3.3-70b-versatile': 'GROQ_API_KEY',
            'gemma2-9b-it': 'GROQ_API_KEY',
            'mixtral-8x7b-32768': 'GROQ_API_KEY'
        }
    },
    'OpenAI': {
        'modelos': ['gpt-4o-mini-2024-07-18', 'gpt-4o-2024-08-06'],
        'chat': OpenAI,
        'env_keys': {
            'gpt-4o-mini-2024-07-18': 'OPENAI_API_KEY',
            'gpt-4o-2024-08-06': 'OPENAI_API_KEY'
        }
    }
}

TIPOS_ARQUIVOS_VALIDOS = [
    'SITE', 
    'YOUTUBE',
    'PDF',
    'CSV',
    'TXT'
]