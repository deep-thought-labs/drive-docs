---
title: "Node Start/Stop Issues"
weight: 542
---

Solutions to common problems related to starting and stopping the blockchain node.

## Node Won't Start

If the node won't start, follow these steps to diagnose and resolve the problem:

### 1. Verify Node is Initialized

The node must be initialized before it can be started. Verify that the genesis file exists:

```bash
./drive.sh exec infinite ls -la /home/ubuntu/.infinited/config/genesis.json
```

**If the file doesn't exist:**
- The node hasn't been initialized
- You need to run `node-init` first
- See the [Node Initialization]({{< relref "../guides/blockchain-nodes/initialization" >}}) guide

**If the file exists:**
- The node is correctly initialized
- Continue to the next step

### 2. Verify No Other Instance is Running

The system doesn't allow multiple instances of the same node. Check the status:

```bash
./drive.sh exec infinite node-process-status
```

**If there's an instance running:**
- You'll see the PID of the running process
- Stop the previous instance first with `node-stop`
- Then try starting again

**If no instance is running:**
- Continue to the next step

### 3. Review Container Logs

Container logs may show startup errors:

```bash
./drive.sh logs infinite-drive
```

**What to look for:**
- Configuration errors
- Permission problems
- Network errors
- Binary problems

### 4. Review Node Logs

If the node attempted to start but failed, review node logs:

```bash
./drive.sh exec infinite node-logs 50
```

**What to look for:**
- Specific error messages
- Synchronization problems
- Peer connection errors

### 5. Verify Configuration

Verify that environment variables are configured correctly:

```bash
./drive.sh exec infinite env | grep NODE_
```

**Important variables:**
- `NODE_CHAIN_ID` - Must be defined
- `NODE_EVM_CHAIN_ID` - Must be defined
- `NODE_HOME` - Must point to the correct directory

### 6. Verify Permissions

If there are permission problems, see [Permission Issues]({{< relref "permission-issues" >}}).

## Node Won't Stop

If the node won't stop correctly:

### 1. Wait for Controlled Shutdown

Controlled shutdown can take up to 30 seconds. Wait a few moments before taking additional actions.

### 2. Verify Status

Verify if the process is still running:

```bash
./drive.sh exec infinite node-process-status
```

**If the process is no longer running:**
- The node stopped correctly
- There may be a delay in status update

**If the process is still running:**
- Continue to the next step

### 3. Verify Supervisor Logs

The supervisor may be restarting the node. Check the logs:

```bash
./drive.sh exec infinite cat /var/log/node/supervisor.log
```

**If the supervisor is restarting the node:**
- The auto-start flag still exists
- The supervisor detects that the node stopped and restarts it
- Stop the supervisor first or remove the auto-start flag

### 4. Force Shutdown (Last Resort)

> [!WARNING]
> **⚠️ Warning: Force Shutdown**
>
> Forcing node shutdown can cause:
> - Loss of unsaved data
> - Synchronization problems
> - Slashing for validators (in extreme cases)
>
> Only use it as a last resort after trying all previous methods.

If it's absolutely necessary to force shutdown:

```bash
# 1. Find the process PID
./drive.sh exec infinite node-process-status

# 2. Remove auto-start flag to prevent restart
./drive.sh exec infinite rm -f /home/ubuntu/.node/auto-start

# 3. Stop the supervisor
./drive.sh exec infinite pkill -f node-supervisor

# 4. Send forced termination signal (last resort)
./drive.sh exec infinite kill -KILL <PID>
```

**After forcing shutdown:**
- Verify that the process has stopped
- Review logs to identify the cause of the problem
- Consider reinitializing the node if there's data corruption

## Node Restarts Automatically

If the node restarts automatically after stopping it:

### Cause: Active Auto-Start Flag

The node has an auto-start flag that indicates it should restart automatically. This is normal if you manually started the node, but can be problematic if you want to keep it stopped.

### Solution

1. **Stop the node correctly:**
   ```bash
   ./drive.sh exec infinite node-stop
   ```
   
   The `node-stop` command automatically removes the auto-start flag.

2. **Verify that the flag was removed:**
   ```bash
   ./drive.sh exec infinite ls -la /home/ubuntu/.node/auto-start
   ```
   
   If the file doesn't exist, the flag was removed correctly.

3. **If the node still restarts:**
   - Verify that the supervisor is stopped
   - Verify that there are no multiple supervisor instances
   - Review supervisor logs

## Node Won't Start After Container Restart

If the node doesn't start automatically after restarting the container:

### Verify Auto-Start Flag

The node only starts automatically if the auto-start flag exists:

```bash
./drive.sh exec infinite ls -la /home/ubuntu/.node/auto-start
```

**If the flag doesn't exist:**
- The node won't start automatically
- This is normal if you manually stopped the node before restarting the container
- Start the node manually with `node-start`

**If the flag exists but the node won't start:**
- Review container logs: `./drive.sh logs infinite-drive`
- Verify that the node is initialized
- Review auto-start logs if available

## Synchronization Problems After Restart

If the node has synchronization problems after restarting it:

### Verify Synchronization Status

```bash
./drive.sh exec infinite node-process-status
```

### Review Logs

```bash
./drive.sh exec infinite node-logs -f
```

**What to look for:**
- Peer connection errors
- Network problems
- Block validation errors

### Common Solutions

1. **Wait for synchronization** - Synchronization can take time
2. **Verify network connectivity** - See [Network Diagnosis]({{< relref "network-diagnosis" >}})
3. **Restart the node** - Sometimes a restart resolves temporary problems
4. **Clean data and resynchronize** - As a last resort, see [Delete Node Data]({{< relref "../guides/blockchain-nodes/delete-node-data" >}})

## See Also

- [Start/Stop Node]({{< relref "../guides/blockchain-nodes/start-stop-node" >}}) - Complete guide on how to start and stop the node
- [Node Monitoring]({{< relref "../guides/blockchain-nodes/node-monitoring" >}}) - How to monitor node status
- [Common Issues]({{< relref "common-issues" >}}) - Other common problems
- [Network Diagnosis]({{< relref "network-diagnosis" >}}) - Network diagnostic tools

