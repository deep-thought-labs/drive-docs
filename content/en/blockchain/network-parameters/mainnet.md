---
title: "Mainnet Parameters"
weight: 310
---

# Mainnet Network Parameters

Complete reference of all network parameters configured for Infinite Improbability Drive **mainnet**.

## Network Identity

- **Chain Name**: `infinite`
- **Cosmos Chain ID**: `infinite_421018-1`
- **EVM Chain ID**: `421018`
- **Bech32 Prefix**: `infinite`

## Token Configuration

- **Base Denomination**: `drop`
- **Display Denomination**: `Improbability`
- **Symbol**: `42`
- **Token Name**: `Improbability`
- **Description**: `Improbability Token — Project 42: Sovereign, Perpetual, DAO-Governed`

## Auth Module

| Parameter | Value | Description |
|-----------|-------|-------------|
| `tx_sig_limit` | `10` | Maximum number of signatures allowed for multisig wallets |

## Staking Module

| Parameter | Value | Description |
|-----------|-------|-------------|
| `bond_denom` | `drop` | Denomination for staking bonds |
| `unbonding_time` | `1814400s` (21 days) | Time required to unbond tokens |
| `max_validators` | `100` | Maximum number of validators |
| `historical_entries` | `10000` | Number of historical entries to keep |
| `max_entries` | `7` | Maximum unbonding/delegation entries |
| `min_commission_rate` | `0.000000000000000000` (0%) | Minimum validator commission rate |

## Mint Module (Inflation)

| Parameter | Value | Description |
|-----------|-------|-------------|
| `mint_denom` | `drop` | Denomination for minted tokens |
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
| `signed_blocks_window` | `10000` | Number of blocks for slashing window |
| `min_signed_per_window` | `0.050000000000000000` (5%) | Minimum blocks signed per window to avoid slashing |
| `downtime_jail_duration` | `600s` (10 minutes) | Time a validator is jailed for downtime |
| `slash_fraction_double_sign` | `0.050000000000000000` (5%) | Fraction of stake slashed for double signing |
| `slash_fraction_downtime` | `0.000100000000000000` (0.01%) | Fraction of stake slashed for downtime |

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

## Related Documentation

- **[Network Parameters Overview]({{< relref ".." >}})** - Comparison between networks
- **[Tokenomics]({{< relref "../tokenomics" >}})** - Token supply and distribution
- **[Module Accounts]({{< relref "../module-accounts" >}})** - ModuleAccount configuration
- **[Vesting Accounts]({{< relref "../vesting-accounts" >}})** - Vesting account configuration
