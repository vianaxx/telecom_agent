# 📡 Telecom Field Assistant – Rede 5G

> Assistente técnico inteligente para redes 5G, integrado com RAG (Retrieval-Augmented Generation), LLM (Ollama) e telemetria de equipamentos.

O sistema fornece diagnósticos passo a passo e permite consultas em tempo real a dispositivos críticos da rede (BBU, RRU, Antenas). O projeto inclui uma interface Web (Streamlit) e uma CLI para técnicos em campo.

**Demo Online:** [Acessar App](https://telecomagent.streamlit.app/)
*(Nota: Para a versão online funcionar, é necessária uma API Key de uma instância Ollama acessível publicamente.*
---

## 🔹 Funcionalidades

1. **Consultas técnicas com contexto (RAG)**

    * Busca na base de conhecimento relevante antes de gerar a resposta (procedimentos de Telecom, boas práticas 5G).
    * Mantém histórico de conversa para contexto contínuo.

2. **Monitoramento de dispositivos**

    * Comando `status <DEVICE_ID>` para obter status de equipamentos (BBU/RRU), alarmes, SNR, potência de sinal, tráfego e logs.

3. **Histórico de chat**

    * Memória limitada às últimas 20 interações.

4. **Interface CLI e Web (Streamlit)**

    * CLI para técnicos em campo.
    * Web para visualização de contexto, logs e respostas detalhadas.

---

## 🔹 Pré-requisitos

* Python 3.10+

* `.env` com variável:

```bash
OLLAMA_API_KEY=your_api_key_here
```

* Dependências:

```bash
pip install chromadb ollama streamlit python-dotenv
```

---

## 🔹 Estrutura do Projeto

```
agent/
├─ agent.py           
├─ memory.py          
├─ tools/
│  └─ device_api.py   
rag/
├─ kb_data.py         
├─ vector_store.py    
run.py                
api/
└─ main.py            
```

---

## 🔹 Exemplos de Interação

### CLI

```bash
$ python run.py
📡 Telecom Field Assistant CLI – TELECOM 5G

Digite sua dúvida técnica ou 'status <DEVICE_ID>'

User > Como reiniciar a RRU do site ABC123?
Agent >
1. Verifique alarmes ativos na RRU ABC123
2. Execute reboot remoto via console BBU
3. Monitore logs e SNR após reinício

User > status BBU12345
Dispositivo BBU12345 status: ok, SNR 35 dB, tráfego 450 Mbps, sem alarmes críticos
```

### Streamlit

* Abra o app:

```bash
streamlit run app.py
```

* Interação:

1. Digite sua dúvida técnica:

   ```
   Como otimizar tráfego de backhaul no site XYZ?
   ```

2. Comando de status:

   ```
   status RRU98765
   ```

* O histórico do chat exibe:

    * Pergunta do usuário
    * Resposta detalhada do agente, incluindo SNR, alarmes e tráfego

* Limpar conversa: clique no botão **🧹 Limpar Conversa**.

---

## 🔹 Como funciona internamente

1. **RAG + LLM**

    * Busca na KB (via ChromaDB) os procedimentos oficiais TELECOM mais relevantes.
    * Envia contexto + histórico de chat para LLM gerar resposta passo a passo.

2. **Memória**

    * Armazena até 20 mensagens (usuário + agente).

3. **Device API**

    * Simula ou consulta status dinâmico de BBU, RRU e antenas (`ok`, `degraded`, `critical`) com SNR, tráfego e logs.

4. **Cache simples**

    * Respostas anteriores são guardadas para agilizar consultas repetidas.

---
