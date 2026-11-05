import random, json

SEED = 42
random.seed(SEED)
CATEGORIES = ["Apparel", "Electronics", "Home", "Footwear", "Beauty"]
STATUSES = ["Placed", "Shipped", "Delivered", "Returned", "Refunded"]

def generate_orders(n=50):
    orders = []
    for c in CATEGORIES:
        for _ in range(3):
            orders.append({"category": c, "status": random.choice(STATUSES), "days_since_created": random.randint(0, 30), "delayed_shipment": False})
    for s in STATUSES:
        orders.append({"category": random.choice(CATEGORIES), "status": s, "days_since_created": random.randint(0, 30), "delayed_shipment": False})
    for _ in range(n - len(orders)):
        orders.append({"category": random.choice(CATEGORIES), "status": random.choice(STATUSES), "days_since_created": random.randint(0, 30), "delayed_shipment": False})
    random.shuffle(orders)
    del_idx = set(random.sample(range(n), int(n * 0.20)))
    for idx, item in enumerate(orders):
        item["record_id"] = f"NYK-{10001 + idx}"
        item["order_value_inr"] = random.randint(299, 8999)
        item["delayed_shipment"] = idx in del_idx
    return orders

if __name__ == "__main__":
    data = generate_orders(50)
    with open("data/orders_dataset.json", "w") as f:
        json.dump(data, f, indent=2)
    print("Dataset created with 50 records!")