---
title: "Keyring vs Private Validator Key"
weight: 3
---

This document explains the fundamental differences between the **Keyring** and the **Private Validator Key**, two distinct but related cryptographic components in blockchain nodes.

## Summary of Differences

| Aspect | Private Validator Key | Keyring |
|--------|----------------------|---------|
| **Purpose** | Identify and sign blocks as validator | Sign transactions and on-chain operations |
| **When used** | Automatically by the node when validating blocks | Manually when executing transactions |
| **Location** | `persistent-data/config/priv_validator_key.json` | `persistent-data/keyring-file/` (encrypted keyring) |
| **Recovery** | Depends on initialization mode | Always recoverable with seed phrase |
| **Management** | Automatically generated during initialization | Manually managed by adding keys |
| **Multiple keys** | Only one key per node | Multiple keys can coexist |
| **Use in validators** | Critical - without it you cannot validate blocks | Recommended - for on-chain operations |
| **Use in full nodes** | Not critical - automatically generated | Not necessary |

## Private Validator Key

The **Private Validator Key** (`priv_validator_key.json`) is the cryptographic identity of your validator on the blockchain.

### Characteristics

- **One key per node** - Each node has exactly one Private Validator Key
- **Automatically generated** - During node initialization
- **Signs blocks** - Automatically used by the node to sign blocks it proposes or validates
- **Permanent identity** - Once registered on the blockchain, it's permanently linked to your validator
- **Recoverability depends on mode** - Only recoverable if you used [recovery initialization]({{< relref "../drive/guides/blockchain-nodes/initialization/recovery-initialization" >}})

### When It's Used

- Automatically when the node proposes a new block
- Automatically when the node validates blocks from other validators
- No manual intervention required - the node uses it internally

For more information, see [Private Validator Key]({{< relref "private-validator-key" >}}).

## Keyring

The **keyring** is a secure storage where you can keep multiple cryptographic keys for different purposes.

### Characteristics

- **Multiple keys** - You can have several keys in the same keyring
- **Manual management** - You decide which keys to add and when
- **Signs transactions** - Keys are used to sign on-chain transactions
- **Always recoverable** - You can always restore keys using their seed phrase
- **Password protected** - The keyring is encrypted and protected by a password

### When It's Used

- Manually when you execute on-chain transactions
- To create a validator (`create-validator`)
- To delegate tokens
- For governance operations
- For any operation that requires cryptographic authentication

For more information, see [Keyring]({{< relref "keyring" >}}).

## Relationship Between Both

Although they are separate components, **it's highly recommended to use the same seed phrase for both**:

### Advantages of Using the Same Seed

- ✅ **Simplicity:** You only need to manage one seed phrase
- ✅ **Consistency:** Your validator and your operations are linked to the same identity
- ✅ **Fewer errors:** You avoid confusion about which key to use for which operation
- ✅ **Unified recovery:** If you need to restore everything, you only need one seed phrase

### Practical Example

When you create a validator, you need:

1. **Initialize the node with [recovery mode]({{< relref "../drive/guides/blockchain-nodes/initialization/recovery-initialization" >}})** using your seed phrase → Generates your `priv_validator_key`
2. **Add the same seed phrase to the keyring** → To be able to sign the `create-validator` transaction

If you use the same seed for both, everything works coherently and simply.

## Independence of Components

It's important to understand that they are **separate processes**:

- The Private Validator Key is generated during node initialization
- The keyring is managed independently, adding keys when you need them
- They can use the same seed phrase or different ones
- Technically it's possible to use different keys, but it's not recommended

## For Validators

If you're setting up a validator:

- **Private Validator Key:** You MUST initialize with [recovery mode]({{< relref "../drive/guides/blockchain-nodes/initialization/recovery-initialization" >}}) so it's recoverable
- **Keyring:** Recommended to add the same seed phrase for on-chain operations
- **Same seed:** Use the same seed phrase for both for simplicity and consistency

## For Full Nodes

If you're running a full node (not a validator):

- **Private Validator Key:** Automatically generated, not critical
- **Keyring:** Not necessary unless you want to perform transactions
- **No worries:** You don't need to manage keys manually

## See Also

- [Keyring]({{< relref "keyring" >}}) - What is a keyring and how it works
- [Private Validator Key]({{< relref "private-validator-key" >}}) - What is the Private Validator Key and its importance
- [Node Initialization]({{< relref "../drive/guides/blockchain-nodes/initialization" >}}) - Complete guide on initialization modes and recoverability
- [Understanding Keys]({{< relref "../drive/guides/blockchain-nodes/keys/understanding-keys" >}}) - Applied guide on how these concepts relate

