---
title: "Simple Initialization"
weight: 52231
---

Step-by-step guide to initialize a blockchain node using simple mode. This mode is suitable for [full nodes]({{< relref "../keys/understanding-keys" >}}) that will not act as validators.

## What is Simple Initialization?

Simple initialization generates a [Private Validator Key]({{< relref "../../../../../concepts/private-validator-key" >}}) that is **random and unique** and **cannot be recovered** if you lose it. It's the fastest and simplest method to initialize a node.

**Characteristics:**
- ✅ **Fast and simple** - No need to manage seed phrases
- ✅ **Suitable for full nodes** - You don't need to recover the key
- ❌ **Not recoverable** - If you lose the `priv_validator_key.json` file, there's no way to recover it
- ❌ **Different each time** - Each initialization generates a new key

> [!WARNING]
> **⚠️ DO NOT Use for Validators**
>
> If you initialize your node simply and then create a validator with that key, **you will NOT be able to recover that key if you lose it**. If you lose the `priv_validator_key.json` file, you will permanently lose control of your validator.
>
> **If you're a validator, YOU MUST use [Recovery Initialization]({{< relref "recovery-initialization" >}}).**

## Using Graphical Interface

1. Open the graphical interface (see [Graphical Interface]({{< relref "../graphical-interface" >}}))

2. Navigate: Main Menu → **"Node Operations"** → **"Advanced Operations"** → **"Initialize Node (Simple)"**

   ![Initialize Node (Simple) selected](/images/node-ui-advanced-operations-op1-init-simple.png)

3. Follow the on-screen instructions to complete initialization

## Using Command Line

```bash
./drive.sh exec infinite node-init
```

> [!NOTE]
> **What the Command Does**
>
> The command creates configuration files, generates a random [Private Validator Key]({{< relref "../../../../../concepts/private-validator-key" >}}) (not recoverable), and downloads the official [genesis file]({{< relref "../../../../../concepts/genesis-file" >}}). For technical details of the process, see [Technical Initialization Flow]({{< relref "../../../internal-workings/initialization-flow" >}}).

### Expected Output

After running the command, you should see:

```
✅ Node initialized successfully!
```

> [!NOTE]
> **Created Files**
>
> Configuration files are created in `./persistent-data/config/` (host) or `/home/ubuntu/.infinited/config/` (container). For more details on the data structure, see [Node Data]({{< relref "../../../../../concepts/node-data" >}}).

## Verification

After initializing, verify that everything was created correctly. See [Post-Initialization Verification]({{< relref "verification" >}}) for more details.

## Troubleshooting

### Error: "Node already initialized"

If you receive this error, it means the node was already initialized previously. To reinitialize:

1. **Stop the node** (if it's running)
2. **Delete node data** using the graphical interface or commands
3. **Reinitialize** with your preferred method

For more details on how to delete node data, see [Delete Node Data]({{< relref "../delete-node-data" >}}).

### I Cannot Find my Configuration Files

Configuration files are stored at:

- **Host path:** `./persistent-data/config/` (relative to the service directory)
- **Container path:** `/home/ubuntu/.infinited/config/`

Make sure you're in the correct service directory when looking for these files.

## Next Steps

After initializing your node:

1. **[Post-Initialization Verification]({{< relref "verification" >}})** - Verify that everything was created correctly
2. **[Start/Stop Node]({{< relref "../start-stop-node" >}})** - Learn to start and stop your node
3. **[Graphical Interface]({{< relref "../graphical-interface" >}})** - Use the graphical interface to manage your node

## See Also

- [Recovery Initialization]({{< relref "recovery-initialization" >}}) - If you need recoverability (required for validators)
- [Post-Initialization Verification]({{< relref "verification" >}}) - Verify that initialization was successful
- [Node Initialization]({{< relref "." >}}) - Mode comparison and when to use each one
- [Private Validator Key]({{< relref "../../../../../concepts/private-validator-key" >}}) - What is the Private Validator Key

