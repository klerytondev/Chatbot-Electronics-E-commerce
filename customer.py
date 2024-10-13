from langserve import RemoteRunnable

remote_chain = RemoteRunnable("http://localhost:8000/tradutor")
response = remote_chain.invoke({"idioma": "ingles", "texto": "eu te amo"})
print(response)