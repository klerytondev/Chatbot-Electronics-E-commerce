from dotenv import load_dotenv
import os
from openai import OpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import tiktoken

def parameters() -> tuple:
    load_dotenv()
    OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = ChatOpenAI(model="gpt-4o-mini")
    parser = StrOutputParser()
    return model, parser

model, parser  = parameters()
model_name = model.model_name 
codificador = tiktoken.encoding_for_model(model_name)

def model(prompt_system_model, prompt_usuario):
    token_list = codificador.encode(prompt_system_model + prompt_usuario)
    number_tokens = len(token_list)
    print(f"Número de tokens na entrada: {number_tokens}")
    expected_output_size = 2048
    selected_model = ChatOpenAI(model="gpt-4o-mini")
    if number_tokens >= 4096 - expected_output_size:
        selected_model = ChatOpenAI(model="gpt-4o")
    print(f"Modelo selecionado: {selected_model.model_name}")

    return selected_model