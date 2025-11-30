---
title: "Service Structure"
---

# Service Structure

## Architecture Overview

Drive services are Docker containers defined using Docker Compose. Each service has:
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

## Docker Compose Configuration

Services are defined in `docker-compose.yml`, which contains all service-specific configurations:

- **Container image and version** - The Docker image used for the service
- **Environment variables** - Service configuration through environment variables (see [Environment Variables]({{< relref "blockchain-nodes/environment-variables" >}}))
- **Volume mounts** - Persistent data directories mapped to the container
- **Port mappings** - Network ports exposed by the service (see [Port Strategy]({{< relref "ports/strategy" >}}))
- **Network configuration** - Container networking setup

The `docker-compose.yml` file is the central configuration point for each service, defining how the container runs, what resources it uses, and how it connects to your system.

## drive.sh Script

The `drive.sh` script provides consistent management across all services:

### Basic Commands

```bash
cd services/<service-name>

./drive.sh up -d      # Start in daemon mode
./drive.sh stop       # Stop gracefully
./drive.sh restart    # Restart service
./drive.sh start      # Start (if stopped)
./drive.sh bash       # Access container shell
./drive.sh ps         # Show container status
./drive.sh logs       # View container logs
```

### Script Features

- Automatic permission handling
- Works with or without sudo
- Consistent interface across services

## Persistent Data

Each service's `persistent-data/` directory:
- Stored locally on your system
- Never shared or synced
- Contains service-specific data:
  - Blockchain nodes: chain data, keys, configuration

## Service Types

### Blockchain Nodes

All blockchain nodes share the same Docker image but differ in:
- Network/chain configuration
- Binary download URLs
- Genesis files
- Port assignments

See [Blockchain Nodes Catalog]({{< relref "blockchain-nodes/catalog" >}}) for specific configurations.
