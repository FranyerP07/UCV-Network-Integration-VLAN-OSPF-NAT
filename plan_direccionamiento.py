"""
Plan de direccionamiento de la red universitaria (Laboratorio #6, Redes de Computadoras).

Para cada facultad (R1-R4) calcula:
- la IP del gateway (primera IP válida de la red),
- la IP estática reservada (.10),
- el rango excluido del DHCP (las primeras 20 IP),
- el pool del DHCP (del .21 al último host).

Usa solo la librería estándar de Python: ipaddress.
Ejecutar: python plan_direccionamiento.py
"""

import ipaddress

# Red de tránsito entre el Data Center (R0) y las facultades
RED_TRANSITO = ipaddress.ip_network("10.0.0.0/24")
DNS = "8.8.8.8"

# Redes de cada facultad, según la tabla de distribución del laboratorio
FACULTADES = {
    "R1 Rectorado":  {"vlans": {11: "192.168.11.0/24", 12: "192.168.12.0/24"}, "ip_transito": "10.0.0.1"},
    "R2 Ciencias":   {"vlans": {21: "192.168.21.0/24", 22: "192.168.22.0/24"}, "ip_transito": "10.0.0.2"},
    "R3 Medicina":   {"vlans": {31: "192.168.31.0/24", 32: "192.168.32.0/24"}, "ip_transito": "10.0.0.3"},
    "R4 Ingeniería": {"vlans": {41: "192.168.41.0/24", 42: "192.168.42.0/24"}, "ip_transito": "10.0.0.4"},
}

RESERVADAS_DHCP = 20  # primeras 20 IP fuera del pool


def calcular_red(red_txt):
    red = ipaddress.ip_network(red_txt)
    hosts = list(red.hosts())

    gateway = hosts[0]                      # primera IP válida
    estatica = red.network_address + 10     # IP .10 para equipos con IP fija
    fin_excluido = hosts[RESERVADAS_DHCP - 1]
    pool_inicio = hosts[RESERVADAS_DHCP]
    pool_fin = hosts[-1]

    # Comprobaciones: la IP estática debe quedar dentro del rango reservado
    assert gateway <= estatica <= fin_excluido, "la IP estática no está reservada"
    assert red.overlaps(RED_TRANSITO) is False, "la red choca con el tránsito"

    return {
        "red": str(red),
        "gateway": str(gateway),
        "estatica": str(estatica),
        "excluido": f"{hosts[0]} - {fin_excluido}",
        "pool": f"{pool_inicio} - {pool_fin}",
        "dns": DNS,
    }


def generar_plan():
    plan = []
    for facultad, datos in FACULTADES.items():
        for vlan, red_txt in datos["vlans"].items():
            info = calcular_red(red_txt)
            info.update({"facultad": facultad, "vlan": vlan})
            plan.append(info)
    return plan


if __name__ == "__main__":
    plan = generar_plan()
    print(f"{'Facultad':<15}{'VLAN':<6}{'Red':<20}{'Gateway':<15}{'Estática':<14}{'Pool DHCP'}")
    for p in plan:
        print(f"{p['facultad']:<15}{p['vlan']:<6}{p['red']:<20}{p['gateway']:<15}"
              f"{p['estatica']:<14}{p['pool']}")

    print("\nRed de tránsito:", RED_TRANSITO)
    for facultad, datos in FACULTADES.items():
        print(f"{facultad}: IP en el tránsito = {datos['ip_transito']}")
