---
title: "Genesis"
weight: 401
---

Guides for working with Genesis files and gentxs (genesis transactions).

## What is Genesis?

The genesis file defines the initial state of a blockchain. It contains information about initial accounts, validators, network parameters, and module configuration.

## Available Guides

- **[Obtain Genesis from URL]({{< relref "obtain-genesis" >}})** - Download the official genesis file for mainnet or testnet (for joining an existing network)
- **[Create Gentx]({{< relref "create-gentx" >}})** - Complete guide to create a gentx from a base genesis (for chain launch participation)

## When to Use Each Guide

**Use "Obtain Genesis from URL" if:**
- You're joining an existing network (mainnet or testnet)
- You want to run a node with the official genesis configuration
- You're setting up a new node after the chain has launched

**Use "Create Gentx" if:**
- You're participating in a chain launch
- The development team has asked you to create a gentx
- You're a validator joining the network at genesis

## Related Concepts

To better understand the fundamental concepts, see:

- [Genesis File]({{< relref "../../concepts/genesis-file" >}}) - What is a genesis file and its purpose
- [Node Initialization]({{< relref "../../concepts/node-initialization" >}}) - Node initialization process

## Related Documentation

- **[Tokenomics]({{< relref "../tokenomics" >}})** - Learn about ModuleAccounts and vesting accounts in genesis
- **[Network Overview]({{< relref "../overview" >}})** - Network identity and chain IDs