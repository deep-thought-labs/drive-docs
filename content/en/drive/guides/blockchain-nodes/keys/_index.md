---
title: "Key Management"
weight: 5222
---

Complete guide to manage cryptographic keys in the keyring of your Drive blockchain nodes.

## What is Key Management?

Key management is the process of creating, storing, protecting, and using cryptographic keys that identify your node on the blockchain and allow you to sign transactions and blocks. This section guides you through everything you need to know to manage keys securely and effectively.

## Recommended Reading Order

To get the best out of this documentation, we recommend following this order:

### 1. 📚 Understand Fundamental Concepts

**Start here if you're new to key management:**

- **[Understanding Keys]({{< relref "understanding-keys" >}})** - Explains the differences between validators and full nodes regarding key management, especially about the recoverability of the Private Validator Key during initialization.

> [!NOTE]
> **Recommended Prerequisites**
>
> If you don't yet understand the basic concepts about keys, we recommend reading the atomic concepts first:
>
> - [Key]({{< relref "../../../../../concepts/key" >}}) - What is a cryptographic key and what it's used for in blockchains
> - [Keyring]({{< relref "../../../../../concepts/keyring" >}}) - What is a keyring and how it works
> - [Private Validator Key]({{< relref "../../../../../concepts/private-validator-key" >}}) - What is the Private Validator Key and its importance
> - [Keyring vs Private Validator Key]({{< relref "../../../../../concepts/keyring-vs-validator-key" >}}) - Detailed differences between both components
> - [Node Initialization]({{< relref "../initialization" >}}) - Complete guide on initialization modes and recoverability

### 2. 🔧 Learn Operations

**Once you understand the concepts, learn to perform operations:**

- **[Management Operations]({{< relref "operations" >}})** - Complete guide of all available operations:
  - 🔑 Generate keys (Dry-Run and save directly)
  - ➕ Add existing keys from seed phrase
  - 📋 List and show key details
  - 🗑️ Delete keys
  - 🔒 Reset keyring password

### 3. 🔐 Security Best Practices

**Before creating or using keys, learn to protect them correctly:**

- **[Security Best Practices]({{< relref "security" >}})** - Essential recommendations:
  - Secure seed phrase backup
  - Keyring protection
  - General server security

### 4. 🚀 Workflow for Validators

**If you act as a validator, follow this step-by-step workflow:**

- **[Workflow for Validators]({{< relref "validator-workflow" >}})** - Step-by-step guide that takes you from key creation to node initialization:
  - Create and backup your seed phrase
  - Initialize the node with recovery
  - Add keys to the keyring for operations

### 5. 🔐 Multisig Wallets (Advanced)

**For users who need additional security or shared control:**

- **[Multisig Wallets Overview]({{< relref "multisig-overview" >}})** - Introduction and when to use multisig wallets
- **[Multisig Operations]({{< relref "multisig-operations" >}})** - How to create and use multisig wallets
- **[Multisig Security]({{< relref "multisig-security" >}})** - Specific security best practices

## Are You a Validator or Full Node?

To understand the differences between validators and full nodes regarding key management, especially about when and why you need to worry about the recoverability of the Private Validator Key, see [Understanding Keys]({{< relref "understanding-keys" >}}).

**Quick summary:**
- **Validators:** MUST use recovery mode during initialization to ensure recoverability of their Private Validator Key
- **Full Nodes:** Can use simple initialization; don't need to worry about Private Validator Key recoverability, but CAN use account keys for operations

**Recommended paths:**
- **If you're a Validator:** Read [Understanding Keys]({{< relref "understanding-keys" >}}), learn [Security Best Practices]({{< relref "security" >}}), and then follow the [Workflow for Validators]({{< relref "validator-workflow" >}})
- **If you're a Full Node:** You can use [Management Operations]({{< relref "operations" >}}) if you need account keys for operations, or continue with [Node Initialization]({{< relref "../initialization" >}}) if you only want to run the node

## Troubleshooting

If you encounter problems managing keys, see:

- **[Key Management Issues]({{< relref "../../../troubleshooting/key-management-issues" >}})** - Solutions to common problems such as:
  - I can't see my seed phrase
  - I forgot my keyring password
  - Error: Key not found
  - I need to recover a deleted key

## Related Documentation

### Fundamental Concepts

- [Key]({{< relref "../../../../../concepts/key" >}}) - What is a cryptographic key and what it's used for in blockchains
- [Keyring]({{< relref "../../../../../concepts/keyring" >}}) - What is a keyring and how it works
- [Private Validator Key]({{< relref "../../../../../concepts/private-validator-key" >}}) - What is the Private Validator Key
- [Keyring vs Private Validator Key]({{< relref "../../../../../concepts/keyring-vs-validator-key" >}}) - Detailed differences between both components
- [Node Initialization]({{< relref "../initialization" >}}) - Complete guide on initialization modes and recoverability
- [Multisig Wallet]({{< relref "../../../../../concepts/multisig-wallet" >}}) - What is a multisig wallet and what it's used for
- [Multisig Threshold]({{< relref "../../../../../concepts/multisig-threshold" >}}) - What is the M-of-N threshold and how it works
- [Multisig Signer]({{< relref "../../../../../concepts/multisig-signer" >}}) - What is a signer and their role in multisig wallets

### Related Guides

- [Graphical Interface]({{< relref "../graphical-interface" >}}) - Use the graphical interface to manage keys
- [Node Initialization]({{< relref "../initialization" >}}) - How to initialize a node using your keys
- [Start/Stop Node]({{< relref "../start-stop-node" >}}) - How to start and stop your node after configuring keys

