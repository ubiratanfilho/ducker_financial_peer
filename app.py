import os
import requests
import streamlit as st
import dotenv
from chatbot_api.src.chains.tutor import conversational_rag_chain
import json

dotenv.load_dotenv()

if "messages" not in st.session_state:
    with open('data/courses.json', 'r', encoding='utf-8') as file:
        courses = json.load(file)["courses"]
    
    courses_str = "\n".join([f"{i+1}. {course['name']}" for i, course in enumerate(courses)])
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Eu sou o Ducker, seu assistente de investimentos. Eu posso tanto te ensinar sobre educação financeira a partir dos cursos disponíveis, ou então, faça qualquer pergunta para mim."},
        {"role": "assistant", "content": "Cursos disponíveis:\n" + courses_str},
    ]

with st.sidebar:
    st.image("images/logo.png", width=200)
    
    st.markdown("### Sobre você")
    st.markdown("Para que eu possa te ajudar, preciso de algumas informações sobre você.")
    st.markdown("Qual é o seu nome?")
    user_name = st.text_input("Digite aqui...", key="user_name")
    st.markdown("Qual é o seu objetivo financeiro?")
    user_goal = st.selectbox(
        "Selecione uma opção",
        [
            "Juntar dinheiro para a aposentadoria",
            "Comprar um carro",
            "Comprar uma casa",
            "Fazer uma viagem",
            "Outro (especifique)",
        ],
    )
    if user_goal == "Outro (especifique)":
        user_goal = st.text_input("Digite aqui...", key="user_goal_other")
    st.markdown("Qual é o seu perfil de investidor?")
    user_investor_profile = st.selectbox(
        "Selecione uma opção",
        [
            "Conservador",
            "Moderado",
            "Agressivo",
        ],
    )

st.title("Ducker AI - Seu Tutor Financeiro")
st.info('O Ducker é um assistente virtual que a partir de uma base de conhecimento de cursos de finanças, te ensina sobre educação financeira. Faça uma pergunta ou então peça para ele te ensinar sobre um tópico específico.')

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    
if prompt := st.chat_input("Digite aqui..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    data = {"input": prompt, "user_info": {"name": user_name, "goal": user_goal, "investor_profile": user_investor_profile}}
    
    with st.spinner("Carregando..."):
        config = {'configurable': {'session_id': '1'}}
        response = conversational_rag_chain.invoke(data, config=config)
    
    st.chat_message("assistant").markdown(response['answer'])
    st.session_state.messages.append({"role": "assistant", "content": response['answer']})