---
title: "Managing Services"
---

# Managing Services

Drive services are organized in the `services/` directory. Each service is independent and can be managed separately.

## Basic Commands

All services use `drive.sh` in their directory:

```bash
cd services/<service-name>

# Start service (background)
./drive.sh up -d

# Stop service
./drive.sh stop

# Restart service
./drive.sh restart

# Access container shell
./drive.sh bash
```

## Service Types

Each service type has specific features. **Blockchain Nodes** include a graphical interface and specialized node management commands.

For detailed service structure, configuration, and advanced topics, see [Service Structure]({{< relref "/drive/services/service-structure" >}}).

## Next Steps

- [Blockchain Node Guides]({{< relref "/drive/guides/blockchain-nodes" >}})
- [Service Catalog]({{< relref "/drive/services/blockchain-nodes/catalog" >}})
