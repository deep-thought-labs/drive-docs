---
title: "QOM Network (node3-qom)"
---

**Service Number:** 3  
**Service Directory:** `node3-qom`  
**Service/Container Name:** `qom`  
**Network:** QOM Network  
**Type:** Blockchain Node

## Description

QOM Network blockchain node. Uses alternative binary configuration (qomd). All ports have a +30 offset from default ports. This is a different blockchain project that uses the same Drive infrastructure.

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

**Service Number:** 3  
**Port Offset:** +30

| Port Type | Host Port | Container Port |
|-----------|-----------|---------------|
| P2P | 26686 | 26656 |
| RPC | 26687 | 26657 |
| gRPC | 9120 | 9090 |
| gRPC-Web | 9121 | 9091 |
| REST API | 1347 | 1317 |
| JSON-RPC HTTP | 8575 | 8545 |
| JSON-RPC WS | 8576 | 8546 |

### Port Calculation

{{< expand "Port Calculation Details" "↕" >}}
This service uses **Service Number 3**, so all ports have a +30 offset:

- **P2P**: 26656 + (3 × 10) = **26686**
- **RPC**: 26657 + (3 × 10) = **26687**
- **gRPC**: 9090 + (3 × 10) = **9120**
- **gRPC-Web**: 9091 + (3 × 10) = **9121**
- **REST API**: 1317 + (3 × 10) = **1347**
- **JSON-RPC HTTP**: 8545 + (3 × 10) = **8575**
- **JSON-RPC WebSocket**: 8546 + (3 × 10) = **8576**

For detailed descriptions of each port type, see [Port Reference: Blockchain Nodes]({{< relref "../ports/blockchain-nodes" >}}).
{{< /expand >}}

### Required Ports

{{< expand "Required Ports Details" "↕" >}}
These ports must be configured for the service to function:

| Port Type | Host Port | Container Port | Description |
|-----------|-----------|---------------|-------------|
| **P2P** | 26686 | 26656 | Peer-to-peer network communication |
| **RPC** | 26687 | 26657 | Tendermint RPC API |
{{< /expand >}}

### Optional Ports

{{< expand "Optional Ports Details" "↕" >}}
These ports can be enabled if needed for specific use cases:

| Port Type | Host Port | Container Port | Description | When to Enable |
|-----------|-----------|---------------|-------------|----------------|
| **gRPC** | 9120 | 9090 | Cosmos SDK gRPC queries | Public API endpoint, wallet connections |
| **gRPC-Web** | 9121 | 9091 | gRPC-Web (browser) | Web applications, browser wallets |
| **REST API** | 1347 | 1317 | Cosmos SDK REST API | Legacy application compatibility |
| **JSON-RPC HTTP** | 8575 | 8545 | Ethereum JSON-RPC (HTTP) | MetaMask, Ethereum tools, dApps |
| **JSON-RPC WebSocket** | 8576 | 8546 | Ethereum JSON-RPC (WebSocket) | Real-time blockchain events |
| **Prometheus** | 26690 | 26660 | Prometheus metrics | Node monitoring |
| **EVM Metrics** | 6095 | 6065 | EVM Prometheus metrics | EVM performance monitoring |
| **Geth Metrics** | 8130 | 8100 | Geth-compatible metrics | Geth monitoring tools |
{{< /expand >}}

---

## Environment Variables

This service uses the following environment variables with the values shown below. For complete documentation of all available environment variables, see [Environment Variables: Blockchain Nodes]({{< relref "../environment/blockchain-nodes" >}}).

### Binary Configuration

This service uses an **alternative binary** (`qomd`) instead of the default Infinite binary. The binary is downloaded from the specified URL at container startup.

**Alternative Binary Configuration:**
- **Binary Name:** `qomd`
- **Binary URL (AMD64):** `https://github.com/WizardLatino/test-qom-node/releases/download/v1.0.1/qomd-linux-amd64`
- **Home Directory:** `/home/ubuntu/.qomd`

### Chain Identification

{{< expand "Chain Identification Variables" "↕" >}}
This service is configured with the following chain identification variables:

**NODE_CHAIN_ID**  
The chain ID for the QOM Network. This uniquely identifies the blockchain network.

```yaml
NODE_CHAIN_ID: "qom_766-1"
```

**NODE_EVM_CHAIN_ID**  
The EVM Chain ID for EIP-155 compatible replay protection.

This is separate from the Cosmos chain ID and is used for Ethereum-compatible transactions.

```yaml
NODE_EVM_CHAIN_ID: "766"
```

**NODE_GENESIS_URL**  
URL to download the official genesis file during node initialization.

The genesis file contains the initial state of the blockchain.

```yaml
NODE_GENESIS_URL: "https://raw.githubusercontent.com/deep-thought-labs/babelfish-vm/main/resources/genesis.json"
```
{{< /expand >}}

### Network P2P Configuration

{{< expand "Network P2P Configuration Variables" "↕" >}}
This service uses the following P2P network configuration variables:

**NODE_P2P_SEEDS**  
Seed nodes for P2P discovery. These nodes help your node discover other peers in the network during initial connection.

Seed nodes are used for network discovery but are not persistent connections.

```yaml
NODE_P2P_SEEDS: "7768864af4003165c10b77802a673006f98d54c6@p2p.foxxone.one:26656"
```

**NODE_PERSISTENT_PEERS**  
Persistent peer nodes maintain continuous connections, unlike seed nodes which are only used for discovery.

```yaml
NODE_PERSISTENT_PEERS: "7768864af4003165c10b77802a673006f98d54c6@p2p.foxxone.one:26656"
```

**NODE_P2P_EXTERNAL_ADDRESS**  
External address to advertise to peers for them to dial. Used when the node is behind NAT or firewall.

This service does not have a pre-configured value for this variable. If needed, configure it with your node's public IP address or domain name.

```yaml
# NODE_P2P_EXTERNAL_ADDRESS: ""  # No pre-configured value for this service
```
{{< /expand >}}

### Alternative Binary Configuration

{{< expand "Alternative Binary Configuration Variables" "↕" >}}
This service uses an alternative binary instead of the default Infinite binary. The following variables configure the alternative binary:

**NODE_ALT_BINARY_URL_AMD64**  
URL to download the alternative binary for AMD64/x86_64 architecture.

The binary will be downloaded at container startup.

```yaml
NODE_ALT_BINARY_URL_AMD64: "https://github.com/WizardLatino/test-qom-node/releases/download/v1.0.1/qomd-linux-amd64"
```

**NODE_ALT_BINARY_NAME**  
Name of the alternative binary executable.

This is the name of the binary file (without path). It will be installed in `/home/ubuntu/bin/`.

```yaml
NODE_ALT_BINARY_NAME: "qomd"
```

**NODE_ALT_HOME**  
Custom home directory for the alternative blockchain node.

This is where the blockchain node stores its data and configuration files.

```yaml
NODE_ALT_HOME: "/home/ubuntu/.qomd"
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

## Docker Compose Configuration

{{< expand "Minimal Configuration (Required Ports Only)" "↕" >}}
```yaml
services:
  qom:
    image: deepthoughtlabs/infinite-drive:dev
    container_name: qom
    restart: unless-stopped

    ports:
      - "26686:26656"  # P2P (required)
      - "26687:26657"  # RPC (required)
    
    volumes:
      - ./persistent-data:/home/ubuntu/.qomd

    environment:
      NODE_CHAIN_ID: "qom_766-1"
      NODE_EVM_CHAIN_ID: "766"
      NODE_GENESIS_URL: "https://raw.githubusercontent.com/deep-thought-labs/babelfish-vm/main/resources/genesis.json"
      NODE_P2P_SEEDS: "7768864af4003165c10b77802a673006f98d54c6@p2p.foxxone.one:26656"
      NODE_PERSISTENT_PEERS: "7768864af4003165c10b77802a673006f98d54c6@p2p.foxxone.one:26656"
      NODE_ALT_BINARY_URL_AMD64: "https://github.com/WizardLatino/test-qom-node/releases/download/v1.0.1/qomd-linux-amd64"
      NODE_ALT_BINARY_NAME: "qomd"
      NODE_ALT_HOME: "/home/ubuntu/.qomd"
```
{{< /expand >}}

{{< expand "Full Configuration (All Ports)" "↕" >}}
```yaml
services:
  qom:
    image: deepthoughtlabs/infinite-drive:dev
    container_name: qom
    restart: unless-stopped

    ports:
      # Required ports
      - "26686:26656"  # P2P
      - "26687:26657"  # RPC
      
      # Optional ports (uncomment if needed)
      - "9120:9090"    # gRPC
      - "9121:9091"    # gRPC-Web
      - "1347:1317"    # REST API
      - "8575:8545"    # JSON-RPC HTTP
      - "8576:8546"    # JSON-RPC WebSocket
      - "26690:26660"  # Prometheus
      - "6095:6065"    # EVM Metrics
      - "8130:8100"    # Geth Metrics
    
    volumes:
      - ./persistent-data:/home/ubuntu/.qomd

    environment:
      NODE_CHAIN_ID: "qom_766-1"
      NODE_EVM_CHAIN_ID: "766"
      NODE_GENESIS_URL: "https://raw.githubusercontent.com/deep-thought-labs/babelfish-vm/main/resources/genesis.json"
      NODE_P2P_SEEDS: "7768864af4003165c10b77802a673006f98d54c6@p2p.foxxone.one:26656"
      NODE_PERSISTENT_PEERS: "7768864af4003165c10b77802a673006f98d54c6@p2p.foxxone.one:26656"
      NODE_ALT_BINARY_URL_AMD64: "https://github.com/WizardLatino/test-qom-node/releases/download/v1.0.1/qomd-linux-amd64"
      NODE_ALT_BINARY_NAME: "qomd"
      NODE_ALT_HOME: "/home/ubuntu/.qomd"
      # NODE_P2P_EXTERNAL_ADDRESS: ""
```
{{< /expand >}}

---

## Firewall Configuration

**⚠️ Critical:** Before configuring any firewall rules for this service, you must first allow SSH (port 22) on your system. If you're connecting to a remote server via SSH and you enable the firewall without allowing SSH first, you will lose access to your server.

The complete firewall configuration process, including how to verify and allow SSH (port 22), is described in detail in the [Firewall Configuration Guide]({{< relref "../ports/firewall-configuration" >}}). The commands shown below are specific to this service with the correct port numbers for QOM Network, but please review the guide for the complete setup process.

### Required Ports

{{< tabs "firewall-required" >}}
{{< tab "Ubuntu/Linux" >}}
```bash
# P2P port (required for validators and peer connections)
sudo ufw allow 26686/tcp

# RPC port (optional, only if exposing RPC API)
sudo ufw allow 26687/tcp
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
5. Add rules to allow incoming connections for the required ports (26686, 26687)

**Second Option - Command Line (Advanced):**
If you prefer command-line configuration, you can modify `/etc/pf.conf`:

```bash
# Edit /etc/pf.conf and add rules:
# pass in proto tcp from any to any port 26686  # P2P port
# pass in proto tcp from any to any port 26687  # RPC port

# Then reload the firewall:
sudo pfctl -f /etc/pf.conf
```
{{< /tab >}}
{{< tab "Windows" >}}
```powershell
# P2P port (required for validators and peer connections)
New-NetFirewallRule -DisplayName "Drive P2P" -Direction Inbound -LocalPort 26686 -Protocol TCP -Action Allow

# RPC port (optional, only if exposing RPC API)
New-NetFirewallRule -DisplayName "Drive RPC" -Direction Inbound -LocalPort 26687 -Protocol TCP -Action Allow
```
{{< /tab >}}
{{< /tabs >}}

### Optional Ports

{{< tabs "firewall-optional" >}}
{{< tab "Ubuntu/Linux" >}}
```bash
# gRPC (if exposing gRPC API)
sudo ufw allow 9120/tcp

# gRPC-Web (if exposing gRPC-Web API)
sudo ufw allow 9121/tcp

# REST API (if exposing REST API)
sudo ufw allow 1347/tcp

# JSON-RPC HTTP (if exposing Ethereum-compatible API)
sudo ufw allow 8575/tcp

# JSON-RPC WebSocket (if exposing WebSocket API)
sudo ufw allow 8576/tcp

# Prometheus (if exposing metrics)
sudo ufw allow 26690/tcp

# EVM Metrics (if exposing EVM metrics)
sudo ufw allow 6095/tcp

# Geth Metrics (if exposing Geth metrics)
sudo ufw allow 8130/tcp
```

**Note:** The `/tcp` protocol specification is optional in UFW. You can use either `sudo ufw allow 26686/tcp` or `sudo ufw allow 26686` - both work the same way.
{{< /tab >}}
{{< tab "macOS" >}}
**Recommended:** macOS typically allows incoming connections by default, so you may not need to configure anything. However, we recommend verifying your firewall settings.

**First Option - System Preferences (Recommended):**
Use the built-in graphical interface to configure firewall rules:
1. Open **System Preferences** (or **System Settings** on newer macOS versions)
2. Go to **Security & Privacy** > **Firewall**
3. Click the lock icon and enter your password to make changes
4. Click **Firewall Options...**
5. Add rules to allow incoming connections for the optional ports you want to expose (9120, 9121, 1347, 8575, 8576, 26690, 6095, 8130)

**Second Option - Command Line (Advanced):**
If you prefer command-line configuration, you can modify `/etc/pf.conf`:

```bash
# Edit /etc/pf.conf and add rules for each port you want to expose:
# pass in proto tcp from any to any port 9120  # gRPC
# pass in proto tcp from any to any port 9121  # gRPC-Web
# pass in proto tcp from any to any port 1347  # REST API
# pass in proto tcp from any to any port 8575  # JSON-RPC HTTP
# pass in proto tcp from any to any port 8576  # JSON-RPC WebSocket
# pass in proto tcp from any to any port 26690 # Prometheus
# pass in proto tcp from any to any port 6095  # EVM Metrics
# pass in proto tcp from any to any port 8130  # Geth Metrics

# Then reload the firewall:
sudo pfctl -f /etc/pf.conf
```
{{< /tab >}}
{{< tab "Windows" >}}
```powershell
# gRPC (if exposing gRPC API)
New-NetFirewallRule -DisplayName "Drive gRPC" -Direction Inbound -LocalPort 9120 -Protocol TCP -Action Allow

# gRPC-Web (if exposing gRPC-Web API)
New-NetFirewallRule -DisplayName "Drive gRPC-Web" -Direction Inbound -LocalPort 9121 -Protocol TCP -Action Allow

# REST API (if exposing REST API)
New-NetFirewallRule -DisplayName "Drive REST API" -Direction Inbound -LocalPort 1347 -Protocol TCP -Action Allow

# JSON-RPC HTTP (if exposing Ethereum-compatible API)
New-NetFirewallRule -DisplayName "Drive JSON-RPC HTTP" -Direction Inbound -LocalPort 8575 -Protocol TCP -Action Allow

# JSON-RPC WebSocket (if exposing WebSocket API)
New-NetFirewallRule -DisplayName "Drive JSON-RPC WS" -Direction Inbound -LocalPort 8576 -Protocol TCP -Action Allow

# Prometheus (if exposing metrics)
New-NetFirewallRule -DisplayName "Drive Prometheus" -Direction Inbound -LocalPort 26690 -Protocol TCP -Action Allow

# EVM Metrics (if exposing EVM metrics)
New-NetFirewallRule -DisplayName "Drive EVM Metrics" -Direction Inbound -LocalPort 6095 -Protocol TCP -Action Allow

# Geth Metrics (if exposing Geth metrics)
New-NetFirewallRule -DisplayName "Drive Geth Metrics" -Direction Inbound -LocalPort 8130 -Protocol TCP -Action Allow
```
{{< /tab >}}
{{< /tabs >}}

---

## Persistent Data

### Volume Mapping

- **Host Path:** `./persistent-data`
- **Container Path:** `/home/ubuntu/.qomd`

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
