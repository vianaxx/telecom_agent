import streamlit as st
from agent.agent import TelecomAgent
from agent.tools.router_api import get_device_status
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Telecom Field Assistant", page_icon="📡", layout="centered")

# Inicializa agente
agent = TelecomAgent()

# Título e descrição
st.title("📡 Telecom Field Assistant")
st.write("Assistente para técnicos de instalação e manutenção de redes 5G.")
st.divider()

# Inicializa histórico de chat e status
if "chat" not in st.session_state:
    st.session_state.chat = []

# Função para reconstruir o chat
def display_chat():
    for entry in st.session_state.chat:
        user_msg = entry["user"]
        bot_msg = entry["bot"]
        st.chat_message("user").write(user_msg)
        st.chat_message("assistant").write(bot_msg)

        # Reconstruir expander para status, se existir
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
                    df_cells = pd.DataFrame.from_dict(cells, orient="index")
                    df_cells = df_cells.rename(columns={"snr": "SNR (dB)", "traffic": "Tráfego (Mbps)"})
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

# Mostra histórico
display_chat()

# Input do usuário
user_input = st.chat_input("Digite sua dúvida técnica ou 'status <DEVICE_ID>'...")

if user_input:
    response_placeholder = st.chat_message("assistant")
    status_placeholder = st.empty()

    # Comando status
    if user_input.lower().startswith("status "):
        device_id = user_input.split(" ", 1)[1]
        status = get_device_status(device_id)

        # Armazena no histórico
        st.session_state.chat.append({
            "user": user_input,
            "bot": f"Status do {device_id} exibido",  # texto simples
            "status_info": {**status, "device_id": device_id}  # inclui device_id para reconstrução
        })

        status_placeholder.empty()
        st.rerun()

    else:
        # Consulta normal ao agente
        status_placeholder.info("⏳ Analisando sua solicitação...")
        reply = agent.run(user_input)
        status_placeholder.empty()

        # Armazena no histórico
        st.session_state.chat.append({
            "user": user_input,
            "bot": reply
        })

        response_placeholder.write(reply)
        st.rerun()

# Botão para limpar conversa
if st.button("🧹 Limpar Conversa"):
    st.session_state.chat.clear()
    agent.memory.clear()
    st.rerun()
