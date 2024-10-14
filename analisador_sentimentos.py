from dotenv import load_dotenv
import os
import openai
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt_sistema = f"""
        Você é um analisador de sentimentos de avaliações de produtos.
        Escreva um parágrafo com até 50 palavras resumindo as avaliações e 
        depois atribua qual o sentimento geral para o produto.
        Identifique também 3 pontos fortes e 3 pontos fracos identificados a partir das avaliações.

        # Formato de Saída e escrita do arquivo:

        Nome do Produto:
        Resumo das Avaliações:
        Sentimento Geral: [utilize aqui apenas Positivo, Negativo ou Neutro]
        Ponto fortes: lista com três bullets
        Pontos fracos: lista com três bullets
    """

def parameters() -> tuple:
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    modelo = ChatOpenAI(model="gpt-4o-mini", max_tokens=256)
    parser = StrOutputParser()
    return modelo, parser

def template_mensagem(prompt_sistema, prompt_usuario) -> str:
    template = ChatPromptTemplate.from_messages([
        ("system", "{system}"),
        ("user", "{user}"),
    ])
    rendered_template = template.format(user=prompt_usuario, system=prompt_sistema)
    return rendered_template

def load(nome_do_arquivo) -> str:
    try:
        with open(nome_do_arquivo, "r", encoding="utf-8") as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        print(f"Erro: {e}")

def save(nome_do_arquivo, conteudo) -> None:
    try:
        with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")

def analisador_sentimentos(produto, prompt_sistema) -> None:
    try:
        prompt_usuario = load(f"./data/avaliacoes-{produto}.txt")
        print(f"Iniciou a análise de sentimentos do produto {produto}")
        template = template_mensagem(prompt_sistema, prompt_usuario)
        
        modelo, parser = parameters()
        chain = modelo | parser
        analise = chain.invoke(template)
        
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
    analisador_sentimentos(produto, prompt_sistema)