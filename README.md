# Chatbot Allspark E-commerce

**Desenvolvido por:** Kleryton de Souza Maria

## Visão Geral

O projeto "Chatbot Allspark E-commerce" visa desenvolver um chatbot inteligente para auxiliar clientes em um e-commerce de eletrônicos. Utilizando a API da OpenAI e a biblioteca `langchain`, o chatbot é capaz de fornecer respostas precisas e relevantes, melhorando a experiência do usuário e otimizando o atendimento ao cliente. A integração de IA Generativa e Modelos de Linguagem de Grande Escala (LLM) permite que o chatbot compreenda e responda a uma ampla variedade de consultas de forma natural e eficiente.

## Visão de Negócio

A implementação de um chatbot no e-commerce de eletrônicos visa:

- Melhorar a experiência do cliente com respostas rápidas e precisas.
- Reduzir a carga de trabalho do atendimento ao cliente.
- Aumentar a satisfação do cliente e, consequentemente, as vendas.

## Valor Gerado

O chatbot ajuda a transformar a interação com o cliente em uma experiência mais eficiente e agradável, permitindo que a empresa:

- **Responda a perguntas frequentes de forma automática:** O chatbot pode lidar com consultas comuns, liberando os atendentes humanos para lidar com questões mais complexas.
- **Ofereça suporte 24/7:** Com o chatbot, os clientes podem obter ajuda a qualquer hora do dia, melhorando a acessibilidade e a conveniência.
- **Direcione os clientes para os produtos certos com base em suas necessidades:** O chatbot pode recomendar produtos com base nas preferências e necessidades dos clientes, aumentando as chances de conversão.
- **Aumente a eficiência operacional:** Ao automatizar o atendimento ao cliente, a empresa pode reduzir custos operacionais e melhorar a eficiência.
- **Melhore a satisfação do cliente:** Respostas rápidas e precisas aumentam a satisfação do cliente, o que pode levar a um aumento na fidelidade e nas vendas.

## Sumário

- [Descrição do Projeto](#descrição-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Execução](#execução)
- [Testes](#testes)
- [Referências](#referências)
- [Licença](#licença)

## Descrição do Projeto

O chatbot é desenvolvido utilizando a API da OpenAI para processamento de linguagem natural. Ele é capaz de responder a perguntas frequentes, fornecer informações sobre produtos e ajudar os clientes a navegar pelo site de e-commerce.

### Importância da IA Generativa e LLM

A IA Generativa e os Modelos de Linguagem de Grande Escala (LLM) desempenham um papel crucial neste projeto. Eles permitem que o chatbot compreenda e gere respostas em linguagem natural, proporcionando uma interação mais humana e eficiente com os clientes. A utilização de LLMs, como os oferecidos pela OpenAI, garante que o chatbot possa lidar com uma ampla variedade de consultas e fornecer respostas precisas e contextualmente relevantes.

## Pré-requisitos

Certifique-se de ter as seguintes ferramentas instaladas:

- [Python 3.8+](https://www.python.org/)
- [pip](https://pip.pypa.io/en/stable/installing/)
- Um ambiente virtual separado para gerenciar as dependências do projeto.

### Bibliotecas Necessárias

- `numpy`
- `openai`
- `python-dotenv`
- `tiktoken`
- `flask`
- `opencv-python`
- `langchain`

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/maiagia/chatbot-allspark-e-commerce.git
   cd chatbot-allspark-e-commerce
   ```

2. Crie um ambiente virtual separado para o projeto e ative-o:

   **Windows:**
   ```bash
   python -m venv chatbot-allspark-e-commerce
   chatbot-allspark-e-commerce\Scripts\activate
   ```

   **Mac/Linux:**
   ```bash
   python3 -m venv chatbot-allspark-e-commerce
   source chatbot-allspark-e-commerce/bin/activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

## Configuração

Configure o arquivo `.env` com as suas credenciais da API da OpenAI:

```env
OPENAI_API_KEY=your_openai_api_key
```

## Estrutura do Projeto

A estrutura do projeto é organizada da seguinte forma:

```
chatbot-allspark-e-commerce/
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── tests/
│   └── test_app.py
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── scripts.js
└── utils/
    └── helpers.py
```

### Descrição das Pastas

- **app.py**: Arquivo principal que contém a lógica do chatbot e inicializa o servidor Flask.
- **requirements.txt**: Lista de dependências do projeto.
- **.env.example**: Exemplo de arquivo de configuração de ambiente.
- **README.md**: Documentação do projeto.
- **tests/**: Contém os testes unitários do projeto.
  - **test_app.py**: Testes para o arquivo `app.py`.
- **templates/**: Contém os templates HTML utilizados pelo Flask.
  - **index.html**: Template principal da aplicação.
- **static/**: Contém arquivos estáticos como CSS e JavaScript.
  - **css/**: Contém arquivos de estilo CSS.
    - **styles.css**: Arquivo de estilos da aplicação.
  - **js/**: Contém arquivos JavaScript.
    - **scripts.js**: Arquivo de scripts da aplicação.
- **utils/**: Contém funções auxiliares e utilitárias.
  - **helpers.py**: Funções auxiliares utilizadas no projeto.

## Execução

Para rodar o chatbot:

```bash
python app.py
```

O chatbot estará disponível em `http://127.0.0.1:5000/`.

## Testes

Para executar os testes unitários:

```bash
pytest
```

## Referências

- [Preços OpenAI](https://openai.com/pricing)

## Licença

Este projeto está licenciado sob a MIT License. Sinta-se à vontade para usar, modificar e distribuir este software, desde que mantenha os créditos apropriados.