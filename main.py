from dotenv import load_dotenv
import os
from openai import OpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
chave_api = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

# mensagens = [
#     SystemMessage("Traduza o texto a seguir para inglês"),
#     HumanMessage("Se inscrevam no canal para aprender Python")
# ]

# chain = modelo | parser

# resposta = modelo.invoke(mensagens)
# texto = parser.invoke(resposta)

# texto = chain.invoke(mensagens)
# print(texto)


template_mensagem = ChatPromptTemplate.from_messages([
    ("system", "Traduza o texto a seguir para {idioma}"),
    ("user", "{texto}"),
])

# reposta = template_mensagem.invoke({"idioma": "francês", "texto": "Dê like no vídeo e comente o que você tá achando"}))
# print(reposta)
# # print(template_mensagem.invoke({"idioma": "francês", "texto": "Dê like no vídeo e comente o que você tá achando"}))

chain = template_mensagem | modelo | parser
texto = chain.invoke({"idioma": "francês", "texto": "Dê like no vídeo e comente o que você tá achando"})
print(texto)

