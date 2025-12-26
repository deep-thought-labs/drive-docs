---
title: "Configuración de Puertos: Infinite Testnet"
---

**Número de Servicio:** 1  
**Service Name:** `infinite-testnet`  
**Container Name:** `infinite-testnet`

This document contains the complete port configuration for the Infinite Testnet service. All ports are calculated using the standard formula: `Puerto del Host = Default Port + (Service Number × 10)`.

Since this is Servicio #1, all ports have a +10 offset from the default ports.

---

## Referencia Rápida

**Número de Servicio:** 1  
**Desplazamiento de Puerto:** +10

| Tipo de Puerto | Puerto del Host | Puerto del Contenedor |
|-----------|-----------|---------------|
| P2P | 26666 | 26656 |
| RPC | 26667 | 26657 |
| gRPC | 9100 | 9090 |
| gRPC-Web | 9101 | 9091 |
| REST API | 1327 | 1317 |
| JSON-RPC HTTP | 8555 | 8545 |
| JSON-RPC WS | 8556 | 8546 |

---

## Cálculo de Puertos

Este servicio usa **Número de Servicio 1**, por lo que todos los puertos tienen un desplazamiento de +10:

- **P2P**: 26656 + (1 × 10) = **26666**
- **RPC**: 26657 + (1 × 10) = **26667**
- **gRPC**: 9090 + (1 × 10) = **9100**
- **gRPC-Web**: 9091 + (1 × 10) = **9101**
- **REST API**: 1317 + (1 × 10) = **1327**
- **JSON-RPC HTTP**: 8545 + (1 × 10) = **8555**
- **JSON-RPC WebSocket**: 8546 + (1 × 10) = **8556**

---

## Puertos Requeridos

Estos puertos deben estar configurados para que el servicio funcione:

| Tipo de Puerto | Puerto del Host | Puerto del Contenedor | Descripción |
|-----------|-----------|---------------|-------------|
| **P2P** | 26666 | 26656 | Comunicación de red peer-to-peer |
| **RPC** | 26667 | 26657 | API RPC de Tendermint |

---

## Puertos Opcionales

Estos puertos pueden habilitarse si se necesitan para casos de uso específicos:

| Tipo de Puerto | Puerto del Host | Puerto del Contenedor | Descripción | Cuándo Habilitar |
|-----------|-----------|---------------|-------------|----------------|
| **gRPC** | 9100 | 9090 | Consultas gRPC del Cosmos SDK | Endpoint de API pública, conexiones de billetera |
| **gRPC-Web** | 9101 | 9091 | gRPC-Web (navegador) | Aplicaciones web, billeteras de navegador |
| **REST API** | 1327 | 1317 | API REST del Cosmos SDK | Compatibilidad con aplicaciones legacy |
| **JSON-RPC HTTP** | 8555 | 8545 | Ethereum JSON-RPC (HTTP) | MetaMask, herramientas Ethereum, dApps |
| **JSON-RPC WebSocket** | 8556 | 8546 | Ethereum JSON-RPC (WebSocket) | Eventos de blockchain en tiempo real |
| **Prometheus** | 26670 | 26660 | Métricas de Prometheus | Monitoreo de nodos |
| **EVM Metrics** | 6075 | 6065 | Métricas Prometheus de EVM | Monitoreo de rendimiento EVM |
| **Geth Metrics** | 8110 | 8100 | Métricas compatibles con Geth | Herramientas de monitoreo Geth |

---

## Configuración de Docker Compose

### Configuración Mínima (Solo Puertos Requeridos)

```yaml
services:
  infinite-testnet:
    ports:
      - "26666:26656"  # P2P (required)
      - "26667:26657"  # RPC (required)
```

### Configuración Completa (Todos los Puertos)

```yaml
services:
  infinite-testnet:
    ports:
      # Puertos requeridos
      - "26666:26656"  # P2P
      - "26667:26657"  # RPC
      
      # Puertos opcionales (descomenta si es necesario)
      - "9100:9090"    # gRPC
      - "9101:9091"    # gRPC-Web
      - "1327:1317"    # REST API
      - "8555:8545"    # JSON-RPC HTTP
      - "8556:8546"    # JSON-RPC WebSocket
      - "26670:26660"  # Prometheus
      - "6075:6065"    # EVM Metrics
      - "8110:8100"    # Geth Metrics
```

---

## Configuración de Firewall

If you need to accept incoming connections from external networks, configurar tu firewall using UFW (Ubuntu):

### Puertos Requeridos

```bash
# Puerto P2P (requerido para validadores y conexiones peer)
sudo ufw allow 26666/tcp

# Puerto RPC (opcional, solo si expones la API RPC)
sudo ufw allow 26667/tcp
```

### Puertos Opcionales

```bash
# gRPC (if exposing gRPC API)
sudo ufw allow 9100/tcp

# gRPC-Web (if exposing gRPC-Web API)
sudo ufw allow 9101/tcp

# REST API (if exposing REST API)
sudo ufw allow 1327/tcp

# JSON-RPC HTTP (if exposing Ethereum-compatible API)
sudo ufw allow 8555/tcp

# JSON-RPC WebSocket (if exposing WebSocket API)
sudo ufw allow 8556/tcp

# Prometheus (if exposing metrics)
sudo ufw allow 26670/tcp

# EVM Metrics (if exposing EVM metrics)
sudo ufw allow 6075/tcp

# Geth Metrics (if exposing Geth metrics)
sudo ufw allow 8110/tcp
```

**Note:** The `/tcp` protocol specification is optional in UFW. You can use either `sudo ufw allow 26666/tcp` or `sudo ufw allow 26666` - both work the same way.

---

## Ver También

- [Estrategia de Puertos]({{< relref ".." >}}) - Estrategia de asignación de puertos e información general
- [Referencia de Puertos: Nodos Blockchain]({{< relref "../blockchain-nodes" >}}) - Descripciones detalladas de puertos
- [Catálogo de Servicios]({{< relref "../../catalog" >}}) - Complete service listings
