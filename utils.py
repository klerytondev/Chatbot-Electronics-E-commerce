from langchain_core.prompts import ChatPromptTemplate
import openai

# Função para criar um template de mensagem
def template_mensagem(prompt_system, prompt_usuario) -> str:
    try:
        template = ChatPromptTemplate.from_messages([
            ("system", prompt_system),
            ("user", prompt_usuario),
        ])
        rendered_template = template.format(user=prompt_usuario, system=prompt_system)
        return rendered_template
    except openai.APIError as e:
        return f"Erro de API: {str(e)}"
    except openai.AuthenticationError as e:
        return f"Erro de Autenticação: {str(e)}"
    except Exception as e:
        return f"Ocorreu um erro inesperado: {str(e)}"
    
# Função para carregar um arquivo
def load(nome_do_arquivo) -> str:
    try:
        with open(nome_do_arquivo, "r", encoding="utf-8") as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        print(f"Erro: {e}")