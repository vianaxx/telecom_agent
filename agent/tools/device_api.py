
import random
from datetime import datetime

# Configurações de exemplo
ANTENNAS_PER_RRU = 3
CELLS_PER_ANTENNA = 3

def get_device_status(device_id: str):
    """
    Simula status completo de equipamentos TELECOM 5G.
    Inclui BBU/RRU, antenas, células, SNR, tráfego, alarms e logs.
    """
    # Métricas principais
    snr_avg = round(random.uniform(20, 40), 1)          # SNR médio em dB
    traffic_total = random.randint(100, 1000)           # Mbps
    packet_loss = round(random.uniform(0, 5), 2)        # %

    # Determinar status principal
    if packet_loss < 1 and snr_avg >= 30:
        status = "operacional"
    elif packet_loss < 3 or snr_avg >= 25:
        status = "degradado"
    else:
        status = "crítico"

    # Alarmes dinâmicos (múltiplos possíveis)
    alarms_options = ["nenhum", "minor", "major", "critical"]
    alarms = random.choices(alarms_options, weights=[50, 25, 15, 10], k=random.randint(1,2))
    alarms = ", ".join(sorted(set(alarms)))

    # Logs simulados (últimos 5 eventos)
    logs = []
    for _ in range(5):
        event_type = random.choice(["INFO", "WARN", "ERROR"])
        msg = random.choice([
            "Sincronização OK",
            "Pacotes perdidos detectados",
            "Reinício de RRU",
            "Alarme minor detectado",
            "Backhaul congestionado"
        ])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logs.append(f"{timestamp} | {event_type} | {msg}")

    # SNR por antena e célula
    antennas = {}
    for ant in range(1, ANTENNAS_PER_RRU + 1):
        cells = {}
        for cell in range(1, CELLS_PER_ANTENNA + 1):
            cells[f"Cell_{cell}"] = {
                "snr": round(random.uniform(20, 40), 1),
                "traffic": random.randint(10, 200)
            }
        antennas[f"Antenna_{ant}"] = cells

    return {
        "device_id": device_id,
        "status": status,
        "snr_avg": snr_avg,
        "traffic_total": traffic_total,
        "packet_loss": f"{packet_loss}%",
        "alarms": alarms,
        "logs": logs,
        "antennas": antennas
    }
