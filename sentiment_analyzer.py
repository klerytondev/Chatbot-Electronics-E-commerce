from dotenv import load_dotenv
import os
import openai
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from constants import prompt_system_analyzer
from utils import template_mensagem, load


def parameters() -> tuple:
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    modelo = ChatOpenAI(model="gpt-4o-mini")
    parser = StrOutputParser()
    return modelo, parser

def save(nome_do_arquivo, conteudo) -> None:
    try:
        with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")

def analisador_sentimentos(produto, prompt_system_analyzer) -> None:
    try:
        prompt_usuario = load(f"./data/avaliacoes-{produto}.txt")
        print(f"Iniciou a análise de sentimentos do produto {produto}")
        
        modelo, parser = parameters()
        chain = modelo | parser
        analise = chain.invoke(template_mensagem(prompt_system_analyzer, prompt_usuario))
        
        # Salvar a análise gerada
        save(f"./data/analise-{produto}.txt", analise)
        print(f"Análise salva em ./data/analise-{produto}.txt")
    except openai.AuthenticationError as e:
        print(f"Erro de Autenticação: {e}")
    except openai.APIError as e:
        print(f"Erro de API: {e}")

# Mockado
lista_de_produtos = ["Maquiagem mineral"]
for produto in lista_de_produtos:
    analisador_sentimentos(produto, prompt_system_analyzer)