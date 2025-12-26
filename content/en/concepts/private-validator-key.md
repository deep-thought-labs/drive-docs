---
title: "Private Validator Key"
weight: 5
---

The **Private Validator Key** (`priv_validator_key.json`) is a unique cryptographic key that identifies and authorizes your validator on the blockchain. It's fundamental to understand its importance and how it relates to other system components.

## What is the Private Validator Key?

When you initialize a blockchain node, the system automatically generates a file called `priv_validator_key.json` (Private Validator Key). This file contains a unique cryptographic key that:

- **Identifies your validator** on the blockchain
- **Signs the blocks** that your validator proposes and validates
- **Is permanently linked** to your validator once you register it on the blockchain

## Analogy: Your Validator's "ID Card"

**Think of the Private Validator Key as your validator's "ID card"**: once you register your validator on the blockchain using this key, that identity is permanently associated with it. If you want to move your validator to another server or restore it after a failure, you'll need exactly the same `priv_validator_key`.

## Importance for Validators

The Private Validator Key is **critical** for validators because:

- **Without it, you cannot sign blocks** - Your validator won't be able to participate in consensus
- **It's permanently linked to your validator** - Once registered on the blockchain, it cannot be changed
- **It's necessary to restore your validator** - If you lose the server, you need this key to restore your validator

**⚠️ CRITICAL:** If you lose your `priv_validator_key` and cannot recover it (because you didn't use recovery mode), you will permanently lose control of your validator.

## Private Validator Key Generation

The Private Validator Key is generated during node initialization. The initialization mode determines whether the key will be recoverable:

- **Simple Initialization:** Generates a random and unique key that **cannot be recovered**
- **Recovery Initialization:** Always generates the same key using a seed phrase, **recoverable at any time**

For more details, see [Node Initialization]({{< relref "../drive/guides/blockchain-nodes/initialization" >}}).

## Location

The Private Validator Key is stored at:

- **Host path:** `./persistent-data/config/priv_validator_key.json` (relative to the service directory)
- **Container path:** `/home/ubuntu/.infinited/config/priv_validator_key.json`

## See Also

- [Keyring vs Private Validator Key]({{< relref "keyring-vs-validator-key" >}}) - Detailed differences between keyring and Private Validator Key
- [Keyring]({{< relref "keyring" >}}) - What is a keyring and how it works
- [Node Initialization]({{< relref "../drive/guides/blockchain-nodes/initialization" >}}) - Complete guide on initialization modes and recoverability
- [Understanding Keys]({{< relref "../drive/guides/blockchain-nodes/keys/understanding-keys" >}}) - Applied guide on how these concepts relate

