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
            """
Você é um educador especializado e é responsável por acompanhar o usuário neste plano de aula. 
Certifique-se de guiá-los ao longo do processo, incentivando-os a progredir quando apropriado. 
Se fizerem perguntas não relacionadas a este guia de introdução, decline educadamente de respondê-las e lembre-os de permanecer no tópico.

Por favor, limite qualquer resposta a apenas um conceito ou etapa por vez. 
Esta é uma aula interativa - não dê palestras, mas sim envolva e guie-os ao longo do caminho!
-----------------

De ação em ação, o investidor enche a carteira. E é para isso que serve o mercado fracionário da B3, a bolsa de valores do Brasil: permitir a compra e a venda de ações de forma unitária.

Nesse ambiente, é possível negociar pequenas quantidades de papéis, o que viabiliza operações com valores reduzidos e, na prática, abre caminho para que o aplicador dê os primeiros passos no mercado acionário.

Para quem está começando ou já tem algum conhecimento da bolsa, as chamadas ações “fracionadas” permitem, por exemplo, diversificar os investimentos sem ocupar uma fatia muito expressiva do patrimônio. Uma alternativa que facilita a vida de quem busca retornos maiores, mas deseja adicionar risco ao portfólio em doses homeopáticas.

Neste guia, você entenderá como funciona o fracionário, saberá a diferença em relação ao mercado regular – no qual as ações são negociadas em lotes mínimos –, e conhecerá um pouco mais desse universo.

Também vai encontrar detalhes com os quais você precisa ficar atento para, por exemplo, não gastar mais do que o necessário e, com isso, prejudicar sua lucratividade.

O que é mercado fracionário
O mercado fracionário da Bolsa é um ambiente que permite a compra e venda de ações em pequenas quantidades – que variam de 1 a 99 unidades.

O objetivo é viabilizar transações de menor volume financeiro, permitindo também ao investidor fazer aportes periódicos com poucos recursos.

Nesse universo, não existe uma quantidade mínima de ações exigida para cada operação, como acontece no mercado tradicional, em que os papéis são negociados em “lote padrão”.

Como funciona
Todas as ações listadas na bolsa possuem um código, também chamado de ticker, que é usado para realizar as operações. No mercado padrão, ele é composto por quatro letras seguidas de um número. Um exemplo é PETR3, que representa as ações ordinárias (com direito a voto) da Petrobras.

No ambiente fracionário, no entanto, existe uma identificação extra para os papéis. É justamente o acréscimo da letra “F” no fim do código.

No exemplo citado, da Petrobras, o investidor que deseja comprar ou vender ações fracionadas precisa utilizar os códigos PETR3F. Se quiser negociar as ações preferenciais (sem direito a voto e com prioridade na distribuição de dividendos), o código será PETR4F.

Qual a diferença entre mercado fracionário e mercado padrão?
“As regras do mercado fracionário são as mesmas do mercado de lote padrão, com exceção do tamanho do lote e que o código de negociação do instrumento fracionário possui o ‘F’ ao final”, explica Gabriela Shibata, gerente de cash equities da B3.

Em termos práticos, o fracionário possibilita negociar ações em unidades menores que 100, enquanto no mercado regular as transações são realizadas por meio de lotes, compostos normalmente por 100 papéis cada. É o chamado “lote padrão” ou “mínimo”, que serve de referência para o volume de transações.

Como os ambientes são integrados, um investidor que for adquirindo aos poucos ações de uma companhia pode, quando completar 100 unidades (ou múltiplos de 100), vendê-las de uma só vez como um lote padrão, se desejar.

É importante destacar que, em ambos os casos, os negócios acontecem no chamado “mercado à vista” da Bolsa, no qual as operações são liquidadas em até três dias úteis.

Vale ressaltar ainda que não existe nenhuma diferenciação em termos de direitos para os detentores de ações negociadas nos dois ambientes.

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

while True:
    question = input("\n\nVocê: ")
    print("\nDucker:", end=" ")
    response = with_message_history.stream(
        {'messages': [HumanMessage(content=question)]},
        config=config,
    )
    
    for r in response:
        print(r.content, end="")