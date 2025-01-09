import sys
import os
import streamlit as st
import json


# Add the parent directory of 'agents' to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from agents._azure_storage_agent import AzureStorageAgent

# Inicializar o agente
azure_storage_agent = AzureStorageAgent()


# Configuração do Streamlit
st.set_page_config(page_title="Azure Storage Agent", layout="wide")
st.title("Azure Storage Agent")
st.subheader("Interaja com o assistente especializado em Azure Storage Accounts")

# Histórico de mensagens
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Entrada do usuário
user_input = st.text_input("Digite sua solicitação:", placeholder="e.g., list all storage accounts")

# Processar entrada
if st.button("Enviar"):
    if user_input:
        with st.spinner("Processando..."):
            # Processa o prompt do usuário e obtém a resposta
            response = azure_storage_agent.handle_prompt(user_input)
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.chat_history.append({"role": "assistant", "content": response})

# Exibir o histórico de mensagens
st.subheader("Histórico de Conversas")
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"**Usuário:** {msg['content']}")
    else:
        st.markdown(f"**Agente:** {msg['content']}")
