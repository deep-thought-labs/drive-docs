---
title: "Variables de Entorno: Nodos Blockchain"
---

Complete reference for all environment variables that can be configured in `docker-compose.yml` files for blockchain node services.

## Tabla de Contenidos

- [Identificación de Cadena](#chain-identification)
- [Configuración de Red P2P](#network-p2p-configuration)
- [Alternative Configuración del Binario](#alternative-binary-configuration)
- [Conditional Argument Flags](#conditional-argument-flags)
- [Default Configuración del Binario](#default-binary-configuration)

---

## Identificación de Cadena

### `NODE_CHAIN_ID`

**Required:** Yes  
**Tipo:** String  
**Default:** `infinite_421018-1`  
**Descripción:** El ID de cadena para la red blockchain.

**Examples:**
```yaml
NODE_CHAIN_ID: "infinite_421018-1"      # Infinite mainnet
NODE_CHAIN_ID: "infinite_421018001-1"   # Infinite testnet
NODE_CHAIN_ID: "qom_766-1"              # QOM network
```

---

### `NODE_EVM_CHAIN_ID`

**Required:** Yes  
**Tipo:** String (numeric)  
**Default:** `421018`  
**Descripción:** El ID de cadena EVM para protección contra replay compatible con EIP-155. Esto es independiente del ID de cadena de Cosmos.

**Examples:**
```yaml
NODE_EVM_CHAIN_ID: "421018"      # Infinite mainnet
NODE_EVM_CHAIN_ID: "421018001"   # Infinite testnet
NODE_EVM_CHAIN_ID: "766"         # QOM network
```

**Note:** This value is only used if `NODE_FLAG_EVM_CHAIN_ID_ENABLED` is `true`. See [Conditional Argument Flags](#conditional-argument-flags).

---

### `NODE_GENESIS_URL`

**Required:** Yes  
**Tipo:** URL (String)  
**Default:** `https://raw.githubusercontent.com/deep-thought-labs/infinite/migration/config/genesis/assets/pre-mainet-genesis.json`  
**Descripción:** URL para descargar el archivo genesis oficial durante la inicialización del nodo.

**Examples:**
```yaml
NODE_GENESIS_URL: "https://raw.githubusercontent.com/deep-thought-labs/infinite/migration/config/genesis/assets/pre-mainet-genesis.json"
NODE_GENESIS_URL: "https://raw.githubusercontent.com/deep-thought-labs/babelfish-vm/main/resources/genesis.json"
```

---

## Configuración de Red P2P

### `NODE_P2P_SEEDS`

**Required:** No (optional)  
**Tipo:** String (comma-separated list)  
**Default:** Empty  
**Descripción:** Lista separada por comas de nodos semilla para descubrimiento P2P. Formato: `id@host:port`

**Format:**
- Single seed: `id@ip:port` or `id@domain.com:port`
- Multiple seeds: `id1@ip1:port1,id2@domain.com:port2,id3@ip3:port3`

**Examples:**
```yaml
# Single seed node
NODE_P2P_SEEDS: "88ec87026e7b61eceeca0d74cf47a24cea36642b@66.70.178.128:26666"

# Multiple seed nodes
NODE_P2P_SEEDS: "id1@seed1.example.com:26656,id2@seed2.example.com:26656,id3@seed3.example.com:26656"
```

**Note:** Seed nodes are used for initial network discovery. They are not persistent connections.

---

### `NODE_PERSISTENT_PEERS`

**Required:** No (optional)  
**Tipo:** String (comma-separated list)  
**Default:** Empty  
**Descripción:** Comma-separated list of persistent peer nodes. Format: `id@host:port`

**Format:** Same as `NODE_P2P_SEEDS`

**Examples:**
```yaml
NODE_PERSISTENT_PEERS: "id1@peer1.example.com:26656,id2@peer2.example.com:26656"
```

**Note:** Persistent peers maintain continuous connections, unlike seed nodes which are only used for discovery.

---

### `NODE_P2P_EXTERNAL_ADDRESS`

**Required:** No (optional)  
**Tipo:** String (IP:port or domain:port)  
**Default:** Empty  
**Descripción:** Dirección externa para anunciar a los pares para que se conecten. Se usa cuando el nodo está detrás de NAT o firewall.

**Format:** `ip:port` or `domain.com:port`

**Examples:**
```yaml
# IP address
NODE_P2P_EXTERNAL_ADDRESS: "159.89.10.97:26656"

# Domain name
NODE_P2P_EXTERNAL_ADDRESS: "node.example.com:26656"
```

**Note:** If empty, the node will use the same port as the listen address and introspect to figure out the address.

---

## Alternative Configuración del Binario

These variables are used when you want to use a different blockchain binary instead of the default Infinite binary.

### `NODE_ALT_BINARY_URL_AMD64`

**Required:** Yes (if using alternative binary)  
**Tipo:** URL (String)  
**Default:** Empty  
**Descripción:** URL to download the alternative binary for AMD64/x86_64 architecture.

**Examples:**
```yaml
NODE_ALT_BINARY_URL_AMD64: "https://github.com/WizardLatino/test-qom-node/releases/download/v1.0.1/qomd-linux-amd64"
```

**Note:** Must be provided if using an alternative binary. The binary will be downloaded at container startup.

---

### `NODE_ALT_BINARY_URL_ARM64`

**Required:** No (optional, if alternative binary supports ARM64)  
**Tipo:** URL (String)  
**Default:** Empty  
**Descripción:** URL to download the alternative binary for ARM64/aarch64 architecture.

**Examples:**
```yaml
NODE_ALT_BINARY_URL_ARM64: "https://github.com/example/blockchain/releases/download/v1.0.0/binary-linux-arm64"
```

**Note:** Leave empty or comment out if the alternative binary does not support ARM64.

---

### `NODE_ALT_BINARY_NAME`

**Required:** Yes (if using alternative binary)  
**Tipo:** String  
**Default:** Empty  
**Descripción:** Name of the alternative binary executable.

**Examples:**
```yaml
NODE_ALT_BINARY_NAME: "qomd"
NODE_ALT_BINARY_NAME: "custom-blockchain"
```

**Note:** This is the name of the binary file (without path). It will be installed in `/home/ubuntu/bin/`.

---

### `NODE_ALT_HOME`

**Required:** No (optional)  
**Tipo:** Path (String)  
**Default:** `/home/ubuntu/.${NODE_ALT_BINARY_NAME}`  
**Descripción:** Custom home directory for the alternative blockchain node.

**Examples:**
```yaml
NODE_ALT_HOME: "/home/ubuntu/.qomd"
NODE_ALT_HOME: "/home/ubuntu/.custom-blockchain"
```

**Note:** If not specified, defaults to `/home/ubuntu/.${NODE_ALT_BINARY_NAME}`.

---

## Default Configuración del Binario

These variables are used when using the default Infinite binary (not an alternative binary).

### `NODE_BINARY_URL_AMD64`

**Required:** No (optional)  
**Tipo:** URL (String)  
**Default:** Auto (GitHub releases)  
**Descripción:** Custom URL to download the default Infinite binary for AMD64/x86_64 architecture.

**Examples:**
```yaml
NODE_BINARY_URL_AMD64: "https://github.com/deep-thought-labs/infinite/releases/download/v1.0.0/infinite_Linux_x86_64.tar.gz"
```

**Note:** If not specified, the system will automatically download the latest version desde GitHub releases.

---

### `NODE_BINARY_URL_ARM64`

**Required:** No (optional)  
**Tipo:** URL (String)  
**Default:** Auto (GitHub releases)  
**Descripción:** Custom URL to download the default Infinite binary for ARM64/aarch64 architecture.

**Examples:**
```yaml
NODE_BINARY_URL_ARM64: "https://github.com/deep-thought-labs/infinite/releases/download/v1.0.0/infinite_Linux_ARM64.tar.gz"
```

**Note:** If not specified, the system will automatically download the latest version desde GitHub releases.

---

### `NODE_BINARY_VERSION`

**Required:** No (optional)  
**Tipo:** String  
**Default:** `latest`  
**Descripción:** Version of the default Infinite binary to download.

**Examples:**
```yaml
NODE_BINARY_VERSION: "latest"        # Latest release (default)
NODE_BINARY_VERSION: "v1.0.0"        # Specific version
NODE_BINARY_VERSION: "v1.2.3"        # Another specific version
```

**Note:** Only used when downloading desde GitHub releases. If `NODE_BINARY_URL_AMD64` or `NODE_BINARY_URL_ARM64` are specified, this is ignored.

---

## Conditional Argument Flags

These flags control whether optional arguments are included in the node start command. Some arguments are only supported by certain binaries.

### `NODE_FLAG_EVM_CHAIN_ID_ENABLED`

**Required:** No (optional)  
**Tipo:** Boolean or `auto`  
**Default:** `auto`  
**Descripción:** Controls whether the `--evm.evm-chain-id` argument is included in the start command.

**Values:**
- `true` - Always include `--evm.evm-chain-id` argument (if `NODE_EVM_CHAIN_ID` is set)
- `false` - Never include `--evm.evm-chain-id` argument
- `auto` - Auto-detect based on binary name (default)

**Auto-detection logic:**
- If binary name is `infinited` or starts with `infinite*` → `true`
- If binary name is anything else (e.g., `qomd`) → `false`

**Examples:**
```yaml
# Recommended: Omit the variable entirely (auto-detection)
# The system will automatically detect based on binary name:
# - infinited or infinite* → true (enabled)
# - Other binaries (qomd, etc.) → false (disabled)

# Or explicitly set to auto (same as omitting)
NODE_FLAG_EVM_CHAIN_ID_ENABLED: "auto"

# Force enable (only if you need to override auto-detection)
NODE_FLAG_EVM_CHAIN_ID_ENABLED: "true"

# Force disable (only if you need to override auto-detection)
NODE_FLAG_EVM_CHAIN_ID_ENABLED: "false"
```

**Note:** 
- **This variable is optional** - if not specified, the system automatically detects the correct value based on the binary name
- **Recommended approach:** Omit this variable from `docker-compose.yml` to keep files clean and let the system auto-detect
- The `--evm.evm-chain-id` argument is only supported by `infinited` (Infinite blockchain)
- It is NOT supported by `qomd` (QOM blockchain) or other binaries
- Auto-detection: `infinited` or binaries starting with `infinite*` → `true`, all others → `false`
- Only set this variable if you need to override the auto-detection behavior

---

## Variable Naming Convention

All environment variables follow this pattern:
- `NODE_*` - Node configuration variables
- `NODE_ALT_*` - Alternative binary configuration
- `NODE_FLAG_*` - Conditional argument flags
- `NODE_P2P_*` - P2P network configuration

---

## Referencia Rápida

### Required Variables (Minimum)

```yaml
environment:
  NODE_CHAIN_ID: "your-chain-id"
  NODE_EVM_CHAIN_ID: "your-evm-chain-id"
  NODE_GENESIS_URL: "https://example.com/genesis.json"
```

### Using Alternative Binary

```yaml
environment:
  NODE_CHAIN_ID: "alternative-chain-id"
  NODE_EVM_CHAIN_ID: "alternative-evm-chain-id"
  NODE_GENESIS_URL: "https://example.com/genesis.json"
  NODE_ALT_BINARY_URL_AMD64: "https://example.com/binary-amd64"
  NODE_ALT_BINARY_NAME: "alternative-binary"
  NODE_ALT_HOME: "/home/ubuntu/.alternative"
  NODE_FLAG_EVM_CHAIN_ID_ENABLED: "false"  # If binary doesn't support it
```

### With P2P Configuración

```yaml
environment:
  NODE_CHAIN_ID: "your-chain-id"
  NODE_EVM_CHAIN_ID: "your-evm-chain-id"
  NODE_GENESIS_URL: "https://example.com/genesis.json"
  NODE_P2P_SEEDS: "id1@seed1.example.com:26656,id2@seed2.example.com:26656"
  NODE_PERSISTENT_PEERS: "id1@peer1.example.com:26656"
  NODE_P2P_EXTERNAL_ADDRESS: "node.example.com:26656"
```

---

## Ver También

- [Catálogo de Servicios]({{< relref "../catalog" >}}) - Configuraciones específicas de servicios con valores reales
- [Estrategia de Puertos]({{< relref "../ports" >}}) - Asignación y configuración de puertos
- [Estructura del Servicio]({{< relref "../service-structure" >}}) - Service architecture and configuration
