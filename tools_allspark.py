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
            "name": "validar_codigo_promocional",
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

def validar_codigo_promocional(argumentos):
    codigo = argumentos.get("codigo")
    validade = argumentos.get("validade")

    return f"""
        
        # Formato de Resposta
        
        {codigo} com validade: {validade}. 
        Ainda, diga se é válido ou não para o usuário.

        """

minhas_funcoes = {
    "validar_codigo_promocional": validar_codigo_promocional,
}