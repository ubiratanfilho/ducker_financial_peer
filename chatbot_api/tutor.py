import dotenv
import bs4
import os
import json
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

dotenv.load_dotenv()

# ask for what course the user wants to learn
course = print("\nDucker: Qual curso você deseja aprender? Digite o número correspondente:")
with open('data/courses.json', 'r', encoding='utf-8') as file:
    courses = json.load(file)["courses"]
for course in courses:
    print(f"{course['id']}. {course['name']}")

selected_course = int(input("\nVocê: "))
url = courses[selected_course-1]['url']

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
            f"""
Você é um educador especializado e é responsável por acompanhar o usuário neste plano de aula. 
Certifique-se de guiá-los ao longo do processo, incentivando-os a progredir quando apropriado. 
Se fizerem perguntas não relacionadas a este guia de introdução, decline educadamente de respondê-las e lembre-os de permanecer no tópico.

Por favor, limite qualquer resposta a apenas um conceito ou etapa por vez. 
Esta é uma aula interativa - não dê palestras, mas sim envolva e guie-os ao longo do caminho!
-----------------
{url}
-----------------
Final do conteúdo.""",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)


chain = prompt | model

with_message_history = RunnableWithMessageHistory(
    chain, 
    get_session_history,
    input_messages_key="messages",
)
config = {"configurable": {"session_id": "abc11"}}

question = "Me explique passo a passo sobre o curso escolhido. Faça um sumário do conteúdo e pergunte por onde quero começar."
while True:
    print("\nDucker:", end=" ")
    response = with_message_history.stream(
        {'messages': [HumanMessage(content=question)]},
        config=config,
    )
    
    for r in response:
        print(r.content, end="")
        
    question = input("\n\nVocê: ")