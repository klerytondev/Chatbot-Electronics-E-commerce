from dotenv import load_dotenv
import os
from openai import OpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import tiktoken

prompt_sistema = """
Identifique o perfil de compra para cada cliente a seguir.

O formato de saída deve ser:

cliente - descreva o perfil do cliente em 3 palavras
"""

def parameters() -> tuple:
    load_dotenv()
    OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    modelo = ChatOpenAI(model="gpt-4o-mini")
    parser = StrOutputParser()
    return modelo, parser

def template_mensagem(prompt_sistema, prompt_usuario) -> str:
    template = ChatPromptTemplate.from_messages([
        ("system", prompt_sistema),
        ("user", prompt_usuario),
    ])
    rendered_template = template.format(user=prompt_usuario, system=prompt_sistema)
    return rendered_template

def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r") as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        print(f"Erro: {e}")

prompt_usuario = carrega("data/lista_de_compras_100_clientes.csv")

modelo, parser  = parameters()
modelo_nome = modelo.model_name 
codificador = tiktoken.encoding_for_model(modelo_nome)

lista_de_tokens = codificador.encode(prompt_sistema + prompt_usuario)
numero_de_tokens = len(lista_de_tokens)
print(f"Número de tokens na entrada: {numero_de_tokens}")
tamanho_esperado_saida = 2048

if numero_de_tokens >= 4096 - tamanho_esperado_saida:
    modelo = ChatOpenAI(model="gpt-4o")

print(f"Modelo escolhido: {modelo}")

chain = modelo | parser

template = template_mensagem(prompt_sistema, prompt_usuario)
response = chain.invoke(template)
print(f"Respostas: {response}")
