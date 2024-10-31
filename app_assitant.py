from flask import Flask, render_template, request
from time import sleep
from utils import *
from prompt_system import *
from model_selection import model_str
from persona_selection import *
from select_document import *
from allspark_assistant import *

model, parser, client = initial_parameters()

app = Flask(__name__)
app.secret_key = 'allspark'

assistant = get_json()
thread_id = assistant['thread_id']
vector_store_id = assistant['vector_store_id']
assistant_id = assistant['assistant_id']

STATUS_COMPLETED = "completed" 
STATUS_REQUIRES_ACTION = "requires_action" 

def bot(prompt):
    maximo_tentativas = 1
    repeticao = 0
    while True:
        try:
            personality = prompt_system_personas[selecionar_persona(prompt)]
            client.beta.threads.messages.create(
                            thread_id=thread_id, 
                            role = "user",
                            content =  f"""
                            {prompt_system_persona_selection_update}:

                            # Persona
                            {personality}
                            """,
                            # file_ids=file_ids
                        )

            # Cria uma nova mensagem dentro da thread atual "thread"
            client.beta.threads.messages.create(
                thread_id=thread_id, 
                role = "user",
                content = prompt,
                # file_ids=file_ids
            )
            # Cria uma nova execução dentro da thread atual, associando-a 
            # ao assistente que irá responder à pergunta do usuário.
            run = client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id
            )
            # Aguarda até que até que o assistente resposta a pergunta do usuário.
            while run.status !=STATUS_COMPLETED:
                run = client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run.id
            )
                print(f"Status: {run.status}")
                
                if run.status == STATUS_REQUIRES_ACTION:
                    tools_acionadas = run.required_action.submit_tool_outputs.tool_calls
                    respostas_tools_acionadas = [] 
                    for uma_tool in tools_acionadas:
                        nome_funcao = uma_tool.function.name
                        funcao_escolhida = minhas_funcoes[nome_funcao]
                        argumentos = json.loads(uma_tool.function.arguments)
                        print(argumentos)
                        resposta_funcao = funcao_escolhida(argumentos)

                        respostas_tools_acionadas.append({
                                "tool_call_id": uma_tool.id,
                                "output": resposta_funcao
                            })
                    
                    run = client.beta.threads.runs.submit_tool_outputs(
                            thread_id = thread_id,
                            run_id = run.id,
                            tool_outputs=respostas_tools_acionadas
                        )  

            #  Recupera uma lista de todas as mensagens dentro da thread atual.
            historical = list(client.beta.threads.messages.list(thread_id=thread_id).data)
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
    texto_resposta = response.content[0].text.value
    return texto_resposta

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)