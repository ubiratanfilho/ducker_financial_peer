import streamlit as st
from chatbot.tutor import conversational_rag_chain
import json
import numpy as np

# Variáveis globais
OPEN_API_KEY = st.secrets["OPENAI_API_KEY"]
LANGCHAIN_TRACING_V2 = st.secrets["LANGCHAIN_TRACING_V2"]
LANGCHAIN_PROJECT = st.secrets["LANGCHAIN_PROJECT"]
LANGCHAIN_API_KEY = st.secrets["LANGCHAIN_API_KEY"]
LANGCHAIN_ENDPOINT = st.secrets["LANGCHAIN_ENDPOINT"]
BOT_ICON = 'images/logo.webp'
LOGO = 'images/logo.png'
USER_ICON = 'user'

# Carregar os cursos
with open('data/courses.json', 'r', encoding='utf-8') as file:
        courses = json.load(file)["courses"]
    
courses_str = "\n".join([f"- {course['name']}" for i, course in enumerate(courses)])

# Inicializar as variáveis de sessão
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "user_goal" not in st.session_state:
    st.session_state.user_goal = None
if "user_investor_profile" not in st.session_state:
    st.session_state.user_investor_profile = None
if "messages" not in st.session_state:    
    st.session_state.messages = [
{"role": "assistant", 
"avatar": BOT_ICON,
"content": f"""
Olá! Eu sou o Ducker, seu tutor financeiro. Para eu personalizar seu aprendizado, preencha abaixo algumas informações sobre você.
"""},
{"role": "assistant",
"avatar": BOT_ICON,
"content": f"""
Obrigado! Agora, me diga qual curso deseja aprender, ou então faça qualquer pergunta sobre o mercado financeiro.

**Cursos disponíveis:**
{courses_str}

Como posso te ajudar?
"""
}
]
if "session_id" not in st.session_state:
    st.session_state.session_id = np.random.randint(0, 1000000)

# Interface do chatbot
st.title("Ducker AI")
st.subheader("Seu tutor financeiro")
st.info('O Ducker é um assistente virtual que a partir de uma base de conhecimento de cursos de finanças, te ensina sobre educação financeira. Faça uma pergunta ou então peça para ele te ensinar sobre um tópico específico.')

## Mensagens do chatbot
for idx, message in enumerate(st.session_state.messages):
    if idx == 0:
        with st.chat_message(message["role"], avatar=message['avatar']):
            st.markdown(message["content"])
        
        st.session_state.user_name = st.text_input("Qual é o seu nome?")
        st.session_state.user_goal = st.selectbox(
            "Qual é o seu objetivo financeiro?",
            [
                "Juntar dinheiro para a aposentadoria",
                "Comprar um carro",
                "Comprar uma casa",
                "Fazer uma viagem",
                "Outro (especifique)",
            ],
            index=None,
            placeholder="Selecione uma opção..."
        )
        if st.session_state.user_goal == "Outro (especifique)":
            st.session_state.user_goal = st.text_input("Digite aqui...")
        st.session_state.user_investor_profile = st.selectbox(
            "Qual é o seu perfil de investidor?",
            [
                "Conservador",
                "Moderado",
                "Agressivo",
            ],
            index=None,
            placeholder="Selecione uma opção..."
        )
        
        while not (st.session_state.user_name and st.session_state.user_goal and st.session_state.user_investor_profile):
            st.stop()
    else:
        with st.chat_message(message["role"], avatar=message['avatar']):
            st.markdown(message["content"])
    
if prompt := st.chat_input("Digite aqui..."):
    st.chat_message("user", avatar=USER_ICON).markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": USER_ICON})
    
    data = {"input": prompt, 
            "user_info": {"name": st.session_state.user_name, "goal": st.session_state.user_goal, "investor_profile": st.session_state.user_investor_profile},
            "courses_str": courses_str
    }
    
    with st.spinner("Carregando..."):
        config = {'configurable': {'session_id': st.session_state.session_id}}
        response = conversational_rag_chain.invoke(data, config=config)
    
    st.chat_message("assistant", avatar=BOT_ICON).markdown(response['answer'])
    st.session_state.messages.append({"role": "assistant", "content": response['answer'], "avatar": BOT_ICON})