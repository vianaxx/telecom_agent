

import os
import streamlit as st
from agent.agent import TelecomAgent
from agent.tools.device_api import get_device_status
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Telecom Field Assistant", page_icon="📡", layout="centered")

# -------------------- SIDEBAR DE AUTENTICAÇÃO --------------------
with st.sidebar:
    st.header("Autenticação Ollama")
    ollama_api_key = st.text_input("Enter your Ollama API Key", type="password")
    if not ollama_api_key:
        st.warning("Please enter your Ollama API key to use the chatbot.")

# Bloqueia o uso do app se não houver chave
if not ollama_api_key:
    st.stop()

# Define a variável de ambiente antes de criar o agente
os.environ["OLLAMA_API_KEY"] = ollama_api_key

# -------------------- AGENTE --------------------
agent = TelecomAgent()  # agora vai pegar a chave do ambiente

# -------------------- HISTÓRICO DE CHAT --------------------
if "chat" not in st.session_state:
    st.session_state.chat = []

def display_chat():
    for entry in st.session_state.chat:
        st.chat_message("user").write(entry["user"])
        st.chat_message("assistant").write(entry["bot"])
        if entry.get("status_info"):
            status = entry["status_info"]
            with st.expander(f"📡 Status do Dispositivo {status['device_id']}", expanded=True):
                st.markdown(f"**Status geral:** {status['status']}")
                st.markdown(f"**SNR médio:** {status['snr_avg']} dB")
                st.markdown(f"**Tráfego total:** {status['traffic_total']} Mbps")
                st.markdown(f"**Packet Loss:** {status['packet_loss']}")
                st.markdown(f"**Alarms:** {status['alarms']}")
                st.markdown("---")
                st.markdown("📶 **Antenas e Células:**")
                for ant, cells in status["antennas"].items():
                    st.markdown(f"**{ant}**")
                    df_cells = pd.DataFrame.from_dict(cells, orient="index").rename(
                        columns={"snr": "SNR (dB)", "traffic": "Tráfego (Mbps)"})
                    st.table(df_cells)
                st.markdown("---")
                st.markdown("📝 **Últimos Logs:**")
                for log in status["logs"]:
                    if "ERROR" in log:
                        st.error(log)
                    elif "WARN" in log:
                        st.warning(log)
                    else:
                        st.info(log)

# -------------------- TÍTULO E INPUT --------------------
st.title("📡 Telecom Field Assistant")
st.write("Assistente para técnicos de instalação e manutenção de redes 5G.")
st.divider()

display_chat()
user_input = st.chat_input("Digite sua dúvida técnica ou 'status <DEVICE_ID>'...")

if user_input:
    response_placeholder = st.chat_message("assistant")
    status_placeholder = st.empty()

    if user_input.lower().startswith("status "):
        device_id = user_input.split(" ", 1)[1]
        status = get_device_status(device_id)
        st.session_state.chat.append({
            "user": user_input,
            "bot": f"Status do {device_id} exibido",
            "status_info": {**status, "device_id": device_id}
        })
        status_placeholder.empty()
        st.rerun()
    else:
        status_placeholder.info("Analisando sua solicitação...")
        reply = agent.run(user_input)
        status_placeholder.empty()
        st.session_state.chat.append({
            "user": user_input,
            "bot": reply
        })
        response_placeholder.write(reply)
        st.rerun()

if st.button("Limpar Conversa"):
    st.session_state.chat.clear()
    agent.memory.clear()
    st.rerun()
