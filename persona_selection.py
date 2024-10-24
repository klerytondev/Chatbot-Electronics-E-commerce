from dotenv import load_dotenv
from prompt_system import *
from model_selection import model_str
from time import sleep
from utils import *

load_dotenv()

_, parser, cliente = parameters()
parameters = {
    "temperature": 1,
    "max_tokens": 15, ######### 300
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0
}

personality = prompt_system_persona_selection

def selecionar_persona(user_message):
    prompt_system = prompt_system_persona_selection
    selected_model = model_str(prompt_system, user_message)
    resposta = cliente.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": prompt_system
            },
            {
                "role": "user",
                "content" : user_message
            }
        ],
        **parameters,
        model = selected_model
    )
    texto_resposta = parser.invoke(resposta.choices[0].message.content.lower())
    return texto_resposta