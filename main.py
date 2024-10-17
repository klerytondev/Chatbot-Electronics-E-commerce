from dotenv import load_dotenv
import os
from openai import OpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

def parameters() -> tuple:
    load_dotenv()
    OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    modelo = ChatOpenAI(model="gpt-4o-mini", max_tokens=256)
    parser = StrOutputParser()
    return modelo, parser

# def template_mensagem(language, text) -> str:
#     template = ChatPromptTemplate.from_messages([
#         ("system", "Traduza o texto a seguir para {idioma}"),
#         ("user", "{texto}"),
#     ])
#     rendered_template = template.format(idioma=language, texto=text)
#     return rendered_template

def template_mensagem() -> str:
    return ChatPromptTemplate.from_messages([
        ("system", "Traduza o texto a seguir para {idioma}"),
        ("user", "{texto}"),
    ])

modelo, parser = parameters()

# Executando na porta 8000
chain = template_mensagem() | modelo | parser

## Executando no terminal
# user_prompt_idioma = input("Digite o idioma para tradução: ")
# user_prompt_text = input("Digite o texto para tradução: ")
# template = template_mensagem(user_prompt_idioma, user_prompt_text)

# chain = modelo | parser

# texto = chain.invoke(template)
# print(f"Texto traduzido: {texto}")