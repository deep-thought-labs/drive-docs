---
title: "Node Log Issues"
weight: 543
---

Solutions to common problems related to blockchain node logs.

## Node Doesn't Show Logs

If you don't see logs or logs are empty:

### 1. Verify Node is Running

Logs are only generated when the node is running. Check the status:

```bash
# Simplified syntax (recommended)
./drive.sh node-process-status

# Complete syntax (alternative)
./drive.sh exec infinite node-process-status
```

**If the node is not running:**
- Logs won't be generated
- Start the node first with `node-start`
- See [Start/Stop Node]({{< relref "../guides/blockchain-nodes/start-stop-node" >}})

**If the node is running:**
- Continue to the next step

### 2. Verify Log File Exists

The log file is created automatically when the node starts. Verify its existence:

```bash
./drive.sh exec infinite ls -la /var/log/node/node.log
```

**If the file doesn't exist:**
- The node may not have started correctly
- Review container logs: `./drive.sh logs infinite-drive`
- Try restarting the node

**If the file exists:**
- Continue to the next step

### 3. Verify Log File Permissions

Permission problems can prevent log writing:

```bash
./drive.sh exec infinite ls -la /var/log/node/
```

**What to look for:**
- The file must belong to `ubuntu:ubuntu` (UID 1000:GID 1000)
- Permissions must be `644` (rw-r--r--) or `664` (rw-rw-r--)

**If there are permission problems:**
- See [Permission Issues]({{< relref "permission-issues" >}})
- Verify that the `/var/log/node/` directory has correct permissions

### 4. Verify Node is Writing Logs

If the file exists but is empty:

```bash
./drive.sh exec infinite tail -f /var/log/node/node.log
```

**If no new logs appear:**
- The node may be stopped or frozen
- Verify process status: `# Simplified syntax (recommended)
./drive.sh node-process-status

# Complete syntax (alternative)
./drive.sh exec infinite node-process-status`
- Review container logs for errors

## Logs Show Errors

If logs show errors:

### 1. Identify Error Type

Review logs to identify the error type:

```bash
# Simplified syntax (recommended)
./drive.sh node-logs

# Complete syntax (alternative)
./drive.sh exec infinite node-logs 100 | grep -i error
```

**Common error types:**
- **Connection errors:** Problems connecting with peers
- **Synchronization errors:** Problems synchronizing blocks
- **Validation errors:** Problems validating blocks or transactions
- **Configuration errors:** Incorrect configuration

### 2. Look for Patterns

Repetitive errors may indicate a systematic problem:

```bash
# Simplified syntax (recommended)
./drive.sh node-logs

# Complete syntax (alternative)
./drive.sh exec infinite node-logs 500 | grep -i error | sort | uniq -c
```

**What to look for:**
- Errors that repeat frequently
- Errors that appear at specific times
- Errors related to specific components

### 3. Verify Configuration

Some errors may be caused by incorrect configuration:

```bash
./drive.sh exec infinite cat /home/ubuntu/.infinited/config/config.toml
```

**What to verify:**
- P2P network configuration
- Peer and seed configuration
- Port configuration

### 4. Consult Troubleshooting Documentation

For specific errors, see:

- **[Common Issues]({{< relref "common-issues" >}})** - Solutions to general problems
- **[Network Diagnosis]({{< relref "network-diagnosis" >}})** - If errors are network-related
- **[Start/Stop Issues]({{< relref "node-start-stop-issues" >}})** - If errors occur when starting/stopping

## Logs Are Too Long

If logs are very long and difficult to review:

### 1. Limit Number of Lines

Specify how many lines you want to see:

```bash
# Simplified syntax (recommended)
./drive.sh node-logs

# Complete syntax (alternative)
./drive.sh exec infinite node-logs 50   # Last 50 lines
# Simplified syntax (recommended)
./drive.sh node-logs

# Complete syntax (alternative)
./drive.sh exec infinite node-logs 100  # Last 100 lines
```

### 2. Use Real-Time Following

To see only new logs:

```bash
# Simplified syntax (recommended)
./drive.sh node-logs

# Complete syntax (alternative)
./drive.sh exec infinite node-logs -f
```

This will show only logs generated after running the command.

### 3. Filter by Specific Terms

Use tools like `grep` to filter:

```bash
# See only errors
# Simplified syntax (recommended)
./drive.sh node-logs

# Complete syntax (alternative)
./drive.sh exec infinite node-logs 500 | grep -i error

# See only synchronization messages
# Simplified syntax (recommended)
./drive.sh node-logs

# Complete syntax (alternative)
./drive.sh exec infinite node-logs 500 | grep -i sync

# See only peer connections
# Simplified syntax (recommended)
./drive.sh node-logs

# Complete syntax (alternative)
./drive.sh exec infinite node-logs 500 | grep -i peer
```

### 4. Search Supervisor Logs

The supervisor also generates logs:

```bash
./drive.sh exec infinite cat /var/log/node/supervisor.log
```

**What to look for:**
- Automatic restart events
- Node stopped detection
- Supervisor problems

## Logs Don't Update

If logs don't update:

### 1. Verify Node is Active

```bash
# Simplified syntax (recommended)
./drive.sh node-process-status

# Complete syntax (alternative)
./drive.sh exec infinite node-process-status
```

**If the node is not active:**
- Logs won't update
- Start or restart the node

### 2. Verify Log File Size

```bash
./drive.sh exec infinite ls -lh /var/log/node/node.log
```

**If the file doesn't grow:**
- The node may be stopped or frozen
- Verify process status
- Review container logs

### 3. Verify Disk Space

Logs may stop writing if there's no space:

```bash
./drive.sh exec infinite df -h /var/log/node/
```

**If there's no space:**
- Clean old logs if necessary
- Consider implementing log rotation
- Free up system space

## Log Interpretation

### Normal Logs

Normal logs show:

- **Synchronization:** Progress synchronizing with the network
- **Connections:** Peer connection and disconnection
- **Blocks:** Block download and processing
- **Status:** General node status

### Error Logs

Error logs may show:

- **Connection errors:** Problems connecting with peers
- **Validation errors:** Problems validating blocks
- **Network errors:** P2P network problems
- **Configuration errors:** Incorrect configuration

### Supervisor Logs

Supervisor logs show:

- **Monitoring events:** Node monitoring events
- **Restarts:** Automatic restart attempts
- **Shutdown:** Supervision stop
- **Problems:** Problems detected by the supervisor

## See Also

- [Node Monitoring]({{< relref "../guides/blockchain-nodes/node-monitoring" >}}) - Complete guide on how to monitor the node
- [Start/Stop Node]({{< relref "../guides/blockchain-nodes/start-stop-node" >}}) - How to start and stop the node
- [Common Issues]({{< relref "common-issues" >}}) - Other common problems
- [Internal Logging System]({{< relref "../internal-workings/logging-system" >}}) - How the logging system works internally

