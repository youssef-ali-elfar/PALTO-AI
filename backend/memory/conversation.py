from collections import defaultdict
from backend.config import settings

class ConversationMemory:
    def __init__(self):
        self.sessions = defaultdict(list)

    def add(self, session_id, role, content):
        self.sessions[session_id].append({"role": role, "content": content})
        self.sessions[session_id] = self.sessions[session_id][-settings.max_memory_messages:]

    def get(self, session_id):
        return list(self.sessions[session_id])

    def context_text(self, session_id):
        return "\n".join(
            f"{m['role']}: {m['content']}" for m in self.sessions[session_id]
        )

memory = ConversationMemory()
