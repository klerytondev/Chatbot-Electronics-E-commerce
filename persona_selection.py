from dotenv import load_dotenv
from prompt_system import *
from model_selection import model_str
from time import sleep
from utils import *

load_dotenv()

_, parser, client = initial_parameters()
parameters = {
    "temperature": 1,
    "max_tokens": 250,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0
}

personality = prompt_system_persona_selection

def select_persona(user_message):
    prompt_system = prompt_system_persona_selection
    selected_model = model_str(prompt_system, user_message)
    response = client.chat.completions.create(
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
        model = selected_model,
    )
    text_response = parser.invoke(response.choices[0].message.content.lower())
    return text_response