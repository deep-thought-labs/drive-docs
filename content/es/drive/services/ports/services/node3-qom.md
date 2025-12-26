---
title: "Configuración de Puertos: QOM Network"
---

**Número de Servicio:** 3  
**Service Name:** `qom`  
**Container Name:** `qom`

This document contains the complete port configuration for the QOM Network service. All ports are calculated using the standard formula: `Puerto del Host = Default Port + (Service Number × 10)`.

Since this is Servicio #3, all ports have a +30 offset from the default ports.

---

## Referencia Rápida

**Número de Servicio:** 3  
**Desplazamiento de Puerto:** +30

| Tipo de Puerto | Puerto del Host | Puerto del Contenedor |
|-----------|-----------|---------------|
| P2P | 26686 | 26656 |
| RPC | 26687 | 26657 |
| gRPC | 9120 | 9090 |
| gRPC-Web | 9121 | 9091 |
| REST API | 1347 | 1317 |
| JSON-RPC HTTP | 8575 | 8545 |
| JSON-RPC WS | 8576 | 8546 |

---

## Cálculo de Puertos

Este servicio usa **Número de Servicio 3**, por lo que todos los puertos tienen un desplazamiento de +30:

- **P2P**: 26656 + (3 × 10) = **26686**
- **RPC**: 26657 + (3 × 10) = **26687**
- **gRPC**: 9090 + (3 × 10) = **9120**
- **gRPC-Web**: 9091 + (3 × 10) = **9121**
- **REST API**: 1317 + (3 × 10) = **1347**
- **JSON-RPC HTTP**: 8545 + (3 × 10) = **8575**
- **JSON-RPC WebSocket**: 8546 + (3 × 10) = **8576**

---

## Puertos Requeridos

Estos puertos deben estar configurados para que el servicio funcione:

| Tipo de Puerto | Puerto del Host | Puerto del Contenedor | Descripción |
|-----------|-----------|---------------|-------------|
| **P2P** | 26686 | 26656 | Comunicación de red peer-to-peer |
| **RPC** | 26687 | 26657 | API RPC de Tendermint |

---

## Puertos Opcionales

Estos puertos pueden habilitarse si se necesitan para casos de uso específicos:

| Tipo de Puerto | Puerto del Host | Puerto del Contenedor | Descripción | Cuándo Habilitar |
|-----------|-----------|---------------|-------------|----------------|
| **gRPC** | 9120 | 9090 | Consultas gRPC del Cosmos SDK | Endpoint de API pública, conexiones de billetera |
| **gRPC-Web** | 9121 | 9091 | gRPC-Web (navegador) | Aplicaciones web, billeteras de navegador |
| **REST API** | 1347 | 1317 | API REST del Cosmos SDK | Compatibilidad con aplicaciones legacy |
| **JSON-RPC HTTP** | 8575 | 8545 | Ethereum JSON-RPC (HTTP) | MetaMask, herramientas Ethereum, dApps |
| **JSON-RPC WebSocket** | 8576 | 8546 | Ethereum JSON-RPC (WebSocket) | Eventos de blockchain en tiempo real |
| **Prometheus** | 26690 | 26660 | Métricas de Prometheus | Monitoreo de nodos |
| **EVM Metrics** | 6095 | 6065 | Métricas Prometheus de EVM | Monitoreo de rendimiento EVM |
| **Geth Metrics** | 8130 | 8100 | Métricas compatibles con Geth | Herramientas de monitoreo Geth |

---

## Configuración de Docker Compose

### Configuración Mínima (Solo Puertos Requeridos)

```yaml
services:
  qom:
    ports:
      - "26686:26656"  # P2P (required)
      - "26687:26657"  # RPC (required)
```

### Configuración Completa (Todos los Puertos)

```yaml
services:
  qom:
    ports:
      # Puertos requeridos
      - "26686:26656"  # P2P
      - "26687:26657"  # RPC
      
      # Puertos opcionales (descomenta si es necesario)
      - "9120:9090"    # gRPC
      - "9121:9091"    # gRPC-Web
      - "1347:1317"    # REST API
      - "8575:8545"    # JSON-RPC HTTP
      - "8576:8546"    # JSON-RPC WebSocket
      - "26690:26660"  # Prometheus
      - "6095:6065"    # EVM Metrics
      - "8130:8100"    # Geth Metrics
```

---

## Configuración de Firewall

If you need to accept incoming connections from external networks, configurar tu firewall using UFW (Ubuntu):

### Puertos Requeridos

```bash
# Puerto P2P (requerido para validadores y conexiones peer)
sudo ufw allow 26686/tcp

# Puerto RPC (opcional, solo si expones la API RPC)
sudo ufw allow 26687/tcp
```

### Puertos Opcionales

```bash
# gRPC (if exposing gRPC API)
sudo ufw allow 9120/tcp

# gRPC-Web (if exposing gRPC-Web API)
sudo ufw allow 9121/tcp

# REST API (if exposing REST API)
sudo ufw allow 1347/tcp

# JSON-RPC HTTP (if exposing Ethereum-compatible API)
sudo ufw allow 8575/tcp

# JSON-RPC WebSocket (if exposing WebSocket API)
sudo ufw allow 8576/tcp

# Prometheus (if exposing metrics)
sudo ufw allow 26690/tcp

# EVM Metrics (if exposing EVM metrics)
sudo ufw allow 6095/tcp

# Geth Metrics (if exposing Geth metrics)
sudo ufw allow 8130/tcp
```

**Note:** The `/tcp` protocol specification is optional in UFW. You can use either `sudo ufw allow 26686/tcp` or `sudo ufw allow 26686` - both work the same way.

---

## Ver También

- [Estrategia de Puertos]({{< relref ".." >}}) - Estrategia de asignación de puertos e información general
- [Referencia de Puertos: Nodos Blockchain]({{< relref "../blockchain-nodes" >}}) - Descripciones detalladas de puertos
- [Catálogo de Servicios]({{< relref "../../catalog" >}}) - Complete service listings
