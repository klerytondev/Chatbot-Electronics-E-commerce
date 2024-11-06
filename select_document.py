from dotenv import load_dotenv
from utils import *
from model_selection import model_str

load_dotenv()

_, parser, client = initial_parameters()
parameters = {
    "temperature": 1,
    "max_tokens": 250,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0
}

politicas_allspark = load('data/imput/políticas_allspark.txt')
dados_allspark_ecommerce = load('data/imput/dados_allspark_ecommerce.txt')
produtos_allspark = load('data/imput/produtos_allspark.txt')

def select_document(resposta_openai):
    """
    Selects and returns the appropriate document content based on the input response.

    Args:
        resposta_openai (str): The response string from OpenAI containing keywords to determine the document selection.

    Returns:
        str: The concatenated document content based on the keyword found in the response.
             - If "políticas_allspark" is in the response, returns dados_allspark_ecommerce concatenated with politicas_allspark.
             - If "produtos_allspark" is in the response, returns dados_allspark_ecommerce concatenated with produtos_allspark.
             - Otherwise, returns dados_allspark_ecommerce.
    """
    if "políticas_allspark" in resposta_openai:
        return dados_allspark_ecommerce + "\n" + politicas_allspark
    elif "produtos_allspark" in resposta_openai:
        return dados_allspark_ecommerce + "\n" + produtos_allspark
    else:
        return dados_allspark_ecommerce 

def select_context(user_message):
    """
    Selects the most appropriate document context based on the user's message.

    This function evaluates the user's message and determines which of the three main documents 
    of the Allspark company is most relevant to the context of the response. The documents are:
    - Document 1: dados_allspark_ecommerce
    - Document 2: políticas_allspark
    - Document 3: produtos_allspark

    Args:
        user_message (str): The message from the user that needs to be evaluated.

    Returns:
        str: The identifier of the selected document context, which can be one of the following:
             "dados_allspark_ecommerce", "políticas_allspark", or "produtos_allspark".
    """
    prompt_system_user = f"""
    A empresa Allspark possui três documentos principais que detalham diferentes aspectos do negócio:

    #Documento 1 "\n {dados_allspark_ecommerce} "\n"
    #Documento 2 "\n" {politicas_allspark} "\n"
    #Documento 3 "\n" {produtos_allspark} "\n"

    Avalie o prompt do usuário e retorne o documento mais indicado para ser usado no contexto da resposta. Retorne "dados_allspark_ecommerce" se for o Documento 1, "políticas_allspark" se for o Documento 2 e "produtos_allspark" se for o Documento 3. 

    """
    selected_model = model_str(prompt_system_user, user_message)
    resposta = client.chat.completions.create(
        # model=modelo,
        messages=[
            {
                "role": "system",
                "content": prompt_system_user
            },
            {
                "role": "user",
                "content" : user_message
            }
        ],
        **parameters,
        model = selected_model
    )

    contexto = parser.invoke(resposta.choices[0].message.content.lower())
    print(f"Contexto selecionado: {contexto}")
    return contexto