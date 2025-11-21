# agent/tools/router_api.py
import random

def get_router_status(device_id: str):
    """Simula status dinâmico de roteador/ONT."""
    return {
        "device_id": device_id,
        "packet_loss": f"{random.randint(0,20)}%",
        "latency": f"{random.randint(10,300)}ms",
        "status": random.choice(["ok", "degraded", "critical"])
    }
