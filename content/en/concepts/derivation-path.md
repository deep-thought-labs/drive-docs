---
title: "Derivation Path"
weight: 6
---

A **derivation path** (also called **HD path** or **BIP44 path**) is a sequence of numbers that specifies which specific key to generate from a seed phrase during [key derivation]({{< relref "key-derivation" >}}).

## What is a Derivation Path?

Think of a derivation path as a unique "address" that tells the system which specific key to create from your seed phrase. It's like coordinates on a map - the same seed phrase with different paths will produce different keys.

The derivation path follows the **BIP44 standard**, which ensures compatibility across different wallets and systems.

## Structure of a Derivation Path

A BIP44 derivation path has the following structure:

```
m / 44' / coin_type' / account' / change / address_index
```

**Components:**

- **`m`** - Master key indicator
- **`44'`** - BIP44 purpose (hardened)
- **`coin_type'`** - Blockchain identifier (hardened)
  - `60'` for Ethereum-compatible chains (Drive uses this)
  - `118'` for Cosmos Hub
- **`account'`** - [Account Index]({{< relref "account-index" >}}) (hardened)
- **`change`** - Change chain (usually `0` for external/receiving addresses)
- **`address_index`** - Address index (usually `0` for the first address)

## Hardened vs Non-Hardened

**Hardened derivation** (indicated by `'` after the number):
- Provides stronger security isolation
- Used for: purpose, coin type, and account index
- Example: `44'`, `60'`, `0'`

**Non-hardened derivation** (no `'`):
- Allows normal derivation
- Used for: change and address index
- Example: `0`, `0`

## Default Path in Drive

Drive uses the following default derivation path:

```
m/44'/60'/account'/0/0
```

Where:
- `44'` - BIP44 purpose
- `60'` - Ethereum-compatible coin type
- `account'` - The [account index]({{< relref "account-index" >}}) you specify (default: `0`)
- `0` - Change chain (external addresses)
- `0` - Address index (first address)

## Examples

**Example 1: Default path (account 0)**
```
m/44'/60'/0'/0/0
```
This is the path used when you don't specify an account index.

**Example 2: Account index 1**
```
m/44'/60'/1'/0/0
```
This path generates a different key using account index 1.

**Example 3: Account index 2**
```
m/44'/60'/2'/0/0
```
This path generates yet another different key using account index 2.

## Custom Derivation Paths

For advanced users, you can specify a complete custom derivation path:

```bash
./drive.sh exec infinite node-keys add <key-name> --hd-path "m/44'/60'/0'/0/0"
```

> [!WARNING]
> **⚠️ EXPERIMENTAL: Custom Paths**
>
> Custom derivation paths are experimental and need to be tested and validated. Use at your own risk and always verify the results.

**When to use custom paths:**
- You need compatibility with a specific wallet
- You want to match a specific derivation path from another system
- You're migrating from another blockchain or wallet

## Why Derivation Paths Matter

Derivation paths are important because they:

- **Enable multiple keys** - Same seed phrase, different paths = different keys
- **Ensure compatibility** - Standard format works across wallets
- **Provide organization** - Hierarchical structure for managing keys
- **Allow recovery** - Same path + same seed = same key (deterministic)

## See Also

- [Key Derivation]({{< relref "key-derivation" >}}) - How key derivation uses derivation paths
- [Account Index]({{< relref "account-index" >}}) - Understanding the account component of the path
- [Key]({{< relref "key" >}}) - What is a cryptographic key
- [Multiple Keys from Same Seed Phrase]({{< relref "../drive/guides/blockchain-nodes/keys/multiple-keys-from-seed" >}}) - Practical guide with examples
