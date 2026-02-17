---
title: "Creative Parameters"
weight: 330
---

# Creative Network Parameters

Complete reference of all network parameters configured for Infinite Improbability Drive **creative** network (experimental playground).

## Network Identity

- **Chain Name**: `infinite`
- **Cosmos Chain ID**: `infinite_421018002-1`
- **EVM Chain ID**: `421018002`
- **Bech32 Prefix**: `infinite`

## Token Configuration

- **Base Denomination**: `cdrop`
- **Display Denomination**: `CreativeImprobability`
- **Symbol**: `CRE42`
- **Token Name**: `CreativeImprobability`
- **Description**: `CreativeImprobability Token — Project 42 Creative: Experimental Playground Network`

## Auth Module

| Parameter | Value | Description |
|-----------|-------|-------------|
| `tx_sig_limit` | `10` | Maximum number of signatures allowed for multisig wallets |

## Staking Module

| Parameter | Value | Description |
|-----------|-------|-------------|
| `bond_denom` | `cdrop` | Denomination for staking bonds |
| `unbonding_time` | `86400s` (1 day) | Time required to unbond tokens |
| `max_validators` | `50` | Maximum number of validators |
| `historical_entries` | `1000` | Number of historical entries to keep |
| `max_entries` | `7` | Maximum unbonding/delegation entries |
| `min_commission_rate` | `0.000000000000000000` (0%) | Minimum validator commission rate |

## Mint Module (Inflation)

| Parameter | Value | Description |
|-----------|-------|-------------|
| `mint_denom` | `cdrop` | Denomination for minted tokens |
| `inflation_min` | `0.000000000000000000` (0%) | Minimum annual inflation rate |
| `inflation_max` | `0.000000000000000000` (0%) | Maximum annual inflation rate |
| `inflation_rate_change` | `0.000000000000000000` (0%) | Maximum annual rate of change |
| `goal_bonded` | `0.500000000000000000` (50%) | Target percentage of bonded tokens |
| `blocks_per_year` | `6311520` | Estimated blocks per year |
| `initial_inflation` | `0.000000000000000000` (0%) | Initial inflation rate at genesis |
| `initial_annual_provisions` | `0.000000000000000000` | Initial annual provisions (calculated automatically) |

> **Note**: Creative network has **zero inflation** - it's designed as an experimental playground with no token emission.

## Governance Module

| Parameter | Value | Description |
|-----------|-------|-------------|
| `min_deposit` | `100000000000000000` (0.1 tokens) | Minimum deposit required to create a proposal |
| `expedited_min_deposit` | `1000000000000000000` (1 token) | Minimum deposit for expedited proposals |
| `max_deposit_period` | `3600s` (1 hour) | Maximum time to collect deposits |
| `voting_period` | `3600s` (1 hour) | Time period for voting on proposals |
| `expedited_voting_period` | `1800s` (30 minutes) | Time period for expedited proposals |
| `quorum` | `0.100000000000000000` (10%) | Minimum voting power participation required |
| `threshold` | `0.500000000000000000` (50%) | Minimum percentage of Yes votes to pass |
| `veto_threshold` | `0.200000000000000000` (20%) | Minimum percentage of Veto votes to reject |

> **Note**: Creative network has **faster governance periods** (1 hour vs 2 days) for rapid experimentation.

## Slashing Module

| Parameter | Value | Description |
|-----------|-------|-------------|
| `signed_blocks_window` | `5000` | Number of blocks for slashing window |
| `min_signed_per_window` | `0.010000000000000000` (1%) | Minimum blocks signed per window to avoid slashing |
| `downtime_jail_duration` | `60s` (1 minute) | Time a validator is jailed for downtime |
| `slash_fraction_double_sign` | `0.010000000000000000` (1%) | Fraction of stake slashed for double signing |
| `slash_fraction_downtime` | `0.000010000000000000` (0.001%) | Fraction of stake slashed for downtime |

> **Note**: Creative network has **lighter slashing penalties** and shorter jail durations for experimentation.

## Fee Market Module (EIP-1559)

| Parameter | Value | Description |
|-----------|-------|-------------|
| `no_base_fee` | `true` | Whether base fee is disabled |
| `base_fee` | `0` | Initial base fee (disabled) |
| `min_gas_price` | `0` | Minimum gas price |
| `min_gas_multiplier` | `0.100000000000000000` (0.1) | Minimum gas price multiplier |
| `base_fee_change_denominator` | `8` | Denominator for base fee changes |
| `elasticity_multiplier` | `2` | Elasticity multiplier for fee calculation |
| `enable_height` | `0` | Block height at which fee market is enabled |
| `block_gas` | `0` | Target block gas limit |

> **Note**: Creative network has **no base fee** (`no_base_fee: true`) - transactions are essentially free for experimentation.

## Distribution Module

| Parameter | Value | Description |
|-----------|-------|-------------|
| `community_tax` | `0.000000000000000000` (0%) | Percentage of fees sent to community pool |
| `base_proposer_reward` | `0.000000000000000000` (0%) | Base reward for block proposer |
| `bonus_proposer_reward` | `0.000000000000000000` (0%) | Bonus reward for block proposer |
| `withdraw_addr_enabled` | `true` | Whether withdrawal addresses can be changed |

> **Note**: Creative network has **zero distribution rewards** - all fees go to validators directly.

## Consensus Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| `max_gas` | `20000000` | Maximum gas per block (2x mainnet) |
| `max_bytes` | `22020096` | Maximum bytes per block |
| `evidence_max_age_duration` | `86400000000000` (1 day) | Maximum age of evidence (nanoseconds) |
| `evidence_max_age_num_blocks` | `50000` | Maximum age of evidence (blocks) |
| `evidence_max_bytes` | `1048576` (1 MB) | Maximum size of evidence |

> **Note**: Creative network has **higher block gas limit** (20M vs 10M) for experimentation with larger transactions.

## Key Differences from Mainnet/Testnet

Creative network is optimized for experimentation and development:

| Feature | Mainnet/Testnet | Creative |
|---------|----------------|----------|
| **Inflation** | 7-20% (dynamic) | 0% (disabled) |
| **Base Fee** | Enabled (1 Gwei) | Disabled (free) |
| **Unbonding Time** | 21 days | 1 day |
| **Governance Periods** | 2 days | 1 hour |
| **Slashing Penalties** | Standard | Lighter |
| **Max Validators** | 100 | 50 |
| **Block Gas Limit** | 10M | 20M |
| **Distribution Rewards** | 2% community tax | 0% (all to validators) |

## Related Documentation

- **[Network Parameters Overview]({{< relref ".." >}})** - Comparison between networks
- **[Mainnet Parameters]({{< relref "mainnet" >}})** - Mainnet configuration
- **[Testnet Parameters]({{< relref "testnet" >}})** - Testnet configuration
