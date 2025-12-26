---
title: "Delete Node Data"
weight: 5225
---

Guide to delete blockchain node data. This operation deletes all node data, including synchronized blocks, application state, and cryptographic keys.

> [!WARNING]
> **⚠️ CRITICAL WARNING: Delete Node Data**
>
> **This operation permanently deletes:**
> - All synchronized blocks
> - Application state
> - Cryptographic keys (if not backed up)
> - Configuration files
>
> **Make sure you have backups before deleting data, especially if you're a validator.**
>
> **For validators:** If you used recovery initialization, you can recover your Private Validator Key using your seed phrase. If you don't have the seed phrase backed up, you will permanently lose access to your validator.

## When to Delete Node Data?

You may need to delete node data in the following cases:

- **Reinitialize the node** - To change the initialization mode (simple to recovery or vice versa)
- **Resolve synchronization issues** - To start from scratch if the node has synchronization problems
- **Change networks** - To connect to a different network
- **Verify recoverability** - To test that you can recover your validator using your seed phrase (see [Post-Initialization Verification]({{< relref "initialization/verification#special-verification-for-recovery-mode" >}}))

## Prerequisites

Before deleting node data:

1. **Stop the node** - The node must be stopped before deleting data
2. **Backups** - Make sure you have backups of:
   - Your seed phrase (if you used recovery mode)
   - Your Private Validator Key (`priv_validator_key.json`) if you didn't use recovery
   - Any custom configuration you've made

> [!IMPORTANT]
> **Difference between Container and Node**
>
> It's important to understand the difference:
> - **Container:** Is the Docker environment where the node lives
> - **Node:** Is the blockchain process running inside the container
>
> To delete node data, you need to **stop the node** (not necessarily the container) and then **delete node data** before reinitializing.

## Using Graphical Interface (Recommended)

The graphical interface is the safest and clearest way to delete node data, as it shows clear warnings before proceeding.

### Step 1: Stop the Node

First, make sure the node is stopped:

1. Open the graphical interface (see [Graphical Interface]({{< relref "graphical-interface" >}}))

2. Navigate: Main Menu → **"Node Operations"** → **"Stop Node"** (if the node is running)

   ![Stop Node selected](/images/node-ui-operations-op2-stop.png)

### Step 2: Delete Node Data

Once the node is stopped:

1. Navigate: Main Menu → **"Node Operations"** → **"Advanced Operations"** → **"Delete Node Data"**

   ![Delete Node Data selected](/images/node-ui-advanced-operations-op4-clean-data.png)

2. **Read carefully the warning** shown about permanent data loss

3. Confirm the operation when prompted

The graphical interface will automatically delete all node data safely.

## Using Command Line

If you prefer to use the command line, you can delete node data manually.

### Step 1: Stop the Node

First, make sure the node is stopped:

```bash
./drive.sh exec infinite node-stop
```

Verify that the node is stopped:

```bash
./drive.sh exec infinite node-process-status
```

### Step 2: Delete Node Data

You have two options to delete data:

#### Option A: Delete from Host (Recommended)

This is the most direct and recommended way:

```bash
# Delete all content from the persistent-data directory
rm -rf ./persistent-data/*

# Or delete only node data (keeping other data if any)
rm -rf ./persistent-data/data
rm -rf ./persistent-data/config
```

#### Option B: Delete from Container

If you prefer to do it from inside the container:

```bash
# Access the container shell
./drive.sh exec infinite bash

# Inside the container, delete data
rm -rf /home/ubuntu/.infinited/data
rm -rf /home/ubuntu/.infinited/config

# Exit the shell
exit
```

## What Gets Deleted

When you delete node data, the following components are removed:

### Blockchain Database

- **`persistent-data/data/`** - Contains:
  - All synchronized blocks
  - Transaction history
  - Application state
  - Indexes for fast searches

### Configuration Files

- **`persistent-data/config/`** - Contains:
  - `config.toml` - General node configuration
  - `app.toml` - Blockchain application configuration
  - `client.toml` - Client configuration
  - `genesis.json` - Blockchain genesis file
  - `priv_validator_key.json` - Private Validator Key (critical for validators)

### What is NOT Deleted (if it exists)

- **`persistent-data/keys/`** - Keyring (if it's in a separate location)
- Other directories you may have created in `persistent-data/`

## After Deleting Data

After deleting node data, you need to reinitialize the node:

### For Validators

If you're a validator, **you MUST** use [Recovery Initialization]({{< relref "initialization/recovery-initialization" >}}) with your seed phrase to recover your Private Validator Key:

1. Use the same seed phrase you used originally
2. The node will generate exactly the same Private Validator Key
3. You can verify that the key is the same by comparing it with a backup

For more information on how to verify that you recovered the same key, see [Post-Initialization Verification]({{< relref "initialization/verification#special-verification-for-recovery-mode" >}}).

### For Full Nodes

If you're a full node, you can use either method:

- **[Simple Initialization]({{< relref "initialization/simple-initialization" >}})** - Generates a new random key
- **[Recovery Initialization]({{< relref "initialization/recovery-initialization" >}})** - If you want to maintain consistency

For more information on initialization, see [Node Initialization]({{< relref "initialization" >}}).

## Verification Practice: Reinitialize the Node

This practice allows you to verify that you can always recover exactly the same Private Validator Key using your seed phrase. It's especially useful for validators who want to confirm that their backup process works correctly.

> [!TIP]
> **Recommended Practice: Recoverability Verification**
>
> Before creating your validator on the blockchain, it's highly recommended that you verify you can correctly recover your Private Validator Key. This will give you confidence that you'll always be able to restore your validator if necessary.

### Complete Procedure

1. **Note or save the content of your Private Validator Key:**
   ```bash
   cat persistent-data/config/priv_validator_key.json > my-validator-key-backup.json
   ```

2. **Stop the node:**
   - Use the graphical interface: **"Node Operations"** → **"Stop Node"**
   - Or use command line: `./drive.sh exec infinite node-stop`

3. **Delete node data:**
   - Use the graphical interface: **"Node Operations"** → **"Advanced Operations"** → **"Delete Node Data"**
   - Or delete manually: `rm -rf ./persistent-data/data ./persistent-data/config`

4. **Reinitialize the node with the same seed phrase:**
   - Follow the complete procedure of [Recovery Initialization]({{< relref "initialization/recovery-initialization" >}}) using exactly the same seed phrase you used before

5. **Verify that exactly the same key was generated:**
   ```bash
   diff persistent-data/config/priv_validator_key.json my-validator-key-backup.json
   ```

**Expected result:** Should be exactly the same key. If it's different, something went wrong in the process.

**Benefits of this practice:**
- ✅ Gives you confidence that you'll always be able to restore your validator
- ✅ Helps you familiarize yourself with the process
- ✅ Allows you to detect problems before creating the validator on the blockchain
- ✅ Creates expertise in key management

> [!NOTE]
> **Repeat the Procedure**
>
> You can repeat this verification procedure 2-3 times to make sure you always get the same result. This will help you be confident that if you perform the procedure correctly, you'll always be able to backup or restore your validator node as many times as necessary.

## Troubleshooting

### I Cannot Delete Node Data

If you have problems deleting data:

1. **Make sure the node is stopped:**
   ```bash
   ./drive.sh exec infinite node-process-status
   ```
   If the node is running, stop it first.

2. **Verify directory permissions:**
   ```bash
   ls -la ./persistent-data/
   ```

3. **If there are permission problems, see:**
   - [Permission Issues]({{< relref "../../troubleshooting/permission-issues" >}})
   - [Container Management]({{< relref "../general/container-management" >}})

### Private Validator Key is Different After Reinitializing

If you used recovery mode and the key is different after reinitializing:

1. **Verify that you entered exactly the same seed phrase:**
   - There should be no extra spaces at the beginning or end
   - All words must be spelled correctly
   - Must be exactly the same phrase (12 or 24 words)

2. **Verify that you used the BIP39 standard format:**
   - The seed phrase must be valid according to the BIP39 standard

3. **Consider reinitializing with the correct seed phrase:**
   - If there's any doubt, try again with the correct seed phrase

### I Lost my Seed Phrase

If you lost your seed phrase and deleted node data:

- **For validators:** If you don't have the seed phrase backed up, **there's no way to recover your Private Validator Key**. You will permanently lose access to your validator.
- **For full nodes:** You can reinitialize with a new key, but you'll lose the previous node identity.

**Prevention:**
- Always backup your seed phrase before deleting data
- See [Security Best Practices]({{< relref "keys/security" >}}) for backup recommendations

## Next Steps

After deleting node data:

1. **[Node Initialization]({{< relref "initialization" >}})** - Reinitialize the node using the appropriate method
2. **[Post-Initialization Verification]({{< relref "initialization/verification" >}})** - Verify that initialization was successful
3. **[Start/Stop Node]({{< relref "start-stop-node" >}})** - Start your node after reinitializing

## See Also

- [Node Initialization]({{< relref "initialization" >}}) - How to initialize a node after deleting data
- [Recovery Initialization]({{< relref "initialization/recovery-initialization" >}}) - Required for validators
- [Post-Initialization Verification]({{< relref "initialization/verification" >}}) - Verify that initialization was successful
- [Start/Stop Node]({{< relref "start-stop-node" >}}) - How to manage the node lifecycle
- [Node Data]({{< relref "../../../../concepts/node-data" >}}) - Understand what node data is and its importance
- [Security Best Practices]({{< relref "keys/security" >}}) - How to backup your seed phrase securely

