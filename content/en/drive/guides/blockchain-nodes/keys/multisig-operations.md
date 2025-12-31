---
title: "Multisig Wallet Operations"
weight: 52225
---

Step-by-step guide to create and use multisig wallets in the Drive ecosystem.

> [!NOTE]
> **Fundamental Concepts**
>
> Before continuing, make sure you understand:
> - [Multisig Wallet]({{< relref "../../../../../concepts/multisig-wallet" >}}) - What a multisig wallet is
> - [Multisig Threshold]({{< relref "../../../../../concepts/multisig-threshold" >}}) - How M-of-N works
> - [Multisig Signer]({{< relref "../../../../../concepts/multisig-signer" >}}) - What a signer is
> - [Key]({{< relref "../../../../../concepts/key" >}}) - Basic concepts of keys
> - [Keyring]({{< relref "../../../../../concepts/keyring" >}}) - How keys are stored

> [!NOTE]
> **Graphical Interface Not Available**
>
> Currently, Drive's graphical interface does not support multisig wallet operations. All operations must be performed using commands in the container bash.

## Preparation: Create Individual Keys

Before creating a multisig wallet, each participant must have their own individual key. These keys will be used to form the multisig wallet.

### Step 1: Each Participant Creates Their Key

Each participant must create their own individual key. **This operation is fully supported by the graphical interface**, so you can choose the method you prefer.

> [!NOTE]
> **Graphical Interface Available**
>
> Unlike multisig operations (which require command line), **creating and adding individual keys IS available in the graphical interface**. You can use either method according to your preference.

#### Option 1: Using Graphical Interface (Recommended)

1. Open the graphical interface: `./drive.sh exec infinite node-ui`
2. Navigate to **"Key Management"**
3. Select:
   - **"Generate Key (Dry-Run - Recommended)"** - To create a new key and backup the seed phrase
   - **"Generate and Save Key"** - To create and save directly
   - **"Add Existing Key from Seed Phrase"** - If you already have a seed phrase

For more information on how to use the graphical interface, see [Key Management Operations]({{< relref "operations" >}}).

#### Option 2: Using Command Line

```bash
cd drive/services/node0-infinite  # Or your corresponding service

# Create key with dry-run (recommended to backup seed phrase)
./drive.sh node-keys create participant1 --dry-run

# Or create and save directly
./drive.sh node-keys create participant1
```

For more information on how to create keys from command line, see [Key Management Operations]({{< relref "operations" >}}).

> [!IMPORTANT]
> **Backup Seed Phrase**
>
> Each participant must backup their seed phrase securely. This is the only way to recover their key. For more information, see [Security Best Practices]({{< relref "security" >}}).

### Step 2: Export Public Keys

Each participant must export their public key (without sharing the private key or seed phrase).

**Access container bash:**

```bash
cd drive/services/node0-infinite
./drive.sh exec infinite bash
```

**Inside the container, export the public key:**

```bash
# Show public key in JSON format
infinited keys show participant1 \
  --pubkey \
  --output json \
  --keyring-backend file \
  --home ~/.infinited

# Or show only the public key in text format
infinited keys show participant1 \
  --pubkey \
  --keyring-backend file \
  --home ~/.infinited
```

**Example output (JSON format):**
```json
{
  "@type": "/cosmos.crypto.secp256k1.PubKey",
  "key": "A/pubkey/base64/here"
}
```

> [!WARNING]
> **Only Share Public Keys**
>
> ⚠️ **NEVER** share your private key, seed phrase, or keyring file. Only share the public key (pubkey).

Each participant must send their public key to the coordinator securely (encrypted email, Signal, PGP, etc.).

## Create Multisig Wallet

The coordinator (one of the participants) will be responsible for creating the multisig wallet by combining the public keys.

### Step 1: Import Public Keys to Keyring

The coordinator must import each public key as an "offline-only" key in their keyring.

**Access container bash:**

```bash
cd drive/services/node0-infinite
./drive.sh exec infinite bash
```

**Inside the container, import each public key:**

```bash
# Import public key from participant 1
infinited keys add participant1_pub \
  --pubkey '{"@type":"/cosmos.crypto.secp256k1.PubKey","key":"A/pubkey/base64/participant1"}' \
  --keyring-backend file \
  --home ~/.infinited

# Import public key from participant 2
infinited keys add participant2_pub \
  --pubkey '{"@type":"/cosmos.crypto.secp256k1.PubKey","key":"A/pubkey/base64/participant2"}' \
  --keyring-backend file \
  --home ~/.infinited

# Import public key from participant 3
infinited keys add participant3_pub \
  --pubkey '{"@type":"/cosmos.crypto.secp256k1.PubKey","key":"A/pubkey/base64/participant3"}' \
  --keyring-backend file \
  --home ~/.infinited
```

> [!NOTE]
> **Public Key Format**
>
> Replace `"A/pubkey/base64/participantX"` with the actual public key of each participant in base64 format. The complete format must be valid JSON with the key type.

### Step 2: Create the Multisig Wallet

Once all public keys are imported, create the multisig wallet:

**Example for 2-of-3 (2 signatures required from 3 participants):**

```bash
infinited keys add my_multisig \
  --multisig participant1_pub,participant2_pub,participant3_pub \
  --multisig-threshold 2 \
  --keyring-backend file \
  --home ~/.infinited
```

**Example for 3-of-5 (3 signatures required from 5 participants):**

```bash
infinited keys add my_multisig \
  --multisig participant1_pub,participant2_pub,participant3_pub,participant4_pub,participant5_pub \
  --multisig-threshold 3 \
  --keyring-backend file \
  --home ~/.infinited
```

### Step 3: Get the Multisig Wallet Address

```bash
infinited keys show my_multisig \
  -a \
  --keyring-backend file \
  --home ~/.infinited
```

**Example output:**
```
infinite1abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
```

Share this address with all participants for verification. Each participant can recreate the multisig wallet locally with the same public keys to confirm that the address matches.

## Sign Transactions with Multisig

To send a transaction from a multisig wallet, a distributed signing process is required.

### Step 1: Generate Unsigned Transaction

The coordinator generates the unsigned transaction:

```bash
# Example: Token transfer
infinited tx bank send \
  $(infinited keys show my_multisig -a --keyring-backend file --home ~/.infinited) \
  infinite1recipient123... \
  1000000drop \
  --chain-id infinite_421018-1 \
  --generate-only \
  --keyring-backend file \
  --home ~/.infinited \
  > tx_unsigned.json
```

### Step 2: Each Signer Signs the Transaction

Each participant must sign the transaction with their private key. This is done in a distributed manner:

**Each participant (on their own node or machine):**

```bash
# Access container bash
cd drive/services/node0-infinite
./drive.sh exec infinite bash

# Sign the transaction with the participant's key
infinited tx sign tx_unsigned.json \
  --from participant1 \
  --multisig $(infinited keys show my_multisig -a --keyring-backend file --home ~/.infinited) \
  --sign-mode amino-json \
  --keyring-backend file \
  --home ~/.infinited \
  --output-document signature_participant1.json
```

Repeat this process for each participant who must sign (at least the number required by the threshold).

### Step 3: Combine Signatures

The coordinator combines the signatures from all participants who signed:

```bash
infinited tx multisign \
  tx_unsigned.json \
  my_multisig \
  signature_participant1.json \
  signature_participant2.json \
  --keyring-backend file \
  --home ~/.infinited \
  > tx_signed.json
```

> [!NOTE]
> **Number of Signatures**
>
> You must include at least the number of signatures required by the threshold (M). You can include more signatures if you wish, but only M are needed.

### Step 4: Send the Transaction

Once signatures are combined, send the transaction:

```bash
infinited tx broadcast tx_signed.json \
  --chain-id infinite_421018-1 \
  --keyring-backend file \
  --home ~/.infinited
```

## Verify Multisig Wallet

To verify that a multisig wallet was created correctly:

```bash
# Show multisig wallet information
infinited keys show my_multisig \
  --keyring-backend file \
  --home ~/.infinited

# Show only the address
infinited keys show my_multisig \
  -a \
  --keyring-backend file \
  --home ~/.infinited

# Show the public key
infinited keys show my_multisig \
  --pubkey \
  --keyring-backend file \
  --home ~/.infinited
```

## List Multisig Wallets

To see all keys (including multisig wallets) in your keyring:

```bash
# Using Drive commands (if the wallet is in the keyring)
cd drive/services/node0-infinite
./drive.sh node-keys list

# Or directly in the container
./drive.sh exec infinite bash
infinited keys list \
  --keyring-backend file \
  --home ~/.infinited
```

## See Also

- [Multisig Wallet]({{< relref "../../../../../concepts/multisig-wallet" >}}) - Atomic concept about multisig wallets
- [Multisig Threshold]({{< relref "../../../../../concepts/multisig-threshold" >}}) - Atomic concept about thresholds
- [Multisig Signer]({{< relref "../../../../../concepts/multisig-signer" >}}) - Atomic concept about signers
- [Key Management Operations]({{< relref "operations" >}}) - For operations with simple keys
- [Multisig Security]({{< relref "multisig-security" >}}) - Security best practices
- [Security Best Practices]({{< relref "security" >}}) - General key security

