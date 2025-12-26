---
title: "Key Management Issues"
weight: 544
---

Solutions to common problems related to managing cryptographic keys in the keyring.

## I Can't See My Seed Phrase

If you used the "Generate and Save Key" method and didn't see the seed phrase:

- The seed phrase may not be shown by default in some cases
- Consider using the "dry-run" method to ensure you see and backup the seed phrase

**Solution:**
1. Use the [Generate Key (Dry-Run)]({{< relref "../guides/blockchain-nodes/keys/operations#generate-key-dry-run" >}}) method to generate a new key and see the seed phrase
2. If you already generated the key, you can try adding it again using the dry-run method with a different name to see the seed phrase

For more information on how to generate keys, see [Key Management Operations]({{< relref "../guides/blockchain-nodes/keys/operations" >}}).

## I Forgot My Keyring Password

If you forgot the keyring password:

- You can use the "Reset Keyring Password" option in the graphical interface or command line
- **⚠️ WARNING:** This will create a new keyring and you'll lose access to all stored keys
- **Important:** If you have stored keys, you'll need your seed phrases to restore them after resetting the password

**Solution:**
1. If you have seed phrases backed up:
   - Reset the keyring password using [Reset Keyring Password]({{< relref "../guides/blockchain-nodes/keys/operations#reset-keyring-password" >}})
   - Restore all your keys using [Add Existing Key from Seed Phrase]({{< relref "../guides/blockchain-nodes/keys/operations#add-existing-key-from-seed-phrase" >}})
2. If you don't have seed phrases backed up:
   - **There's no way to recover the keys** without the original password
   - If you're a validator and don't have the seed phrase, you'll permanently lose access to your validator

**Prevention:**
- Store your keyring password in a safe place (separate from the seed phrase)
- Consider using a secure password manager
- See [Security Best Practices]({{< relref "../guides/blockchain-nodes/keys/security" >}}) for more recommendations

## I Need to Recover a Deleted Key

If you deleted a key by mistake:

- If you have the seed phrase backed up, you can add it again using `node-keys add` or the graphical interface
- If you don't have the seed phrase backed up, **there's no way to recover the key**

**Solution:**
1. If you have the seed phrase backed up:
   - Use [Add Existing Key from Seed Phrase]({{< relref "../guides/blockchain-nodes/keys/operations#add-existing-key-from-seed-phrase" >}}) to restore the key
2. If you don't have the seed phrase backed up:
   - **There's no way to recover the key** without the seed phrase
   - If you're a validator and don't have the seed phrase, you'll permanently lose access to your validator

**Prevention:**
- Always backup your seed phrase before deleting a key
- Consider making an additional backup before deleting important keys
- See [Security Best Practices]({{< relref "../guides/blockchain-nodes/keys/security" >}}) for more recommendations

## Error: Key Not Found

If you receive a "key not found" error when using commands that require keys:

### Step-by-Step Verification

1. **Verify you're in the correct directory:**
   ```bash
   pwd  # Should show the service path, e.g.: .../services/node0-infinite
   ```

2. **Verify the keyring exists:**
   ```bash
   ls -la persistent-data/  # Should show directory contents
   ```

3. **List available keys:**
   ```bash
   ./drive.sh exec infinite node-keys list
   ```

4. **If the key is not in the list:**
   - Add the key using [Add Existing Key from Seed Phrase]({{< relref "../guides/blockchain-nodes/keys/operations#add-existing-key-from-seed-phrase" >}}) or the graphical interface
   - Make sure to use the correct key name

### Common Causes

- **Incorrect directory:** You're running the command from a different directory than the service
- **Keyring doesn't exist:** The keyring hasn't been created yet (it's created the first time you save a key)
- **Incorrect name:** You're using a different key name than the one you saved
- **Key deleted:** The key was deleted from the keyring

### Solution

1. Navigate to the correct service directory:
   ```bash
   cd services/node0-infinite  # Or your service name
   ```

2. Verify the keyring exists and list keys:
   ```bash
   ./drive.sh exec infinite node-keys list
   ```

3. If the key is not in the list, add it:
   ```bash
   ./drive.sh exec -it infinite node-keys add my-validator
   ```

4. If you don't have the seed phrase, you won't be able to add the key. In this case, you'll need to generate a new key.

For more information on how to use keys in commands, see [Using Keys in Commands]({{< relref "../guides/blockchain-nodes/keys/operations#using-keys-in-commands" >}}) in Key Management Operations.

## See Also

- [Key Management Operations]({{< relref "../guides/blockchain-nodes/keys/operations" >}}) - Complete guide of all available operations
- [Workflow for Validators]({{< relref "../guides/blockchain-nodes/keys/validator-workflow" >}}) - Step-by-step guide to set up keys as a validator
- [Security Best Practices]({{< relref "../guides/blockchain-nodes/keys/security" >}}) - Security recommendations
- [Keyring]({{< relref "../../../../concepts/keyring" >}}) - What is a keyring and how it works
- [Key]({{< relref "../../../../concepts/key" >}}) - What is a cryptographic key

