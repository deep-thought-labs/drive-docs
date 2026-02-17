---
title: "Testnet Parameters"
weight: 320
---

# Testnet Network Parameters

Complete reference of all network parameters configured for Infinite Improbability Drive **testnet**.

## Network Identity

- **Chain Name**: `infinite`
- **Cosmos Chain ID**: `infinite_421018001-1`
- **EVM Chain ID**: `421018001`
- **Bech32 Prefix**: `infinite`

## Token Configuration

- **Base Denomination**: `tdrop`
- **Display Denomination**: `TestImprobability`
- **Symbol**: `TEST42`
- **Token Name**: `TestImprobability`
- **Description**: `TestImprobability Token — Project 42 Testnet: Sovereign, Perpetual, DAO-Governed`

## Auth Module

| Parameter | Value | Description |
|-----------|-------|-------------|
| `tx_sig_limit` | `10` | Maximum number of signatures allowed for multisig wallets |

## Staking Module

| Parameter | Value | Description |
|-----------|-------|-------------|
| `bond_denom` | `tdrop` | Denomination for staking bonds |
| `unbonding_time` | `1814400s` (21 days) | Time required to unbond tokens |
| `max_validators` | `100` | Maximum number of validators |
| `historical_entries` | `10000` | Number of historical entries to keep |
| `max_entries` | `7` | Maximum unbonding/delegation entries |
| `min_commission_rate` | `0.000000000000000000` (0%) | Minimum validator commission rate |

## Mint Module (Inflation)

| Parameter | Value | Description |
|-----------|-------|-------------|
| `mint_denom` | `tdrop` | Denomination for minted tokens |
| `inflation_min` | `0.070000000000000000` (7%) | Minimum annual inflation rate |
| `inflation_max` | `0.200000000000000000` (20%) | Maximum annual inflation rate |
| `inflation_rate_change` | `0.130000000000000000` (13%) | Maximum annual rate of change |
| `goal_bonded` | `0.670000000000000000` (67%) | Target percentage of bonded tokens |
| `blocks_per_year` | `6311520` | Estimated blocks per year |
| `initial_inflation` | `0.100000000000000000` (10%) | Initial inflation rate at genesis |
| `initial_annual_provisions` | `0.000000000000000000` | Initial annual provisions (calculated automatically) |

## Governance Module

| Parameter | Value | Description |
|-----------|-------|-------------|
| `min_deposit` | `1000000000000000000` (1 token) | Minimum deposit required to create a proposal |
| `expedited_min_deposit` | `5000000000000000000` (5 tokens) | Minimum deposit for expedited proposals |
| `max_deposit_period` | `172800s` (2 days) | Maximum time to collect deposits |
| `voting_period` | `172800s` (2 days) | Time period for voting on proposals |
| `expedited_voting_period` | `86400s` (1 day) | Time period for expedited proposals |
| `quorum` | `0.334000000000000000` (33.4%) | Minimum voting power participation required |
| `threshold` | `0.500000000000000000` (50%) | Minimum percentage of Yes votes to pass |
| `veto_threshold` | `0.334000000000000000` (33.4%) | Minimum percentage of Veto votes to reject |

## Slashing Module

| Parameter | Value | Description |
|-----------|-------|-------------|
| `signed_blocks_window` | `10000` | Number of blocks monitored for validator signing activity |
| `min_signed_per_window` | `0.050000000000000000` (5%) | Minimum percentage of blocks that must be signed within the window to avoid slashing |
| `downtime_jail_duration` | `600s` (10 minutes) | Duration a validator remains jailed **after** downtime is detected (not the tolerance period before detection) |
| `slash_fraction_double_sign` | `0.050000000000000000` (5%) | Fraction of stake slashed for double signing |
| `slash_fraction_downtime` | `0.000100000000000000` (0.01%) | Fraction of stake slashed for downtime |

> **Downtime Tolerance:** With `signed_blocks_window` of 10,000 blocks and `min_signed_per_window` of 5%, validators can be offline for approximately **13.9 hours** (at ~5 seconds per block) before being penalized. The `downtime_jail_duration` of 10 minutes is the jail period **after** downtime is detected, not the tolerance window before detection.

## Fee Market Module (EIP-1559)

| Parameter | Value | Description |
|-----------|-------|-------------|
| `no_base_fee` | `false` | Whether base fee is disabled |
| `base_fee` | `1000000000` | Initial base fee (1 Gwei) |
| `min_gas_price` | `0` | Minimum gas price |
| `min_gas_multiplier` | `0.500000000000000000` (0.5) | Minimum gas price multiplier |
| `base_fee_change_denominator` | `8` | Denominator for base fee changes |
| `elasticity_multiplier` | `2` | Elasticity multiplier for fee calculation |
| `enable_height` | `0` | Block height at which fee market is enabled |
| `block_gas` | `0` | Target block gas limit |

## Distribution Module

| Parameter | Value | Description |
|-----------|-------|-------------|
| `community_tax` | `0.020000000000000000` (2%) | Percentage of fees sent to community pool |
| `base_proposer_reward` | `0.010000000000000000` (1%) | Base reward for block proposer |
| `bonus_proposer_reward` | `0.040000000000000000` (4%) | Bonus reward for block proposer |
| `withdraw_addr_enabled` | `true` | Whether withdrawal addresses can be changed |

## Consensus Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| `max_gas` | `10000000` | Maximum gas per block |
| `max_bytes` | `22020096` | Maximum bytes per block |
| `evidence_max_age_duration` | `172800000000000` (2 days) | Maximum age of evidence (nanoseconds) |
| `evidence_max_age_num_blocks` | `100000` | Maximum age of evidence (blocks) |
| `evidence_max_bytes` | `1048576` (1 MB) | Maximum size of evidence |

## Differences from Mainnet

Testnet uses the same parameters as mainnet, with the following differences:

- **Token denominations**: Uses `tdrop` instead of `drop`
- **Token metadata**: Different display name, symbol, and description
- **Chain IDs**: Different Cosmos and EVM chain IDs

## Related Documentation

- **[Network Parameters Overview]({{< relref ".." >}})** - Comparison between networks
- **[Mainnet Parameters]({{< relref "mainnet" >}})** - Mainnet configuration
- **[Creative Parameters]({{< relref "creative" >}})** - Creative network configuration
