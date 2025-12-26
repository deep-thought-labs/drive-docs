---
title: "Security Best Practices"
weight: 52222
---

Security recommendations to protect your cryptographic keys and keyring.

## Seed Phrase Backup

The seed phrase is the only way to recover your keys. If you lose it, you will permanently lose access to your keys and, if you're a validator, you will lose your validator.

### Recommendations

1. **Multiple copies:** Create at least 2-3 copies of your seed phrase
2. **Separate locations:** Store copies in different physical locations
3. **Disaster resistant:** Use resistant materials (quality paper, metal)
4. **Verification:** Verify that your backup is legible and complete

### Backup Methods

- **Paper:** Write the seed phrase on quality paper and store it in a safe place
- **Metal:** Use a metal backup solution (fire/water resistant)
- **Encrypted storage:** Store in encrypted storage (never in plain text)

### ⚠️ NEVER

- Store the seed phrase in plain text on your computer
- Share the seed phrase with anyone
- Send it via email or messaging
- Store it in the cloud without encryption
- Photograph or scan it without additional protection

## Keyring Protection

The keyring is protected by a password that you set the first time you save a key.

### Recommendations

1. **Strong password:** Use a strong password to protect your keyring
   - Minimum 12 characters
   - Combine uppercase, lowercase, numbers, and symbols
   - Don't use personal information or common words
2. **Don't share:** Never share your keyring password
3. **Backup password:** Store your password in a safe place (separate from the seed phrase)
4. **Password manager:** Consider using a secure password manager

### ⚠️ WARNING: Reset Keyring Password

Resetting the keyring password creates a new keyring, losing access to all previously stored keys. Only do this if:
- You're sure you no longer need the previously stored keys
- You have the seed phrases backed up to restore keys afterward
- You're starting from scratch and don't have important keys stored

For more information, see [Reset Keyring Password]({{< relref "operations#reset-keyring-password" >}}) in Key Management Operations.

## General Security

### Server Access

1. **Limited access:** Only allow server access to trusted people
2. **Strong authentication:** Use two-factor authentication when possible
3. **Privileged users:** Limit the number of users with administrative access

### Network and Firewall

1. **Configured firewall:** Make sure your firewall is correctly configured
2. **Closed ports:** Close all ports you don't need
3. **VPN:** Consider using a VPN for remote access

### Maintenance

1. **Updates:** Keep your system and Drive updated
2. **Monitoring:** Regularly monitor your node's status
3. **Logs:** Regularly review logs to detect suspicious activity
4. **Backups:** Regularly backup your important data

## See Also

- [Key Management Operations]({{< relref "operations" >}}) - Complete guide of all available operations
- [Workflow for Validators]({{< relref "validator-workflow" >}}) - Step-by-step guide to set up keys as a validator
- [Key Management Issues]({{< relref "../../../troubleshooting/key-management-issues" >}}) - Troubleshooting common problems
- [Keyring]({{< relref "../../../../../concepts/keyring" >}}) - What is a keyring and how it works

