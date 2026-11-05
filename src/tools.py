import json, os

def check_order_status(record_id: str) -> dict:
    p = "data/orders_dataset.json"
    if not os.path.exists(p):
        return {"error": "Dataset not generated."}
    with open(p, "r") as f:
        orders = {o["record_id"]: o for o in json.load(f)}
    o = orders.get(record_id.strip().upper())
    if not o:
        return {"error": f"Order {record_id} not found."}
    score = round((0.50 if o["delayed_shipment"] else 0.0) + (0.35 * min(1.0, o["days_since_created"]/30.0)) + (0.15 * min(1.0, o["order_value_inr"]/9000.0)), 3)
    return {**o, "escalation_score": score, "recommend_escalation": score >= 0.45}