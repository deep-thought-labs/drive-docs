---
title: "Recovery Initialization"
weight: 52232
---

Step-by-step guide to initialize a blockchain node using recovery mode. This mode is **required for [validator nodes]({{< relref "../keys/understanding-keys" >}})** and highly recommended for any node that needs to recover its identity.

## What is Recovery Initialization?

Recovery initialization uses a seed phrase to generate **always the same** [Private Validator Key]({{< relref "../../../../../concepts/private-validator-key" >}}), allowing you to recover it at any time.

**Characteristics:**
- ✅ **Recoverable** - You can always regenerate the same key with the seed phrase
- ✅ **Consistent** - The same seed always generates the same key
- ✅ **Portable** - You can restore your validator on any server
- ✅ **Required for validators** - Allows you to recover your validator if something fails

## Prerequisites

Before initializing with recovery, you need:

- **A seed phrase (12 or 24 words)** - You can create one using [Key Management]({{< relref "../keys" >}})
- **Secure backup of the seed phrase** - Make sure you have it backed up before continuing

For more information on how to create and backup a seed phrase, see:
- [Key Management Operations]({{< relref "../keys/operations" >}}) - How to generate keys and get your seed phrase
- [Security Best Practices]({{< relref "../keys/security" >}}) - How to backup your seed phrase securely

## Using Graphical Interface

1. Open the graphical interface (see [Graphical Interface]({{< relref "../graphical-interface" >}}))

2. Navigate: Main Menu → **"Node Operations"** → **"Advanced Operations"** → **"Initialize with Recovery (Validator)"**

   ![Initialize with Recovery selected](/images/node-ui-advanced-operations-op2-init-revery.png)

3. When prompted, enter your seed phrase (12 or 24 words)

4. Follow the on-screen instructions to complete initialization

## Using Command Line

### Simplified Syntax (Recommended)

```bash
./drive.sh node-init --recover
```

The script automatically:
- Detects that it's a `node-init` command
- Gets the service name from the `docker-compose.yml` in the current directory
- Adds `exec` and the service name
- Adds `-it` automatically (since `--recover` requires interactive mode)

### Complete Syntax (Alternative)

If you prefer to explicitly specify the service name:

```bash
./drive.sh exec infinite node-init --recover
```

The script will also add `-it` automatically if you don't specify it.

> [!TIP]
> **You Don't Need to Specify `-it`**
>
> The `drive.sh` script automatically detects that `node-init --recover` requires interactive mode and adds `-it` for you. You can omit it completely.

> [!NOTE]
> **What the Command Does**
>
> The command requests your seed phrase, always generates the same [Private Validator Key]({{< relref "../../../../../concepts/private-validator-key" >}}) using your seed phrase, creates configuration files, and downloads the official [genesis file]({{< relref "../../../../../concepts/genesis-file" >}}). For technical details of the process, see [Technical Initialization Flow]({{< relref "../../../internal-workings/initialization-flow" >}}).

### Expected Output

After running the command, you should see:

```
Enter your bip39 mnemonic
```

Enter your seed phrase (12 or 24 words) when prompted.

After entering the seed phrase correctly:

```
✅ Node initialized successfully!
```

> [!NOTE]
> **Created Files**
>
> Configuration files are created in `./persistent-data/config/` (host) or `/home/ubuntu/.infinited/config/` (container). For more details on the data structure, see [Node Data]({{< relref "../../../../../concepts/node-data" >}}).

## Advantages for Validators

If you initialize with recovery using a seed phrase, you can restore your validator at any time, on any server, simply by using the same seed phrase. This allows you to:

- **Move your validator to another server** - Simply initialize with the same seed phrase on the new server
- **Restore your validator after a system failure** - You don't lose your validator if the server fails
- **Have recovery certainty** - You'll always have access to your validator as long as you have your seed phrase

> [!NOTE]
> **Workflow for Validators**
>
> If you're following the complete workflow for validators, after initializing with recovery, continue with the following workflow steps:
> - Add the key to the keyring (if you used Dry-Run)
> - Verify the Private Validator Key
> - Create the validator on the blockchain
>
> See [Workflow for Validators]({{< relref "../keys/validator-workflow" >}}) for the complete step-by-step flow.

## Verification

After initializing, verify that everything was created correctly. See [Post-Initialization Verification]({{< relref "verification" >}}) for more details.

**Important:** For validators, it's especially important to verify that the Private Validator Key was generated correctly and that you can recover it using the same seed phrase.

## Troubleshooting

### Error: "Invalid mnemonic"

If you receive this error when using recovery mode:

- **Verify that you entered exactly the same seed phrase** (12 or 24 words)
- **Make sure there are no extra spaces** at the beginning or end
- **Verify that all words are spelled correctly**
- **Make sure you're using the BIP39 standard format**

### Error: "Node already initialized"

If you receive this error, it means the node was already initialized previously. To reinitialize:

1. **Stop the node** (if it's running)
2. **Delete node data** using the graphical interface or commands
3. **Reinitialize** with your preferred method

For more details on how to delete node data, see [Delete Node Data]({{< relref "../delete-node-data" >}}).

### I Cannot Find my Configuration Files

Configuration files are stored at:

- **Host path:** `./persistent-data/config/` (relative to the service directory)
- **Container path:** `/home/ubuntu/.infinited/config/`

Make sure you're in the correct service directory when looking for these files.

## Next Steps

After initializing your node:

1. **[Post-Initialization Verification]({{< relref "verification" >}})** - Verify that everything was created correctly
2. **[Start/Stop Node]({{< relref "../start-stop-node" >}})** - Learn to start and stop your node
3. **[Graphical Interface]({{< relref "../graphical-interface" >}})** - Use the graphical interface to manage your node

> [!NOTE]
> **If You're a Validator**
>
> If you're setting up a validator, after initializing with recovery, see [Workflow for Validators]({{< relref "../keys/validator-workflow" >}}) for the additional necessary steps (add key to keyring, verify Private Validator Key, create validator on the blockchain).

## See Also

- [Simple Initialization]({{< relref "simple-initialization" >}}) - If you don't need recoverability (full nodes only)
- [Post-Initialization Verification]({{< relref "verification" >}}) - Verify that initialization was successful
- [Node Initialization]({{< relref "." >}}) - Mode comparison and when to use each one
- [Key Management]({{< relref "../keys" >}}) - Complete guide to manage cryptographic keys
- [Private Validator Key]({{< relref "../../../../../concepts/private-validator-key" >}}) - What is the Private Validator Key

