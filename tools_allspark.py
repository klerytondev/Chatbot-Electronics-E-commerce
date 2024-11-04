from dotenv import load_dotenv
load_dotenv()
from utils import *


model, _, client = initial_parameters()

my_tools = [
    {"type": "file_search"},
    {
      "type": "function",
            "function": {
            "name": "validate_promo_code",
            "description": "Valide um código promocional com base nas diretrizes de Descontos, validade e Promoções da empresa",
            "parameters": {
                "type": "object",
                "properties": {
                    "codigo": {
                        "type": "string",
                        "description": "O código promocional, no formato, TECHXX. Por exemplo: TECH10",
                    },
                    "validade": {
                        "type": "string",
                        "description": f"A validade do cupom esteja associado as políticas_allspark. No formato DD/MM/YYYY.",
                    },
                },
                "required": ["codigo", "validade"],
            }
        }
    }
    
]

def validate_promo_code(argumentos):
    code = argumentos.get("codigo")
    expiration_date = argumentos.get("validade")

    return f"""
        
        # Formato de Resposta
        
        {code} com validade até: {expiration_date}. 
        Ainda, diga se é válido ou não para o usuário.

    #     """
functions = {
    'validate_promo_code' : validate_promo_code,
}