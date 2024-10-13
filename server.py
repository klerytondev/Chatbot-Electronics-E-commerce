from main import chain
from fastapi import FastAPI
from langserve import add_routes

app = FastAPI(title="Electronics E-commerce", 
              description= """
                Este Chat de IA foi desenvolvido 
                para oferecer um atendimento rápido 
                e personalizado, ajudando você a encontrar 
                os produtos eletrônicos ideais. 
                Com ele, você pode tirar dúvidas sobre 
                especificações de produtos, consultar a 
                disponibilidade em estoque, receber 
                recomendações baseadas em suas preferências, 
                acompanhar o status dos pedidos e até 
                obter suporte técnico. Nossa inteligência 
                artificial está sempre disponível, 
                proporcionando uma experiência de compra 
                simplificada e eficiente.
                """
                )

add_routes(app, chain, path="/tradutor")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)