---
title: "Service Structure"
weight: 530
---

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
- **Environment variables** - Service configuration through environment variables (see [Environment Variables]({{< relref "environment" >}}))
- **Volume mounts** - Persistent data directories mapped to the container
- **Port mappings** - Network ports exposed by the service (see [Port Strategy]({{< relref "ports" >}}))
- **Network configuration** - Container networking setup

The `docker-compose.yml` file is the central configuration point for each service, defining how the container runs, what resources it uses, and how it connects to your system.

For detailed technical analysis of the `docker-compose.yml` file, see [Docker Compose Structure]({{< relref "technical/docker-compose-structure" >}}).

## drive.sh Script

The `drive.sh` script provides consistent management across all services:

### Basic Commands

To see all available commands and their detailed usage, see [Container Management]({{< relref "../guides/general/container-management" >}}) in the Guides.

### Script Features

- **Automatic permission handling** - Works with or without `sudo`
- **Consistent interface** - The same commands work across all services
- **Simplified management** - Abstracts Docker Compose complexity

For detailed technical analysis of the `drive.sh` script, including how it manages permissions, see [drive.sh Script Analysis]({{< relref "technical/drive-script-analysis" >}}).

## Persistent Data

Each service's `persistent-data/` directory:
- Stored locally on your system
- Never shared or synced
- Contains service-specific data:
  - Blockchain nodes: chain data, keys, configuration

**Important:** `persistent-data/` permissions are automatically managed by the `drive.sh` script. For complete technical documentation on how Drive handles permissions, see [Permission Handling]({{< relref "technical/permission-handling" >}}).

## Service Types

### Blockchain Nodes

All blockchain nodes share the same Docker image but differ in:
- Network/chain configuration
- Binary download URLs
- Genesis files
- Port assignments

See [Service Catalog]({{< relref "catalog" >}}) for the complete list of all blockchain node services and their configurations.
