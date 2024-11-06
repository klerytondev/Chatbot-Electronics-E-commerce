from langchain_core.prompts import ChatPromptTemplate
import openai
import os
from openai import OpenAI
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

def initial_parameters() -> tuple:
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = ChatOpenAI(model="gpt-4o-mini")
    parser = StrOutputParser()
    return model, parser, client

# Função para criar um template de mensagem
def template_mensagem(prompt_system, prompt_user) -> str:
    """
    Generates a formatted message template using the provided system and user prompts.

    Args:
        prompt_system (str): The system prompt to be included in the template.
        prompt_user (str): The user prompt to be included in the template.

    Returns:
        str: The rendered message template.

    Raises:
        openai.APIError: If there is an error with the OpenAI API.
        openai.AuthenticationError: If there is an authentication error with the OpenAI API.
        Exception: If an unexpected error occurs.
    """
    try:
        template = ChatPromptTemplate.from_messages([
            ("system", prompt_system),
            ("user", prompt_user),
        ])
        rendered_template = template.format(user=prompt_user, system=prompt_system)
        return rendered_template
    except openai.APIError as e:
        return f"Erro de API: {str(e)}"
    except openai.AuthenticationError as e:
        return f"Erro de Autenticação: {str(e)}"
    except Exception as e:
        return f"Ocorreu um erro inesperado: {str(e)}"
    
# Função para carregar um arquivo
def load(file_name) -> str:
    try:
        with open(file_name, "r", encoding="utf-8") as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        print(f"Erro: {e}")