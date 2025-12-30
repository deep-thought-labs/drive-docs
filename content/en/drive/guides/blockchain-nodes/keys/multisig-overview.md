---
title: "Multisig Wallets Overview"
weight: 52224
---

Introduction to multisig wallets and when to use them in the Drive ecosystem.

> [!NOTE]
> **Fundamental Concepts**
>
> Before continuing, make sure you understand:
> - [Multisig Wallet]({{< relref "../../../../../concepts/multisig-wallet" >}}) - What a multisig wallet is and what it's used for
> - [Multisig Threshold]({{< relref "../../../../../concepts/multisig-threshold" >}}) - How the M-of-N threshold works
> - [Multisig Signer]({{< relref "../../../../../concepts/multisig-signer" >}}) - What a signer is and their role
> - [Key]({{< relref "../../../../../concepts/key" >}}) - Basic concepts of cryptographic keys
> - [Keyring]({{< relref "../../../../../concepts/keyring" >}}) - How keys are stored

## What is a Multisig Wallet?

A [multisig wallet]({{< relref "../../../../../concepts/multisig-wallet" >}}) is a blockchain account that requires multiple signatures to authorize transactions, providing additional security and shared control over funds.

Unlike a simple key that requires a single signature, a multisig wallet combines the public keys of multiple participants and requires a minimum number of them (the [threshold]({{< relref "../../../../../concepts/multisig-threshold" >}})) to sign each transaction.

## When to Use Multisig

### Recommended Use Cases

- **Organizations** - Corporate funds requiring approval from multiple executives
- **DAOs** - Treasuries requiring consensus from multiple members
- **Validators** - Validation funds requiring multiple signers
- **Shared funds** - Accounts with distributed control among partners
- **Personal security** - Users who want additional protection against single key loss

### When NOT to Use Multisig

- **Simple personal use** - If you only need a personal account, a simple key is more practical
- **Frequent transactions** - Multisig wallets require more time and coordination
- **Untrustworthy participants** - If you cannot coordinate with other participants, a multisig is not practical

## Advantages and Disadvantages

### Advantages

- ✅ **Enhanced security** - Compromise of a single key does not allow stealing funds
- ✅ **Shared control** - Ideal for organizations or shared funds
- ✅ **Loss resistance** - You can lose some keys without losing access to funds
- ✅ **Audit trail** - All transactions require explicit consensus

### Disadvantages

- ⚠️ **Complexity** - Requires coordination between multiple participants
- ⚠️ **Processing time** - Transactions take longer as they require multiple signatures
- ⚠️ **Gas costs** - May require more gas due to multiple signature verifications

## Differences from Simple Keys

| Aspect | Simple Key | Multisig Wallet |
|--------|------------|-----------------|
| **Signatures required** | 1 | M of N (configurable) |
| **Control** | Individual | Shared |
| **Security** | Depends on one key | Depends on multiple keys |
| **Complexity** | Low | Medium-High |
| **Speed** | Fast | Slower (requires coordination) |

For more details, see [Multisig Wallet]({{< relref "../../../../../concepts/multisig-wallet" >}}).

## Recommended Reading Order

To get the most out of this multisig wallet documentation, we recommend following this order:

### 1. 📚 Understand the Concepts

- **[Multisig Wallet]({{< relref "../../../../../concepts/multisig-wallet" >}})** - What it is and how it works
- **[Multisig Threshold]({{< relref "../../../../../concepts/multisig-threshold" >}})** - How M-of-N works
- **[Multisig Signer]({{< relref "../../../../../concepts/multisig-signer" >}})** - What a signer is

### 2. 🔧 Learn the Operations

- **[Multisig Operations]({{< relref "multisig-operations" >}})** - How to create and use multisig wallets:
  - Create multisig wallet
  - Sign transactions with multiple signers
  - Combine signatures
  - Send transactions

### 3. 🔐 Security Best Practices

- **[Multisig Security]({{< relref "multisig-security" >}})** - Specific best practices:
  - Secure key distribution
  - Signer management
  - Recovery procedures

## Current Limitations

> [!NOTE]
> **Graphical Interface Not Available**
>
> Currently, Drive's graphical interface does not support multisig wallet operations. All operations must be performed using commands in the container bash.

For commands that are not available through `drive.sh`, you will need to access the container bash directly and execute native `infinited` commands.

## Next Steps

Now that you understand the fundamental concepts:

- **[Multisig Operations]({{< relref "multisig-operations" >}})** - Step-by-step guide to create and use multisig wallets
- **[Multisig Security]({{< relref "multisig-security" >}})** - Security best practices
- **[Key Management Operations]({{< relref "operations" >}})** - For operations with simple keys that are available in the graphical interface

## See Also

- [Multisig Wallet]({{< relref "../../../../../concepts/multisig-wallet" >}}) - Atomic concept about multisig wallets
- [Multisig Threshold]({{< relref "../../../../../concepts/multisig-threshold" >}}) - Atomic concept about thresholds
- [Multisig Signer]({{< relref "../../../../../concepts/multisig-signer" >}}) - Atomic concept about signers
- [Key]({{< relref "../../../../../concepts/key" >}}) - Basic concepts of keys
- [Keyring]({{< relref "../../../../../concepts/keyring" >}}) - How keys are stored

