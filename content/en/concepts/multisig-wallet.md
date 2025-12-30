---
title: "Multisig Wallet"
weight: 4
---

A **multisig wallet** is a blockchain account that requires multiple signatures to authorize transactions, providing additional security and shared control over funds.

## What is a Multisig Wallet?

A multisig wallet is a special type of account that:

- **Requires multiple signatures** - Needs multiple participants to sign a transaction before it can be executed
- **Shared control** - No single individual can authorize transactions alone
- **Configurable threshold** - Defines how many signatures are needed (e.g., 2 of 3, 3 of 5)
- **Enhanced security** - Reduces the risk of fund loss due to compromise of a single key

## How It Works

A multisig wallet combines the **public keys** of multiple participants:

1. **Each participant has their own private key** - Kept secure and never shared
2. **Only public keys are shared** - Public keys are combined to create the multisig wallet
3. **M-of-N threshold** - Requires M participants out of N total to sign each transaction
4. **Distributed signing** - Each participant signs the transaction separately with their private key
5. **Signature combination** - Signatures are combined to create a valid transaction

## M-of-N Notation

A multisig wallet configuration is expressed as **M-of-N**:

- **M** - Minimum number of signatures required (threshold)
- **N** - Total number of participants (signers)

**Common examples:**
- **2-of-3** - Requires 2 signatures from 3 participants (tolerance to loss of 1 key)
- **3-of-5** - Requires 3 signatures from 5 participants (tolerance to loss of 2 keys)
- **2-of-2** - Requires both signatures (strict dual control)

## Advantages

- ✅ **Enhanced security** - Compromise of a single key does not allow stealing funds
- ✅ **Shared control** - Ideal for organizations, DAOs, or shared funds
- ✅ **Loss resistance** - You can lose some keys without losing access to funds
- ✅ **Audit trail** - All transactions require explicit consensus

## Disadvantages

- ⚠️ **Complexity** - Requires coordination between multiple participants
- ⚠️ **Processing time** - Transactions take longer as they require multiple signatures
- ⚠️ **Gas costs** - May require more gas due to multiple signature verifications

## Common Use Cases

- **Organizations** - Corporate funds requiring approval from multiple executives
- **DAOs** - Treasuries requiring consensus from multiple members
- **Validators** - Validation funds requiring multiple signers
- **Shared funds** - Accounts with distributed control among partners
- **Personal security** - Users who want additional protection against single key loss

## Differences from Simple Keys

| Aspect | Simple Key | Multisig Wallet |
|--------|------------|-----------------|
| **Signatures required** | 1 | M of N (configurable) |
| **Control** | Individual | Shared |
| **Security** | Depends on one key | Depends on multiple keys |
| **Complexity** | Low | Medium-High |
| **Speed** | Fast | Slower (requires coordination) |

## Creating a Multisig Wallet

Creating a multisig wallet **does not require sharing private keys or seed phrases**. Only the following are needed:

1. **Public keys from each participant** - Each one exports their public key
2. **Threshold configuration** - Decide how many signatures are required (M-of-N)
3. **Local combination** - A coordinator combines the public keys to create the wallet

For more information on how to create a multisig wallet, see [Multisig Operations]({{< relref "../drive/guides/blockchain-nodes/keys/multisig-operations" >}}).

## See Also

- [Multisig Threshold]({{< relref "multisig-threshold" >}}) - How the M-of-N threshold works
- [Multisig Signer]({{< relref "multisig-signer" >}}) - What is a signer and their role
- [Key]({{< relref "key" >}}) - Basic concepts of cryptographic keys
- [Keyring]({{< relref "keyring" >}}) - How keys are stored
- [Multisig Operations]({{< relref "../drive/guides/blockchain-nodes/keys/multisig-operations" >}}) - Practical guide to create and use multisig wallets

