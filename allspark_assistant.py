from utils import *
import json
from openai import OpenAI
from prompt_system import *
from persona_selection import *
from tools_allspark import *

_, _, client = initial_parameters()

def create_thread(vector_store):
    return client.beta.threads.create(
        tool_resources={
            'file_search': {
                'vector_store_ids': [vector_store.id]
            }
        }
    )

def create_vector_store():
    vector_store = client.beta.vector_stores.create(
        name='Allspark Vector Store'
        )

    file_paths = [
        "data/imput/allspark_ecommerce.txt",
        "data/imput/políticas_allspark.txt",
        "data/imput/produtos_allspark.txt"
    ]
    file_streams = [open(path, 'rb') for path in file_paths]

    client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id,
        files=file_streams
    )

    return vector_store


def get_json():
    """
    Retrieves assistant configuration data from a JSON file. If the file does not exist,
    it creates a new assistant, vector store, and thread, saves their IDs to the file, 
    and returns the data.
    Returns:
        dict: A dictionary containing the assistant ID, vector store ID, and thread ID.
    Raises:
        FileNotFoundError: If the JSON file cannot be found when attempting to read it.
    """
    filename = "assistentes.json"
    
    if not os.path.exists(filename):
        vector_store = create_vector_store()
        thread = create_thread(vector_store)
        assistant = create_assistant(vector_store)

        data = {
            'assistant_id': assistant.id,
            'vector_store_id': vector_store.id,
            'thread_id': thread.id
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

def create_assistant(vector_store):
    """
    Creates an assistant instance with specified configurations.

    Args:
        vector_store (VectorStore): The vector store object containing the vector store ID.

    Returns:
        Assistant: The created assistant instance.

    """
    print("Criando assistente...")
    persona = {prompt_system_personas['neutro']}
    selected_model = model_str(prompt_system_allspark, str(persona))
    assistant = client.beta.assistants.create(
        name='Allspark Assistant 01',
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

