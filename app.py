from flask import Flask,render_template, request, Response
from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
from utils import load
from constants import prompt_system_allspark
from model_selection import model_str
from langchain_core.output_parsers import StrOutputParser

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
contexto = load("data/imput/dados_allspark_ecommerce.txt")

app = Flask(__name__)
app.secret_key = 'allspark'

def bot(prompt):
    maximo_tentativas = 1
    repeticao = 0

    while True:
        try:
            prompt_system = f"{prompt_system_allspark}: {contexto}"

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
