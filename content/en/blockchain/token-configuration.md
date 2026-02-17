---
title: "Token Configuration"
weight: 250
---

# Token Configuration

Complete reference of token denominations and metadata configured for each Infinite Improbability Drive network.

## Token Denominations

Each network uses different base denominations:

| Network | Base Denom | Display Denom | Symbol | Token Name |
|---------|-----------|---------------|--------|------------|
| **Mainnet** | `drop` | `Improbability` | `42` | `Improbability` |
| **Testnet** | `tdrop` | `TestImprobability` | `TEST42` | `TestImprobability` |
| **Creative** | `cdrop` | `CreativeImprobability` | `CRE42` | `CreativeImprobability` |

## Mainnet Token Configuration

- **Base Denomination**: `drop`
- **Display Denomination**: `Improbability`
- **Symbol**: `42`
- **Token Name**: `Improbability`
- **Description**: `Improbability Token — Project 42: Sovereign, Perpetual, DAO-Governed`
- **URI**: `https://assets.infinitedrive.xyz/tokens/42/icon.png`

## Testnet Token Configuration

- **Base Denomination**: `tdrop`
- **Display Denomination**: `TestImprobability`
- **Symbol**: `TEST42`
- **Token Name**: `TestImprobability`
- **Description**: `TestImprobability Token — Project 42 Testnet: Sovereign, Perpetual, DAO-Governed`
- **URI**: `https://assets.infinitedrive.xyz/tokens/42/icon.png`

## Creative Token Configuration

- **Base Denomination**: `cdrop`
- **Display Denomination**: `CreativeImprobability`
- **Symbol**: `CRE42`
- **Token Name**: `CreativeImprobability`
- **Description**: `CreativeImprobability Token — Project 42 Creative: Experimental Playground Network`
- **URI**: `https://assets.infinitedrive.xyz/tokens/42/icon.png`

## Denomination Units

All networks use the same denomination unit structure:

- **Base Unit**: `drop` / `tdrop` / `cdrop` (exponent: 0)
- **Display Unit**: `Improbability` / `TestImprobability` / `CreativeImprobability` (exponent: 18)
- **Conversion**: 1 display unit = 10¹⁸ base units

## Module Denominations

All modules are configured to use the network-specific base denomination:

- **Staking Module**: `bond_denom` = base denom
- **Mint Module**: `mint_denom` = base denom
- **EVM Module**: `evm_denom` = base denom
- **Governance Module**: `min_deposit` and `expedited_min_deposit` use base denom

## Token Metadata

Token metadata is stored in the Bank module's `denom_metadata`:

```json
{
  "description": "Improbability Token — Project 42: Sovereign, Perpetual, DAO-Governed",
  "denom_units": [
    {
      "denom": "drop",
      "exponent": 0,
      "aliases": []
    },
    {
      "denom": "Improbability",
      "exponent": 18,
      "aliases": ["improbability"]
    }
  ],
  "base": "drop",
  "display": "Improbability",
  "name": "Improbability",
  "symbol": "42",
  "uri": "https://assets.infinitedrive.xyz/tokens/42/icon.png",
  "uri_hash": ""
}
```

## Equivalencies

- **1 Improbability [42]** = **1 cup** (1 cup of Improbability)
- **1 cup** = **10¹⁸ drop**
- **1 drop** = **10⁻¹⁸ Improbability [42]** = **10⁻¹⁸ cup**

## Examples

- `10 cups` = 10 Improbability [42] = 10 × 10¹⁸ drop
- `50 cups` = 50 Improbability [42] = 50 × 10¹⁸ drop
- `100 cups of Improbability` = 100 Improbability [42] = 100 × 10¹⁸ drop

## Related Documentation

- **[Network Overview]({{< relref "overview" >}})** - Network identity and token details
- **[Network Parameters]({{< relref "network-parameters" >}})** - Network-specific configurations
- **[Tokenomics]({{< relref "tokenomics" >}})** - Token supply and distribution
