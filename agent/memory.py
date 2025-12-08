
class Memory:
    """
    Histórico de chat, limitado às últimas 20 mensagens.
    """
    def __init__(self):
        self.chat_history = []

    def store(self, user, assistant):
        if len(self.chat_history) >= 20:
            self.chat_history = self.chat_history[-18:]  # manter últimas 18 + novo par
        self.chat_history.append({"role": "user", "content": user})
        self.chat_history.append({"role": "assistant", "content": assistant})

    def get(self):
        return self.chat_history

    def clear(self):
        """Remove todo o histórico."""
        self.chat_history = []
