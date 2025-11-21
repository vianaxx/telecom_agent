# api/main.py
import streamlit as st
from agent.agent import TelecomAgent
from agent.tools.router_api import get_router_status

st.set_page_config(page_title="Telecom Field Assistant", page_icon="📡", layout="centered")

agent = TelecomAgent()

st.title("📡 Telecom Field Assistant")
st.write("Assistente para técnicos de instalação e manutenção de redes.")
st.divider()

# Inicializa histórico de chat
if "chat" not in st.session_state:
    st.session_state.chat = []

# Função para exibir o chat
def display_chat():
    for user_msg, bot_msg in st.session_state.chat:
        st.chat_message("user").write(user_msg)
        st.chat_message("assistant").write(bot_msg)

display_chat()

# Input do usuário
user_input = st.chat_input("Digite sua dúvida técnica ou 'status <DEVICE_ID>'...")

if user_input:
    # Placeholder para a resposta e status corporativo
    response_placeholder = st.chat_message("assistant")
    status_placeholder = st.empty()

    # Comando especial: status do dispositivo
    if user_input.lower().startswith("status "):
        device_id = user_input.split(" ", 1)[1]
        status = get_router_status(device_id)
        reply = (f"Dispositivo {device_id} status: {status['status']}, "
                 f"latência {status['latency']}, packet loss {status['packet_loss']}")
    else:
        # Indicador corporativo de processamento
        status_placeholder.info("⏳ Analisando sua solicitação...")

        # Gera resposta do modelo
        reply = agent.run(user_input)

        # Remove o placeholder após gerar resposta
        status_placeholder.empty()

    # Armazena chat e exibe
    st.session_state.chat.append((user_input, reply))
    response_placeholder.write(reply)
    st.rerun()

# Botão para limpar memória e chat
if st.button("🧹 Limpar Conversa"):
    st.session_state.chat.clear()
    agent.memory.clear()
    st.rerun()
