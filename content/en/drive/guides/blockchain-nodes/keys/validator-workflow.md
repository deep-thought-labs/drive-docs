---
title: "Workflow for Validators"
weight: 52223
---

Step-by-step guide to set up cryptographic keys when acting as a validator on the blockchain.

> [!NOTE]
> **Before Starting**
>
> It's highly recommended to first read [Security Best Practices]({{< relref "security" >}}) to understand how to properly protect your keys before following this workflow.

## Introduction

This document provides a **suggested step-by-step workflow** to set up cryptographic keys when acting as a validator on the blockchain.

> [!NOTE]
> **Complete Information in Other Sections**
>
> This workflow is a guide of suggested steps. Complete information about each operation is documented in their respective sections:
>
> - **Create keys:** [Key Management Operations]({{< relref "operations" >}})
> - **Initialize node:** [Node Initialization]({{< relref "../initialization" >}})
> - **Verify initialization:** [Post-Initialization Verification]({{< relref "../initialization/verification" >}})
> - **Backup seed phrase:** [Security Best Practices]({{< relref "security" >}})

For information on how to create the validator on the blockchain (`create-validator` transaction) and other operations related to validation, see the specific documentation on validation operations.

## Step-by-Step Workflow

Follow these steps in order to set up your validator:

## Step 1: Create Key

Create a cryptographic key using one of the available methods. You can use either method:

- **Dry-Run:** Generates the key and you store the seed phrase directly. It's not saved in the keyring.
- **Generate and Save Key:** Generates the key and automatically saves it in the keyring.

> [!NOTE]
> **Complete Information**
>
> For detailed step-by-step instructions on how to create keys, including graphical interface images and command line commands, see [Key Management Operations]({{< relref "operations" >}}):
> - [Generate Key (Dry-Run)]({{< relref "operations#generate-key-dry-run" >}})
> - [Generate and Save Key Directly]({{< relref "operations#generate-and-save-key-directly" >}})

> [!IMPORTANT]
> **Key in Keyring to Create Validator**
>
> If you're going to create a new validator on the blockchain, **it's important that your key is stored in the keyring** before executing the `create-validator` transaction. This transaction requires a key from the keyring to sign it.
>
> - If you used **"Generate and Save Key"**, the key is already in the keyring and you can continue.
> - If you used **Dry-Run**, make sure to add the key to the keyring (see [Step 4](#step-4-add-key-to-keyring-if-you-used-dry-run)) before creating the validator.

## Step 2: Backup Seed Phrase

**⚠️ CRITICAL:** Write and backup the shown seed phrase immediately, regardless of the method you used to create the key.

> [!NOTE]
> **Complete Information**
>
> For backup options, security recommendations, and best practices, see [Security Best Practices]({{< relref "security" >}}), which includes:
> - Backup options (paper, metal, encrypted storage)
> - What to NEVER do with your seed phrase
> - Keyring protection
> - General server security

## Step 3: Initialize Node with Recovery

Use the seed phrase you just created and backed up to initialize your node using recovery mode.

> [!IMPORTANT]
> **Required for Validators**
>
> For validators, **you MUST use recovery initialization** to ensure you can always recover your Private Validator Key. Simple initialization is not suitable for validators.

> [!NOTE]
> **Complete Information**
>
> For the complete recovery initialization procedure, see [Recovery Initialization]({{< relref "../initialization/recovery-initialization" >}}), which includes:
> - What is recovery initialization and its characteristics
> - Prerequisites
> - Step-by-step instructions using the graphical interface (with images)
> - Instructions using command line
> - What the initialization process does
> - Advantages for validators
> - Troubleshooting
>
> To understand the differences between initialization modes and when to use each one, see [Node Initialization]({{< relref "../initialization" >}}).

## Step 4: Add Key to Keyring (If You Used Dry-Run)

> [!IMPORTANT]
> **Necessary to Create Validator (Only for New Validators)**
>
> If you used the Dry-Run method and **you're going to create a new validator** on the blockchain, **you must add the key to the keyring** before executing the `create-validator` transaction. This transaction requires a key from the keyring to sign it.
>
> - If you used **"Generate and Save Key"**, the key is already in the keyring and you can continue to the next step.
> - If you used **Dry-Run**, you must add the key to the keyring now.
>
> **If you already created your validator previously** and you're only restoring the node to work on a different server, **it's not necessary to add the key to the keyring**. Just having the correct `priv_validator_key.json` file in the configuration folder (`persistent-data/config/priv_validator_key.json`), the node will automatically validate when it's active and synchronized.

> [!NOTE]
> **Complete Information**
>
> For detailed step-by-step instructions on how to add an existing key to the keyring, including graphical interface images and command line commands, see [Add Existing Key from Seed Phrase]({{< relref "operations#add-existing-key-from-seed-phrase" >}}) in Key Management Operations.

## Step 5: Verify Private Validator Key

> [!TIP]
> **Recommended Practice: Recoverability Verification**
>
> Before creating your validator on the blockchain, it's highly recommended that you verify you can correctly recover your Private Validator Key. This will give you confidence that you'll always be able to restore your validator if necessary.

### Basic Verification

First, verify that initialization completed correctly.

> [!NOTE]
> **Complete Information**
>
> For basic post-initialization verification, see [Post-Initialization Verification]({{< relref "../initialization/verification" >}}), which includes:
> - Configuration file verification
> - Private Validator Key verification
> - Genesis file verification
> - Chain ID verification
> - Verification checklist
> - Common problems

### Verification Practice: Reinitialize the Node

> [!NOTE]
> **Complete Information**
>
> For the complete recoverability verification practice (reinitialize the node and verify that the same key is generated), see the section [Special Verification for Recovery Mode]({{< relref "../initialization/verification#special-verification-for-recovery-mode" >}}) in Post-Initialization Verification, which includes:
> - Complete step-by-step procedure
> - How to stop the node and delete data
> - How to reinitialize with the same seed phrase
> - How to verify that exactly the same key was generated
> - Benefits of this practice

## Migration of Existing Validators

If your validator **already exists** on the blockchain and you're migrating it to another server or restoring it after a failure:

> [!IMPORTANT]
> **You Don't Need to Create the Validator Again**
>
> The `create-validator` transaction is a **unique action in the validator's lifecycle**. If your validator is already registered on the blockchain, you do NOT need to execute this transaction again.

**What you need to do:**

1. **Make sure you have a synchronized and active blockchain node**
2. **Make sure the node has the correct `priv_validator_key.json` file** in its configuration folder
   - Location: `persistent-data/config/priv_validator_key.json`
   - This file must be exactly the same as your original validator had

**How it works:**
- Any synchronized node on the chain that has your validator's `priv_validator_key.json` file in its configuration folder **will effectively be the validator**
- The node will use this key to sign blocks automatically
- You don't need to execute any additional transactions

> [!WARNING]
> **⚠️ CRITICAL WARNING: Double Signing**
>
> **NEVER have two active blockchain nodes with the same Private Validator Key at the same time.**
>
> This generates **double signing**, which is a serious bad practice among validator nodes and is severely punished on the blockchain:
>
> - ⚠️ **Reprimands** on the blockchain
> - ⚠️ **Risk of losing part of your staked tokens** due to the corresponding penalty
> - ⚠️ **Possible loss of the validator** in extreme cases
>
> **Always make sure to:**
> - Completely stop the previous node before starting a new one with the same key
> - Not share the `priv_validator_key.json` file with other people
> - Not have copies of the file on multiple active servers simultaneously
> - Verify that only one node is active with your Private Validator Key at any time

## Workflow Summary

### For New Validators

1. ✅ **Create Key** - Generate your key using Dry-Run or Generate and Save Key
2. ✅ **Backup Seed Phrase** - Store your seed phrase securely
3. ✅ **Initialize Node with Recovery** - Use your seed phrase to initialize the node
4. ✅ **Add Key to Keyring** - Make sure your key is in the keyring (necessary for `create-validator`)
5. ✅ **Verify Private Validator Key** - Verify that the key was generated correctly and perform recoverability tests
6. ✅ **Create Validator** - Execute the `create-validator` transaction on the blockchain (see documentation on validation operations)

### For Migration of Existing Validators

1. ✅ **Ensure synchronized node** - Your node must be synchronized with the blockchain
2. ✅ **Have the correct `priv_validator_key.json`** - The file must be in `persistent-data/config/priv_validator_key.json`
3. ✅ **Verify only one node is active** - Make sure there's no other active node with the same key (avoid double signing)

## See Also

- [Key Management Operations]({{< relref "operations" >}}) - Complete guide of all available operations
- [Security Best Practices]({{< relref "security" >}}) - Security recommendations
- [Node Initialization]({{< relref "../initialization" >}}) - How to initialize a node using your keys
- [Key Management Issues]({{< relref "../../../troubleshooting/key-management-issues" >}}) - Troubleshooting common problems
- [Understanding Keys]({{< relref "understanding-keys" >}}) - Fundamental concepts about keys and validators

