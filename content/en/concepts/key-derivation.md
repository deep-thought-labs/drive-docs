---
title: "Key Derivation"
weight: 4
---

**Key derivation** (also called **HD key derivation** or **hierarchical deterministic key derivation**) is the process of generating multiple cryptographic keys from a single seed phrase using mathematical algorithms and derivation paths.

## What is Key Derivation?

Key derivation is a cryptographic process that allows you to:

- Generate multiple unique keys from one seed phrase
- Create keys deterministically (the same seed phrase + same path = same key)
- Organize keys hierarchically for different purposes
- Maintain compatibility with standard wallet systems

Instead of generating each key independently, key derivation uses your seed phrase as a "master source" and applies different [derivation paths]({{< relref "derivation-path" >}}) to create unique keys.

## How It Works

When you derive a key from a seed phrase, the system follows this process:

1. **Takes your seed phrase** - The master source (12 or 24 words)
2. **Uses a derivation path** - A sequence that specifies which key to create (e.g., `m/44'/60'/0'/0/0`)
3. **Applies a mathematical algorithm** - Generates a unique private key based on the seed phrase and path
4. **Creates a unique address** - Derives a blockchain address from the generated key

The same seed phrase with different derivation paths will produce different keys, but the process is **deterministic** - the same inputs always produce the same outputs.

## The BIP44 Standard

Key derivation in Drive follows the **BIP44 standard**, which is a widely-used format that ensures:

- **Compatibility** - Works with standard wallets and tools
- **Consistency** - Predictable key generation across systems
- **Organization** - Hierarchical structure for managing multiple keys

The BIP44 standard defines how derivation paths are structured and ensures that different wallets can generate the same keys from the same seed phrase.

## Components of Key Derivation

Key derivation involves several components:

- **[Seed Phrase]({{< relref "key" >}}#seed-phrase)** - The master source (12 or 24 words)
- **[Derivation Path]({{< relref "derivation-path" >}})** - The "address" that specifies which key to generate
- **[Account Index]({{< relref "account-index" >}})** - A component of the derivation path that determines which account/key to create
- **Mathematical Algorithm** - The cryptographic function that generates the key

## Why This Matters

Key derivation is fundamental because it:

- **Simplifies backup** - One seed phrase can recover all your keys
- **Enables organization** - Create separate keys for different purposes (main, backup, test)
- **Ensures compatibility** - Works with standard wallets and tools
- **Provides security** - Each derived key is cryptographically independent
- **Allows recovery** - All keys can be regenerated from the seed phrase

## Example

```
Same seed phrase + account 0 → Key A (address: infinite1abc...)
Same seed phrase + account 1 → Key B (address: infinite1xyz...)
Same seed phrase + account 2 → Key C (address: infinite1def...)
```

All three keys come from the same seed phrase but are completely independent. You can recover all of them using just the seed phrase.

## See Also

- [Key]({{< relref "key" >}}) - What is a cryptographic key and seed phrases
- [Derivation Path]({{< relref "derivation-path" >}}) - Understanding derivation paths and their structure
- [Account Index]({{< relref "account-index" >}}) - How account indices work in key derivation
- [Keyring]({{< relref "keyring" >}}) - Where derived keys are stored
- [Multiple Keys from Same Seed Phrase]({{< relref "../drive/guides/blockchain-nodes/keys/multiple-keys-from-seed" >}}) - Practical guide to using key derivation
