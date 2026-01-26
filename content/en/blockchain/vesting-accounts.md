---
title: "Vesting Accounts"
weight: 500
---

# Vesting Accounts

Technical documentation for vesting accounts configured in Infinite Improbability Drive genesis files.

## What are Vesting Accounts?

Vesting accounts are special account types in Cosmos SDK that hold tokens that unlock gradually over time. They are used to implement token lockups and gradual release schedules.

## Vesting Accounts in Genesis

Infinite Improbability Drive uses vesting accounts to lock **100,000,000 Improbability [42]** (100M cups) that unlock linearly over **42 years**, controlled by on-chain DAO.

## Configuration Files

Vesting accounts are configured via JSON files:

- **Mainnet**: `scripts/genesis-configs/mainnet-vesting-accounts.json`
- **Testnet**: `scripts/genesis-configs/testnet-vesting-accounts.json`
- **Creative**: `scripts/genesis-configs/creative-vesting-accounts.json`

## Vesting Account Structure

Each vesting account is defined with:

```json
{
  "address": "infinite10fhk6nsvuw4mhfdtv6zux754n8mz2z39ynqqf7",
  "amount_tokens": 100000000,
  "vesting_type": "continuous",
  "vesting_start_time": 1769666400,
  "vesting_end_time": 3095388000
}
```

- **`address`**: The public address of the vesting account (multisig wallet)
- **`amount_tokens`**: Total token amount to be vested (in full token units)
- **`vesting_type`**: Type of vesting (`continuous` or `delayed`)
- **`vesting_start_time`**: Unix timestamp when vesting begins
- **`vesting_end_time`**: Unix timestamp when vesting completes

## Vesting Types

### Continuous Vesting

Tokens unlock **linearly** between `start_time` and `end_time`:

- **At `start_time`**: 0% unlocked
- **At `end_time`**: 100% unlocked
- **Between**: Linear unlock (e.g., at 50% of time, 50% unlocked)

### Delayed Vesting

Tokens unlock **all at once** at `end_time`:

- **Before `end_time`**: 0% unlocked
- **At `end_time`**: 100% unlocked

## Mainnet/Testnet Vesting Configuration

Both mainnet and testnet have the same vesting configuration:

| **Parameter** | **Value** | **Description** |
|---------------|-----------|-----------------|
| **Address** | `infinite10fhk6nsvuw4mhfdtv6zux754n8mz2z39ynqqf7` | Multisig wallet address |
| **Amount** | 100,000,000 tokens | Total vested amount |
| **Type** | `continuous` | Linear unlock over time |
| **Start Time** | `1769666400` (2026-01-29 Thursday) | Vesting start timestamp |
| **End Time** | `3095388000` (2068-02-02 Thursday) | Vesting end timestamp |
| **Duration** | 42 years | Total vesting period |

## Token Conversion

The `amount_tokens` value in the JSON configuration is converted to atomic units when creating the vesting account:

- **Conversion**: `amount_tokens × 10¹⁸` (to convert from full tokens to `drop` atomic units)
- **Example**: `100000000 tokens` → `100000000000000000000000000 drop`

## Timestamp Calculation

Vesting timestamps are Unix timestamps (seconds since epoch):

- **Start Time**: Set to the upcoming Thursday after chain launch
- **End Time**: Exactly 42 years from start time (also a Thursday)
- **Calculation**: Ensures both dates fall on the same day of the week

## Behavior Before Chain Launch

If `vesting_start_time` is set **before** the chain's actual launch date:

- **Before Launch**: The vesting account exists but no tokens are unlocked yet
- **At Launch**: The account starts with 0% unlocked (even if `start_time` has passed)
- **After Launch**: Tokens begin unlocking linearly from the launch date (or `start_time`, whichever is later)

This ensures vesting only begins **after** the chain is live, regardless of when `start_time` is set.

## Automatic Setup

Vesting accounts are automatically created by `setup_vesting_accounts.sh` when running `customize_genesis.sh`:

```bash
./scripts/customize_genesis.sh ~/.infinited/config/genesis.json --network mainnet
```

The script:
1. Reads the vesting account configuration file for the specified network
2. Creates each vesting account with the specified parameters
3. Validates the vesting account structure
4. Ensures account-balance consistency

## Querying Vesting Accounts

You can query vesting accounts on-chain:

```bash
# Query account information
infinited query auth account <vesting-account-address>

# Query account balance (total)
infinited query bank balances <vesting-account-address>

# Query spendable balance (unlocked tokens)
infinited query bank spendable-balances <vesting-account-address>
```

## Balance Display

When querying a vesting account:

- **`total` balance**: Shows the **full amount** (100M tokens), including locked tokens
- **`spendable` balance**: Shows only the **unlocked tokens** (gradually increases over time)

This is expected behavior - the full amount is visible, but only the unlocked portion is spendable.

## DAO Control

The vesting account is controlled by a **multisig wallet** that is governed by the on-chain DAO:

- **Address**: `infinite10fhk6nsvuw4mhfdtv6zux754n8mz2z39ynqqf7`
- **Control**: DAO governance via multisig signatures
- **Purpose**: Ensures tokens are spent according to DAO decisions

## Related Documentation

- **[Tokenomics]({{< relref "tokenomics" >}})** - Tokenomics overview and supply breakdown
- **[Network Parameters]({{< relref "network-parameters" >}})** - Network-specific configurations
- **[Module Accounts]({{< relref "module-accounts" >}})** - ModuleAccount configuration
- **[Genesis]({{< relref "genesis" >}})** - How genesis files are created
