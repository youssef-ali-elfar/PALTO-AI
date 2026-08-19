from backend.agents.router import classify_intent

def test_general():
    assert classify_intent("Hello PALTO") == "GENERAL"

def test_interaction():
    assert classify_intent("Can these drugs interact?") == "DRUG_INTERACTION"
