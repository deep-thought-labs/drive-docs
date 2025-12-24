---
title: "Estructura del Servicio"
weight: 530
---

## Arquitectura Overview

Los servicios de Drive son contenedores Docker definidos usando Docker Compose. Cada servicio tiene:
- `docker-compose.yml` - Service definition and configuration
- `drive.sh` - Management wrapper script
- `persistent-data/` - Service-specific data (user-owned, not in repository)

## Service Directory Structure

```
services/
├── <service-name>/
│   ├── docker-compose.yml    # Container definition
│   ├── drive.sh              # Management script
│   └── persistent-data/       # User data (git-ignored)
```

## Configuración de Docker Compose

Servicios are defined in `docker-compose.yml`, which contains all service-specific configurations:

- **Container image and version** - The Docker image used for the service
- **Environment variables** - Service configuration through environment variables (see [Variables de Entorno]({{< relref "environment" >}}))
- **Volume mounts** - Persistent data directories mapped to the container
- **Port mappings** - Network ports exposed by the service (see [Estrategia de Puertos]({{< relref "ports" >}}))
- **Network configuration** - Container networking setup

The `docker-compose.yml` file is the central configuration point for each service, defining how the container runs, what resources it uses, and how it connects to your system.

## drive.sh Script

The `drive.sh` script provides consistent management across all services:

### Comandos Básicos

```bash
cd services/<service-name>

./drive.sh up -d      # Start in daemon mode
./drive.sh stop       # Stop gracefully
./drive.sh down       # Detener y eliminar contenedor
./drive.sh start      # Iniciar (si está detenido)
./drive.sh restart    # Reiniciar servicio
./drive.sh ps         # Mostrar estado del contenedor
./drive.sh logs       # Ver registros del contenedor
./drive.sh bash       # Acceder a la shell del contenedor
```

### Script Features

- Automatic permission handling
- Works with or without sudo
- Consistent interface across services

## Datos Persistentes

Each service's `persistent-data/` directory:
- Stored locally on your system
- Never shared or synced
- Contains service-specific data:
  - Blockchain nodes: chain data, keys, configuration

## Tipos de Servicios

### Nodos Blockchain

All blockchain nodes share the same Docker image but differ in:
- Network/chain configuration
- Binary download URLs
- Genesis files
- Port assignments

See [Catálogo de Servicios]({{< relref "catalog" >}}) for the complete list of all blockchain node services and their configurations.
