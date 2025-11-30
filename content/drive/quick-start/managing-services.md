---
title: "Managing Services"
---

# Managing Services

Drive organizes services in the `services/` directory. Each service is an independent container that you can start, stop, configure, and manage individually.

## Service Architecture

Each service in Drive has its own directory within `services/`. You have complete control over each service:

- **Start or stop** any service independently
- **Configure** service-specific settings
- **Access** the service container directly
- **Manage** persistent data for each service

All actions are performed directly on the selected service by navigating to its directory.

## Basic Service Commands

All services use the `drive.sh` script located in each service directory. This script provides consistent commands across all services.

### Starting a Service

Navigate to the service directory and start it in daemon mode (background):

```bash
cd services/<service-name>
./drive.sh up -d
```

The `-d` flag runs the service in daemon mode, keeping it running in the background.

### Managing a Running Service

Once a service is running, you can use these commands:

```bash
# Stop the service
./drive.sh stop

# Restart the service
./drive.sh restart

# Start the service (if stopped)
./drive.sh start

# Access the container shell
./drive.sh bash
```

These commands work the same way for all services in Drive.

## Service-Specific Features

While all services share the basic commands above, each service type has additional features:

- **Blockchain Nodes** - Include a graphical interface and specialized node management commands
- **Nginx** - Web server configuration and virtual host management
- **Other Services** - Each service type has its own specific capabilities

For detailed instructions on specific service types, see the [Service Guides]({{< relref "/drive/services" >}}).

## Next Steps

- Learn about [Blockchain Node operations]({{< relref "/drive/guides/blockchain-nodes" >}})
- Explore [Nginx configuration]({{< relref "/drive/services/nginx" >}})
- Review the [complete service catalog]({{< relref "/drive/services/blockchain-nodes/catalog" >}})

