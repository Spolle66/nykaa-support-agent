import os
from data.knowledge_base import KNOWLEDGE_BASE
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

def grounded_generation(query: str, threshold: float = 0.60):
    q = query.lower()
    for doc in KNOWLEDGE_BASE:
        if any(w in q for w in doc["topic"].split() if len(w) > 3):
            return f"[Grounded Answer]: {doc['content']}"
    return "[TRIGGER FALLBACK] I don't know based on Nykaa's policies. Escalating to human agent."