import dotenv
import os

from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

dotenv.load_dotenv()

# # System questions
# system_questions = [
# """Olá! Eu sou o Ducker, seu assistente de investimentos. Para que eu possa te ajudar, vou fazer algumas perguntas. Qual é o seu nome?""",
# """Qual é o seu objetivo financeiro? Digite o número correspondente:

# 1. Juntar dinheiro para a aposentadoria
# 2. Comprar um carro
# 3. Comprar uma casa
# 4. Fazer uma viagem
# 5. Outro (especifique)
# """,
# """Qual é o seu perfil de investidor? Digite o número correspondente:
# 1. Conservador - prefere investimentos de baixo risco
# 2. Moderado - aceita um pouco de risco para obter maior rentabilidade
# 3. Agressivo - busca obter a maior rentabilidade possível, mesmo que isso implique em correr mais riscos
# """
# ]

# user_info = {}
# for system_question in system_questions:
#     print(f"Ducker: {system_question}")
#     user_answer = input("Você: ")
#     user_info[system_question] = user_answer
#     print("\n")
    
# print("\nPerfeito! Agora que eu já sei um pouco mais sobre você, me faça uma pergunta sobre investimentos.")

# creating LLM Chatbot
store = {}
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

model = ChatOpenAI(model=os.getenv("OPEN_AI_MODEL"), temperature=0)
with_message_history = RunnableWithMessageHistory(model, get_session_history)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
"""Sua função é ensinar os usuários sobre educação financeira, especialmente sobre as nuances do mercado brasileiro.
Personalize suas respostas de acordo com o perfil de investimento do usuário: {user_info}.
Não responda a nada que não esteja relacionado a perguntas sobre finanças.
Seja educado e claro em suas respostas.
Se não souber a resposta para uma pergunta, diga isso.""",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)
chain = prompt | model

general_qa_chain = RunnableWithMessageHistory(
    chain, 
    get_session_history,
    input_messages_key="messages",
)
config = {"configurable": {"session_id": "abc11"}}

while True:
    question = input("\n\nVocê: ")
    print("\nDucker:", end=" ")
    response = general_qa_chain.stream(
        {'messages': [HumanMessage(content=question)], 'user_info': user_info},
        config=config,
    )
    
    for r in response:
        print(r.content, end="")