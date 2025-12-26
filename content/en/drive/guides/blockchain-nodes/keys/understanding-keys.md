---
title: "Understanding Keys"
weight: 52220
---

This guide explains the differences between validators and full nodes regarding key management, especially about when and why you need to worry about the recoverability of the Private Validator Key during initialization.

> [!NOTE]
> **Fundamental Concepts**
>
> Before continuing, make sure you understand the basic concepts:
>
> - [Key]({{< relref "../../../../../concepts/key" >}}) - What is a cryptographic key and what it's used for in blockchains
> - [Keyring]({{< relref "../../../../../concepts/keyring" >}}) - What is a keyring and how it works
> - [Private Validator Key]({{< relref "../../../../../concepts/private-validator-key" >}}) - What is the Private Validator Key and its importance
> - [Keyring vs Private Validator Key]({{< relref "../../../../../concepts/keyring-vs-validator-key" >}}) - Detailed differences between both components
> - [Node Initialization]({{< relref "../initialization" >}}) - Complete guide on initialization modes and recoverability

## Differences Between Validators and Full Nodes in Key Management

### Use of Keys in General

**Important:** Both validators and full nodes can use [account keys]({{< relref "../../../../../concepts/key" >}}) stored in the [keyring]({{< relref "../../../../../concepts/keyring" >}}) to perform operations such as:
- Signing on-chain transactions
- Delegating tokens
- Participating in governance
- Any operation that requires cryptographic authentication

The critical difference **is NOT** in the general use of keys, but in the **recoverability of the Private Validator Key during node initialization**.

### Full Nodes

Full nodes **do NOT need to worry about the recoverability of the Private Validator Key** because:

- **They don't participate in consensus** - They only verify and store blocks
- **They don't sign blocks** - They don't need a permanent identity on the blockchain
- **Private Validator Key not critical** - The node automatically generates a Private Validator Key for its internal operation, but this is not critical because it's not registered on the blockchain
- **No risk of permanent loss** - If they lose the Private Validator Key, they can simply reinitialize the node with a new one

**For full nodes:**
- You can use [simple initialization]({{< relref "../initialization/simple-initialization" >}}) without worrying about Private Validator Key recoverability
- The node will automatically generate a Private Validator Key for its internal operation
- You don't need to backup the Private Validator Key because it doesn't represent a critical identity on the blockchain
- **You CAN use account keys** in the keyring for operations if needed (transactions, delegations, etc.)

### Validators

Validators **MUST worry about the recoverability of the Private Validator Key** because:

- **They participate in consensus** - They propose and validate blocks
- **Permanent identity** - Once registered on the blockchain, the validator is permanently linked to its [Private Validator Key]({{< relref "../../../../../concepts/private-validator-key" >}})
- **Sign blocks** - They need their Private Validator Key to sign each block they propose
- **Risk of permanent loss** - If they lose their Private Validator Key and cannot recover it (because they didn't use recovery mode), they lose their validator forever

**For validators:**
- **YOU MUST** initialize with [recovery mode]({{< relref "../initialization/recovery-initialization" >}}) using a seed phrase to ensure Private Validator Key recoverability
- **YOU MUST** backup your seed phrase securely
- It's recommended to use the same seed phrase to initialize the node (generate the Private Validator Key) and for the [keyring]({{< relref "../../../../../concepts/keyring" >}}) (account keys for operations)
- If you lose your `priv_validator_key` and didn't use recovery mode, you will permanently lose your validator

## Relationship Between Keyring and Private Validator Key

To understand in detail how these components relate and why it's recommended to use the same seed phrase for both, see [Keyring vs Private Validator Key]({{< relref "../../../../../concepts/keyring-vs-validator-key" >}}).

**Summary:** Although technically it's possible to use different keys, **it's highly recommended to use the same seed phrase for both** for simplicity, consistency, and unified recovery.

## Summary: Validators vs Full Nodes

| Aspect | Full Node | Validator |
|--------|-----------|-----------|
| **Use of account keys (keyring)** | ✅ Optional - for operations if needed | ✅ Recommended - for on-chain operations |
| **Private Validator Key recoverability** | ❌ Not necessary - can use simple initialization | ✅ **CRITICAL** - MUST use recovery mode |
| **Node initialization** | [Simple]({{< relref "../initialization/simple-initialization" >}}) is fine | **MUST be with [recovery]({{< relref "../initialization/recovery-initialization" >}})** |
| **Risk of losing Private Validator Key** | Low impact - can reinitialize | **Permanent loss of validator** |
| **Backup seed phrase** | Not necessary for Private Validator Key | **MANDATORY** for Private Validator Key |

## Next Steps

Now that you understand the fundamental concepts:

- **[Management Operations]({{< relref "operations" >}})** - Learn to perform key management operations
- **[Security Best Practices]({{< relref "security" >}})** - Protect your keys following these recommendations
- **[Workflow for Validators]({{< relref "validator-workflow" >}})** - If you're a validator, follow this step-by-step workflow
- **[Node Initialization]({{< relref "../initialization" >}})** - Practical guide to initialize a node
- **[Graphical Interface]({{< relref "../graphical-interface" >}})** - Use the graphical interface to manage your node

