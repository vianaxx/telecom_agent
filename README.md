# Telecom Field Assistant – Rede 5G

**Status:** Em Desenvolvimento 🚧

Assistente técnico para redes 5G, integrado com base de conhecimento (KB), LLM (Ollama) e monitoramento de equipamentos de rádio (BBU, RRU, antenas e backhaul). Fornece respostas passo a passo, claras e curtas, e permite consultas em tempo real a dispositivos críticos da rede 5G.

---

## 🔹 Funcionalidades

### Consultas técnicas com contexto (RAG)

* Busca na base de conhecimento relevante antes de gerar a resposta (procedimentos de Telecom, boas práticas 5G).
* Mantém histórico de conversa para contexto contínuo.

### Monitoramento de dispositivos

* Comando `status <DEVICE_ID>` para obter status de equipamentos (BBU/RRU), alarmes, SNR, potência de sinal, tráfego e logs.

### Histórico de chat

* Memória limitada às últimas 20 interações.

### Interface CLI e Web (Streamlit)

* CLI para técnicos em campo.
* Web para visualização de contexto, logs e respostas detalhadas.

---

## 🔹 Pré-requisitos

* Python 3.10+

* Dependências:

```bash
pip install chromadb ollama streamlit python-dotenv
```

---

## 🔹 Gerando a API Key da Ollama

Para usar o app pelo Streamlit, cada usuário precisa gerar sua própria API Key da Ollama:

1. Acesse o site da [Ollama](https://ollama.com) e **crie uma conta** ou faça login.
2. No painel da conta, vá até **API / API Keys** (ou seção equivalente).
3. Clique em **“Generate API Key”** ou “Create New Key”.
4. Copie a chave gerada e guarde em local seguro.
5. Abra o app Streamlit em:
   [https://telecomagent-qjj4eptbzadzmmm4mkwb7q.streamlit.app/](https://telecomagent-qjj4eptbzadzmmm4mkwb7q.streamlit.app/)
6. No **menu lateral (sidebar)** do app, cole sua API Key no campo “Ollama API Key” (tipo password).
7. A partir daí, você poderá digitar comandos e interagir com o agente normalmente.

> ⚠️ **Importante:** nunca compartilhe sua API Key publicamente. Ela funciona como uma senha.

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

### RAG + LLM

* Busca na KB (via ChromaDB) os procedimentos oficiais TELECOM mais relevantes.
* Envia contexto + histórico de chat para LLM gerar resposta passo a passo.

### Memória

* Armazena até 20 mensagens (usuário + agente).

### Device API

* Simula ou consulta status dinâmico de BBU, RRU e antenas (`ok`, `degraded`, `critical`) com SNR, tráfego e logs.

### Cache simples

* Respostas anteriores são guardadas para agilizar consultas repetidas.

---

## 🔹 Demonstração


https://github.com/user-attachments/assets/5541d25d-2f58-4d3f-a10f-55a8e8430819


