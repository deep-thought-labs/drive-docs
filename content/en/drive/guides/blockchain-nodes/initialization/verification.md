---
title: "Post-Initialization Verification"
weight: 52233
---

Guide to verify that node initialization completed correctly and that all necessary components were created.

## Why Verify?

After initializing a node, it's important to verify that:

- All configuration files were created correctly
- The [Private Validator Key]({{< relref "../../../../../concepts/private-validator-key" >}}) was generated correctly
- The [genesis file]({{< relref "../../../../../concepts/genesis-file" >}}) was downloaded correctly
- The Chain ID is configured correctly

This verification gives you confidence that the node is ready to start and synchronize with the blockchain.

## Verify Configuration Files

Configuration files should be in the `persistent-data/config/` folder:

```bash
# Verify that configuration files exist
ls -la persistent-data/config/

# Expected files:
# - config.toml
# - app.toml
# - client.toml
# - genesis.json
# - priv_validator_key.json
```

**Expected location:**
- **Host path:** `./persistent-data/config/` (relative to the service directory)
- **Container path:** `/home/ubuntu/.infinited/config/`

### Verify Configuration File Content (Optional)

You can review the content of configuration files to verify they're correct:

```bash
# Verify the Chain ID in config.toml
cat persistent-data/config/config.toml | grep chain_id

# Verify the application configuration
cat persistent-data/config/app.toml | head -20
```

## Verify Private Validator Key

The `priv_validator_key.json` file is critical for node operation, especially for validators.

```bash
# Verify that the file exists
ls -la persistent-data/config/priv_validator_key.json

# Review the content (optional, for verification)
cat persistent-data/config/priv_validator_key.json
```

> [!IMPORTANT]
> **The File is Always Created**
>
> When you initialize a node, **the `priv_validator_key.json` file is always created**, regardless of the initialization method you use (simple or recovery). The difference is in the **content** of the file:
>
> - **Simple initialization:** The content is random and different each time you initialize
> - **Recovery initialization:** The content is always the same if you use the same seed phrase

### Special Verification for Recovery Mode

If you used [recovery initialization]({{< relref "recovery-initialization" >}}), it's especially important to verify that you can recover the same key using your seed phrase.

#### Verification Practice: Reinitialize the Node

This practice allows you to verify that you can always recover exactly the same Private Validator Key using your seed phrase.

> [!IMPORTANT]
> **Difference between Container and Node**
>
> It's important to understand the difference:
> - **Container:** Is the Docker environment where the node lives
> - **Node:** Is the blockchain process running inside the container
>
> For this practice, you need to **stop the node** (not the container) and then **delete node data** before reinitializing.

**Procedure:**

1. **Note or save the content of your Private Validator Key:**
   ```bash
   cat persistent-data/config/priv_validator_key.json > my-validator-key-backup.json
   ```

2. **Stop the node and delete data:**
   - See [Delete Node Data]({{< relref "../delete-node-data" >}}) for complete instructions on how to stop the node and delete node data using the graphical interface.

3. **Reinitialize the node with the same seed phrase:**
   - Follow the complete procedure of [Recovery Initialization]({{< relref "recovery-initialization" >}}) using exactly the same seed phrase you used before.

4. **Verify that exactly the same key was generated:**
   ```bash
   diff persistent-data/config/priv_validator_key.json my-validator-key-backup.json
   ```

**Expected result:** Should be exactly the same key. If it's different, something went wrong in the process.

**Benefits of this practice:**
- ✅ Gives you confidence that you'll always be able to restore your validator
- ✅ Helps you familiarize yourself with the process
- ✅ Allows you to detect problems before creating the validator on the blockchain
- ✅ Creates expertise in key management

> [!NOTE]
> **Repeat the Procedure**
>
> You can repeat this verification procedure 2-3 times to make sure you always get the same result. This will help you be confident that if you perform the procedure correctly, you'll always be able to backup or restore your validator node as many times as necessary.

## Verify Genesis File

The genesis file is necessary for the node to synchronize with the blockchain:

```bash
# Verify that the genesis file exists
ls -la persistent-data/config/genesis.json

# Verify the Chain ID (optional)
cat persistent-data/config/genesis.json | grep chain_id
```

The genesis file must:
- Exist in the expected location
- Contain the correct Chain ID for your network
- Have a reasonable size (depends on the network)

## Verify Chain ID

The Chain ID must be consistent across all files:

```bash
# Verify the Chain ID in config.toml
cat persistent-data/config/config.toml | grep chain_id

# Verify the Chain ID in genesis.json
cat persistent-data/config/genesis.json | grep chain_id
```

Both should show the same Chain ID, which must correspond to the network you're using (mainnet, testnet, etc.).

## Verification Checklist

Use this checklist to make sure everything is correct:

- [ ] File `config.toml` exists
- [ ] File `app.toml` exists
- [ ] File `client.toml` exists
- [ ] File `genesis.json` exists
- [ ] File `priv_validator_key.json` exists
- [ ] Chain ID is correct in `config.toml`
- [ ] Chain ID is correct in `genesis.json`
- [ ] Chain ID matches between both files
- [ ] (If you used recovery) Private Validator Key has the expected content

## Common Problems

### Missing Files

If any file doesn't exist:

1. Verify that you're in the correct service directory
2. Verify that initialization completed without errors
3. Review container logs to see if there were errors

### Incorrect Chain ID

If the Chain ID is not correct:

1. Verify the service configuration in `docker-compose.yml`
2. Verify the service environment variables
3. Consult your network's documentation for the correct Chain ID

### Different Private Validator Key (Recovery Mode)

If you used recovery mode and the key is different:

1. Verify that you entered exactly the same seed phrase
2. Verify that there are no extra spaces or typos
3. Consider reinitializing with the correct seed phrase

## Next Steps

After verifying that initialization was successful:

1. **[Start/Stop Node]({{< relref "../start-stop-node" >}})** - Start your node to begin synchronizing
2. **[Graphical Interface]({{< relref "../graphical-interface" >}})** - Use the graphical interface to monitor your node
3. **[Key Management]({{< relref "../keys" >}})** - If you're a validator, manage your additional keys

## See Also

- [Simple Initialization]({{< relref "simple-initialization" >}}) - Simple initialization procedure
- [Recovery Initialization]({{< relref "recovery-initialization" >}}) - Recovery initialization procedure
- [Node Initialization]({{< relref "." >}}) - Mode comparison and when to use each one
- [Private Validator Key]({{< relref "../../../../../concepts/private-validator-key" >}}) - What is the Private Validator Key
- [Genesis File]({{< relref "../../../../../concepts/genesis-file" >}}) - What is the genesis file

