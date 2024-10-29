from dotenv import load_dotenv
from utils import *
from time import sleep
from prompt_system import *
from persona_selection import *

_, _, cliente = initial_parameters()

dados_allspark_ecommerce = load('data/imput/dados_allspark_ecommerce.txt')

def create_thread():
    return cliente.beta.threads.create()

def create_assistant():
    persona = {prompt_system_personas['neutro']}
    selected_model = model_str(prompt_system_allspark, str(persona))
    assistant = cliente.beta.assistants.create(
        name="Atendente Allspark",
        instructions = f"""{prompt_system_allspark}: 
                            # Contexto {dados_allspark_ecommerce}
                            # Persona {persona}
                        """,
        model = selected_model,
        )
    return assistant

