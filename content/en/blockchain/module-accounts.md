---
title: "Module Accounts"
weight: 400
---

# Module Accounts

Technical documentation for ModuleAccounts configured in Infinite Improbability Drive genesis files.

## What are ModuleAccounts?

ModuleAccounts are special accounts in Cosmos SDK that represent on-chain modules. They have permissions to perform specific actions (like minting tokens, distributing rewards) and cannot be controlled by private keys. They are governed by the DAO through on-chain governance.

## ModuleAccounts in Genesis

All tokenomics pools are implemented as **ModuleAccounts** in genesis. These accounts hold tokens that are governed by the DAO and represent the initial liquid allocation visible at chain launch.

## Configuration Files

ModuleAccounts are configured via JSON files:

- **Mainnet**: `scripts/genesis-configs/mainnet-module-accounts.json`
- **Testnet**: `scripts/genesis-configs/testnet-module-accounts.json`
- **Creative**: `scripts/genesis-configs/creative-module-accounts.json`

## ModuleAccount Structure

Each ModuleAccount is defined with:

```json
{
  "name": "strategic_delegation",
  "amount_tokens": 40
}
```

- **`name`**: The ModuleAccount name (on-chain identifier)
- **`amount_tokens`**: Initial token amount (in full token units, not atomic units)

## Mainnet/Testnet ModuleAccounts

Both mainnet and testnet have the same 6 ModuleAccounts:

| **Name** | **Amount (Tokens)** | **% of Supply** | **Operational Mandate** |
|----------|---------------------|-----------------|-------------------------|
| `strategic_delegation` | 40 | 40% | Never spent — only delegated to validators |
| `security_rewards` | 25 | 25% | Validator + staker rewards |
| `perpetual_rd` | 15 | 15% | Institutional funding (Deep Thought Labs) |
| `fish_bootstrap` | 10 | 10% | Seed liquidity pools |
| `privacy_resistance` | 7 | 7% | ZK, anti-censura R&D |
| `community_growth` | 3 | 3% | Grants, education, integrations |
| **TOTAL** | **100** | **100%** | - |

> **Note**: These 100 tokens are the **initial liquid allocation** visible at chain launch. They represent the tokenomics distribution in a didactic way (40 tokens = 40% of allocation).

## Creative Network ModuleAccounts

The Creative network has only one ModuleAccount:

| **Name** | **Amount (Tokens)** | **Purpose** |
|----------|---------------------|-------------|
| `faucet` | Variable | Test token distribution |

## On-Chain Addresses

ModuleAccounts have deterministic addresses based on their name. The address format follows Cosmos SDK conventions:

- **Format**: `infinite1<module-account-hash>`
- **Derivation**: Based on module name and module account type

## Genesis Bootstrap (100 Tokens)

At **Block 1**, exactly **100 Improbability [42]** (100 cups) are distributed to ModuleAccounts:

- **Purpose:** Provide **visual clarity and educational understanding** of the tokenomics distribution
- **Distribution:** Split proportionally across all 6 pools according to their tokenomics percentages
- **Why 100 tokens?** This makes it **intuitively easy to understand** the distribution:
  - When you see `40 [42]` in the genesis file or on-chain, you immediately understand it represents **40% of the total allocation**
  - The numbers directly correspond to percentages, making the tokenomics **visually transparent** from day one
  - Anyone can verify the distribution by simply looking at the balances: 40 + 25 + 15 + 10 + 7 + 3 = 100

## Token Conversion

The `amount_tokens` value in the JSON configuration is converted to atomic units when creating the ModuleAccount:

- **Conversion**: `amount_tokens × 10¹⁸` (to convert from full tokens to `drop` atomic units)
- **Example**: `40 tokens` → `40000000000000000000 drop`

## Automatic Setup

ModuleAccounts are automatically created by `setup_module_accounts.sh` when running `customize_genesis.sh`:

```bash
./scripts/customize_genesis.sh ~/.infinited/config/genesis.json --network mainnet
```

The script:
1. Reads the ModuleAccount configuration file for the specified network
2. Creates each ModuleAccount with the specified amount
3. Validates the ModuleAccount structure
4. Ensures account-balance consistency

## ModuleAccount Permissions

ModuleAccounts have specific permissions based on their module type:

- **Bank Module**: Can hold and transfer tokens
- **Staking Module**: Can delegate tokens to validators
- **Distribution Module**: Can distribute rewards
- **Governance**: Controlled by DAO proposals

## Querying ModuleAccounts

You can query ModuleAccounts on-chain:

```bash
# List all module accounts
infinited query auth module-accounts

# Query specific module account balance
infinited query bank balances <module-account-address>
```

## Related Documentation

- **[Tokenomics]({{< relref "tokenomics" >}})** - Tokenomics overview and pool allocation
- **[Network Parameters]({{< relref "network-parameters" >}})** - Network-specific configurations
- **[Vesting Accounts]({{< relref "vesting-accounts" >}})** - Vesting account configuration
- **[Genesis]({{< relref "genesis" >}})** - How genesis files are created
