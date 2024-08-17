import bs4
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import dotenv
import os
from langchain_core.messages import HumanMessage
import json

dotenv.load_dotenv()

# carregar o vector store e retriever
with open('data/courses.json', 'r', encoding='utf-8') as file:
    courses = json.load(file)["courses"]
loader = WebBaseLoader(
    web_paths=tuple([course['url'] for course in courses]),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("imds-font-headline mt-4 mb-0", 'lead lh-sm mt-2 mb-0 col-xxl-10', 'article-body mt-4')
        )
    ),
)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

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
    
print("\nDucker: Perfeito! Agora que eu já sei um pouco mais sobre você, posso tanto te ensinar sobre educação financeira a partir dos cursos disponíveis, ou então, faça qualquer pergunta para mim.")

course = print("\nDucker: Cursos disponíveis:")
for course in courses:
    print(f"- {course['name']}")


llm = ChatOpenAI(model=os.getenv("OPEN_AI_MODEL"), temperature=0)
### Contextualize question ###
contextualize_q_system_prompt = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is."""
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)


### Answer question ###
qa_system_prompt = """
Você é um educador especializado e é responsável por acompanhar o usuário neste plano de aula. 
Certifique-se de guiá-los ao longo do processo, incentivando-os a progredir quando apropriado. 
Personalize suas respostas e método de ensino de acordo com o perfil de investimento do usuário: {user_info}.
Por favor, limite qualquer resposta a apenas um conceito ou etapa por vez. 
Esta é uma aula interativa - não dê palestras, mas sim envolva e guie-os ao longo do caminho!

Utilize o contexto abaixo para guiar o usuário pelo curso:

{context}"""
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)


### Statefully manage chat history ###
store = {}
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)

config = {"configurable": {"session_id": "abc11"}}
chat_history = []
while True:
    question = input("\nVocê: ")
    response = conversational_rag_chain.invoke(
        {"input": question, "chat_history": chat_history, "user_info": user_info},
        config=config,
    )

    print("\nDucker:", response['answer'])
    
    chat_history.extend([HumanMessage(content=question), response['answer']])