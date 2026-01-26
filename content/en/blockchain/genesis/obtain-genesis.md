---
title: "Obtain Genesis from URL"
weight: 4010
---

# Obtain Genesis File from URL

This guide shows you how to download the official genesis file for Infinite Improbability Drive mainnet or testnet when joining an existing network.

> [!IMPORTANT]
> **When to Use This Guide**
> 
> Use this guide when:
> - You're joining an existing network (mainnet or testnet)
> - You want to run a node with the official genesis configuration
> - You're setting up a new node after the chain has launched
> 
> **If you're participating in a chain launch**, use the [Create Gentx]({{< relref "create-gentx" >}}) guide instead.

## Prerequisites

Before starting, make sure you have:

- ✅ **Drive installed and configured** with at least one blockchain node service
- ✅ **Node initialized** (or ready to initialize)
- ✅ **Access to the container's bash** of the corresponding service

## Official Genesis URLs

The official genesis files are hosted at:

- **Mainnet**: `https://assets.infinitedrive.xyz/mainnet/genesis.json`
- **Testnet**: `https://assets.infinitedrive.xyz/testnet/genesis.json`

## Method 1: Using Drive (Recommended)

If you're using Drive, the `node-init` command automatically downloads the official genesis file from the configured URL. This is the easiest method:

### For Mainnet

```bash
# 1. Navigate to mainnet service directory
cd drive/services/node0-infinite

# 2. Start the container (if not already running)
./drive.sh up -d

# 3. Initialize the node (automatically downloads genesis)
./drive.sh node-init
```

### For Testnet

```bash
# 1. Navigate to testnet service directory
cd drive/services/node1-infinite-testnet

# 2. Start the container (if not already running)
./drive.sh up -d

# 3. Initialize the node (automatically downloads genesis)
./drive.sh node-init
```

The `node-init` command will:
- Download the official genesis file from the configured URL
- Place it in the correct location (`~/.infinited/config/genesis.json`)
- Validate the genesis file automatically

## Method 2: Manual Download (Direct Installation)

If you're running a node without Drive (direct installation), you can download the genesis file manually:

### For Mainnet

```bash
# 1. Initialize the node (if not already done)
infinited init my-node --chain-id infinite_421018-1 --home ~/.infinited

# 2. Download the official genesis file
curl -o ~/.infinited/config/genesis.json \
  https://assets.infinitedrive.xyz/mainnet/genesis.json

# 3. Validate the genesis file
infinited genesis validate-genesis --home ~/.infinited

# 4. Start the node
infinited start --chain-id infinite_421018-1 --evm.evm-chain-id 421018 --home ~/.infinited
```

### For Testnet

```bash
# 1. Initialize the node (if not already done)
infinited init my-node --chain-id infinite_421018001-1 --home ~/.infinited

# 2. Download the official genesis file
curl -o ~/.infinited/config/genesis.json \
  https://assets.infinitedrive.xyz/testnet/genesis.json

# 3. Validate the genesis file
infinited genesis validate-genesis --home ~/.infinited

# 4. Start the node
infinited start --chain-id infinite_421018001-1 --evm.evm-chain-id 421018001 --home ~/.infinited
```

## Verify the Genesis File

After downloading, verify that the genesis file is correct:

### Check Chain ID

```bash
# From within the container (if using Drive)
cat ~/.infinited/config/genesis.json | jq -r '.chain_id'

# Expected Chain IDs:
# Mainnet: infinite_421018-1
# Testnet: infinite_421018001-1
```

### Validate Genesis Structure

```bash
infinited genesis validate-genesis --home ~/.infinited
```

**This verifies:**
- ✅ Consistency of denominations
- ✅ Total supply matches the sum of all balances
- ✅ JSON structure is correct
- ✅ Basic genesis configuration is valid

## What's Included in the Official Genesis

The official genesis file includes:

- ✅ **All Infinite Drive customizations** (denominations, token metadata, module parameters)
- ✅ **ModuleAccounts** for all 6 tokenomics pools (strategic_delegation, security_rewards, perpetual_rd, fish_bootstrap, privacy_resistance, community_growth)
- ✅ **Vesting accounts** with 100M tokens locked over 42 years
- ✅ **Initial liquid supply** of 200 Improbability [42] (100 for validators + 100 for pools)
- ✅ **Network-specific parameters** (mainnet/testnet configurations)

No additional customization is needed—the genesis file is ready to use.

## Troubleshooting

### Error: "Failed to download genesis"

**Cause:** Network connectivity issue or URL is incorrect.

**Solution:** 
- Verify your internet connection
- Check that the URL is correct: `https://assets.infinitedrive.xyz/<network>/genesis.json`
- Try downloading manually with `curl` or `wget`

### Error: "Invalid genesis file"

**Cause:** The downloaded file is corrupted or incomplete.

**Solution:**
- Re-download the genesis file
- Verify the file size is reasonable (genesis files are typically several MB)
- Check that the file is valid JSON: `cat ~/.infinited/config/genesis.json | jq .`

### Error: "Chain ID mismatch"

**Cause:** The chain ID in the genesis doesn't match your node configuration.

**Solution:**
- Verify you downloaded the correct genesis for your network (mainnet vs testnet)
- Check the chain ID in the genesis: `cat ~/.infinited/config/genesis.json | jq -r '.chain_id'`
- Ensure your node is initialized with the matching chain ID

## Next Steps

After obtaining and validating the genesis file:

1. **Start your node** using Drive or direct installation
2. **Monitor node synchronization** to ensure it's catching up with the network
3. **Verify your node is connected** to the network by checking peers and block height

> 📖 **Start Node**: For information on how to start your node, see [Start/Stop Node]({{< relref "../../../drive/guides/blockchain-nodes/start-stop-node" >}}) in the Drive documentation.

## See Also

- [Genesis File]({{< relref "../../../concepts/genesis-file" >}}) - Genesis file concept
- [Create Gentx]({{< relref "create-gentx" >}}) - For chain launch participation
- [Network Overview]({{< relref "../overview" >}}) - Network identity and chain IDs
- [Tokenomics]({{< relref "../tokenomics" >}}) - What's included in the genesis file
