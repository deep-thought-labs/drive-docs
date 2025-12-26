---
title: "Configuraciones de Puertos de Servicios"
---

Configuraciones completas de puertos para cada servicio, incluyendo mapeos de puertos, ejemplos de Docker Compose y configuraciones de firewall.

## Available Service Configuracións

- [Infinite Mainnet (node0-infinite)]({{< relref "node0-infinite" >}}) - Servicio #0, puertos estándar
- [Infinite Testnet (node1-infinite-testnet)]({{< relref "node1-infinite-testnet" >}}) - Servicio #1, +10 offset
- [Infinite Creative Network (node2-infinite-creative)]({{< relref "node2-infinite-creative" >}}) - Servicio #2, +20 offset
- [QOM Network (node3-qom)]({{< relref "node3-qom" >}}) - Servicio #3, +30 offset

## Qué se Incluye

Each service configuration document includes:

- **Referencia Rápida** - Table of all port mappings
- **Cálculo de Puertos** - How ports are calculated using the service number
- **Puertos Requeridos** - Puertos that must be configured
- **Puertos Opcionales** - Additional ports for specific use cases
- **Configuración de Docker Compose** - Ready-to-use examples (minimal and full)
- **Configuración de Firewall** - UFW commands for each port

## Ver También

- [Estrategia de Puertos]({{< relref ".." >}}) - Estrategia de asignación de puertos e información general
- [Referencia de Puertos: Nodos Blockchain]({{< relref "../blockchain-nodes" >}}) - Descripciones detalladas de puertos
- [Catálogo de Servicios]({{< relref "../../catalog" >}}) - Complete service listings
