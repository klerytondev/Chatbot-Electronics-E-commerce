from openai import OpenAI
from dotenv import load_dotenv
import os
from prompt_system import *
from model_selection import model_str
from langchain_core.output_parsers import StrOutputParser
from time import sleep

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
parser = StrOutputParser()
selected_model = "gpt-4o-mini"
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