---
title: "Puertos"
---

# Port Allocation Strategy

Este documento explica la estrategia y lógica de asignación de puertos para ejecutar múltiples servicios simultáneamente en el mismo host. Para descripciones detalladas de puertos y configuraciones específicas de servicios, consulta los documentos relacionados.

## Tabla de Contenidos

- [Understanding Port Mapping](#understanding-port-mapping)
- [Port Allocation Strategy](#port-allocation-strategy)
- [Service-Specific Configuracións](#service-specific-configurations)
- [Port Conflict Resolution](#port-conflict-resolution)
- [Solución de Problemas](#troubleshooting)

---

## Entendiendo el Mapeo de Puertos

When configuring ports in `docker-compose.yml`, you'll see entries like this:

```yaml
ports:
  - "26656:26656"  # P2P
  - "26657:26657"  # RPC
```

### How Port Mapping Works

The format is: `"HOST_PORT:CONTAINER_PORT"`

- **Left number (HOST_PORT)**: This is the port on your computer/host system. **This is the one you can change** and **must be different** for each service running on your system. This is what you'll use to access the service from your host.

- **Right number (CONTAINER_PORT)**: This is the port **inside the Docker container**. **Never change this value** - it's what the service software expects and is configured in the service's internal settings. This value is fixed and recognized by the service's configuration.

### Why Different Host Puertos?

If you want to run multiple services on the same computer, each one needs different host ports to avoid conflicts. The container ports stay the same (because the software inside expects those specific ports), but you map them to different host ports.

**Example:**
- Service 1: `"26656:26656"` - Uses host port 26656
- Service 2: `"26666:26656"` - Uses host port 26666 (different!), but container still uses 26656 internally

This way, both services can run simultaneously without conflicts!

---

## Estrategia de Asignación de Puertos

### Service Numbering

Each service is assigned a **Service Number** starting from 0:

- **Servicio #0** = Infinite Mainnet (uses puertos estándar)
- **Servicio #1** = Infinite Testnet
- **Servicio #2** = Infinite Creative Network
- **Servicio #3** = QOM Network
- **Servicio #4+** = Future services (follow standard offset formula)
- And so on...

### Cálculo de Puertos Formula

For each port type, calculate the host port using:

**Puerto del Host = Default Port + (Service Number × 10)**

**Example:**
- P2P default port is 26656
- Servicio #0 (Mainnet): 26656 + (0 × 10) = **26656**
- Servicio #1 (Testnet): 26656 + (1 × 10) = **26666**
- Servicio #2 (Creative): 26656 + (2 × 10) = **26676**

This simple formula ensures:
- ✅ No port conflicts between services
- ✅ Easy to remember and calculate
- ✅ Consistent across all port types
- ✅ Supports up to 10+ services without issues

---

## Service-Specific Configuracións

Each preconfigured service has its own detailed configuration. See the [Catálogo de Servicios]({{< relref "../catalog" >}}) for complete service listings and port mappings.

Para descripciones detalladas de lo que hace cada tipo de puerto, consulta [Referencia de Puertos: Nodos Blockchain]({{< relref "blockchain-nodes" >}}).

---

## Resolución de Conflictos de Puertos

### Scenario 1: Port Already in Use

**Error:**
```
Error: bind: address already in use
```

**Solution:**
1. Find what's using the port: `sudo lsof -i :26656` or `sudo netstat -tulpn | grep 26656`
2. Change the host port in `docker-compose.yml` to the next available service number
3. Restart the service

**Example:**
If port 26656 is already in use, use Servicio #1 ports instead:
```yaml
ports:
  - "26666:26656"  # Changed host port, container port stays the same
```

---

### Scenario 2: Running Multiple Servicios Simultaneously

**Solution:** Each service must use a different Service Number

```yaml
# Servicio #0 (Mainnet)
ports:
  - "26656:26656"  # P2P
  - "26657:26657"  # RPC

# Servicio #1 (Testnet)
ports:
  - "26666:26656"  # P2P (different host port)
  - "26667:26657"  # RPC (different host port)

# Servicio #2 (Creative)
ports:
  - "26676:26656"  # P2P (different host port)
  - "26677:26657"  # RPC (different host port)
```

✅ **No conflicts** - Different host ports, same container ports

---

## Solución de Problemas

### Cannot Connect to Service

**Symptoms:**
- Service shows connection errors
- Cannot establish network connections

**Possible Causes:**
1. Firewall blocking required port
2. Wrong port mapping in `docker-compose.yml`
3. NAT/firewall no configurado para dirección externa

**Solution:**
1. Check firewall: `sudo ufw status`
2. Verify port mapping: `docker compose ps` or `docker ps`
3. For blockchain nodes: Configure `NODE_P2P_EXTERNAL_ADDRESS` if behind NAT

---

### RPC Not Accessible

**Symptoms:**
- Cannot access RPC API from host
- Connection refused errors

**Possible Causes:**
1. RPC port not mapped in `docker-compose.yml`
2. Firewall blocking RPC port
3. RPC only listening on localhost inside container

**Solution:**
1. Verify port mapping in `docker-compose.yml`
2. Check firewall rules
3. Test from inside container: `curl http://localhost:26657/status`

---

## Configuración de Firewall

For detailed instructions on how to configure your system's firewall to permitir conexiones entrantes:

- [Configuración de Firewall Guide]({{< relref "firewall-configuration" >}}) - Guía completa para configurar firewalls en Ubuntu/Linux, macOS y Windows

---

## Referencia de Puertos Documentation

Para descripciones detalladas de tipos de puertos por categoría de servicio:

- [Nodos Blockchain]({{< relref "blockchain-nodes" >}}) - Tipos de puertos utilizados por servicios de nodos blockchain
- [General]({{< relref "general" >}}) - Puertos generales compartidos entre servicios

---

## Ver También

- [Catálogo de Servicios]({{< relref "../catalog" >}}) - Listados completos de servicios con configuraciones de puertos
- [Variables de Entorno]({{< relref "../environment" >}}) - Referencia de variables de entorno
