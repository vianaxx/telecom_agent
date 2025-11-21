# run.py
from agent.agent import TelecomAgent
from agent.tools.router_api import get_router_status

agent = TelecomAgent()

print("📡 Telecom Field Assistant CLI")
print("Digite sua dúvida técnica ou 'status <DEVICE_ID>.\n")

while True:
    user = input("User > ").strip()

    # Comando especial: consultar status do dispositivo
    if user.lower().startswith("status "):
        device_id = user.split(" ", 1)[1]
        status = get_router_status(device_id)
        print(f"Dispositivo {device_id} status: {status['status']}, "
              f"latência {status['latency']}, packet loss {status['packet_loss']}")
        continue

    reply = agent.run(user)
    print("Agent >", reply)
