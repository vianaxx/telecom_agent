
import chromadb

class VectorStore:
    """
    Armazena e busca documentos técnicos usando ChromaDB.
    """
    def __init__(self, name="telecom_knowledge"):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(name)

    def add_document(self, text, metadata=None):
        """Adiciona um documento ao vetor store."""
        self.collection.add(
            documents=[text],
            metadatas=[metadata or {}],
            ids=[metadata.get("id", str(hash(text)))]
        )

    def search(self, query, top_k=3):
        """Retorna lista de documentos mais relevantes."""
        result = self.collection.query(query_texts=[query], n_results=top_k)
        if result and "documents" in result and result["documents"]:
            return result["documents"][0]  # lista de strings
        return []
