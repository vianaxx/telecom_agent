# agent/agent.py
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
            {"role": "system",
             "content": "Você é um assistente técnico experiente. Responda de forma curta, clara, humana e passo a passo."},
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
            answer = "Opa, algo deu errado 😅. Pode tentar de novo?"

        self.memory.store(text, answer)
        self.cache[text] = answer
        return answer
