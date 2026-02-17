---
title: "Multiple Keys from Same Seed Phrase"
weight: 52223
---

Learn how to create multiple keys from a single seed phrase using different account indices. This is useful for organizing keys by purpose (main, backup, test) or managing multiple accounts from one mnemonic.

## Quick Overview

**What you can do:**
- Create multiple keys from the same seed phrase
- Each key has a unique address
- Organize keys by purpose (main, backup, test, etc.)
- All keys are recoverable with the same seed phrase

**When to use:**
- You want separate keys for different purposes (main account, backup, testing)
- You need multiple accounts but want to manage them with one seed phrase
- You're migrating from a wallet that uses different account indices
- You want to organize your keys by purpose or environment

## Understanding Key Derivation

> [!NOTE]
> **Fundamental Concepts**
>
> Before continuing, make sure you understand the basic concepts:
>
> - [Key Derivation]({{< relref "../../../../../concepts/key-derivation" >}}) - How multiple keys are generated from a single seed phrase
> - [Account Index]({{< relref "../../../../../concepts/account-index" >}}) - How account indices determine which key is created
> - [Derivation Path]({{< relref "../../../../../concepts/derivation-path" >}}) - Understanding derivation paths and their structure

**Key derivation** is the process of generating multiple cryptographic keys from a single seed phrase. This guide shows you how to use it in practice.

### Quick Overview

When you add a key with a seed phrase, the system uses [key derivation]({{< relref "../../../../../concepts/key-derivation" >}}) to generate the key. The [derivation path]({{< relref "../../../../../concepts/derivation-path" >}}) includes an [account index]({{< relref "../../../../../concepts/account-index" >}}) that determines which specific key is created.

**Default behavior:**
- If you don't specify an account index, it uses `0` (first account)
- Each account index creates a different key and address
- All keys come from the same seed phrase but are completely independent

**Example:**
```
Same seed phrase + account 0 → Key A (address: infinite1abc...)
Same seed phrase + account 1 → Key B (address: infinite1xyz...)
Same seed phrase + account 2 → Key C (address: infinite1def...)
```

For detailed information about how key derivation works, see [Key Derivation]({{< relref "../../../../../concepts/key-derivation" >}}).

## Common Use Cases

### Use Case 1: Main and Backup Keys

Create a main key for daily operations and a backup key for emergencies:

```bash
# Main key (account 0 - default)
./drive.sh exec infinite node-keys add my-main-key

# Backup key (account 1)
./drive.sh exec infinite node-keys add my-backup-key --account 1
```

**What happens:**
- Both keys use the same seed phrase when you add them
- `my-main-key` uses account index 0
- `my-backup-key` uses account index 1
- They have different addresses and are independent

### Use Case 2: Separate Keys for Different Networks

Organize keys by network or environment:

```bash
# Mainnet key
./drive.sh exec infinite node-keys add my-mainnet-key

# Testnet key
./drive.sh exec infinite node-keys add my-testnet-key --account 1

# Development key
./drive.sh exec infinite node-keys add my-dev-key --account 2
```

### Use Case 3: Keys for Different Purposes

Organize keys by their intended use:

```bash
# Personal account
./drive.sh exec infinite node-keys add my-personal-key

# Business account
./drive.sh exec infinite node-keys add my-business-key --account 1

# Savings account
./drive.sh exec infinite node-keys add my-savings-key --account 2
```

## How to Add Keys with Different Indices

### Basic Syntax

**Default (account 0):**
```bash
./drive.sh exec infinite node-keys add <key-name>
```

**With account index:**
```bash
./drive.sh exec infinite node-keys add <key-name> --account <index>
```

### Step-by-Step Example

Let's create three keys from the same seed phrase:

**Step 1: Add first key (account 0)**
```bash
./drive.sh exec infinite node-keys add my-main-key
# Enter your seed phrase when prompted
```

**Step 2: Add second key (account 1)**
```bash
./drive.sh exec infinite node-keys add my-backup-key --account 1
# Enter the SAME seed phrase when prompted
```

**Step 3: Add third key (account 2)**
```bash
./drive.sh exec infinite node-keys add my-test-key --account 2
# Enter the SAME seed phrase when prompted
```

**Step 4: Verify all keys**
```bash
./drive.sh exec infinite node-keys list
```

You should see all three keys listed with different addresses.

## Advanced: Custom Derivation Paths

For advanced users, you can specify a complete HD path:

```bash
./drive.sh exec infinite node-keys add <key-name> --hd-path "m/44'/60'/0'/0/0"
```

> [!WARNING]
> **⚠️ EXPERIMENTAL: Hardware Wallets and Custom Paths**
>
> **This section is experimental and needs to be tested and validated.**
>
> If you're reading this, feel free to perform tests, but until these instructions are confirmed by the development team, **take this documentation only as illustrative and remember: don't trust, verify.**
>
> Custom derivation paths and hardware wallet compatibility are still being validated. Use at your own risk and always verify the results.

**When to use:**
- You need compatibility with a specific wallet
- You want to match a specific derivation path
- You're migrating from another system

> [!NOTE]
> **Default Coin Type**
>
> Drive uses coin type `60` (Ethereum-compatible) by default. The default path is `m/44'/60'/account'/0/0`.

## Important Notes

### ✅ What Works

- All keys from the same seed phrase are recoverable with that seed phrase
- Each key has a unique address
- Keys are independent (funds in one don't affect the other)
- You can add keys in any order

### ⚠️ Important Considerations

- **Same seed phrase**: You must use the **exact same seed phrase** for all keys
- **Account index**: Each account index creates a different key
- **Key names**: Use descriptive names to remember which key is which
- **Backup**: Always backup your seed phrase - it's the only way to recover all keys

### ❌ Common Mistakes

- **Using different seed phrases**: Each seed phrase creates different keys. To get multiple keys from one seed, you must use the same phrase with different account indices.
- **Forgetting the account index**: If you forget which account index you used, you'll need to try different indices or check your records.
- **Mixing up key names**: Use clear, descriptive names to avoid confusion.

## Verification

After adding keys, verify they were created correctly:

```bash
# List all keys
./drive.sh exec infinite node-keys list

# Show details of a specific key
./drive.sh exec infinite node-keys show <key-name>
```

Each key should show a different address, confirming they are separate keys.

## Troubleshooting

**Problem: I added a key but got the same address as before**

**Solution:** Make sure you're using a different account index. Check the command you used - if you didn't specify `--account`, it defaults to 0.

**Problem: I can't remember which account index I used**

**Solution:** Try adding the key again with different account indices (0, 1, 2, etc.) until you find the one that matches your expected address. You can check addresses with `node-keys show`.

**Problem: The key address doesn't match what I expected**

**Solution:** Verify you're using the correct seed phrase and account index. Different seed phrases or indices will produce different addresses.

## See Also

- **[Key Management Operations]({{< relref "operations" >}})** - Complete guide to all key operations
- **[Understanding Keys]({{< relref "understanding-keys" >}})** - Learn about different types of keys
- **[Security Best Practices]({{< relref "security" >}})** - Protect your keys and seed phrases
