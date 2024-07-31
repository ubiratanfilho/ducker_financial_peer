import os
import requests
import streamlit as st

CHATBOT_URL = os.getenv("CHATBOT_URL", "http://localhost:8000/finance-chatbot")

with st.sidebar:
    st.image("logo.png", width=200)
    st.header("Sobre")
    st.markdown(
        """
        **Ducker Financial Peer**

        Ducker é um assistente inteligente projetado para responder suas perguntas sobre mercados financeiros. Basta digitar sua pergunta, e o Ducker fornecerá as respostas.
        """
    )

st.title("Ducker Financial Peer")
st.info("Olá! Eu sou o Ducker, seu assistente para o mercado financeiro.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Digite sua pergunta sobre o mercado financeiro aqui..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    data = {"text": prompt}

    with st.spinner("Buscando a melhor resposta..."):
        response = requests.post(CHATBOT_URL, json=data)

        if response.status_code == 200:
            output_text = response.json()["output"]
        else:
            output_text = "Ocorreu um erro ao processar sua mensagem. Por favor, tente novamente."

    st.chat_message("assistant").markdown(output_text)
    st.session_state.messages.append({"role": "assistant", "content": output_text})
