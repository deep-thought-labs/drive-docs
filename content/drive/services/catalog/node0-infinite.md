---
title: "Infinite Mainnet (node0-infinite)"
---

**Service Number:** 0  
**Service Directory:** `node0-infinite`  
**Service/Container Name:** `infinite`  
**Network:** Infinite Mainnet  
**Type:** Blockchain Node

## Description

Mainnet blockchain node for the Infinite network. Uses standard/default ports (no offset). This is the primary production network for the Infinite blockchain.

---

## Table of Contents

- [Port Configuration](#port-configuration)
- [Environment Variables](#environment-variables)
- [Essential Commands](#essential-commands)
- [Docker Compose Configuration](#docker-compose-configuration)
- [Firewall Configuration](#firewall-configuration)
- [Persistent Data](#persistent-data)
- [See Also](#see-also)

---

## Port Configuration

### Quick Reference

**Service Number:** 0  
**Port Offset:** +0 (standard ports)

| Port Type | Host Port | Container Port |
|-----------|-----------|---------------|
| P2P | 26656 | 26656 |
| RPC | 26657 | 26657 |
| gRPC | 9090 | 9090 |
| gRPC-Web | 9091 | 9091 |
| REST API | 1317 | 1317 |
| JSON-RPC HTTP | 8545 | 8545 |
| JSON-RPC WS | 8546 | 8546 |

### Port Calculation

{{< expand "Port Calculation Details" "↕" >}}
This service uses **Service Number 0**, so all ports use the default values:

- **P2P**: 26656 + (0 × 10) = **26656**
- **RPC**: 26657 + (0 × 10) = **26657**
- **gRPC**: 9090 + (0 × 10) = **9090**
- **gRPC-Web**: 9091 + (0 × 10) = **9091**
- **REST API**: 1317 + (0 × 10) = **1317**
- **JSON-RPC HTTP**: 8545 + (0 × 10) = **8545**
- **JSON-RPC WebSocket**: 8546 + (0 × 10) = **8546**

For detailed descriptions of each port type, see [Port Reference: Blockchain Nodes]({{< relref "../ports/blockchain-nodes" >}}).
{{< /expand >}}

### Required Ports

{{< expand "Required Ports Details" "↕" >}}
These ports must be configured for the service to function:

| Port Type | Host Port | Container Port | Description |
|-----------|-----------|---------------|-------------|
| **P2P** | 26656 | 26656 | Peer-to-peer network communication |
| **RPC** | 26657 | 26657 | Tendermint RPC API |
{{< /expand >}}

### Optional Ports

{{< expand "Optional Ports Details" "↕" >}}
These ports can be enabled if needed for specific use cases:

| Port Type | Host Port | Container Port | Description | When to Enable |
|-----------|-----------|---------------|-------------|----------------|
| **gRPC** | 9090 | 9090 | Cosmos SDK gRPC queries | Public API endpoint, wallet connections |
| **gRPC-Web** | 9091 | 9091 | gRPC-Web (browser) | Web applications, browser wallets |
| **REST API** | 1317 | 1317 | Cosmos SDK REST API | Legacy application compatibility |
| **JSON-RPC HTTP** | 8545 | 8545 | Ethereum JSON-RPC (HTTP) | MetaMask, Ethereum tools, dApps |
| **JSON-RPC WebSocket** | 8546 | 8546 | Ethereum JSON-RPC (WebSocket) | Real-time blockchain events |
| **Prometheus** | 26660 | 26660 | Prometheus metrics | Node monitoring |
| **EVM Metrics** | 6065 | 6065 | EVM Prometheus metrics | EVM performance monitoring |
| **Geth Metrics** | 8100 | 8100 | Geth-compatible metrics | Geth monitoring tools |
{{< /expand >}}

---

## Environment Variables

This service uses the following environment variables with the values shown below. For complete documentation of all available environment variables, see [Environment Variables: Blockchain Nodes]({{< relref "../environment/blockchain-nodes" >}}).

### Binary Configuration

This service uses the **default Infinite binary** (not an alternative binary). The binary is automatically downloaded from GitHub releases.

**Note:** For services using alternative binaries (like QOM), see the respective service documentation.

### Chain Identification

{{< expand "Chain Identification Variables" "↕" >}}
This service is configured with the following chain identification variables:

**NODE_CHAIN_ID**  
The chain ID for the Infinite mainnet network. This uniquely identifies the blockchain network.

```yaml
NODE_CHAIN_ID: "infinite_421018-1"
```

**NODE_EVM_CHAIN_ID**  
The EVM Chain ID for EIP-155 compatible replay protection.

This is separate from the Cosmos chain ID and is used for Ethereum-compatible transactions.

```yaml
NODE_EVM_CHAIN_ID: "421018"
```

**NODE_GENESIS_URL**  
URL to download the official genesis file during node initialization.

The genesis file contains the initial state of the blockchain.

```yaml
NODE_GENESIS_URL: "https://raw.githubusercontent.com/deep-thought-labs/infinite/migration/assets/pre-mainet-genesis.json"
```
{{< /expand >}}

### Network P2P Configuration

{{< expand "Network P2P Configuration Variables" "↕" >}}
This service uses the following P2P network configuration variables:

**NODE_P2P_SEEDS**  
Seed nodes for P2P discovery. These nodes help your node discover other peers in the network during initial connection.

Seed nodes are used for network discovery but are not persistent connections.

```yaml
NODE_P2P_SEEDS: "71a48afac2463a77bc5825d78dd83299174c4a6c@66.70.178.128:26656"
```

**NODE_PERSISTENT_PEERS**  
Persistent peer nodes maintain continuous connections, unlike seed nodes which are only used for discovery.

This service does not have a pre-configured value for this variable.

```yaml
# NODE_PERSISTENT_PEERS: ""  # No pre-configured value for this service
```

**NODE_P2P_EXTERNAL_ADDRESS**  
External address to advertise to peers for them to dial. Used when the node is behind NAT or firewall.

This service does not have a pre-configured value for this variable. If needed, configure it with your node's public IP address or domain name.

```yaml
# NODE_P2P_EXTERNAL_ADDRESS: ""  # No pre-configured value for this service
```
{{< /expand >}}

---

## Docker Compose Configuration

{{< expand "Minimal Configuration (Required Ports Only)" "↕" >}}
```yaml
services:
  infinite:
    image: deepthoughtlabs/infinite-drive:dev
    container_name: infinite
    restart: unless-stopped

    ports:
      - "26656:26656"  # P2P (required)
      - "26657:26657"  # RPC (required)
    
    volumes:
      - ./persistent-data:/home/ubuntu/.infinited

    environment:
      NODE_CHAIN_ID: "infinite_421018-1"
      NODE_EVM_CHAIN_ID: "421018"
      NODE_GENESIS_URL: "https://raw.githubusercontent.com/deep-thought-labs/infinite/migration/assets/pre-mainet-genesis.json"
      NODE_P2P_SEEDS: "71a48afac2463a77bc5825d78dd83299174c4a6c@66.70.178.128:26656"
```
{{< /expand >}}

{{< expand "Full Configuration (All Ports)" "↕" >}}
```yaml
services:
  infinite:
    image: deepthoughtlabs/infinite-drive:dev
    container_name: infinite
    restart: unless-stopped

    ports:
      # Required ports
      - "26656:26656"  # P2P
      - "26657:26657"  # RPC
      
      # Optional ports (uncomment if needed)
      - "9090:9090"    # gRPC
      - "9091:9091"    # gRPC-Web
      - "1317:1317"    # REST API
      - "8545:8545"    # JSON-RPC HTTP
      - "8546:8546"    # JSON-RPC WebSocket
      - "26660:26660"  # Prometheus
      - "6065:6065"    # EVM Metrics
      - "8100:8100"    # Geth Metrics
    
    volumes:
      - ./persistent-data:/home/ubuntu/.infinited

    environment:
      NODE_CHAIN_ID: "infinite_421018-1"
      NODE_EVM_CHAIN_ID: "421018"
      NODE_GENESIS_URL: "https://raw.githubusercontent.com/deep-thought-labs/infinite/migration/assets/pre-mainet-genesis.json"
      NODE_P2P_SEEDS: "71a48afac2463a77bc5825d78dd83299174c4a6c@66.70.178.128:26656"
      # NODE_PERSISTENT_PEERS: ""
      # NODE_P2P_EXTERNAL_ADDRESS: ""
```
{{< /expand >}}

---

## Essential Commands

This service is a blockchain node, which requires specialized commands for initialization, starting, stopping, and managing the node.

General container management commands (start, stop, restart, etc.) are described in the [Managing Services]({{< relref "../../quick-start/managing-services" >}}) section.

For detailed information about blockchain node-specific commands, including:
- How to initialize a blockchain node
- How to start and stop nodes
- Key management operations
- Accessing the graphical interface

See the [Blockchain Nodes Guides]({{< relref "../../guides/blockchain-nodes" >}}) section in the documentation.

---

## Firewall Configuration

**⚠️ Critical:** Before configuring any firewall rules for this service, you must first allow SSH (port 22) on your system. If you're connecting to a remote server via SSH and you enable the firewall without allowing SSH first, you will lose access to your server.

The complete firewall configuration process, including how to verify and allow SSH (port 22), is described in detail in the [Firewall Configuration Guide]({{< relref "../ports/firewall-configuration" >}}). The commands shown below are specific to this service with the correct port numbers for Infinite Mainnet, but please review the guide for the complete setup process.

### Required Ports

{{< tabs "firewall-required" >}}
{{< tab "Ubuntu/Linux" >}}
```bash
# P2P port (required for validators and peer connections)
sudo ufw allow 26656/tcp

# RPC port (optional, only if exposing RPC API)
sudo ufw allow 26657/tcp
```
{{< /tab >}}
{{< tab "macOS" >}}
**Recommended:** macOS typically allows incoming connections by default, so you may not need to configure anything. However, we recommend verifying your firewall settings.

**First Option - System Preferences (Recommended):**
Use the built-in graphical interface to configure firewall rules:
1. Open **System Preferences** (or **System Settings** on newer macOS versions)
2. Go to **Security & Privacy** > **Firewall**
3. Click the lock icon and enter your password to make changes
4. Click **Firewall Options...**
5. Add rules to allow incoming connections for the required ports (26656, 26657)

**Second Option - Command Line (Advanced):**
If you prefer command-line configuration, you can modify `/etc/pf.conf`:

```bash
# Edit /etc/pf.conf and add rules:
# pass in proto tcp from any to any port 26656  # P2P port
# pass in proto tcp from any to any port 26657  # RPC port

# Then reload the firewall:
sudo pfctl -f /etc/pf.conf
```
{{< /tab >}}
{{< tab "Windows" >}}
```powershell
# P2P port (required for validators and peer connections)
New-NetFirewallRule -DisplayName "Drive P2P" -Direction Inbound -LocalPort 26656 -Protocol TCP -Action Allow

# RPC port (optional, only if exposing RPC API)
New-NetFirewallRule -DisplayName "Drive RPC" -Direction Inbound -LocalPort 26657 -Protocol TCP -Action Allow
```
{{< /tab >}}
{{< /tabs >}}

### Optional Ports

{{< tabs "firewall-optional" >}}
{{< tab "Ubuntu/Linux" >}}
```bash
# gRPC (if exposing gRPC API)
sudo ufw allow 9090/tcp

# gRPC-Web (if exposing gRPC-Web API)
sudo ufw allow 9091/tcp

# REST API (if exposing REST API)
sudo ufw allow 1317/tcp

# JSON-RPC HTTP (if exposing Ethereum-compatible API)
sudo ufw allow 8545/tcp

# JSON-RPC WebSocket (if exposing WebSocket API)
sudo ufw allow 8546/tcp

# Prometheus (if exposing metrics)
sudo ufw allow 26660/tcp

# EVM Metrics (if exposing EVM metrics)
sudo ufw allow 6065/tcp

# Geth Metrics (if exposing Geth metrics)
sudo ufw allow 8100/tcp
```

**Note:** The `/tcp` protocol specification is optional in UFW. You can use either `sudo ufw allow 26656/tcp` or `sudo ufw allow 26656` - both work the same way.
{{< /tab >}}
{{< tab "macOS" >}}
**Recommended:** macOS typically allows incoming connections by default, so you may not need to configure anything. However, we recommend verifying your firewall settings.

**First Option - System Preferences (Recommended):**
Use the built-in graphical interface to configure firewall rules:
1. Open **System Preferences** (or **System Settings** on newer macOS versions)
2. Go to **Security & Privacy** > **Firewall**
3. Click the lock icon and enter your password to make changes
4. Click **Firewall Options...**
5. Add rules to allow incoming connections for the optional ports you want to expose (9090, 9091, 1317, 8545, 8546, 26660, 6065, 8100)

**Second Option - Command Line (Advanced):**
If you prefer command-line configuration, you can modify `/etc/pf.conf`:

```bash
# Edit /etc/pf.conf and add rules for each port you want to expose:
# pass in proto tcp from any to any port 9090  # gRPC
# pass in proto tcp from any to any port 9091  # gRPC-Web
# pass in proto tcp from any to any port 1317  # REST API
# pass in proto tcp from any to any port 8545  # JSON-RPC HTTP
# pass in proto tcp from any to any port 8546  # JSON-RPC WebSocket
# pass in proto tcp from any to any port 26660 # Prometheus
# pass in proto tcp from any to any port 6065  # EVM Metrics
# pass in proto tcp from any to any port 8100  # Geth Metrics

# Then reload the firewall:
sudo pfctl -f /etc/pf.conf
```
{{< /tab >}}
{{< tab "Windows" >}}
```powershell
# gRPC (if exposing gRPC API)
New-NetFirewallRule -DisplayName "Drive gRPC" -Direction Inbound -LocalPort 9090 -Protocol TCP -Action Allow

# gRPC-Web (if exposing gRPC-Web API)
New-NetFirewallRule -DisplayName "Drive gRPC-Web" -Direction Inbound -LocalPort 9091 -Protocol TCP -Action Allow

# REST API (if exposing REST API)
New-NetFirewallRule -DisplayName "Drive REST API" -Direction Inbound -LocalPort 1317 -Protocol TCP -Action Allow

# JSON-RPC HTTP (if exposing Ethereum-compatible API)
New-NetFirewallRule -DisplayName "Drive JSON-RPC HTTP" -Direction Inbound -LocalPort 8545 -Protocol TCP -Action Allow

# JSON-RPC WebSocket (if exposing WebSocket API)
New-NetFirewallRule -DisplayName "Drive JSON-RPC WS" -Direction Inbound -LocalPort 8546 -Protocol TCP -Action Allow

# Prometheus (if exposing metrics)
New-NetFirewallRule -DisplayName "Drive Prometheus" -Direction Inbound -LocalPort 26660 -Protocol TCP -Action Allow

# EVM Metrics (if exposing EVM metrics)
New-NetFirewallRule -DisplayName "Drive EVM Metrics" -Direction Inbound -LocalPort 6065 -Protocol TCP -Action Allow

# Geth Metrics (if exposing Geth metrics)
New-NetFirewallRule -DisplayName "Drive Geth Metrics" -Direction Inbound -LocalPort 8100 -Protocol TCP -Action Allow
```
{{< /tab >}}
{{< /tabs >}}

---

## Persistent Data

### Volume Mapping

- **Host Path:** `./persistent-data`
- **Container Path:** `/home/ubuntu/.infinited`

### Data Stored

The persistent data directory contains:
- **Chain data** - Blockchain state and history
- **Keys** - Validator and account keys (if configured)
- **Configuration files** - Node configuration files (`config.toml`, `app.toml`)
- **Genesis file** - Downloaded genesis file

**Important:** This data is stored locally on your system and is never shared or synced. It is exclusively yours.

---

## See Also

- [Port Strategy]({{< relref "../ports" >}}) - Port allocation strategy and general information
- [Port Reference: Blockchain Nodes]({{< relref "../ports/blockchain-nodes" >}}) - Detailed descriptions of all port types
- [Environment Variables: Blockchain Nodes]({{< relref "../environment/blockchain-nodes" >}}) - Complete environment variable reference
- [Service Structure]({{< relref "../service-structure" >}}) - Technical architecture and service structure
