from backend.memory.conversation import ConversationMemory

def test_memory_limit():
    m = ConversationMemory()
    for i in range(20):
        m.add("x", "doctor", str(i))
    assert len(m.get("x")) <= 10
