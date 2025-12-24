---
title: "Docker Compose Structure"
weight: 5361
---

> [!WARNING]
> **⚠️ Documentation Under Construction**
>
> This document is under construction and contains technical analysis in development. It is being used by developers to identify the best solution to the permission problem between the host system and Docker containers.
>
> **Do not take this document as a usage guide yet.** This is a technical analysis that may change significantly while the final solution is being developed.

Complete technical analysis of the `docker-compose.yml` file used by Drive services.

## File Location

Each service has its own `docker-compose.yml` file in its directory:

```
services/
└── <service-name>/
    └── docker-compose.yml
```

## General Structure

The `docker-compose.yml` file defines a Docker Compose service with the following structure:

```yaml
services:
  <service-name>:
    # Container configuration
    image: <docker-image>
    container_name: <container-name>
    restart: unless-stopped
    
    # Network configuration
    ports:
      - "<host-port>:<container-port>"
    
    # Volume configuration
    volumes:
      - ./persistent-data:/home/ubuntu/.infinited
    
    # Environment variables
    environment:
      VARIABLE_NAME: "value"
```

## Main Components

### Container Configuration

#### `image`
- **Purpose:** Specifies the Docker image to use
- **Example:** `deepthoughtlabs/infinite-drive:latest`
- **Note:** Image version is defined in the image itself

#### `container_name`
- **Purpose:** Defines the container name
- **Example:** `infinite`
- **Note:** Must be unique on the host system

#### `restart`
- **Purpose:** Automatic restart policy
- **Value:** `unless-stopped`
- **Behavior:** Container will restart automatically unless manually stopped

### Container User Configuration

**⚠️ Important:** The `docker-compose.yml` file **does not explicitly specify** the user that runs the container. This means:

- The container uses the default user defined in the Docker image
- According to the `drive.sh` script, the container runs as user `ubuntu` with **UID 1000**
- This configuration is defined in the image's Dockerfile, not in `docker-compose.yml`

**Implication:** To change the container's UID, it would be necessary to modify the image's Dockerfile or add a `user` configuration in `docker-compose.yml`.

### Port Configuration

```yaml
ports:
  - "<host-port>:<container-port>"
```

- **Format:** `"HOST_PORT:CONTAINER_PORT"`
- **HOST_PORT:** Port on the host system (may vary based on service number)
- **CONTAINER_PORT:** Port inside the container (fixed, defined by the application)
- **Example:** `"26656:26656"` - P2P port mapped from host to container

For more information on port allocation strategy, see [Port Strategy]({{< relref "../ports" >}}).

### Volume Configuration

```yaml
volumes:
  - ./persistent-data:/home/ubuntu/.infinited
```

- **Format:** `"<host-path>:<container-path>"`
- **Type:** Bind mount (direct mount of host filesystem)
- **HOST_PATH:** `./persistent-data` - Relative path to service directory
- **CONTAINER_PATH:** `/home/ubuntu/.infinited` - Path inside container

**Important characteristics:**
- Bind mounts preserve numeric UIDs/GIDs from the filesystem
- Docker does not translate usernames, only uses numeric UIDs
- This is critical for permission management (see [Permission Handling]({{< relref "permission-handling" >}}))

### Environment Variables

```yaml
environment:
  VARIABLE_NAME: "value"
```

- **Purpose:** Configure service behavior
- **Scope:** Available inside container during execution
- **Common types:**
  - Chain identification (`NODE_CHAIN_ID`, `NODE_EVM_CHAIN_ID`)
  - Network configuration (`NODE_P2P_SEEDS`, `NODE_PERSISTENT_PEERS`)
  - Resource URLs (`NODE_GENESIS_URL`)

For complete environment variable documentation, see [Environment Variables]({{< relref "../environment" >}}).

## Current Configuration Analysis

### Container User

The current `docker-compose.yml` **does not specify** an explicit user, which means:

1. **Default user:** Container runs as the user defined in the Dockerfile
2. **Expected UID:** According to `drive.sh`, container runs as UID 1000 (user `ubuntu`)
3. **Implication:** If the Dockerfile changes the UID, the permission logic in `drive.sh` would need to be updated

### Permission Management

The `docker-compose.yml` **does not manage permissions** directly. Permission management is performed in:

- **`drive.sh` script:** Configures `persistent-data` permissions before executing Docker Compose
- **Docker bind mounts:** Preserve host filesystem permissions

For technical details on how permissions are handled, see [Permission Handling]({{< relref "permission-handling" >}}).

## Limitations and Considerations

### Current Limitations

1. **Fixed user:** Container always runs as UID 1000 (defined in Dockerfile)
2. **No user configuration in Compose:** No way to change UID from `docker-compose.yml` without modifying the image
3. **Permissions depend on host:** `persistent-data` permissions depend on host user and logic in `drive.sh`

### Considerations for Future Improvements

If support for different UIDs is needed:

1. **Option 1:** Add `user` configuration in `docker-compose.yml`:
   ```yaml
   user: "${UID:-1000}:${GID:-1000}"
   ```
   Would require passing UID/GID environment variables from host.

2. **Option 2:** Modify Dockerfile to accept UID/GID as build arguments.

3. **Option 3:** Use an entrypoint script that adjusts UID when starting the container.

## See Also

- [drive.sh Script Analysis]({{< relref "drive-script-analysis" >}}) - How the script manages permissions
- [Permission Handling]({{< relref "permission-handling" >}}) - Complete technical documentation on permissions
- [Service Structure]({{< relref "../service-structure" >}}) - Overview of service architecture

