---
title: "Keyring"
weight: 2
---

A **keyring** is a secure and encrypted storage where your cryptographic keys are kept. Drive automatically generates and manages the keyring for each node.

## What is a Keyring?

Think of the keyring as a **wallet** where you can have multiple accounts or keys:

- **Adding keys to the keyring** is like adding accounts to your wallet
- You can have **multiple keys** in the same keyring for different purposes
- Keys in the keyring are used to **sign transactions** and perform on-chain operations
- For example, the transaction to create a validator (`create-validator`) requires a key from the keyring
- You can add multiple keys from the same seed phrase using different account indices

> [!TIP]
> **Multiple Keys from Same Seed Phrase**
>
> You can create multiple keys from one seed phrase and add them all to the keyring. This is useful for organizing keys by purpose (main, backup, test) or managing multiple accounts. See [Multiple Keys from Same Seed Phrase]({{< relref "../drive/guides/blockchain-nodes/keys/multiple-keys-from-seed" >}}) for detailed examples.

## Keyring Location

The keyring is stored in a specific subdirectory within the node's persistent data folder:

- **Host path:** `./persistent-data/keyring-file/` (relative to the service directory)
- **Container path:** `/home/ubuntu/.infinited/keyring-file/`

When you use commands that require keys (such as transactions or on-chain operations), the system will look for keys in this location. If the command cannot find the key, verify that you're working from the correct service directory and that the keyring exists in `persistent-data/keyring-file/`.

## Keyring Protection

The keyring is protected by a password that you set the first time you save a key. This password is required to access the stored keys.

## Use in Operations

Keys stored in the keyring are used for:

- Signing on-chain transactions
- Creating validators (`create-validator`)
- Delegating tokens
- Performing governance operations
- Any operation that requires cryptographic authentication

## See Also

- [Keyring vs Private Validator Key]({{< relref "keyring-vs-validator-key" >}}) - Detailed differences between keyring and Private Validator Key
- [Private Validator Key]({{< relref "private-validator-key" >}}) - What is the Private Validator Key
- [Node Initialization]({{< relref "../drive/guides/blockchain-nodes/initialization" >}}) - Complete guide on initialization modes
- [Key Management]({{< relref "../drive/guides/blockchain-nodes/keys" >}}) - Practical guide to manage keys in the keyring

