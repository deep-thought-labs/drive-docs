---
title: "Key Management Operations"
weight: 52221
---

Complete guide of all available operations to manage cryptographic keys in the keyring of your blockchain nodes.

## Graphical Interface vs Command Line

The actions available through the graphical interface are **exactly the same** as if you called them from the command line. The graphical interface only provides a visual environment to navigate between options and select the desired action, but **does not add different functionalities**.

This means that:
- Generating a key from the graphical interface produces the same result as doing it from the command line
- Resetting the keyring password from the graphical interface has the same consequences as doing it from the command line
- All operations are equivalent, regardless of the method you use

## Key Management Submenu

To access key management, open the graphical interface (see [Graphical Interface]({{< relref "../graphical-interface" >}})) and navigate: Main Menu → **"Key Management"**

![Key Management submenu](/images/node-ui-keys.png)

> [!NOTE]
> **Command Syntax and Container Names**
>
> To understand how to structure commands with `drive.sh` and know the correct container names for each service, see the section [Commands that Require Container Name]({{< relref "../../general/container-management#commands-that-require-container-name" >}}) in Container Management.

## Key Management Operations

Below are all available operations to manage keys, showing both the command line method and the graphical interface method for each.

### 🔑 Generate Key (Dry-Run)

Generates a cryptographic key and shows your seed phrase **without saving it** in the keyring. This allows you to backup the seed phrase before using it to initialize your node.

**What it achieves:**
- Generates a new cryptographic key
- **Shows your seed phrase (12 or 24 words)**
- **Does NOT save** the key in the keyring (that's why it's called "dry-run")
- Allows you to backup the seed phrase before committing

**Key difference:** Unlike "Generate and Save Key", this method **does not save** the key in the [keyring]({{< relref "../../../../../concepts/keyring" >}}). You store the seed phrase directly and use it to initialize the node in [recovery mode]({{< relref "../initialization/recovery-initialization" >}}).

#### Using Command Line

**Simplified syntax (recommended):**
```bash
./drive.sh node-keys create my-validator --dry-run
```

**Complete syntax (alternative):**
```bash
./drive.sh exec infinite node-keys create my-validator --dry-run
```

**Expected output:**
- Shows the generated seed phrase
- Shows the key address
- Instructions to backup the seed phrase

**⚠️ CRITICAL:** Write and backup this seed phrase immediately. This is the only way to recover your key.

#### Using Graphical Interface

1. In the "Key Management" submenu, select **"Generate Key (Dry-Run - Recommended)"**

   ![Generate Key (Dry-Run) selected](/images/node-ui-key-op1-generate-key-dryrun.png)

2. Enter a name for your key (e.g., `my-validator`)
3. The system will generate and **show your seed phrase** (12 or 24 words)
4. **⚠️ CRITICAL:** Write and backup this seed phrase immediately
5. The key **is NOT saved** in the keyring
6. Use this seed phrase to initialize your node in [recovery mode]({{< relref "../initialization/recovery-initialization" >}})

**When to use:** When you want to create a new key and have complete control over your seed phrase before using it.

### 💾 Generate and Save Key Directly

Generates a new key and automatically saves it in the keyring in a single step.

**What it achieves:**
- Generates a new key
- Automatically saves the key in the keyring
- May show the seed phrase (depending on configuration)

**Key difference:** Unlike "Dry-Run", this method **saves** the key in the [keyring]({{< relref "../../../../../concepts/keyring" >}}), allowing you to use it directly in node operations without having to add it manually afterward.

**Note:** If you use this method, make sure to backup your seed phrase if it's shown.

#### Using Command Line

**Simplified syntax (recommended):**
```bash
./drive.sh node-keys create my-validator
```

**Complete syntax (alternative):**
```bash
./drive.sh exec infinite node-keys create my-validator
```

**What it does:**
- Requests a password for the keyring (if it's the first time)
- Generates and automatically saves the key in the keyring
- May show the seed phrase (depending on configuration)

> [!TIP]
> **You Don't Need to Specify `-it`**
>
> The `drive.sh` script automatically detects that `node-keys create` requires interactive mode and adds `-it` for you. You can omit it completely.

#### Using Graphical Interface

1. In the "Key Management" submenu, select **"Generate and Save Key"**

   ![Generate and Save Key selected](/images/node-ui-key-op2-generate-key-save.png)

2. Enter a name for your key
3. Enter a password to protect the keyring (if it's the first time)
4. The system will generate the key and save it automatically
5. **⚠️ IMPORTANT:** Make sure to backup your seed phrase if it's shown

**When to use:** When you want to generate and save a key in a single step, ready to use in node operations.

### ➕ Add Existing Key from Seed Phrase

If you already have a seed phrase (from a previous node, from another system, or from a key you created with dry-run), you can add it to the keyring for future use.

**What it achieves:**
- Restores an existing key using its seed phrase
- Adds the key to the keyring for future use
- Allows using the key in node operations without having to enter the seed phrase each time

#### Using Command Line

**Simplified syntax (recommended):**
```bash
./drive.sh node-keys add my-validator
```

**Complete syntax (alternative):**
```bash
./drive.sh exec infinite node-keys add my-validator
```

**What it does:**
- Requests you to enter your seed phrase (12 or 24 words)
- Requests the keyring password if necessary
- Adds the key to the keyring

> [!TIP]
> **You Don't Need to Specify `-it`**
>
> The `drive.sh` script automatically detects that `node-keys add` requires interactive mode and adds `-it` for you.

**When to use:** When you want to restore an existing key or add a key from another node.

> [!TIP]
> **Multiple Keys from Same Seed Phrase**
>
> You can create multiple keys from the same seed phrase using different account indices. This is useful for organizing keys by purpose (main, backup, test) or managing multiple accounts. See [Multiple Keys from Same Seed Phrase]({{< relref "multiple-keys-from-seed" >}}) for detailed examples and use cases.

#### Using Graphical Interface

1. In the "Key Management" submenu, select **"Add Existing Key from Seed Phrase"**

   ![Add Existing Key from Seed Phrase selected](/images/node-ui-key-op3-add-key.png)

2. Enter a name for the key
3. Enter your seed phrase (12 or 24 words) when prompted
4. Enter the keyring password if necessary
5. The key will be added to your keyring

### 📋 List All Keys

Shows all keys you have stored in your keyring.

**What it achieves:**
- Shows a list of all key names in the keyring
- Allows you to see what keys you have available
- Useful to verify that a key was added correctly

#### Using Command Line

```bash
# Simplified syntax (recommended)
./drive.sh node-keys list

# Complete syntax (alternative)
./drive.sh exec infinite node-keys list
```

**Expected output:** List of names of all keys stored in the keyring.

#### Using Graphical Interface

1. In the "Key Management" submenu, select **"List All Keys"**

   ![List All Keys selected](/images/node-ui-key-op4-list.png)

2. You'll see a list of all stored key names

### 🔍 Show Key Details

Shows detailed information about a specific key stored in your keyring.

**What it achieves:**
- Shows complete information about a specific key
- Includes details such as address, key type, etc.
- Useful to verify key information before using it

#### Using Command Line

```bash
# Simplified syntax (recommended)
./drive.sh node-keys show

# Complete syntax (alternative)
./drive.sh exec infinite node-keys show my-validator
```

**Expected output:**
- Key name
- Key type
- Associated address
- Other relevant information

#### Using Graphical Interface

1. In the "Key Management" submenu, select **"Show Key Details"**

   ![Show Key Details selected](/images/node-ui-key-op5-show-key-details.png)

2. Enter the key name
3. You'll see information such as address, key type, etc.

### 🗑️ Delete a Key

Permanently deletes a key from the keyring.

**What it achieves:**
- Deletes a key from the keyring
- **⚠️ WARNING:** This action cannot be undone
- The key is deleted from the keyring but if you have the seed phrase backed up, you can add it again

**When to use:** Only when you're sure you no longer need the key. Consider backing up the seed phrase before deleting.

#### Using Command Line

```bash
# Simplified syntax (recommended)
./drive.sh node-keys delete

# Complete syntax (alternative)
./drive.sh exec infinite node-keys delete my-validator --yes
```

**⚠️ WARNING:** This action permanently deletes the key from the keyring. It cannot be undone.

#### Using Graphical Interface

1. In the "Key Management" submenu, select **"Delete Key"**

   ![Delete Key selected](/images/node-ui-key-op6-delete-key.png)

2. Enter the name of the key to delete
3. Confirm deletion
4. **⚠️ WARNING:** This action cannot be undone

### 🔒 Reset Keyring Password

> [!WARNING]
> **⚠️ CRITICAL WARNING: Reset Keyring Password**
>
> **Resetting the keyring password creates a new keyring with a new password, causing you to NO LONGER have access to keys you previously stored.**
>
> This action:
> - Creates a new encrypted keyring with the new password
> - **Removes access to all keys stored in the previous keyring**
> - Previous keys cannot be recovered without the original password
>
> **Only use this option if:**
> - You're sure you no longer need the previously stored keys
> - You have the seed phrases backed up to restore keys afterward
> - You're starting from scratch and don't have important keys stored
>
> This warning is shown during the process both in the graphical interface and when executed from the command line.

Allows changing the password that protects your keyring. **Important:** This operation creates a new keyring, losing access to previously stored keys.

**What it achieves:**
- Creates a new keyring with a new password
- **⚠️ WARNING:** You'll lose access to all keys stored in the previous keyring
- Useful only if you're starting from scratch or have all your seed phrases backed up

#### Using Graphical Interface

1. In the "Key Management" submenu, select **"Reset Keyring Password"**

   ![Reset Keyring Password selected](/images/node-ui-key-op7-reset-keyring-password.png)

2. **Read the warning** shown about losing access to previous keys
3. Confirm that you understand the consequences
4. Follow the instructions to set a new password

#### Using Command Line

This operation is primarily available through the graphical interface. If you need to reset the password from the command line, the process is equivalent to creating a new keyring, which will delete all stored keys. Make sure you have your seed phrases backed up before proceeding.

## Using Keys in Commands

When you use commands that require keys (such as transactions or on-chain operations), the system will look for keys in the [keyring]({{< relref "../../../../../concepts/keyring" >}}) stored in the persistent data folder.

For more information on the keyring location and how it works, see [Keyring]({{< relref "../../../../../concepts/keyring" >}}).

**Example:**
```bash
# Verify that the keyring exists and contains your key
# Simplified syntax (recommended)
./drive.sh node-keys list

# Complete syntax (alternative)
./drive.sh exec infinite node-keys list

# Now you can use commands that require keys
# The system will automatically search in persistent-data
```

**If you receive a "key not found" error:**
1. Verify that you're in the correct service directory
2. Verify that the keyring exists in `persistent-data`
3. List available keys with `node-keys list`
4. If the key is not there, add it using `node-keys add` or the graphical interface

For more information on troubleshooting, see [Key Management Issues]({{< relref "../../../troubleshooting/key-management-issues" >}}).

## See Also

- [Workflow for Validators]({{< relref "validator-workflow" >}}) - Step-by-step guide to set up keys as a validator
- [Security Best Practices]({{< relref "security" >}}) - Security recommendations
- [Key Management Issues]({{< relref "../../../troubleshooting/key-management-issues" >}}) - Troubleshooting common problems
- [Keyring]({{< relref "../../../../../concepts/keyring" >}}) - What is a keyring and how it works
- [Graphical Interface]({{< relref "../graphical-interface" >}}) - Complete guide to the graphical interface

