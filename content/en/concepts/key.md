---
title: "Key"
weight: 1
---

A **key** is a fundamental cryptographic component in blockchains that allows identifying, authenticating, and authorizing operations on the network.

## What is a Key?

A cryptographic key is a pair of mathematically related keys:

- **Private Key** - Kept secret and never shared. Used to sign transactions and blocks.
- **Public Key** - Derived from the private key and can be shared publicly. Used to verify signatures and generate addresses.

## Purpose in Blockchains

Cryptographic keys in blockchains are used to:

- **Identify entities** - Each key generates a unique address on the blockchain
- **Sign transactions** - The private key signs transactions to prove ownership
- **Sign blocks** - Validators use keys to sign blocks they propose
- **Authentication** - Verify that an operation was authorized by the key owner
- **Manage funds** - Addresses derived from keys can receive and store tokens

## Seed Phrase

Keys are typically generated from a **seed phrase** (mnemonic phrase):

- **12 or 24 words** - A sequence of words that represents the private key
- **BIP39 standard** - Standard format used in most blockchains
- **Recovery** - The same seed phrase always generates the same key
- **Critical backup** - If you lose your seed phrase, you permanently lose access to your keys
- **Multiple keys** - You can create multiple keys from the same seed phrase using different account indices

**⚠️ IMPORTANT:** The seed phrase is the only way to recover your keys. If you lose it, there's no way to recover access.

> [!TIP]
> **Multiple Keys from One Seed Phrase**
>
> You can create multiple keys from the same seed phrase using different account indices. This allows you to organize keys by purpose (main, backup, test) or manage multiple accounts from one mnemonic. See [Multiple Keys from Same Seed Phrase]({{< relref "../drive/guides/blockchain-nodes/keys/multiple-keys-from-seed" >}}) for detailed examples.

## Use of Keys in Blockchain Nodes

In the context of blockchain nodes, keys are used in different ways:

### Specific Key Types

There are two main types of keys in blockchain nodes:

1. **Account Keys** - Standard keys stored in the [keyring]({{< relref "keyring" >}}) and used for:
   - Signing on-chain transactions
   - Creating validators (`create-validator`)
   - Delegating tokens
   - Performing governance operations
   - Any operation that requires cryptographic authentication from the user
   
   These are the "normal" keys that you manage manually and can add to the keyring as needed.

2. **[Private Validator Key]({{< relref "private-validator-key" >}})** - Specific type of key that identifies and authorizes a validator to sign blocks. It's automatically generated during node initialization and used internally by the node to participate in consensus.

### Storage Systems

- **[Keyring]({{< relref "keyring" >}})** - Secure storage system where **account keys** are stored for signing on-chain transactions

**Important:** 
- The keyring is a **storage** where you keep account keys
- Account keys are the "normal" type of key you use for on-chain operations
- The Private Validator Key is a **specific type of key** with a particular purpose (signing blocks as a validator)
- Both types of keys are different and used for different purposes

To better understand how these components relate, see [Keyring vs Private Validator Key]({{< relref "keyring-vs-validator-key" >}}).

## Key Security

Cryptographic keys are fundamental for security:

- **Never share your private key** - Whoever has access to your private key has total control
- **Backup the seed phrase** - Store your seed phrase in a safe place and offline
- **Use secure storage** - Consider using hardware wallets or encrypted keyrings
- **Multiple copies** - Create several copies of your seed phrase in separate locations

## See Also

- [Keyring]({{< relref "keyring" >}}) - Secure storage for multiple keys
- [Private Validator Key]({{< relref "private-validator-key" >}}) - Specific key for validators
- [Keyring vs Private Validator Key]({{< relref "keyring-vs-validator-key" >}}) - Differences between key types
- [Node Initialization]({{< relref "../drive/guides/blockchain-nodes/initialization" >}}) - How keys are generated during initialization
- [Key Management]({{< relref "../drive/guides/blockchain-nodes/keys" >}}) - Practical guide to manage keys

