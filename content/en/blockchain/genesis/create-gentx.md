---
title: "Create Gentx"
weight: 4011
---

Step-by-step guide to create a gentx (genesis transaction) from a base genesis file provided by the development team.

> [!IMPORTANT]
> **Context and Use of this Guide**
> 
> Operations related to gentx are used exclusively during **the launch or creation of a blockchain**. This process is not part of the daily lifecycle of a blockchain, but occurs only when launching a new chain, whether it's a test chain or the definitive mainnet.
> 
> If you're reading this guide, it's because you're actively participating in a chain launch. This guide provides a global explanation of the complete flow, but **the development team will provide you with specific instructions** for each launch, including:
> - Specific URL and command to download the base genesis
> - Specific amounts for account creation
> - Specific parameters for the gentx according to the context
> 
> **Always follow the specific instructions provided by the development team for each particular launch.**

Before continuing, make sure you understand the fundamental concepts: [Genesis File]({{< relref "../../../concepts/genesis-file" >}}), [Key]({{< relref "../../../concepts/key" >}}), and [Keyring]({{< relref "../../../concepts/keyring" >}}).

## What is a Gentx?

A **gentx** (genesis transaction) is a transaction that is included in the genesis file of a chain. It allows creating validators from block 1 (genesis block) of the chain.

When you participate in a chain launch, you create your gentx from a base genesis provided by the development team. Your gentx contains the necessary information to register your validator in the final genesis.

## Prerequisites

Before starting, make sure you have:

- ✅ **Drive installed and configured** with at least one blockchain node service
- ✅ **Node initialized** (the initialization process creates the necessary folders)
- ✅ **Access to the container's bash** of the corresponding service
- ✅ **Seed phrase** of your validator account stored securely

**About the `infinited` binary**: Although you can review the source code in the [official Infinite repository](https://github.com/deep-thought-labs/infinite), **you don't need to compile the binary yourself**. The `infinited` binary is already included within each Drive service. You just need to access the container's bash and run the commands from there:

```bash
# Mainnet
cd services/node0-infinite
./drive.sh exec infinite bash

# Testnet
cd services/node1-infinite-testnet
./drive.sh exec infinite-testnet bash

# Creative
cd services/node2-infinite-creative
./drive.sh exec infinite-creative bash
```

Once inside the container's bash, the `infinited` binary will be available directly. All operations described in this document will be performed from within the container. For more information, see [Container Management]({{< relref "../../../drive/guides/general/container-management#accessing-the-container-shell" >}}).

## Step 1: Get the Base Genesis

The development team will provide you with the base genesis file needed to create your gentx. The team will provide:

- **Specific URL** from where to download the base genesis
- **Specific command** to download the file that will already specify the final path where the genesis should be

The command provided by the team will download the base genesis directly to the correct location (`~/.infinited/config/genesis.json` or the path you use with `--home`), replacing the genesis file that was generated during your node's initialization.

**⚠️ Important:**
- Make sure you're inside the container's bash before executing the command
- The downloaded file will replace the existing genesis
- Verify that the file is valid JSON after downloading it

### Verify the Chain ID

After downloading the base genesis, verify the Chain ID to make sure it's correct:

```bash
cat ~/.infinited/config/genesis.json | jq -r '.chain_id'
```

**Expected Chain IDs:**
- **Mainnet:** `infinite_421018-1`
- **Testnet:** `infinite_421018001-1`
- **Creative:** `infinite_421018002-1`

Note the Chain ID, you'll need it later when generating your gentx.

### Validate the Base Genesis

Before proceeding to create your gentx, validate that the downloaded base genesis is correct:

```bash
infinited genesis validate-genesis --home ~/.infinited
```

**This verifies:**
- ✅ Consistency of denominations
- ✅ Total supply matches the sum of all balances
- ✅ JSON structure is correct
- ✅ Basic genesis configuration is valid

If validation is successful, you can proceed with confidence to create your gentx. If there are errors, contact the development team before continuing.

---

## Step 2: Create or Recover your Account

### 2-1. Recover your Account from Seed Phrase

⚠️ **Continue only if you already have a mnemonic (seed phrase) stored securely.**

```bash
infinited keys add validator --recover --keyring-backend file --home ~/.infinited
```

- `validator`: Account name (you can use any name)
- `--recover`: Recovery mode using seed phrase
- `--keyring-backend file`: Use file-based keyring
- `--home ~/.infinited`: Node home directory

The system will ask you to enter your seed phrase. Make sure you have it handy and enter it correctly.

> 📖 **Key Management**: For more information on how to manage keys, see [Key Management]({{< relref "../../../drive/guides/blockchain-nodes/keys" >}}) in the Drive documentation.

### 2-2. Add Funds to the Account in Genesis

Add your account to the genesis with the initial balance needed to create the validator. **The development team will specify the exact amount** you should use during the launch process. The values shown here are general examples:

**General example:**

```bash
# Mainnet (example)
infinited genesis add-genesis-account validator 1000000000000000000000drop \
  --keyring-backend file \
  --home ~/.infinited

# Testnet (example)
infinited genesis add-genesis-account validator 1000000000000000000000tdrop \
  --keyring-backend file \
  --home ~/.infinited

# Creative (example)
infinited genesis add-genesis-account validator 1000000000000000000000cdrop \
  --keyring-backend file \
  --home ~/.infinited
```

**Parameters:**
- `validator`: Name of the account you just created/recovered
- **Amount**: The development team will indicate the exact amount to use (in atomic units)
- Denominations:
  - Mainnet: `drop`
  - Testnet: `tdrop`
  - Creative: `cdrop`

**⚠️ Important:**
- Always use atomic units (10¹⁸)
- Include the correct denomination suffix according to the network
- **Use the specific amounts provided by the development team** for the ongoing launch
- Make sure you have enough tokens for the minimum required self-delegation

---

## Step 3: Generate the Gentx

### 3-1. Create the Validator's Gentx

Generate your gentx with your validator's parameters. **The development team may specify particular values** for some parameters (such as commission rates, minimum self-delegation, etc.) according to the launch context. The values shown here are general examples:

**General example for Mainnet:**
```bash
infinited genesis gentx validator 10000000000000000000drop \
  --chain-id infinite_421018-1 \
  --commission-rate "0.10" \
  --commission-max-rate "0.20" \
  --commission-max-change-rate "0.01" \
  --min-self-delegation "1000000000000000000" \
  --keyring-backend file \
  --home ~/.infinited
```

**General example for Testnet:**
```bash
infinited genesis gentx validator 10000000000000000000tdrop \
  --chain-id infinite_421018001-1 \
  --commission-rate "0.10" \
  --commission-max-rate "0.20" \
  --commission-max-change-rate "0.01" \
  --min-self-delegation "1000000000000000000" \
  --keyring-backend file \
  --home ~/.infinited
```

**General example for Creative:**
```bash
infinited genesis gentx validator 10000000000000000000cdrop \
  --chain-id infinite_421018002-1 \
  --commission-rate "0.01" \
  --commission-max-rate "0.05" \
  --commission-max-change-rate "0.01" \
  --min-self-delegation "1000000000000000000" \
  --keyring-backend file \
  --home ~/.infinited
```

**Parameters explained:**
- `validator`: Account name (must exist in the keyring and have funds in genesis)
- **Self-delegation amount**: The development team will indicate the exact amount to use
  - General examples:
    - Mainnet: `10000000000000000000drop` (10 tokens)
    - Testnet: `10000000000000000000tdrop` (10 tokens)
    - Creative: `10000000000000000000cdrop` (10 tokens)
- `--chain-id`: Must match exactly the Chain ID of the base genesis provided by the team
- `--commission-rate`: Initial commission rate (the team may specify particular values)
- `--commission-max-rate`: Maximum allowed commission rate (the team may specify particular values)
- `--commission-max-change-rate`: Maximum rate change per update (the team may specify particular values)
- `--min-self-delegation`: Minimum required self-delegation (the team may specify particular values)

**Location of the generated gentx:**
The gentx will be generated at: `~/.infinited/config/gentx/gentx-<moniker>.json`

---

## Step 4: Validate the Gentx

### 4-1. Verify that the Gentx was Created Correctly

```bash
# List generated gentxs
ls -la ~/.infinited/config/gentx/
```

You should see a file with the format `gentx-<moniker>.json`.

### 4-2. Validate the Genesis with your Gentx

Before delivering your gentx, validate that the genesis works correctly with it:

```bash
# Collect gentxs (includes yours)
infinited genesis collect-gentxs --home ~/.infinited

# Validate the resulting genesis
infinited genesis validate-genesis --home ~/.infinited
```

**This verifies:**
- ✅ Consistency of denominations
- ✅ Total supply matches the sum of all balances
- ✅ Validator configuration is valid
- ✅ JSON structure is correct

If validation is successful, your gentx is ready to deliver.

---

## Step 5: Deliver your Gentx

### 5-1. Locate your Gentx File

Your gentx is at:
```bash
~/.infinited/config/gentx/gentx-<moniker>.json
```

### 5-2. Deliver to the Development Team

Follow the development team's instructions to deliver your gentx. This may be:

- Upload the file to a specific repository
- Send it through a secure communication channel
- Another method indicated by the team

**⚠️ Important:**
- Only deliver the gentx file, NOT the complete genesis
- Verify that you're delivering the correct file
- Keep a backup of your gentx

---

## Process Summary

```
1. Download base genesis using command provided by the team
   ↓
2. Verify Chain ID of the downloaded genesis
   ↓
3. Recover account from seed phrase
   ↓
4. Add account with funds to genesis (amounts specified by the team)
   ↓
5. Generate gentx with validator parameters (values specified by the team)
   ↓
6. Validate gentx and genesis
   ↓
7. Deliver gentx to the development team
```

---

## Troubleshooting

### Error: "account does not exist"

**Cause:** The account doesn't exist in the keyring or the name is incorrect.

**Solution:** Verify that you created/recovered the account correctly:
```bash
infinited keys list --keyring-backend file --home ~/.infinited
```

### Error: "insufficient funds"

**Cause:** There aren't enough funds in the account for self-delegation.

**Solution:** Increase the amount of funds added to the genesis in Step 2-2.

### Error: "chain-id mismatch"

**Cause:** The Chain ID used doesn't match the one from the base genesis.

**Solution:** Verify the Chain ID of the base genesis and use it exactly:
```bash
cat ~/.infinited/config/genesis.json | jq -r '.chain_id'
```

### Error: "gentx file not found"

**Cause:** The gentx wasn't generated correctly or is in another location.

**Solution:** Verify that the `genesis gentx` command executed without errors and check:
```bash
ls -la ~/.infinited/config/gentx/
```

---

## Next Steps

Once the development team compiles all gentxs into the final genesis:

1. You'll receive the compiled final genesis
2. You'll replace your local genesis with the final genesis
3. **Validate the final genesis before starting the node:**
   ```bash
   infinited genesis validate-genesis --home ~/.infinited
   ```
   This validation verifies that the genesis is correct and ready to use. It's important to run it before starting the node to avoid problems.
4. You'll start your node with the final genesis
5. Your validator will be active from block 1

> 📖 **Start Node**: For information on how to start your node, see [Start/Stop Node]({{< relref "../../../drive/guides/blockchain-nodes/start-stop-node" >}}) in the Drive documentation.

---

## See Also

- [Genesis File]({{< relref "../../../concepts/genesis-file" >}}) - Genesis file concept
- [Key Management]({{< relref "../../../drive/guides/blockchain-nodes/keys" >}}) - Cryptographic key management

