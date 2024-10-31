from utils import *
import json
from prompt_system import *
from persona_selection import *
from tools_allspark import *

_, _, cliente = initial_parameters()

# dados_allspark_ecommerce = load('data/imput/dados_allspark_ecommerce.txt')
# dados_allspark_ecommerce = load('data/imput/allspark_ecommerce.txt')

def create_vector_store():
    vector_store = cliente.beta.vector_stores.create(
        name='Allspark Vector Store'
        )

    file_paths = [
        "data/imput/allspark_ecommerce.txt",
        "data/imput/políticas_allspark.txt",
        "data/imput/produtos_allspark.txt"
    ]
    file_streams = [open(path, 'rb') for path in file_paths]

    cliente.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id,
        files=file_streams
    )

    return vector_store


# def create_list_ids():
#     list_file_ids = []

#     file_allspark_ecommerce = cliente.files.create(
#         file=open("data/imput/allspark_ecommerce.txt", "rb"),
#         purpose="assistants"
#     )
#     list_file_ids.append(file_allspark_ecommerce.id)

#     file_politicas = cliente.files.create(
#         file=open("data/imput/políticas_allspark.txt", "rb"),
#         purpose="assistants"
#     )
#     list_file_ids.append(file_politicas.id)

#     file_produtos = cliente.files.create(
#         file=open("data/imput/produtos_allspark.txt","rb"),
#         purpose="assistants"
#     )
#     list_file_ids.append(file_produtos.id)

#     return list_file_ids

def get_json():
    filename = "assistentes.json"
    
    if not os.path.exists(filename):
        vector_store = create_vector_store()
        thread = create_thread(vector_store)
        assistant = create_assistant(vector_store)
        data = {
            "assistant_id": assistant.id,
            "thread_id": vector_store.id,
            "thread_id": thread.id
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

# def create_assistant(file_ids=[]):
#     persona = {prompt_system_personas['neutro']}
#     selected_model = model_str(prompt_system_allspark, str(persona))
#     assistant = cliente.beta.assistants.create(
#         name="Atendente Allspark",
#         instructions = f"{prompt_system_allspark}",
#         model = selected_model,
#         tools = my_tools,
#         file_ids = file_ids
#         )
#     return assistant

def create_assistant(vector_store):
    persona = {prompt_system_personas['neutro']}
    selected_model = model_str(prompt_system_allspark, str(persona))
    assistant = cliente.beta.assistants.create(
        name='Ecomart Assistant',
        instructions=f"{prompt_system_allspark}",
        model=selected_model,
        tools=my_tools,
        tool_resources={
            'file_search': {
                'vector_store_ids': [vector_store.id]
            }
        }
    )
    return assistant

