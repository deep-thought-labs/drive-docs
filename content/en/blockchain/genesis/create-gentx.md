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
- ✅ **Node initialized** using the recovery process with your validator seed phrase
- ✅ **Key added to the keyring** using the same validator seed phrase you used to initialize the node
- ✅ **Know the name of your key** that you added to the keyring (this is the name you chose when adding the key)
- ✅ **Access to the container's bash** of the corresponding service

**⚠️ Important about the key:**
- You must have initialized your node using the recovery process with your validator seed phrase
- You must have added that same seed phrase as a key to the keyring with a specific name (for example: `validator`, `my-validator`, etc.)
- **You must remember and be clear about what the name of that key is**, as you will need it in all commands in this document
- This key name is what you will use in the `add-genesis-account` and `genesis gentx` commands

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

## Step 2: Verify your Key in the Keyring

Before continuing, verify that your key exists in the keyring and remember its name:

```bash
infinited keys list --keyring-backend file --home ~/.infinited
```

This command will show all the keys you have in the keyring. **Identify and note the name of the key** that corresponds to your validator (the one you added using your validator seed phrase).

**Example output:**
```
- name: validator
  type: local
  address: infinite1abc123...
  pubkey: '{"@type":"/cosmos.crypto.secp256k1.PubKey","key":"..."}'
```

In this example, the key name is `validator`. **Use this same name** in the following steps.

> 📖 **Key Management**: For more information on how to manage keys, see [Key Management]({{< relref "../../../drive/guides/blockchain-nodes/keys" >}}) in the Drive documentation.

---

## Step 3: Add Funds to the Account in Genesis

**💡 Tip:** Before executing the command, you can prepare it in a plain text editor for easier editing. This will allow you to review and edit the complete command (including your key name and amount) before copying and pasting it into the console.

Add your account to the genesis with the initial balance needed to create the validator. **The development team will specify the exact amount** you should use during the launch process. The values shown here are general examples:

**General example:**

```bash
# Mainnet (example)
infinited genesis add-genesis-account <your-key-name> 1000000000000000000000drop \
  --keyring-backend file \
  --home ~/.infinited

# Testnet (example)
infinited genesis add-genesis-account <your-key-name> 1000000000000000000000tdrop \
  --keyring-backend file \
  --home ~/.infinited

# Creative (example)
infinited genesis add-genesis-account <your-key-name> 1000000000000000000000cdrop \
  --keyring-backend file \
  --home ~/.infinited
```

**Parameters:**
- `<your-key-name>`: **Use the exact name of your key** that you verified in Step 2 (for example: `validator`, `my-validator`, etc.). Replace `<your-key-name>` with your actual key name.
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

### Verify that the Account was Added Correctly

Before generating the gentx, it's recommended to verify that your account was added correctly to the genesis. You can do this by checking the genesis content:

```bash
cat ~/.infinited/config/genesis.json | jq '.app_state.bank.balances'
```

This command will show all balances in the genesis. Look for your public address (the same one you saw when listing your keys) and verify that it has the correct amount.

**Example expected output for Mainnet:**
```json
[
  {
    "address": "infinite1rs3s0jx0rvnsjwfjch59lg9ypp6k3vmg2cn68j",
    "coins": [
      {
        "denom": "drop",
        "amount": "1000000000000000000000"
      }
    ]
  }
]
```

**Example expected output for Testnet:**
```json
[
  {
    "address": "infinite1rs3s0jx0rvnsjwfjch59lg9ypp6k3vmg2cn68j",
    "coins": [
      {
        "denom": "tdrop",
        "amount": "1000000000000000000000"
      }
    ]
  }
]
```

**Example expected output for Creative:**
```json
[
  {
    "address": "infinite1rs3s0jx0rvnsjwfjch59lg9ypp6k3vmg2cn68j",
    "coins": [
      {
        "denom": "cdrop",
        "amount": "1000000000000000000000"
      }
    ]
  }
]
```

You can also verify the account information in the accounts section:

```bash
cat ~/.infinited/config/genesis.json | jq '.app_state.auth.accounts'
```

**Example expected output:**
```json
[
  {
    "@type": "/cosmos.auth.v1beta1.BaseAccount",
    "address": "infinite1rs3s0jx0rvnsjwfjch59lg9ypp6k3vmg2cn68j",
    "pub_key": null,
    "account_number": "0",
    "sequence": "0"
  }
]
```

If you see your address with the correct amount and the appropriate denomination according to the network (Mainnet: `drop`, Testnet: `tdrop`, Creative: `cdrop`), you can proceed with confidence to generate your gentx.

---

## Step 4: Generate the Gentx

**💡 Tip:** Before executing the command, you can prepare it in a plain text editor for easier editing. This will allow you to review and edit the complete command (including your key name and all parameters) before copying and pasting it into the console.

### 3-1. Create the Validator's Gentx

Generate your gentx with your validator's parameters. **The development team may specify particular values** for some parameters (such as commission rates, minimum self-delegation, etc.) according to the launch context. The values shown here are general examples:

**General example for Mainnet:**
```bash
infinited genesis gentx <your-key-name> 10000000000000000000drop \
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
infinited genesis gentx <your-key-name> 10000000000000000000tdrop \
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
infinited genesis gentx <your-key-name> 10000000000000000000cdrop \
  --chain-id infinite_421018002-1 \
  --commission-rate "0.01" \
  --commission-max-rate "0.05" \
  --commission-max-change-rate "0.01" \
  --min-self-delegation "1000000000000000000" \
  --keyring-backend file \
  --home ~/.infinited
```

**⚠️ Important:** Replace `<your-key-name>` with the exact name of your key that you verified in Step 2.

**Parameters explained:**
- `<your-key-name>`: **Use the exact name of your key** that you verified in Step 2 (must exist in the keyring and have funds in genesis). Replace `<your-key-name>` with your actual key name.
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

## Step 5: Validate the Gentx

### 4-1. Verify that the Gentx was Created Correctly

```bash
# List generated gentxs
ls -la ~/.infinited/config/gentx/
```

You should see a file with a hash format, similar to: `gentx-adba573456c82908c3221163185703c421a2dd1f.json`

**⚠️ Important:** The file name does NOT include your moniker, but a unique hash generated automatically. **You should NOT rename this JSON file**.

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

## Step 6: Deliver your Gentx

### 6-1. Locate your Gentx File

Your gentx was generated in:
```bash
~/.infinited/config/gentx/
```

The gentx file has a format with a unique hash, similar to: `gentx-adba573456c82908c3221163185703c421a2dd1f.json`

**⚠️ Important:** The file name does NOT include your moniker, but a unique hash generated automatically. **You should NOT rename this JSON file**.

To see the exact name of your file:
```bash
ls -la ~/.infinited/config/gentx/
```

### 6-2. Prepare the File for Delivery

**If you need to extract the file from the server:**

The gentx file is stored in the Docker persistent volume, so it's accessible from the host system:

```bash
# From the host system, navigate to the service directory
cd services/<service-name>

# Copy the file maintaining its original name (replace <hash> with the actual hash)
cp persistent-data/.infinited/config/gentx/gentx-<hash>.json ~/
```

**If you need to compress the file:**

**⚠️ Important:** 
- The JSON gentx file must maintain its original name (with the hash, don't rename it)
- The compressed file CAN include your moniker in its name to facilitate identification

```bash
# Create a compressed file with your moniker (replace <moniker> with your moniker and <hash> with the file hash)
tar -czf gentx-<moniker>.tar.gz gentx-<hash>.json

# Or using zip
zip gentx-<moniker>.zip gentx-<hash>.json
```

**Compressed file structure:**
- **Compressed file name:** `gentx-<your-moniker>.tar.gz` (can include your moniker for identification)
- **Content of compressed file:** `gentx-<hash>.json` (the original JSON file with its original name)

### 6-3. Deliver to Development Team

Follow the development team's instructions to deliver your gentx. This may be:

- Upload the file to a specific repository
- Send it through a secure communication channel (such as Telegram)
- Another method indicated by the team

**⚠️ Important:**
- Only deliver the gentx file, NOT the complete genesis
- Verify that you are delivering the correct file
- Keep a backup copy of your gentx
- If you compress the file, the compressed file can have your moniker, but the JSON inside must maintain its original name

---

## Process Summary

```
1. Download base genesis using command provided by the team
   ↓
2. Verify Chain ID of the downloaded genesis
   ↓
3. Verify that your key exists in the keyring and remember its name
   ↓
4. Add account with funds to genesis using your key name (amounts specified by the team)
   ↓
5. Generate gentx using your key name with validator parameters (values specified by the team)
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

