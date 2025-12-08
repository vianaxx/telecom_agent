
from agent.agent import TelecomAgent
from agent.tools.device_api import get_device_status

agent = TelecomAgent()

print("📡 Telecom Field Assistant CLI – 5G")
print("Digite sua dúvida técnica ou 'status <DEVICE_ID>'.\n")

while True:
    user = input("User > ").strip()

    if user.lower().startswith("status "):
        device_id = user.split(" ", 1)[1]
        status = get_device_status(device_id)

        print(f"\n--- Status do Dispositivo {device_id} ---")
        print(f"Status geral: {status['status']}")
        print(f"SNR médio: {status['snr_avg']} dB")
        print(f"Tráfego total: {status['traffic_total']} Mbps")
        print(f"Packet Loss: {status['packet_loss']}")
        print(f"Alarms: {status['alarms']}")
        print("\n--- Antenas e Células ---")
        for ant, cells in status["antennas"].items():
            print(f"{ant}:")
            for cell, metrics in cells.items():
                print(f"  {cell} | SNR: {metrics['snr']} dB | Tráfego: {metrics['traffic']} Mbps")
        print("\n--- Últimos Logs ---")
        for log in status["logs"]:
            print(f"  {log}")
        print("\n")
        continue


    reply = agent.run(user)
    print("Agent >", reply)
