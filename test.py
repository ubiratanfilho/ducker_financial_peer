# __import__('pysqlite3')
# import sys

# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from streamlit import logger
import sqlite3

app_logger = logger.get_logger(__name__)
app_logger.info(f"sqlite version: {sqlite3.version}")
# app_logger.info(f"sys version: {sys.version}")