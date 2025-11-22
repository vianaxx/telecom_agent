
# Telecom Field Assistant – Rede 5G

Assistente técnico para redes 5G, integrado com base de conhecimento (KB), LLM (Ollama) e monitoramento de equipamentos de rádio (BBU, RRU, antenas e backhaul).
Fornece respostas passo a passo, claras e curtas, e permite consultas em tempo real a dispositivos críticos da rede 5G.

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

## 🔹 Demonstração

https://github.com/user-attachments/assets/1a4689c5-6d5b-4c1e-97f4-4b0ecfccfb6d



https://github.com/user-attachments/assets/35e87569-c5a9-472e-94d2-c6de6dc17fe1



---

