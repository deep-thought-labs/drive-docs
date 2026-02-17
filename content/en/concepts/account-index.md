---
title: "Account Index"
weight: 5
---

An **account index** (also called **account number**) is a component of the [derivation path]({{< relref "derivation-path" >}}) that determines which specific key is generated from a seed phrase during [key derivation]({{< relref "key-derivation" >}}).

## What is an Account Index?

Think of the account index as a "slot number" - each slot produces a different key from the same seed phrase. When you specify an account index, you're telling the system which specific key to generate.

**Key points:**
- Each account index creates a **different key** and **different address**
- All keys come from the **same seed phrase** but are **completely independent**
- The account index is part of the [derivation path]({{< relref "derivation-path" >}}) used in [key derivation]({{< relref "key-derivation" >}})

## How It Works

When you add a key with a seed phrase:

1. If you **don't specify** an account index, the system uses `0` (first account) by default
2. If you **specify** an account index (e.g., `--account 1`), the system uses that index
3. The system combines your seed phrase with the account index to generate a unique key
4. Each different account index produces a completely different key and address

## Default Behavior

**Default account index:** `0`

If you don't specify an account index when adding a key, the system automatically uses account index `0`. This means:

```bash
# These two commands produce the same key:
./drive.sh exec infinite node-keys add my-key
./drive.sh exec infinite node-keys add my-key --account 0
```

## Examples

**Example 1: Different account indices produce different keys**

```
Same seed phrase + account 0 → Key A (address: infinite1abc...)
Same seed phrase + account 1 → Key B (address: infinite1xyz...)
Same seed phrase + account 2 → Key C (address: infinite1def...)
```

**Example 2: Using account indices in commands**

```bash
# Account 0 (default)
./drive.sh exec infinite node-keys add my-main-key

# Account 1
./drive.sh exec infinite node-keys add my-backup-key --account 1

# Account 2
./drive.sh exec infinite node-keys add my-test-key --account 2
```

## In the Derivation Path

The account index is the third component in a BIP44 derivation path:

```
m / 44' / coin_type' / account' / change / address_index
                      ↑
                 Account Index
```

The account index is typically "hardened" (indicated by the `'` after the number), which means it provides stronger security isolation between different accounts.

## Common Use Cases

Account indices are commonly used to:

- **Organize keys by purpose** - Main account (0), backup account (1), test account (2)
- **Separate by network** - Mainnet (0), testnet (1), development (2)
- **Manage multiple accounts** - Personal (0), business (1), savings (2)
- **Migrate from other wallets** - Match account indices used in other systems

## Important Notes

### ✅ What Works

- Each account index creates a unique, independent key
- All keys are recoverable with the same seed phrase
- You can add keys in any order
- Keys are cryptographically independent (funds in one don't affect the other)

### ⚠️ Important Considerations

- **Same seed phrase required** - You must use the **exact same seed phrase** for all account indices
- **Remember the index** - If you forget which account index you used, you'll need to try different indices
- **Descriptive names** - Use clear key names to remember which account index each key uses

### ❌ Common Mistakes

- **Using different seed phrases** - Each seed phrase creates different keys. To get multiple keys from one seed, you must use the same phrase with different account indices.
- **Forgetting the account index** - If you forget which index you used, you'll need to try different indices or check your records.

## See Also

- [Key Derivation]({{< relref "key-derivation" >}}) - How key derivation works
- [Derivation Path]({{< relref "derivation-path" >}}) - Understanding derivation paths and where account index fits
- [Key]({{< relref "key" >}}) - What is a cryptographic key
- [Multiple Keys from Same Seed Phrase]({{< relref "../drive/guides/blockchain-nodes/keys/multiple-keys-from-seed" >}}) - Practical guide with examples
