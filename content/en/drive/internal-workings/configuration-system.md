---
title: "Internal Configuration System"
weight: 404
---

The Drive system uses a centralized configuration system based on environment variables and a shared configuration file (`node-config.sh`). This section documents how this configuration system works.

## Configuration System Architecture

### Central File: `node-config.sh`

All system scripts load configuration from a centralized file:

```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/node-config.sh"
```

**Location in container:**
```
/usr/local/bin/node-config.sh
```

**Purpose:**
- Define default values for all variables
- Load container environment variables
- Provide utility functions for configuration
- Validate configuration before use

## Configuration Variables

### Core Configuration

#### Node Identification

```bash
NODE_CHAIN_ID="${NODE_CHAIN_ID:-infinite_421018-1}"
NODE_EVM_CHAIN_ID="${NODE_EVM_CHAIN_ID:-421018}"
```

**Purpose:**
- `NODE_CHAIN_ID`: Blockchain chain identifier
- `NODE_EVM_CHAIN_ID`: Chain identifier for EVM compatibility

**Default values:**
- Chain ID: `infinite_421018-1`
- EVM Chain ID: `421018`

**Usage:**
- Passed as arguments to the `infinited` binary
- Used to build the process detection pattern
- Identify the specific blockchain network

#### Fixed Paths

```bash
NODE_HOME="/home/ubuntu/.infinited"
NODE_BINARY_PATH="/usr/local/bin/infinited"
NODE_LOG_FILE="/var/log/node/node.log"
NODE_CONTROL_DIR="/home/ubuntu/.node"
```

**Purpose:**
- `NODE_HOME`: Main node directory (configuration and data)
- `NODE_BINARY_PATH`: Path to the node executable binary
- `NODE_LOG_FILE`: File where node logs are written
- `NODE_CONTROL_DIR`: Directory for control files (PIDs, flags)

**Note:** These paths are fixed and cannot be changed via environment variables.

#### Genesis Configuration

```bash
NODE_GENESIS_URL="${NODE_GENESIS_URL:-https://raw.githubusercontent.com/deep-thought-labs/infinite/migration/config/genesis/assets/pre-mainet-genesis.json}"
```

**Purpose:**
- URL from where to download the official genesis file
- Used during node initialization

**Default value:**
- URL from the official Infinite repository

#### P2P Network Configuration

```bash
NODE_P2P_SEEDS="${NODE_P2P_SEEDS:-}"
NODE_PERSISTENT_PEERS="${NODE_PERSISTENT_PEERS:-}"
NODE_P2P_EXTERNAL_ADDRESS="${NODE_P2P_EXTERNAL_ADDRESS:-}"
```

**Purpose:**
- `NODE_P2P_SEEDS`: Seed nodes for initial peer discovery
- `NODE_PERSISTENT_PEERS`: Persistent peers for direct connection
- `NODE_P2P_EXTERNAL_ADDRESS`: External node address (format: `IP:port`)

**Format:**
- Seeds and peers: Comma-separated list of `ID@IP:port` addresses
- External address: `IP:port` or `domain:port`

**Example:**
```bash
NODE_P2P_SEEDS="abc123@1.2.3.4:26656,def456@5.6.7.8:26656"
NODE_PERSISTENT_PEERS="abc123@1.2.3.4:26656"
NODE_P2P_EXTERNAL_ADDRESS="example.com:26656"
```

#### Keyring Configuration

```bash
NODE_KEYRING_BACKEND="file"
```

**Purpose:**
- Defines the keyring backend (always `file` in this system)
- Cannot be changed, it's fixed

### Derived Paths

These paths are built from base paths:

```bash
NODE_GENESIS_FILE="${NODE_HOME}/config/genesis.json"
NODE_CONFIG_FILE="${NODE_HOME}/config/config.toml"
NODE_PID_FILE="${NODE_CONTROL_DIR}/node.pid"
NODE_SUPERVISOR_PID_FILE="${NODE_CONTROL_DIR}/supervisor.pid"
NODE_AUTO_START_FLAG="${NODE_CONTROL_DIR}/auto-start"
NODE_SUPERVISOR_LOG_FILE="${NODE_SUPERVISOR_LOG_FILE:-/var/log/node/supervisor.log}"
```

**Purpose:**
- Simplify references to important files
- Centralize path construction logic
- Facilitate future structure changes

### Process Detection Pattern

```bash
NODE_PROCESS_PATTERN="${NODE_BINARY_PATH} start.*--chain-id ${NODE_CHAIN_ID}"
```

**Purpose:**
- Pattern used by `pgrep` to identify the node process
- Allows multiple nodes on the same host (different chain-id)
- Avoids false positives with other processes

**Pattern example:**
```
/usr/local/bin/infinited start.*--chain-id infinite_421018-1
```

## Utility Functions

### `build_node_start_command()`

Builds the complete command to start the node with all necessary arguments.

**Implementation:**
```bash
build_node_start_command() {
    local cmd="${NODE_BINARY_PATH} start"
    
    # Required arguments
    cmd="${cmd} --home ${NODE_HOME}"
    cmd="${cmd} --chain-id ${NODE_CHAIN_ID}"
    cmd="${cmd} --evm.evm-chain-id ${NODE_EVM_CHAIN_ID}"
    
    # Optional arguments (only if defined)
    if [ -n "${NODE_P2P_SEEDS}" ]; then
        cmd="${cmd} --p2p.seeds \"${NODE_P2P_SEEDS}\""
    fi
    
    if [ -n "${NODE_PERSISTENT_PEERS}" ]; then
        cmd="${cmd} --p2p.persistent_peers \"${NODE_PERSISTENT_PEERS}\""
    fi
    
    if [ -n "${NODE_P2P_EXTERNAL_ADDRESS}" ]; then
        cmd="${cmd} --p2p.external_address \"${NODE_P2P_EXTERNAL_ADDRESS}\""
    fi
        
    echo "$cmd"
}
```

**Characteristics:**
- Builds the command dynamically based on configuration
- Correctly handles arguments with commas and special characters using quotes
- Only includes optional arguments if they're defined

**Usage:**
```bash
START_CMD=$(build_node_start_command)
eval ${START_CMD} > ${NODE_LOG_FILE} 2>&1
```

### `validate_node_config()`

Validates that required configuration is present and valid.

**Implementation:**
```bash
validate_node_config() {
    local errors=0
    
    if [ ! -f "${NODE_BINARY_PATH}" ]; then
        echo "Error: Binary not found at ${NODE_BINARY_PATH}" >&2
        errors=$((errors + 1))
    fi
    
    if [ -z "${NODE_CHAIN_ID}" ]; then
        echo "Error: NODE_CHAIN_ID is not set" >&2
        errors=$((errors + 1))
    fi
    
    if [ -z "${NODE_EVM_CHAIN_ID}" ]; then
        echo "Error: NODE_EVM_CHAIN_ID is not set" >&2
        errors=$((errors + 1))
    fi
    
    return $errors
}
```

**Validations:**
1. Verifies that the binary exists at the specified path
2. Verifies that `NODE_CHAIN_ID` is defined
3. Verifies that `NODE_EVM_CHAIN_ID` is defined

**Usage:**
```bash
if ! validate_node_config; then
    print_error "Invalid node configuration"
    exit 1
fi
```

## Environment Variable Loading

### Precedence Order

1. **Container environment variables** (highest priority)
2. **Default values in `node-config.sh`** (if variable is not defined)

**Syntax:**
```bash
VARIABLE="${VARIABLE:-default_value}"
```

**Example:**
```bash
NODE_CHAIN_ID="${NODE_CHAIN_ID:-infinite_421018-1}"
```

If `NODE_CHAIN_ID` is defined in the environment, that value is used. If not, `infinite_421018-1` is used.

### Environment Variables in Docker

Environment variables can be defined in:

1. **`docker-compose.yml`:**
   ```yaml
   environment:
     - NODE_CHAIN_ID=infinite_421018-1
     - NODE_P2P_SEEDS=abc123@1.2.3.4:26656
   ```

2. **`.env` file:**
   ```
   NODE_CHAIN_ID=infinite_421018-1
   NODE_P2P_SEEDS=abc123@1.2.3.4:26656
   ```

3. **Command line:**
   ```bash
   docker compose run -e NODE_CHAIN_ID=test-chain infinite-drive node-start
   ```

## Variable Export

All variables are exported so they're available in child scripts:

```bash
export NODE_CHAIN_ID="${NODE_CHAIN_ID:-infinite_421018-1}"
export NODE_HOME="/home/ubuntu/.infinited"
# ... etc
```

**Purpose:**
- Make variables available to scripts executed from other scripts
- Allow functions to access variables

## Usage in Scripts

### Standard Loading

All scripts load configuration in the same way:

```bash
#!/bin/bash

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load centralized configuration
source "${SCRIPT_DIR}/node-config.sh"

# Load styles (if necessary)
source "${SCRIPT_DIR}/styles.sh"
```

**Note:** `node-config.sh` must be in the same directory as the scripts, or in `/usr/local/bin/` where they're installed.

## Per-Service Configuration

Each blockchain node service can have its own configuration via environment variables in `docker-compose.yml`:

```yaml
services:
  node0-infinite:
    environment:
      - NODE_CHAIN_ID=infinite_421018-1
      - NODE_EVM_CHAIN_ID=421018
      - NODE_P2P_SEEDS=abc123@1.2.3.4:26656
      - NODE_GENESIS_URL=https://...
```

This allows multiple nodes with different configurations to coexist on the same system.

## Runtime Validation

Scripts validate configuration before performing critical operations:

```bash
# In node-start.sh
if ! validate_node_config; then
    print_error "Invalid node configuration. Please check environment variables."
    exit 1
fi
```

**Advantages:**
- Detects configuration problems early
- Provides clear error messages
- Prevents execution with invalid configuration

## Variable Summary

### Required Variables (with default values)
- `NODE_CHAIN_ID` - Chain ID
- `NODE_EVM_CHAIN_ID` - EVM chain ID

### Optional Variables
- `NODE_P2P_SEEDS` - Seed nodes
- `NODE_PERSISTENT_PEERS` - Persistent peers
- `NODE_P2P_EXTERNAL_ADDRESS` - External address
- `NODE_GENESIS_URL` - Genesis URL
- `NODE_SUPERVISOR_LOG_FILE` - Supervisor log path

### Fixed Variables (not configurable)
- `NODE_HOME` - Node home directory
- `NODE_BINARY_PATH` - Binary path
- `NODE_LOG_FILE` - Log file
- `NODE_CONTROL_DIR` - Control directory
- `NODE_KEYRING_BACKEND` - Keyring backend

## See Also

- [Internal Directory Structure]({{< relref "directory-structure" >}}) - Where configuration files are stored
- [Container Architecture]({{< relref "container-architecture" >}}) - How `node-config.sh` is installed
- [Container Internal Scripts]({{< relref "internal-scripts" >}}) - How scripts use configuration

