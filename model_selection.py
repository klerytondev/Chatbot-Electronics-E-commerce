from dotenv import load_dotenv
import os
from openai import OpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import tiktoken
from utils import *

model, *_ = initial_parameters()
model_name = model.model_name 
codificador = tiktoken.encoding_for_model(model_name)

def model_str(prompt_system_model, prompt_usuario):
    """
    Selects an appropriate language model based on the number of tokens in the input prompts.
    This function encodes the combined input prompts and calculates the number of tokens.
    Depending on the token count, it selects either a smaller or larger language model.
    Args:
        prompt_system_model (str): The system-generated prompt.
        prompt_usuario (str): The user-generated prompt.
    Returns:
        str: The name of the selected language model.
    """
    token_list = codificador.encode(prompt_system_model + prompt_usuario)
    number_tokens = len(token_list)
    print(f"Número de tokens na entrada: {number_tokens}")
    expected_output_size = 2048
    selected_model = ChatOpenAI(model="gpt-4o-mini")
    if number_tokens >= 4096 - expected_output_size:
        selected_model = ChatOpenAI(model="gpt-4o")
    print(f"Modelo selecionado: {selected_model.model_name}")

    return selected_model.model_name
