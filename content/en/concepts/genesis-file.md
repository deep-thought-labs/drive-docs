---
title: "Genesis File"
weight: 4
---

The **genesis file** (`genesis.json`) is the document that defines the initial state of a blockchain. It contains all the information necessary for a node to begin synchronizing with the network from the initial block (block 0).

## What is the Genesis File?

The genesis file is a JSON file that acts as the "starting point" of the blockchain. It defines:

- **The initial state** of the blockchain
- **The initial validators** of the network
- **Consensus and governance parameters**
- **The blockchain application configuration**
- **The Chain ID** that identifies the network

## Purpose of the Genesis File

### Initial State of the Blockchain

The genesis file establishes the initial state of the blockchain, including:

- Initial token distribution
- Initial accounts and their balances
- Initially deployed smart contracts (if applicable)
- Module configuration and parameters

### Initial Validators

It defines who are the validators that participate in consensus from the start:

- Validator addresses
- Initial voting power (staking)
- Consensus information

### Network Parameters

It establishes the network's operational parameters:

- Consensus parameters
- Governance configuration
- Economic parameters (inflation, rewards, etc.)
- Network limits and restrictions

### Chain ID

The genesis file defines the **Chain ID**, which is a unique identifier for the blockchain network. This ID:

- Identifies the specific network
- Prevents replay attacks between different networks
- Allows nodes to connect to the correct network

## Download During Initialization

During [node initialization]({{< relref "node-initialization" >}}), the system:

1. **Generates an initial genesis file** using the `infinited init` command
2. **Automatically downloads the official genesis file** of the network from the official repository
3. **Replaces the generated genesis** with the official one if the download is successful and the file is valid JSON
4. **Keeps the generated genesis** if the download fails or the downloaded file is not valid

**Location:**
- **Host path:** `./persistent-data/config/genesis.json` (relative to the service directory)
- **Container path:** `/home/ubuntu/.infinited/config/genesis.json`

**Note:** The system verifies that the downloaded file is valid JSON before replacing the generated genesis. If the download fails, the node can function with the initially generated genesis, although it's recommended to have the official genesis.

## Importance of the Genesis File

The genesis file is critical because:

- **Enables synchronization** - Without it, the node cannot begin synchronizing with the blockchain
- **Ensures consistency** - All nodes must use the same genesis file to be on the same network
- **Defines network identity** - The Chain ID and parameters identify the specific network
- **Establishes the rules** - The parameters define how the blockchain operates

## Verifying the Genesis File

After initializing a node, you can verify that the genesis file was downloaded correctly:

```bash
# Verify that the file exists
ls -la persistent-data/config/genesis.json

# Verify the Chain ID
cat persistent-data/config/genesis.json | grep chain_id
```

## See Also

- [Node Initialization]({{< relref "node-initialization" >}}) - What is initialization and what components it creates
- [Node Data]({{< relref "node-data" >}}) - What is node data and where it's stored
- [Node Initialization]({{< relref "../drive/guides/blockchain-nodes/initialization" >}}) - Practical guide to initialize a node

