import dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain_core.messages import AIMessage
import os

dotenv.load_dotenv()

finance_template_str = """
Your function is to teach users about financial education, especially about the nuances of the Brazilian market. Do not respond to anything that is not related to questions about finance. Be polite and clear in your answers. If you don't know the answer to a question, say so.
"""

finance_system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=[],
        template=finance_template_str,
    )
)

human_template_str = """
A partir do meu perfil de investidor abaixo (no formato pergunta:resposta, o dígito representa qual resposta se refere):
{user_info}

{question}
"""
finance_human_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["question", "user_info"],
        template=human_template_str,
    )
)
messages = [finance_system_prompt, finance_human_prompt]

finance_prompt_template = ChatPromptTemplate(
    input_variables=["question", "user_info"],
    messages=messages,
)

chat_model = ChatOpenAI(model=os.getenv("OPEN_AI_MODEL"), temperature=0)

finance_chain = finance_prompt_template | chat_model


## example usage
ai_questions = [
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
for ai_question in ai_questions:
    print(f"Ducker: {AIMessage(ai_question).content}")
    user_answer = input("Você: ")
    user_info[ai_question] = user_answer
    print("\n")
    
print("\nPerfeito! Agora que eu já sei um pouco mais sobre você, me faça uma pergunta sobre investimentos.")

while True:
    user_question = input("Você: ")
    ai_response = finance_chain.invoke({"question": user_question, "user_info":user_info}).content
    print(f"Ducker: {ai_response}")
    print("\n")