---
title: "Configuración de Puertos: Infinite Creative Network"
---

**Número de Servicio:** 2  
**Service Name:** `infinite-creative`  
**Container Name:** `infinite-creative`

This document contains the complete port configuration for the Infinite Creative Network service. All ports are calculated using the standard formula: `Puerto del Host = Default Port + (Service Number × 10)`.

Since this is Servicio #2, all ports have a +20 offset from the default ports.

---

## Referencia Rápida

**Número de Servicio:** 2  
**Desplazamiento de Puerto:** +20

| Tipo de Puerto | Puerto del Host | Puerto del Contenedor |
|-----------|-----------|---------------|
| P2P | 26676 | 26656 |
| RPC | 26677 | 26657 |
| gRPC | 9110 | 9090 |
| gRPC-Web | 9111 | 9091 |
| REST API | 1337 | 1317 |
| JSON-RPC HTTP | 8565 | 8545 |
| JSON-RPC WS | 8566 | 8546 |

---

## Cálculo de Puertos

Este servicio usa **Número de Servicio 2**, por lo que todos los puertos tienen un desplazamiento de +20:

- **P2P**: 26656 + (2 × 10) = **26676**
- **RPC**: 26657 + (2 × 10) = **26677**
- **gRPC**: 9090 + (2 × 10) = **9110**
- **gRPC-Web**: 9091 + (2 × 10) = **9111**
- **REST API**: 1317 + (2 × 10) = **1337**
- **JSON-RPC HTTP**: 8545 + (2 × 10) = **8565**
- **JSON-RPC WebSocket**: 8546 + (2 × 10) = **8566**

---

## Puertos Requeridos

Estos puertos deben estar configurados para que el servicio funcione:

| Tipo de Puerto | Puerto del Host | Puerto del Contenedor | Descripción |
|-----------|-----------|---------------|-------------|
| **P2P** | 26676 | 26656 | Comunicación de red peer-to-peer |
| **RPC** | 26677 | 26657 | API RPC de Tendermint |

---

## Puertos Opcionales

Estos puertos pueden habilitarse si se necesitan para casos de uso específicos:

| Tipo de Puerto | Puerto del Host | Puerto del Contenedor | Descripción | Cuándo Habilitar |
|-----------|-----------|---------------|-------------|----------------|
| **gRPC** | 9110 | 9090 | Consultas gRPC del Cosmos SDK | Endpoint de API pública, conexiones de billetera |
| **gRPC-Web** | 9111 | 9091 | gRPC-Web (navegador) | Aplicaciones web, billeteras de navegador |
| **REST API** | 1337 | 1317 | API REST del Cosmos SDK | Compatibilidad con aplicaciones legacy |
| **JSON-RPC HTTP** | 8565 | 8545 | Ethereum JSON-RPC (HTTP) | MetaMask, herramientas Ethereum, dApps |
| **JSON-RPC WebSocket** | 8566 | 8546 | Ethereum JSON-RPC (WebSocket) | Eventos de blockchain en tiempo real |
| **Prometheus** | 26680 | 26660 | Métricas de Prometheus | Monitoreo de nodos |
| **EVM Metrics** | 6085 | 6065 | Métricas Prometheus de EVM | Monitoreo de rendimiento EVM |
| **Geth Metrics** | 8120 | 8100 | Métricas compatibles con Geth | Herramientas de monitoreo Geth |

---

## Configuración de Docker Compose

### Configuración Mínima (Solo Puertos Requeridos)

```yaml
services:
  infinite-creative:
    ports:
      - "26676:26656"  # P2P (required)
      - "26677:26657"  # RPC (required)
```

### Configuración Completa (Todos los Puertos)

```yaml
services:
  infinite-creative:
    ports:
      # Puertos requeridos
      - "26676:26656"  # P2P
      - "26677:26657"  # RPC
      
      # Puertos opcionales (descomenta si es necesario)
      - "9110:9090"    # gRPC
      - "9111:9091"    # gRPC-Web
      - "1337:1317"    # REST API
      - "8565:8545"    # JSON-RPC HTTP
      - "8566:8546"    # JSON-RPC WebSocket
      - "26680:26660"  # Prometheus
      - "6085:6065"    # EVM Metrics
      - "8120:8100"    # Geth Metrics
```

---

## Configuración de Firewall

If you need to accept incoming connections from external networks, configurar tu firewall using UFW (Ubuntu):

### Puertos Requeridos

```bash
# Puerto P2P (requerido para validadores y conexiones peer)
sudo ufw allow 26676/tcp

# Puerto RPC (opcional, solo si expones la API RPC)
sudo ufw allow 26677/tcp
```

### Puertos Opcionales

```bash
# gRPC (if exposing gRPC API)
sudo ufw allow 9110/tcp

# gRPC-Web (if exposing gRPC-Web API)
sudo ufw allow 9111/tcp

# REST API (if exposing REST API)
sudo ufw allow 1337/tcp

# JSON-RPC HTTP (if exposing Ethereum-compatible API)
sudo ufw allow 8565/tcp

# JSON-RPC WebSocket (if exposing WebSocket API)
sudo ufw allow 8566/tcp

# Prometheus (if exposing metrics)
sudo ufw allow 26680/tcp

# EVM Metrics (if exposing EVM metrics)
sudo ufw allow 6085/tcp

# Geth Metrics (if exposing Geth metrics)
sudo ufw allow 8120/tcp
```

**Note:** The `/tcp` protocol specification is optional in UFW. You can use either `sudo ufw allow 26676/tcp` or `sudo ufw allow 26676` - both work the same way.

---

## Ver También

- [Estrategia de Puertos]({{< relref ".." >}}) - Estrategia de asignación de puertos e información general
- [Referencia de Puertos: Nodos Blockchain]({{< relref "../blockchain-nodes" >}}) - Descripciones detalladas de puertos
- [Catálogo de Servicios]({{< relref "../../catalog" >}}) - Complete service listings
