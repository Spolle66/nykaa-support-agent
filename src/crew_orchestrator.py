import re, os
from pydantic import BaseModel
from src.rag_core import grounded_generation
from src.tools import check_order_status
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

class AgentResponseSchema(BaseModel):
    trace_id: str
    query_sanitized: str
    agent_path: str
    escalate: bool
    output_text: str
    confidence_score: float
    pii_detected: bool

class NykaaOrchestrationCrew:
    def run(self, user_input: str, session_id: str = "default", trace_id: str = "tr-001") -> AgentResponseSchema:
        if re.search(r"ignore previous instructions", user_input, re.I):
            return AgentResponseSchema(trace_id=trace_id, query_sanitized="[BLOCKED]", agent_path="SecurityGuardrail", escalate=True, output_text="Prompt injection blocked.", confidence_score=0.0, pii_detected=False)
        pii = bool(re.search(r"\d{10}", user_input) or re.search(r"\d{4}[-\s]?\d{4}", user_input))
        clean = re.sub(r"\d{10}", "[MASKED_PHONE]", user_input)
        m = re.search(r"NYK-\d{5}", clean, re.I)
        if m:
            res = check_order_status(m.group(0))
            return AgentResponseSchema(trace_id=trace_id, query_sanitized=clean, agent_path="LookupAgent", escalate=res.get("recommend_escalation", False), output_text=str(res), confidence_score=1.0, pii_detected=pii)
        ans = grounded_generation(clean)
        fb = "[TRIGGER FALLBACK]" in ans
        return AgentResponseSchema(trace_id=trace_id, query_sanitized=clean, agent_path="RetrievalAgent", escalate=fb, output_text=ans, confidence_score=0.4 if fb else 0.95, pii_detected=pii)