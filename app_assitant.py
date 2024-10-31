from flask import Flask, render_template, request
from time import sleep
from utils import *
from prompt_system import *
from model_selection import model_str
from persona_selection import *
from select_document import *
from allspark_assistant import *

model, parser, cliente = initial_parameters()

app = Flask(__name__)
app.secret_key = 'allspark'

#### Thread e Assistente
# assistant = create_assistant()
# thread = create_thread()

assistant = get_json()
thread_id = assistant["thread_id"]
assistant_id = assistant["assistant_id"]
file_ids = assistant["file_ids"]

def bot(prompt):
    maximo_tentativas = 1
    repeticao = 0
    while True:
        try:
            personality = prompt_system_personas[selecionar_persona(prompt)]

            cliente.beta.threads.messages.create(
                            thread_id=thread_id, 
                            role = "user",
                            content =  f"""
                            {prompt_system_persona_selection_update}:

                            # Persona
                            {personality}
                            """,
                            file_ids=file_ids
                        )

            # Cria uma nova mensagem dentro da thread atual "thread"
            cliente.beta.threads.messages.create(
                thread_id=thread_id, 
                role = "user",
                content = prompt,
                file_ids=file_ids
            )
            # Cria uma nova execução dentro da thread atual, associando-a 
            # ao assistente que irá responder à pergunta do usuário.
            run = cliente.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id
            )
            # Aguarda até que até que o assistente resposta a pergunta do usuário.
            while run.status !="completed":
                run = cliente.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run.id
            )
            #  Recupera uma lista de todas as mensagens dentro da thread atual.
            historical = list(cliente.beta.threads.messages.list(thread_id=thread_id).data)
            response = historical[0]
            
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
    response = bot(prompt)
    print(f"Response: {response}")
    texto_resposta = response.content[0].text.value
    return texto_resposta

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)
