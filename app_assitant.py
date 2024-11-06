from flask import Flask, render_template, request
from time import sleep
from utils import *
from prompt_system import *
from model_selection import model_str
from persona_selection import *
from select_document import *
from allspark_assistant import *

model, parser, client = initial_parameters()

app = Flask(__name__)
app.secret_key = 'allspark'

assistant = get_json()
thread_id = assistant['thread_id']
vector_store_id = assistant['vector_store_id']
assistant_id = assistant['assistant_id']

STATUS_COMPLETED = "completed" 
STATUS_REQUIRES_ACTION = "requires_action" 

def bot(prompt):
    max_attempts = 1
    attempts = 0
    while True:
        try:
            personality = prompt_system_personas[select_persona(prompt)]
            client.beta.threads.messages.create(
                            thread_id=thread_id, 
                            role = "user",
                            content =  f"""
                            {prompt_system_persona_selection_update}:

                            # Persona
                            {personality}
                            """,
                            # file_ids=file_ids
                        )

            # Create a new message within the current thread "thread"
            client.beta.threads.messages.create(
                thread_id=thread_id, 
                role = "user",
                content = prompt,
                # file_ids=file_ids
            )
            # Create a new run within the current thread, associating it 
            # with the assistant who will answer the user's question.
            run = client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id
            )
            # Wait until the assistant answers the user's question.
            while run.status != STATUS_COMPLETED:
                run = client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run.id
            )
                print(f"Status: {run.status}")
                
                if run.status == STATUS_REQUIRES_ACTION:
                    triggered_tools = run.required_action.submit_tool_outputs.tool_calls
                    triggered_tools_responses = [] 
                    for one_tool in triggered_tools:
                        function_name = one_tool.function.name
                        chosen_function = functions[function_name]
                        arguments = json.loads(one_tool.function.arguments)
                        print(arguments)
                        function_response = chosen_function(arguments)

                        triggered_tools_responses.append({
                                "tool_call_id": one_tool.id,
                                "output": function_response
                            })
                    
                    run = client.beta.threads.runs.submit_tool_outputs(
                            thread_id = thread_id,
                            run_id = run.id,
                            tool_outputs = triggered_tools_responses
                        )  

            # Retrieve a list of all messages within the current thread.
            historical = list(client.beta.threads.messages.list(thread_id=thread_id).data)
            response = historical[0]
            
            return response
        except Exception as error:
                attempts += 1
                if attempts >= max_attempts:
                        return "GPT Error: %s" % error
                print('Communication error with OpenAI:', error)
                sleep(1)
            

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json["msg"]
    response = bot(prompt)
    response_text = response.content[0].text.value
    return response_text

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)