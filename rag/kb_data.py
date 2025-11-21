# rag/kb_data.py

KB_DOCS = [
    ("Passo a passo para reduzir packet loss: 1. Verifique conexões físicas; 2. Reinicie o ONT/roteador; 3. Execute teste de ping; 4. Confirme taxa de erro <1%.", {"id": "packet_loss"}),
    ("Comando para reiniciar roteador via CLI: system restart. Aguarde 2-3 minutos para reinicialização completa.", {"id": "router_reboot"}),
    ("Como resetar um ONT FTTH: pressione botão reset por 10s até LED piscar. Configure novamente após reinício.", {"id": "ont_reset"}),
    ("Checklist de instalação FTTH: verifique fibra, limpe conectores, conecte ONT e teste sinal.", {"id": "fiber_check"}),
    ("Teste de latência: execute ping <gateway> com 20 pacotes. Latência ideal <30ms, perda de pacotes <1%.", {"id": "latency_test"}),
    ("Atualização de firmware do roteador: baixe versão oficial, faça upload e reinicie equipamento.", {"id": "firmware_update"}),
    ("Verifique sinal óptico: OTDR ou medidor de potência. Nível mínimo aceitável: -28 dBm.", {"id": "signal_strength"}),
    ("Configuração VLAN: VLAN 10 para voz, VLAN 20 para dados, configure firewall conforme padrão.", {"id": "vlan_config"}),
    ("Sem conexão de internet: 1. Verifique LEDs do ONT; 2. Reinicie equipamentos; 3. Teste cabos; 4. Confirme DHCP.", {"id": "troubleshoot_no_internet"}),
]
