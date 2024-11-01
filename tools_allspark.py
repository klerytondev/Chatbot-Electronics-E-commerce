import datetime
from flask import Flask,render_template, request, Response
from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
load_dotenv()
from utils import *


model, _, client = initial_parameters()

my_tools = [
    {"type": "file_search"},
    {
      "type": "function",
            "function": {
            "name": "validate_promo_code",
            "description": "Valide um código promocional com base nas diretrizes de Descontos e Promoções da empresa",
            "parameters": {
                "type": "object",
                "properties": {
                    "codigo": {
                        "type": "string",
                        "description": "O código promocional, no formato, TECHXX. Por exemplo: TECH10",
                    },
                    "validade": {
                        "type": "string",
                        "description": f"A validade do cupom, caso seja válido e esteja associado as políticas. No formato DD/MM/YYYY.",
                    },
                },
                "required": ["codigo", "validade"],
            }
        }
    }
    
]

def validate_promo_code(argumentos):
    print('Entrou na função')
    code = argumentos.get("codigo")
    expiration_date = argumentos.get("validade")

    return f"""
        
        # Formato de Resposta
        
        {code} com validade: {expiration_date}. 
        Ainda, diga se é válido ou não para o usuário.

        """

minhas_funcoes = {
    'validate_promo_code' : validate_promo_code,
}