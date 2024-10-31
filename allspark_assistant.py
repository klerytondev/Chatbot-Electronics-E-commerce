from utils import *
import json
from prompt_system import *
from persona_selection import *

_, _, cliente = initial_parameters()

dados_allspark_ecommerce = load('data/imput/dados_allspark_ecommerce.txt')
dados_allspark_ecommerce = load('data/imput/allspark_ecommerce.txt')

def create_list_ids():
    list_file_ids = []

    file_allspark_ecommerce = cliente.files.create(
        file=open("data/imput/allspark_ecommerce.txt", "rb"),
        purpose="assistants"
    )
    list_file_ids.append(file_allspark_ecommerce.id)

    file_politicas = cliente.files.create(
        file=open("data/imput/políticas_allspark.txt", "rb"),
        purpose="assistants"
    )
    list_file_ids.append(file_politicas.id)

    file_produtos = cliente.files.create(
        file=open("data/imput/produtos_allspark.txt","rb"),
        purpose="assistants"
    )
    list_file_ids.append(file_produtos.id)

    return list_file_ids

def get_json():
    filename = "assistentes.json"
    
    if not os.path.exists(filename):
        thread_id    = create_thread()
        file_id_list = create_list_ids()
        assistant_id = create_assistant(file_id_list)
        data = {
            "assistant_id": assistant_id.id,
            "thread_id": thread_id.id,
            "file_ids": file_id_list
        }

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print("Arquivo 'assistentes.json' criado com sucesso.")
    
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("Arquivo 'assistentes.json' não encontrado.")


def create_thread():
    return cliente.beta.threads.create()

def create_assistant(file_ids=[]):
    persona = {prompt_system_personas['neutro']}
    selected_model = model_str(prompt_system_allspark, str(persona))
    assistant = cliente.beta.assistants.create(
        name="Atendente Allspark",
        instructions = f"{prompt_system_allspark}",
        model = selected_model,
        file_ids = file_ids
        )
    return assistant

