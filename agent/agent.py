
import os
import logging
from dotenv import load_dotenv
from ollama import Client
from agent.memory import Memory
from rag.kb_data import KB_DOCS
from rag.vector_store import VectorStore

# Carrega .env
load_dotenv()

# Logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/agent.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger("TelecomAgent")

class TelecomAgent:
    """Agente técnico FTTH integrado com KB e LLM."""
    def __init__(self, model="gpt-oss:120b"):
        api_key = os.getenv("OLLAMA_API_KEY")
        if not api_key:
            raise ValueError("Missing OLLAMA_API_KEY in .env")
        self.client = Client(
            host="https://ollama.com",
            headers={'Authorization': f'Bearer {api_key}'}
        )
        self.model = model
        self.memory = Memory()
        self.vector = VectorStore()

        # Carrega KB
        for text, meta in KB_DOCS:
            self.vector.add_document(text, meta)

        # Cache simples
        self.cache = {}
        logger.info(f"TelecomAgent initialized with model: {self.model}")

    def run(self, text: str) -> str:
        """Processa input do usuário e retorna resposta LLM com contexto RAG."""
        logger.info(f"User input: {text}")

        if text in self.cache:
            logger.info("Cache hit")
            return self.cache[text]

        docs = self.vector.search(text, top_k=1)
        context = docs[0] if docs else ""

        messages = [
            {
                "role": "system",
                "content": """
        Você é um Assistente Técnico especializado em equipamentos TELECOM para redes 5G, incluindo BBU, RRU, antenas e backhaul.
        Seu comportamento deve seguir estas regras:
        
        1. Estilo de Resposta
           - Forneça respostas claras, concisas e passo a passo.
           - Seja técnico, preciso e profissional, mas mantenha linguagem compreensível.
           - Foco em solução prática e imediata.
        
        2. Consulta ao Conhecimento
           - Use a base de conhecimento (KB) para procedimentos oficiais TELECOM.
           - Se não houver documentação, utilize boas práticas de instalação e troubleshooting 5G.
        
        3. Monitoramento em Tempo Real
           - Pode consultar status de equipamentos, alarmes, SNR, potência de sinal, tráfego de backhaul e logs de BBU/RRU.
           - Inclua esses dados na resposta sempre que relevante.
           - Sugira ações corretivas baseadas nos dados em tempo real.
        
        4. Passo a Passo
           - Para instalação: conexão de cabos de alimentação, fibra, backhaul, alinhamento de antena, configuração de BBU/RRU, teste de sinal e tráfego.
           - Para manutenção: diagnóstico de alarmes, logs de falha, reboot de equipamentos, testes de tráfego, otimização de parâmetros de rádio.
        
        5. Escalonamento
           - Se o problema for complexo, fora do KB ou crítico para a rede, sugira escalonamento para engenheiro ou técnico sênior.
           - Sempre forneça diagnóstico parcial antes de escalar.
        
        6. Segurança
           - Nunca execute comandos críticos sem confirmação do usuário.
           - Certifique-se de que procedimentos sigam normas de segurança elétrica e de RF.
           - Mantenha logs de todas as ações sugeridas.
        
        7. Tom
           - Profissional, direto, confiável.
           - Pergunte por informações adicionais do equipamento ou rede antes de dar uma solução completa, se necessário.
        """
            },
            {"role": "system", "content": f"Contexto relevante (use se útil):\n{context}"},
            *self.memory.get(),
            {"role": "user", "content": text}
        ]


        try:
            stream = self.client.chat(model=self.model, messages=messages, stream=True)
            answer = ""
            for chunk in stream:
                if "message" in chunk and "content" in chunk["message"]:
                    part = chunk["message"]["content"]
                    answer += part
                    print(part, end="", flush=True)
            print()
            logger.info(f"Response: {answer[:120]}...")
        except Exception as e:
            logger.error(f"Model error: {e}")
            answer = "Opa, algo deu errado. Pode tentar de novo?"

        self.memory.store(text, answer)
        self.cache[text] = answer
        return answer
