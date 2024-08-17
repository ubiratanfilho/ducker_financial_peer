import dotenv
import os

from langchain import hub
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import json
from langchain.agents import (
    create_openai_functions_agent,
    Tool,
    AgentExecutor,
)
from general_qa import general_qa_chain
import json


dotenv.load_dotenv()

# System questions
system_questions = [
"""Olá! Eu sou o Ducker, seu assistente de investimentos. Para que eu possa te ajudar, vou fazer algumas perguntas. Qual é o seu nome?""",
"""Qual é o seu objetivo financeiro? Digite o número correspondente:

1. Juntar dinheiro para a aposentadoria
2. Comprar um carro
3. Comprar uma casa
4. Fazer uma viagem
5. Outro (especifique)
""",
"""Qual é o seu perfil de investidor? Digite o número correspondente:
1. Conservador - prefere investimentos de baixo risco
2. Moderado - aceita um pouco de risco para obter maior rentabilidade
3. Agressivo - busca obter a maior rentabilidade possível, mesmo que isso implique em correr mais riscos
"""
]

user_info = {}
for system_question in system_questions:
    print(f"Ducker: {system_question}")
    user_answer = input("Você: ")
    user_info[system_question] = user_answer
    print("\n")
    
print("\nPerfeito! Agora que eu já sei um pouco mais sobre você, me faça uma pergunta sobre investimentos, ou então podemos passar pelo nosso catálogo de cursos:")
with open('data/courses.json', 'r', encoding='utf-8') as file:
    courses = json.load(file)["courses"]
for course in courses:
    print(f"{course['id']}. {course['name']}")

# creating the agent
agent_prompt = hub.pull("hwchase17/openai-functions-agent")
tools = [
    Tool(
        name='general_qa',
        func=general_qa_chain.stream,
        description='Útil para responder perguntas gerais sobre investimentos.',
    )
]

chat_model = ChatOpenAI(model=os.getenv("OPEN_AI_MODEL"), temperature=0)
agent = create_openai_functions_agent(
    prompt=agent_prompt,
    tools=tools,
    llm=chat_model
)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    return_intermediate_steps=True,
    verbose=True
)

config = {"configurable": {"session_id": "abc11"}}
while True:
    question = input("\nVocê: ")
    response = agent_executor.invoke(
        {"input": question}
    )
    print("\nDucker:", end=" ")
    # for r in response:
    #     print(r.content, end="")
