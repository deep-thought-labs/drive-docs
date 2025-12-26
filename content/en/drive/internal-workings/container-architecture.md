---
title: "Container Architecture"
weight: 406
---

The Drive Docker container is built from a Dockerfile that defines the base image, installs dependencies, downloads the node binary, and configures the environment. This section documents the complete container architecture.

## Base Image

### Base Image

```dockerfile
FROM ubuntu:24.04
```

**Characteristics:**
- Based on Ubuntu 24.04 LTS
- Minimal and lightweight image
- Support for multiple architectures (amd64, arm64)

## Dependency Installation

### System Dependencies

```dockerfile
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    ca-certificates \
    tar \
    libc6 \
    libgcc-s1 \
    procps \
    net-tools \
    jq \
    dialog \
    bc \
    util-linux \
    && rm -rf /var/lib/apt/lists/*
```

**Purpose of each dependency:**

- **wget:** Download the node binary from GitHub
- **curl:** Make HTTP requests to the GitHub API
- **ca-certificates:** SSL/TLS certificates for secure connections
- **tar:** Extract the compressed binary file
- **libc6, libgcc-s1:** C libraries required by the binary
- **procps:** Process management tools (`pgrep`, `ps`, etc.)
- **net-tools:** Network tools (`netstat`, etc.)
- **jq:** Process JSON (to parse GitHub API responses)
- **dialog:** Terminal graphical interface (TUI) for `node-ui`
- **bc:** Calculator for mathematical operations
- **util-linux:** System utilities (`setsid`, etc.)

**Optimization:**
- `rm -rf /var/lib/apt/lists/*` - Cleans apt cache to reduce image size

## Multi-Architecture

### Build Arguments

```dockerfile
ARG TARGETARCH
ARG TARGETPLATFORM
```

**Purpose:**
- `TARGETARCH`: Target architecture (amd64, arm64)
- `TARGETPLATFORM`: Complete platform (linux/amd64, linux/arm64)

**Usage:**
- Automatically set by Docker Buildx
- Allow building images for multiple architectures
- Used to select the correct binary

## Binary Download

### Download Process

The Dockerfile automatically downloads the latest binary version from GitHub:

```dockerfile
# 1. Get latest version from GitHub
LATEST_VERSION=$(curl -s https://api.github.com/repos/deep-thought-labs/infinite/releases/latest | jq -r '.tag_name')

# 2. Build binary URL based on architecture
if [ "$TARGETARCH" = "arm64" ]; then
    FINAL_BINARY_URL="https://github.com/deep-thought-labs/infinite/releases/download/${LATEST_VERSION}/infinite_Linux_ARM64.tar.gz"
elif [ "$TARGETARCH" = "amd64" ]; then
    FINAL_BINARY_URL="https://github.com/deep-thought-labs/infinite/releases/download/${LATEST_VERSION}/infinite_Linux_x86_64.tar.gz"
fi

# 3. Download, extract, and install
wget --tries=3 --timeout=30 --progress=bar:force:noscroll \
    -O /tmp/infinite.tar.gz "$FINAL_BINARY_URL"
tar -xzf /tmp/infinite.tar.gz -C /tmp/extract
BINARY_PATH=$(find /tmp/extract -type f \( -name "infinited" -o -name "infinite" -o -name "infinite*" \) -executable 2>/dev/null | head -n 1)
mv "${BINARY_PATH}" /usr/local/bin/infinited
chmod +x /usr/local/bin/infinited
```

**Characteristics:**
- Automatic download of latest version
- Support for multiple architectures
- Downloaded file validation
- Automatic binary search in extracted file
- Installation in `/usr/local/bin/infinited`

### Validations

The process includes multiple validations:

1. **Version verification:**
   ```bash
   if [ -z "$LATEST_VERSION" ] || [ "$LATEST_VERSION" = "null" ]; then
       echo "Error: Could not fetch latest version from GitHub"
       exit 1
   fi
   ```

2. **Architecture verification:**
   ```bash
   if [ "$TARGETARCH" != "arm64" ] && [ "$TARGETARCH" != "amd64" ]; then
       echo "Error: Unsupported architecture: ${TARGETARCH}"
       exit 1
   fi
   ```

3. **Download verification:**
   ```bash
   test -f /tmp/infinite.tar.gz || (echo "Error: Download failed" && exit 1)
   test -s /tmp/infinite.tar.gz || (echo "Error: File is empty" && exit 1)
   ```

4. **Extraction verification:**
   ```bash
   tar -tzf /tmp/infinite.tar.gz > /dev/null 2>&1 || (echo "Error: Not a valid tar.gz" && exit 1)
   ```

5. **Binary verification:**
   ```bash
   if [ -z "${BINARY_PATH}" ]; then
       echo "Error: Binary not found"
       exit 1
   fi
   ```

## Directory Configuration

### Directory Creation

```dockerfile
RUN mkdir -p /home/ubuntu/.infinited /var/log/node /home/ubuntu/.node && \
    chown -R 1000:1000 /home/ubuntu /var/log/node
```

**Directories created:**

1. **`/home/ubuntu/.infinited`** - Node home directory (configuration and data)
2. **`/var/log/node`** - System logs directory
3. **`/home/ubuntu/.node`** - Control directory (PIDs, flags)

**Permissions:**
- Owner: `ubuntu` (UID 1000)
- Group: `ubuntu` (GID 1000)
- Permissions: `755` (rwxr-xr-x)

## Script Installation

### Script Copying

```dockerfile
COPY scripts/ /tmp/scripts/
RUN chmod +x /tmp/scripts/*.sh && \
    mv /tmp/scripts/styles.sh /usr/local/bin/styles.sh && \
    mv /tmp/scripts/node-config.sh /usr/local/bin/node-config.sh && \
    mv /tmp/scripts/node-init.sh /usr/local/bin/node-init && \
    mv /tmp/scripts/node-keys.sh /usr/local/bin/node-keys && \
    mv /tmp/scripts/node-start.sh /usr/local/bin/node-start && \
    mv /tmp/scripts/node-stop.sh /usr/local/bin/node-stop && \
    mv /tmp/scripts/node-logs.sh /usr/local/bin/node-logs && \
    mv /tmp/scripts/node-update-genesis.sh /usr/local/bin/node-update-genesis && \
    mv /tmp/scripts/node-network-diagnosis.sh /usr/local/bin/node-network-diagnosis && \
    mv /tmp/scripts/node-process-status.sh /usr/local/bin/node-process-status && \
    mv /tmp/scripts/node-help.sh /usr/local/bin/node-help && \
    mv /tmp/scripts/node-ui.sh /usr/local/bin/node-ui && \
    mv /tmp/scripts/node-supervisor.sh /usr/local/bin/node-supervisor && \
    mv /tmp/scripts/node-auto-start.sh /usr/local/bin/node-auto-start && \
    mv /tmp/scripts/node-validate-genesis.sh /usr/local/bin/node-validate-genesis && \
    mv /tmp/scripts/node-clean-data.sh /usr/local/bin/node-clean-data && \
    mv /tmp/scripts/container-info.sh /usr/local/bin/container-info.sh && \
    mv /tmp/scripts/dialog-theme.sh /usr/local/bin/dialog-theme.sh && \
    chown -R 1000:1000 /usr/local/bin/node-* /usr/local/bin/styles.sh /usr/local/bin/node-config.sh /usr/local/bin/container-info.sh /usr/local/bin/dialog-theme.sh && \
    rm -rf /tmp/scripts
```

**Process:**

1. **Copy:** All scripts are copied to `/tmp/scripts/`
2. **Permissions:** Made executable with `chmod +x`
3. **Installation:** Moved to `/usr/local/bin/` (without `.sh` extension for most)
4. **Ownership:** Changed ownership to `ubuntu:ubuntu`
5. **Cleanup:** Temporary directory is removed

**Installed scripts:**

- Utility scripts: `styles.sh`, `node-config.sh`, `container-info.sh`, `dialog-theme.sh`
- Main scripts: `node-init`, `node-start`, `node-stop`, `node-logs`, `node-keys`
- System scripts: `node-supervisor`, `node-auto-start`
- Management scripts: `node-clean-data`, `node-process-status`, `node-network-diagnosis`
- UI scripts: `node-ui`
- Help scripts: `node-help`, `node-update-genesis`, `node-validate-genesis`

## User Configuration

### Default User

```dockerfile
USER 1000:1000
```

**Characteristics:**
- User: `ubuntu` (UID 1000)
- Group: `ubuntu` (GID 1000)
- All processes run as this user
- Avoids permission problems with mounted volumes

### Working Directory

```dockerfile
WORKDIR /home/ubuntu
```

**Purpose:**
- Sets the default working directory
- Commands execute from this directory
- Facilitates use of relative paths

## Entrypoint and CMD

### Startup Command

```dockerfile
CMD ["/bin/bash", "-c", "/usr/local/bin/node-auto-start > /dev/null 2>&1; sleep infinity"]
```

**Explanation:**

1. **`/usr/local/bin/node-auto-start`** - Executes the auto-start script
   - Checks if the node should start automatically
   - Starts the node if the auto-start flag exists
   - Redirects output to `/dev/null` to avoid noise in container logs

2. **`sleep infinity`** - Keeps the container running
   - The container must remain active for the node to function
   - `sleep infinity` is a process that never terminates
   - Allows the container to continue running indefinitely

**Complete flow:**

```
Container starts
    ↓
Executes node-auto-start
    ↓
Does auto-start flag exist?
    ├─ Yes → Start node
    └─ No → Do nothing
    ↓
sleep infinity (keeps container alive)
```

## Final Container Structure

### Filesystem

```
/
├── usr/
│   └── local/
│       └── bin/
│           ├── infinited              # Node binary
│           ├── node-init              # Management scripts
│           ├── node-start
│           ├── node-stop
│           ├── node-logs
│           ├── node-keys
│           ├── node-supervisor
│           ├── node-auto-start
│           ├── node-config.sh          # Configuration
│           ├── styles.sh               # Styles
│           └── ...                     # Other scripts
│
├── home/
│   └── ubuntu/
│       ├── .infinited/                 # Node data
│       └── .node/                      # Node control
│
└── var/
    └── log/
        └── node/                       # System logs
```

## Environment Variables

Environment variables can be passed to the container via:

1. **`docker-compose.yml`:**
   ```yaml
   environment:
     - NODE_CHAIN_ID=infinite_421018-1
     - NODE_P2P_SEEDS=...
   ```

2. **`.env` file:**
   ```
   NODE_CHAIN_ID=infinite_421018-1
   ```

3. **Command line:**
   ```bash
   docker compose run -e NODE_CHAIN_ID=test infinite-drive node-start
   ```

## Persistent Volumes

Data directories are mapped to persistent volumes:

```yaml
volumes:
  - ./persistent-data/.infinited:/home/ubuntu/.infinited
  - ./persistent-data/.node:/home/ubuntu/.node
  - ./persistent-data/logs:/var/log/node
```

**Advantages:**
- Data persists between container restarts
- Accessible from the host
- Not lost when recreating the container

## Optimizations

### Size Reduction

1. **apt cache cleanup:** `rm -rf /var/lib/apt/lists/*`
2. **Temporary file removal:** `rm -rf /tmp/scripts`
3. **Minimal base image:** Ubuntu without unnecessary packages

### Multi-Stage Build

Although not currently used, a multi-stage build could be implemented to further reduce the final image size.

## See Also

- [Internal Directory Structure]({{< relref "directory-structure" >}}) - Where data is stored
- [Internal Configuration System]({{< relref "configuration-system" >}}) - How the container is configured
- [Container Internal Scripts]({{< relref "internal-scripts" >}}) - What scripts are installed

