from flask import Flask, render_template, request, Response
from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
from utils import *
from prompt_system import *
from model_selection import model_str
from persona_selection import *
from langchain_core.output_parsers import StrOutputParser
from select_document import *

model, parser, cliente = initial_parameters()

app = Flask(__name__)
app.secret_key = 'allspark'

def bot(prompt):
    maximo_tentativas = 1
    repeticao = 0
    personality = prompt_system_personas[selecionar_persona(prompt)]
    contexto = select_context(prompt)
    documento_selecionado = select_document(contexto)
    while True:
        try:
            prompt_system = f"""{prompt_system_allspark}: 
                                # Contexto {documento_selecionado}
                                # Persona {personality}
                            """

            selected_model = model_str(prompt_system, prompt)
            response = cliente.chat.completions.create(
                messages=[
                        {
                                "role": "system",
                                "content": prompt_system
                        },
                        {
                                "role": "user",
                                "content": prompt
                        }
                ],
                **parameters,
                model = selected_model
                )
            
            return response
        except Exception as erro:
                repeticao += 1
                if repeticao >= maximo_tentativas:
                        return "Erro no GPT: %s" % erro
                print('Erro de comunicação com OpenAI:', erro)
                sleep(1)
            

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json["msg"]
    resposta = bot(prompt)
    texto_resposta = parser.invoke(resposta.choices[0].message.content)
    return texto_resposta

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)
