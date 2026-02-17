---
title: "Network Parameters"
weight: 300
---

# Network Parameters

Complete reference of all network parameters configured for each Infinite Improbability Drive network.

## Available Networks

- **[Mainnet Parameters]({{< relref "mainnet" >}})** - Production network configuration
- **[Testnet Parameters]({{< relref "testnet" >}})** - Test network configuration
- **[Creative Parameters]({{< relref "creative" >}})** - Experimental playground network

## Parameter Categories

Each network configuration includes:

- **Network Identity**: Chain IDs, Bech32 prefix
- **Token Configuration**: Denominations, metadata
- **Auth Module**: Multisig signature limits
- **Staking Module**: Bonding, unbonding, validator limits
- **Mint Module**: Inflation parameters
- **Governance Module**: Proposal and voting parameters
- **Slashing Module**: Penalty and jail parameters
- **Fee Market Module**: EIP-1559 fee parameters
- **Distribution Module**: Fee distribution parameters
- **Consensus Parameters**: Block size, gas limits, evidence

## Dynamic Inflation Model (Mainnet/Testnet)

Mainnet and testnet use a **Target-Bonded Dynamic Inflation Model**. See individual network pages for complete parameter details.

## Creative Network: Zero Inflation

The Creative network is designed as an experimental playground with **zero inflation** and minimal fees. See [Creative Parameters]({{< relref "creative" >}}) for details.

## Related Documentation

- **[Token Configuration]({{< relref "../token-configuration" >}})** - Token denominations and metadata
- **[Tokenomics]({{< relref "../tokenomics" >}})** - Token supply and distribution
- **[Module Accounts]({{< relref "../module-accounts" >}})** - ModuleAccount configuration
- **[Vesting Accounts]({{< relref "../vesting-accounts" >}})** - Vesting account configuration
