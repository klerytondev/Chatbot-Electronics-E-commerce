from flask import Flask, render_template, request, Response
from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
from utils import load
from prompt_system import *
from model_selection import model_str
from persona_selection import *
from langchain_core.output_parsers import StrOutputParser
from select_document import *

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

app = Flask(__name__)
app.secret_key = 'allspark'

def bot(prompt):
    maximo_tentativas = 1
    repeticao = 0
    personality = prompt_system_personas[selecionar_persona(prompt)]
    contexto = selecionar_contexto(prompt)
    documento_selecionado = selecionar_documento(contexto)
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
