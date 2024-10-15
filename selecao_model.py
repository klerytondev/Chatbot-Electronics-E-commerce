from dotenv import load_dotenv
import os
from openai import OpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import tiktoken
from constants import prompt_system_model
from utils import template_mensagem, load

def parameters() -> tuple:
    load_dotenv()
    OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    modelo = ChatOpenAI(model="gpt-4o-mini")
    parser = StrOutputParser()
    return modelo, parser

prompt_usuario = load("data/lista_de_compras_100_clientes.csv")

modelo, parser  = parameters()
modelo_nome = modelo.model_name 
codificador = tiktoken.encoding_for_model(modelo_nome)

lista_de_tokens = codificador.encode(prompt_system_model + prompt_usuario)
numero_de_tokens = len(lista_de_tokens)
print(f"Número de tokens na entrada: {numero_de_tokens}")
tamanho_esperado_saida = 2048

if numero_de_tokens >= 4096 - tamanho_esperado_saida:
    modelo = ChatOpenAI(model="gpt-4o")

print(f"Modelo escolhido: {modelo}")

chain = modelo | parser

template = template_mensagem(prompt_system_model, prompt_usuario)
response = chain.invoke(template)
print(f"Respostas: {response}")
