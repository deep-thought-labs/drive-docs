---
title: "Node Initialization"
weight: 3
---

**Blockchain node initialization** is the process of configuring its initial state, creating all the necessary components for the node to function correctly on the blockchain network.

## What is Initialization?

When you initialize a blockchain node, the system performs a series of operations that configure the node's environment from scratch:

- **Creates configuration files** - Establishes node operation parameters
- **Generates cryptographic keys** - Creates the necessary identities for the node
- **Downloads the genesis file** - Obtains the initial state of the blockchain
- **Sets the Chain ID** - Configures the blockchain network identification

## Components Created During Initialization

### Configuration Files

During initialization, three main configuration files are created:

- **`config.toml`** - General node configuration (network, consensus, etc.)
- **`app.toml`** - Blockchain application configuration
- **`client.toml`** - Client configuration to interact with the node

### Cryptographic Keys

The initialization process automatically generates:

- **[Private Validator Key]({{< relref "private-validator-key" >}})** (`priv_validator_key.json`) - Key that identifies the validator on the blockchain
- **Node Key** - Key for the node's identity on the P2P network
- **Consensus Key** - Key for consensus (if applicable)

**Note:** The [keyring]({{< relref "keyring" >}}) (where account keys are stored) is created the first time you add a key, not during node initialization.

### Genesis File

The official network [genesis file]({{< relref "genesis-file" >}}) is downloaded, which contains:

- The initial state of the blockchain
- Initial validators
- Network parameters
- Consensus configuration

## Component Location

All components created during initialization are stored in [node data]({{< relref "node-data" >}}):

- **Configuration files and Private Validator Key:**
  - **Host path:** `./persistent-data/config/` (relative to the service directory)
  - **Container path:** `/home/ubuntu/.infinited/config/`

- **Keyring (account keys):**
  - **Host path:** `./persistent-data/keyring-file/` (relative to the service directory)
  - **Container path:** `/home/ubuntu/.infinited/keyring-file/`
  
  **Note:** The keyring is created when you add your first account key, not during node initialization.

## Initialization Modes

There are two initialization modes available:

- **Simple Initialization** - Generates random keys that cannot be recovered
- **Recovery Initialization** - Uses a seed phrase to generate recoverable keys

For more details on how to initialize a node and when to use each mode, see the practical guide [Node Initialization]({{< relref "../drive/guides/blockchain-nodes/initialization" >}}).

## Importance of Initialization

Initialization is a critical step because:

- **Defines node identity** - The generated keys identify the node on the blockchain
- **Establishes base configuration** - Configuration files determine how the node operates
- **Connects to the network** - The genesis file allows the node to synchronize with the blockchain
- **Determines recoverability** - The initialization mode determines if you can restore the node

## See Also

- [Genesis File]({{< relref "genesis-file" >}}) - What is the genesis file and its purpose
- [Node Data]({{< relref "node-data" >}}) - What is node data and where it's stored
- [Private Validator Key]({{< relref "private-validator-key" >}}) - What is the Private Validator Key
- [Node Initialization]({{< relref "../drive/guides/blockchain-nodes/initialization" >}}) - Practical guide to initialize a node

