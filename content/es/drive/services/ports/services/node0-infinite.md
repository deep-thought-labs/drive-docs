---
title: "Configuración de Puertos: Infinite Mainnet"
---

**Número de Servicio:** 0  
**Service Name:** `infinite`  
**Container Name:** `infinite`

This document contains the complete port configuration for the Infinite Mainnet service. All ports are calculated using the standard formula: `Puerto del Host = Default Port + (Service Number × 10)`.

Since this is Servicio #0 (Mainnet), it uses the standard/default ports.

---

## Referencia Rápida

**Número de Servicio:** 0  
**Desplazamiento de Puerto:** +0 (puertos estándar)

| Tipo de Puerto | Puerto del Host | Puerto del Contenedor |
|-----------|-----------|---------------|
| P2P | 26656 | 26656 |
| RPC | 26657 | 26657 |
| gRPC | 9090 | 9090 |
| gRPC-Web | 9091 | 9091 |
| REST API | 1317 | 1317 |
| JSON-RPC HTTP | 8545 | 8545 |
| JSON-RPC WS | 8546 | 8546 |

---

## Cálculo de Puertos

Este servicio usa **Número de Servicio 0**, por lo que todos los puertos usan los valores predeterminados:

- **P2P**: 26656 + (0 × 10) = **26656**
- **RPC**: 26657 + (0 × 10) = **26657**
- **gRPC**: 9090 + (0 × 10) = **9090**
- **gRPC-Web**: 9091 + (0 × 10) = **9091**
- **REST API**: 1317 + (0 × 10) = **1317**
- **JSON-RPC HTTP**: 8545 + (0 × 10) = **8545**
- **JSON-RPC WebSocket**: 8546 + (0 × 10) = **8546**

---

## Puertos Requeridos

Estos puertos deben estar configurados para que el servicio funcione:

| Tipo de Puerto | Puerto del Host | Puerto del Contenedor | Descripción |
|-----------|-----------|---------------|-------------|
| **P2P** | 26656 | 26656 | Comunicación de red peer-to-peer |
| **RPC** | 26657 | 26657 | API RPC de Tendermint |

---

## Puertos Opcionales

Estos puertos pueden habilitarse si se necesitan para casos de uso específicos:

| Tipo de Puerto | Puerto del Host | Puerto del Contenedor | Descripción | Cuándo Habilitar |
|-----------|-----------|---------------|-------------|----------------|
| **gRPC** | 9090 | 9090 | Consultas gRPC del Cosmos SDK | Endpoint de API pública, conexiones de billetera |
| **gRPC-Web** | 9091 | 9091 | gRPC-Web (navegador) | Aplicaciones web, billeteras de navegador |
| **REST API** | 1317 | 1317 | API REST del Cosmos SDK | Compatibilidad con aplicaciones legacy |
| **JSON-RPC HTTP** | 8545 | 8545 | Ethereum JSON-RPC (HTTP) | MetaMask, herramientas Ethereum, dApps |
| **JSON-RPC WebSocket** | 8546 | 8546 | Ethereum JSON-RPC (WebSocket) | Eventos de blockchain en tiempo real |
| **Prometheus** | 26660 | 26660 | Métricas de Prometheus | Monitoreo de nodos |
| **EVM Metrics** | 6065 | 6065 | Métricas Prometheus de EVM | Monitoreo de rendimiento EVM |
| **Geth Metrics** | 8100 | 8100 | Métricas compatibles con Geth | Herramientas de monitoreo Geth |

---

## Configuración de Docker Compose

### Configuración Mínima (Solo Puertos Requeridos)

```yaml
services:
  infinite:
    ports:
      - "26656:26656"  # P2P (required)
      - "26657:26657"  # RPC (required)
```

### Configuración Completa (Todos los Puertos)

```yaml
services:
  infinite:
    ports:
      # Puertos requeridos
      - "26656:26656"  # P2P
      - "26657:26657"  # RPC
      
      # Puertos opcionales (descomenta si es necesario)
      - "9090:9090"    # gRPC
      - "9091:9091"    # gRPC-Web
      - "1317:1317"    # REST API
      - "8545:8545"    # JSON-RPC HTTP
      - "8546:8546"    # JSON-RPC WebSocket
      - "26660:26660"  # Prometheus
      - "6065:6065"    # EVM Metrics
      - "8100:8100"    # Geth Metrics
```

---

## Configuración de Firewall

If you need to accept incoming connections from external networks, configurar tu firewall using UFW (Ubuntu):

### Puertos Requeridos

```bash
# Puerto P2P (requerido para validadores y conexiones peer)
sudo ufw allow 26656/tcp

# Puerto RPC (opcional, solo si expones la API RPC)
sudo ufw allow 26657/tcp
```

### Puertos Opcionales

```bash
# gRPC (if exposing gRPC API)
sudo ufw allow 9090/tcp

# gRPC-Web (if exposing gRPC-Web API)
sudo ufw allow 9091/tcp

# REST API (if exposing REST API)
sudo ufw allow 1317/tcp

# JSON-RPC HTTP (if exposing Ethereum-compatible API)
sudo ufw allow 8545/tcp

# JSON-RPC WebSocket (if exposing WebSocket API)
sudo ufw allow 8546/tcp

# Prometheus (if exposing metrics)
sudo ufw allow 26660/tcp

# EVM Metrics (if exposing EVM metrics)
sudo ufw allow 6065/tcp

# Geth Metrics (if exposing Geth metrics)
sudo ufw allow 8100/tcp
```

**Note:** The `/tcp` protocol specification is optional in UFW. You can use either `sudo ufw allow 26656/tcp` or `sudo ufw allow 26656` - both work the same way.

---

## Ver También

- [Estrategia de Puertos]({{< relref ".." >}}) - Estrategia de asignación de puertos e información general
- [Referencia de Puertos: Nodos Blockchain]({{< relref "../blockchain-nodes" >}}) - Descripciones detalladas de puertos
- [Catálogo de Servicios]({{< relref "../../catalog" >}}) - Complete service listings
