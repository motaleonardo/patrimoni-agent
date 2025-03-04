from dotenv import load_dotenv, find_dotenv
import os

from llama_index.llms.openai import OpenAI

_ = load_dotenv(find_dotenv())

def ingest_data()