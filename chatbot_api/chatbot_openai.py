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

finance_human_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["question"],
        template="{question}",
    )
)
messages = [finance_system_prompt, finance_human_prompt]

finance_prompt_template = ChatPromptTemplate(
    input_variables=["question"],
    messages=messages,
)

chat_model = ChatOpenAI(model=os.getenv("OPEN_AI_MODEL"), temperature=0)

finance_chain = finance_prompt_template | chat_model


## example usage
ai_questions = [
    """Olá! Eu sou o Ducker, seu assistente de investimentos. Para que eu possa te ajudar, vou fazer algumas perguntas. Qual é o seu nome?""",
    """Qual é o seu objetivo financeiro?""",
    """Qual é o seu perfil de investidor?"""
]

# print the question and then asks for the user input
for ai_question in ai_questions:
    print(f"Ducker: {AIMessage(ai_question).content}")
    user_question = input("Você: ")
    ai_response = finance_chain.invoke({"question": user_question}).content
    print(f"Ducker: {ai_response}")
    print("\n")