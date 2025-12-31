---
title: "Multisig Threshold"
weight: 5
---

The **multisig threshold** is the minimum number of signatures required to authorize a transaction from a [multisig wallet]({{< relref "multisig-wallet" >}}).

## What is the Threshold?

The threshold is the value **M** in the **M-of-N** notation:

- **M** - Minimum number of signatures required (threshold)
- **N** - Total number of participants (signers)

**Example:** In a **2-of-3** configuration:
- **N = 3** - There are 3 total participants
- **M = 2** - At least 2 signatures are required to authorize a transaction

## How It Works

The threshold determines:

1. **How many signatures are needed** - A transaction requires exactly M valid signatures
2. **Fault tolerance** - You can lose up to (N - M) keys without losing access
3. **Security level** - A higher threshold requires more consensus

## Configuration Examples

### 2-of-3 (Recommended for 3 Participants)

- **Signatures required:** 2 of 3
- **Tolerance:** You can lose 1 key
- **Use:** Balance between security and flexibility
- **Example:** 3 partners, 2 must approve each transaction

### 3-of-5 (Recommended for 5 Participants)

- **Signatures required:** 3 of 5
- **Tolerance:** You can lose 2 keys
- **Use:** Higher security with more participants
- **Example:** DAO with 5 committee members

### 2-of-2 (Dual Control)

- **Signatures required:** Both (2 of 2)
- **Tolerance:** You cannot lose any key
- **Use:** Strict control between two parties
- **Example:** Two partners who must approve each transaction

### 1-of-2 (Not Recommended)

- **Signatures required:** 1 of 2
- **Tolerance:** You can lose 1 key
- **Use:** ⚠️ **Does not provide additional security** - Anyone can authorize
- **Note:** This configuration makes no sense for security, only for redundancy

## Considerations for Choosing the Threshold

### Security vs Flexibility

- **High threshold (e.g., 3-of-3)** - Maximum security, but less flexibility
- **Medium threshold (e.g., 2-of-3)** - Balance between security and flexibility
- **Low threshold (e.g., 1-of-2)** - Little additional security

### Key Loss Tolerance

The number of keys you can lose without losing access is: **N - M**

- **2-of-3:** You can lose 1 key ✅
- **3-of-5:** You can lose 2 keys ✅
- **2-of-2:** You cannot lose any key ⚠️

### General Rule

For a secure and practical configuration:

- **M must be greater than 1** - At least 2 signatures required
- **M must be less than N** - Not everyone must be required to sign
- **M must be at least half of N** - Requires majority consensus

**Recommended formula:** `M = ⌈N/2⌉ + 1` (more than half)

## Impact on Operations

### Transaction Creation

When you create a transaction from a multisig wallet:

1. The unsigned transaction is generated
2. It is distributed to all participants
3. At least M participants must sign it
4. Signatures are combined
5. The transaction is sent to the blockchain

### Processing Time

- **Low threshold:** Faster (less coordination needed)
- **High threshold:** Slower (more participants must be available)

## See Also

- [Multisig Wallet]({{< relref "multisig-wallet" >}}) - What is a multisig wallet
- [Multisig Signer]({{< relref "multisig-signer" >}}) - What is a signer
- [Multisig Operations]({{< relref "../drive/guides/blockchain-nodes/keys/multisig-operations" >}}) - How to create wallets with different thresholds

