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
import os
import json
import streamlit as st

llm = ChatOpenAI(model_name=str(st.secrets['OPEN_AI_MODEL']), temperature=0)

# And the root-level secrets are also accessible as environment variables:
# st.write(
#     "Has environment variables been set:",
#     os.environ["db_username"] == st.secrets["db_username"],
# )