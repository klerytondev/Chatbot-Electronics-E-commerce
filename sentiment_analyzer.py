from dotenv import load_dotenv
import os
import openai
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from prompt_system import prompt_system_analyzer
from utils import *
from model_selection import model

_, parser, _ = initial_parameters()

def save(nome_do_arquivo, conteudo) -> None:
    try:
        with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")

def analisador_sentimentos(produto, prompt_system_analyzer) -> None:
    try:
        prompt_usuario = load(f"data/imput/avaliacoes/avaliacoes-{produto}.txt")
        print(f"Iniciou a análise de sentimentos do produto {produto}")
        
        selected_model = model(prompt_system_analyzer, prompt_usuario)
        chain = selected_model | parser
        analise = chain.invoke(template_mensagem(prompt_system_analyzer, prompt_usuario))
        
        # Salvar a análise gerada
        save(f"./data/output/analise-{produto}.txt", analise)
        print(f"Análise salva em ./data/analise-{produto}.txt")
    except openai.AuthenticationError as e:
        print(f"Erro de Autenticação: {e}")
    except openai.APIError as e:
        print(f"Erro de API: {e}")

if __name__ == "__main__":
    # Mockado
    lista_de_produtos = ["Monitor de Alta Resolucao"]
    for produto in lista_de_produtos:
        analisador_sentimentos(produto, prompt_system_analyzer)