---
title: "Multisig Signer"
weight: 6
---

A **multisig signer** is a participant who possesses one of the private keys needed to sign transactions from a [multisig wallet]({{< relref "multisig-wallet" >}}).

## What is a Signer?

A signer is:

- **Owner of a private key** - Has access to one of the keys that form part of the multisig wallet
- **Authorized participant** - Can sign transactions for the multisig wallet
- **Part of consensus** - Their signature counts towards the required [threshold]({{< relref "multisig-threshold" >}})

## Signer Role

### Responsibilities

1. **Keep their private key secure** - Protect their seed phrase and private key
2. **Sign transactions when requested** - Review and sign proposed transactions
3. **Verify transactions** - Ensure transactions are legitimate before signing
4. **Coordinate with other signers** - Communicate to complete transactions that require multiple signatures

### Powers

- ✅ **Can sign transactions** - Their signature counts towards the required threshold
- ✅ **Can verify transactions** - Can review transactions before signing
- ❌ **Cannot authorize alone** - Needs other signers to also sign (unless threshold is 1)

## How Signers are Added

To add a signer to a multisig wallet:

1. **The signer generates or exports their public key** - Without sharing the private key
2. **The public key is added to the wallet** - Combined with other public keys
3. **Configuration is updated** - The wallet is recreated with the new set of signers

> [!NOTE]
> **Private Keys Are Not Shared**
>
> Signers **never** share their private keys or seed phrases. They only share their public keys to create the multisig wallet.

## How Signers are Removed

To remove a signer:

1. **Recreate the wallet** - A new multisig wallet is created without the public key of the signer to be removed
2. **Migrate funds** - Funds are transferred from the old wallet to the new one
3. **Update configuration** - All participants update their local configuration

> [!WARNING]
> **Removing Signers Requires Migration**
>
> Removing a signer requires creating a new wallet and migrating funds. It is not possible to simply "remove" a key from an existing wallet.

## Types of Signers

### Active Signer

- Regularly participates in transaction signing
- Keeps their key accessible and available
- Responds quickly to signing requests

### Backup Signer

- Has a key but does not actively participate
- Used as backup in case of loss of other keys
- Only activated when needed to reach the threshold

### Emergency Signer

- Has a key stored ultra-securely (e.g., safe deposit box)
- Only used in emergency situations
- Can help recover access if other keys are lost

## Signer Security

### Private Key Protection

Each signer must:

- **Backup their seed phrase** - Store it securely and offline
- **Use secure storage** - Consider hardware wallets or encrypted storage
- **Never share** - Never share the private key or seed phrase with anyone
- **Use secure channels** - Communicate with other signers through encrypted channels

### Access Management

- **Geographic distribution** - Ideally, signers are in different locations
- **Independence** - Each signer must be independent and not controlled by others
- **Rotation** - Consider rotating signers periodically for greater security

## Coordination Between Signers

### Signing Process

1. **A coordinator generates the transaction** - Creates the unsigned transaction
2. **Distributes the transaction** - Shares the transaction with all signers
3. **Each signer reviews and signs** - Each one signs with their private key
4. **Signatures are combined** - The coordinator combines the signatures
5. **Transaction is sent** - The signed transaction is sent to the blockchain

### Communication

- **Secure channels** - Use encrypted communication (Signal, PGP, etc.)
- **Verification** - Each signer must verify the transaction before signing
- **Transparency** - All signers must be able to see proposed transactions

## See Also

- [Multisig Wallet]({{< relref "multisig-wallet" >}}) - What is a multisig wallet
- [Multisig Threshold]({{< relref "multisig-threshold" >}}) - How the M-of-N threshold works
- [Key]({{< relref "key" >}}) - Basic concepts of cryptographic keys
- [Multisig Operations]({{< relref "../drive/guides/blockchain-nodes/keys/multisig-operations" >}}) - How to add and manage signers
- [Multisig Security]({{< relref "../drive/guides/blockchain-nodes/keys/multisig-security" >}}) - Security best practices for signers

