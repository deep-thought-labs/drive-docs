---
title: "Multisig Security"
weight: 52226
---

Security best practices specific to multisig wallets.

> [!NOTE]
> **Fundamental Concepts**
>
> Before continuing, make sure you understand:
> - [Multisig Wallet]({{< relref "../../../../../concepts/multisig-wallet" >}}) - What a multisig wallet is
> - [Multisig Signer]({{< relref "../../../../../concepts/multisig-signer" >}}) - What a signer is
> - [Security Best Practices]({{< relref "security" >}}) - General key security

## Secure Distribution of Public Keys

When creating a multisig wallet, only public keys are shared, but you must still do this securely.

### Recommendations

1. **Encrypted channels** - Use encrypted communication to share public keys:
   - Encrypted email (PGP)
   - Signal or Telegram with encryption
   - Secure private channels
   - Never use plain email or unencrypted messaging

2. **Verification** - Each participant must verify they received the correct public key:
   - Compare with the public key they exported
   - Verify that the multisig wallet address matches

3. **Transparency** - All participants must be able to see all public keys that form part of the wallet

4. **Multiple verification** - Verify public keys through multiple channels or sources:
   - Receive the public key directly from the participant
   - Verify that the multisig wallet address matches when everyone recreates it
   - Compare received public keys with those each participant exported
   - Do not trust only one intermediary or a single communication channel

### ⚠️ NEVER

- Share private keys or seed phrases
- Share keyring files
- Use unencrypted communication channels
- Trust a single source or intermediary to receive public keys without verification

## Signer Management

### Signer Selection

1. **Independence** - Each signer must be independent and not controlled by others
2. **Geographic distribution** - Ideally, signers are in different locations
3. **Reliability** - Signers must be trustworthy people or entities
4. **Availability** - Signers must be available when signatures are needed

### Adding Signers

To add a new signer:

1. **Verify identity** - Make sure the new signer is who they claim to be
2. **Obtain public key** - Receive the new signer's public key securely
3. **Recreate wallet** - Create a new multisig wallet with the new set of signers
4. **Migrate funds** - Transfer funds from the old wallet to the new one
5. **Update configuration** - All participants update their local configuration

### Removing Signers

To remove a signer:

1. **Recreate wallet** - Create a new multisig wallet without the key of the signer to be removed
2. **Migrate funds** - Transfer funds from the old wallet to the new one
3. **Update configuration** - All participants update their local configuration

> [!WARNING]
> **Adding or Removing Signers Creates a New Wallet**
>
> ⚠️ **IMPORTANT:** Adding or removing signers **does NOT modify** the existing wallet. Instead, a **new multisig wallet with a new public address** is created.
>
> **Consequences:**
> - The old wallet's address remains unchanged
> - The new wallet has a completely different address
> - You must migrate all funds from the old wallet to the new one
> - Any reference to the old address (contracts, configurations, etc.) must be updated
>
> **It is not possible to modify signers of an existing wallet without changing its address.**

## Protection Against Partial Compromise

One of the advantages of multisig wallets is that compromise of a single key does not allow stealing funds. However, you must protect against partial compromises:

### Recommendations

1. **Adequate threshold** - Use a threshold that requires more than one signature (M > 1)
2. **Key distribution** - Do not store all keys in the same place
3. **Monitoring** - Monitor transactions to detect suspicious activity
4. **Rotation** - Consider rotating signers periodically

### Each Signer's Protection

Each signer must follow [security best practices]({{< relref "security" >}}):

- **Backup seed phrase** - Store it securely and offline
- **Use secure storage** - Consider hardware wallets or encrypted storage
- **Never share** - Never share the private key or seed phrase
- **Use secure channels** - Communicate with other signers through encrypted channels

## Recovery Procedures

### Loss of One Key

If a signer loses their key:

1. **Verify threshold** - Make sure you still have enough signers to reach the threshold
2. **Continue operations** - You can continue using the remaining keys
3. **Optional: Replace signer** - If necessary, you can add a new signer and recreate the wallet

### Loss of Multiple Keys

If you lose too many keys and cannot reach the threshold:

1. **Assess situation** - Determine how many keys you have available
2. **Contact other signers** - Coordinate with other signers to recover access
3. **Consider migration** - If necessary, recreate the wallet with a new set of signers

> [!WARNING]
> **Loss of Access**
>
> If you lose enough keys to not be able to reach the threshold, you will permanently lose access to funds in the multisig wallet. Make sure you have a backup plan.

## Signer Rotation

> [!NOTE]
> **What is Signer Rotation?**
>
> Signer rotation refers to the process of **replacing some or all signers** of a multisig wallet with new signers. This may involve:
> - Removing signers who are no longer trustworthy or available
> - Adding new signers to replace those removed
> - Changing the complete set of signers for security reasons
>
> **Important:** Rotation **is NOT recommended to be done frequently** because:
> - Requires creating a new wallet with a new address
> - Requires migrating all funds
> - Can interrupt ongoing operations
> - Can cause confusion if done too often

### When to Rotate

Consider rotating signers or recreating the multisig wallet **only when necessary**:

- A signer is no longer trustworthy or has been compromised
- A signer has lost their key and cannot recover it
- Major organizational changes require new signers
- **Do NOT rotate periodically** unless there is a specific security reason

> [!WARNING]
> **Frequent Rotation Not Recommended**
>
> Signer rotation should be an **exceptional** process, not routine. Each rotation:
> - Creates a new wallet with a new address
> - Requires fund migration
> - Can interrupt operations
> - Increases the risk of errors
>
> **Best practice:** Design your multisig wallet with trustworthy signers from the start and only rotate when absolutely necessary.

### Rotation Process

1. **Select new signers** - Identify who will be added/removed
2. **Obtain public keys** - Receive the public keys of the new signers
3. **Recreate wallet** - Create a new multisig wallet with the new set
4. **Migrate funds** - Transfer funds from the old wallet to the new one
5. **Update configuration** - All participants update their configuration
6. **Update references** - Update any reference to the old address (contracts, configurations, etc.)

## Custody Considerations

### Distributed Custody

- **Geographic distribution** - Ideally, keys are in different locations
- **Independence** - Each signer must have independent control of their key
- **Backup** - Each signer must have their own backup of their seed phrase

### Institutional Custody

> [!WARNING]
> **Cypherpunk Philosophy: "Not Your Keys, Not Your Crypto"**
>
> The cypherpunk philosophy promotes **self-custody** and **distrust of centralized institutions**. It is recommended:
>
> - ✅ **Manage your own keys** securely without trusting external organizations
> - ✅ **Use distributed custody** among trustworthy participants
> - ✅ **Maintain total control** over your private keys
> - ❌ **Avoid institutional custody** unless absolutely necessary
>
> Institutional custody is only recommended in specific cases where:
> - Regulatory or legal requirements demand it
> - The organization does not have technical capacity to manage keys securely
> - It involves corporate funds requiring specific compliance
>
> **In the best case, follow the cypherpunk philosophy and manage your own keys securely.**

If you **must** use an institution for custody (only in specific cases):

- **Verify reputation** - Make sure the institution is trustworthy and has a proven track record
- **Clear contracts** - Have clear contracts about responsibilities, limits, and procedures
- **Audit** - Conduct regular audits of operations and verify the institution follows best practices
- **Fund segregation** - Make sure your funds are segregated and not mixed with others
- **Exit plan** - Have a clear plan to recover your keys if you decide to change institutions

## Audit and Monitoring

### Transaction Monitoring

1. **Review all transactions** - Each signer must review transactions before signing
2. **Alerts** - Configure alerts for transactions from the multisig wallet
3. **Records** - Keep records of all transactions and signatures

### Regular Audit

1. **Verify signers** - Periodically verify that all signers remain trustworthy
2. **Review configuration** - Review the multisig wallet configuration
3. **Test recovery** - Periodically test recovery procedures

## Secure Communication

### Communication Channels

- **Encryption** - Always use encrypted communication
- **Identity verification** - Verify the identity of other signers before sharing information
- **Private channels** - Use private channels for communication about transactions

### Signing Process

1. **Transparency** - All signers must be able to see proposed transactions
2. **Verification** - Each signer must verify the transaction before signing
3. **Confirmation** - Confirm that you received and signed the correct transaction

## Multisig Wallets in Genesis

If a multisig wallet is included in the `genesis.json` file, the public address is fixed from the start of the chain. The address is calculated from the signers' public keys, so **you cannot modify signers without changing the address**.

### Considerations Before Including in Genesis

Before including a multisig wallet in the genesis, consider:

1. **Permanent signer selection** - Choose signers who will be trustworthy long-term, as changing them after launch may not be viable
2. **Purpose and context** - Fully understand **why** and **how** the wallet is being used in the genesis
3. **Appropriate threshold** - Configure a threshold that allows operations even if some signers are unavailable
4. **Documentation** - Clearly document who the signers are and how to contact them

### Limitations When Changing Signers After Launch

Changing signers after launch requires creating a new wallet with a new address. However, **depending on the context, this may not be viable**:

**Cases where changing the address is NOT possible:**

- **Programmed unlock funds** - If the wallet receives funds through a mechanism programmed in the genesis, the protocol will continue sending funds to the original address. You cannot modify the mechanism to send to a different address.

- **Automatic protocol mechanisms** - If the wallet receives automatic rewards, governance distributions, or treasury/module funds, these mechanisms are hardcoded in the genesis and will continue operating with the original address. **These mechanisms cannot be modified after launch.**

- **Module accounts or special permissions** - If the wallet has special permissions, these are linked to the specific address and cannot be transferred.

**Special case: Smart contracts**

- **Linked smart contracts** - If there are contracts programmed to send funds to that address, the behavior depends on the contract design:
  - **If the contract is well designed** - It may include functionality to update addresses through administration or governance functions, allowing the destination address to be changed without redeploying the contract.
  - **If the contract does not have this functionality** - It would require redeploying the contract and migrating all logic, which can be complex or unviable depending on the case.
  
  Unlike genesis mechanisms which are immutable, smart contracts can be designed with update capability if planned from the start.

> [!WARNING]
> **Changing Signers May Be Impossible**
>
> If the wallet in the genesis has a critical purpose (programmed unlock, automatic mechanisms, etc.), changing signers after launch may result in the original address continuing to receive funds indefinitely, while the new address will not receive those automatic funds.

### Recommendations

- If the wallet has a specific and critical purpose in the genesis, **do NOT change signers** after launch
- If you plan to change signers frequently, consider **NOT including the wallet in the genesis** and create it after launch
- If you must include it in the genesis, **make sure signers are permanent and trustworthy long-term**

## See Also

- [Multisig Signer]({{< relref "../../../../../concepts/multisig-signer" >}}) - Atomic concept about signers
- [Multisig Wallet]({{< relref "../../../../../concepts/multisig-wallet" >}}) - Atomic concept about multisig wallets
- [Security Best Practices]({{< relref "security" >}}) - General key security
- [Multisig Operations]({{< relref "multisig-operations" >}}) - How to create and use multisig wallets

