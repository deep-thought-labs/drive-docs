---
title: "Managing Services"
weight: 513
---

Drive services are organized in the `services/` directory. Each service is independent and can be managed separately.

## Basic Commands

All services use `drive.sh` in their directory:

```bash
cd services/<service-name>

# Start service (background)
./drive.sh up -d

# Show container status
./drive.sh ps

# Stop service
./drive.sh stop

# Stop and remove container
./drive.sh down

# Start (if stopped)
./drive.sh start      

# Restart service (if already running)
./drive.sh restart

# View container logs
./drive.sh logs

# Access container shell
./drive.sh bash
```

## Service Types

Each service type has specific features. **Blockchain Nodes** include a graphical interface and specialized node management commands.

For detailed service structure, configuration, and advanced topics, see [Service Structure]({{< relref "/drive/services/service-structure" >}}).

## Next Steps

- [Service Catalog]({{< relref "/drive/services/catalog" >}}) - All available services
- [Blockchain Node Guides]({{< relref "/drive/guides/blockchain-nodes" >}})
