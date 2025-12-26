---
title: "Restart Node"
weight: 5225
---

Guide to restart the blockchain node (stop and start again). This guide covers both the **graphical interface (recommended)** and **command line operations (for advanced users)**.

## When to Restart the Node?

You may need to restart the node in the following situations:

- **After configuration changes** - Some changes require restarting the node
- **Synchronization issues** - A restart can resolve temporary problems
- **Updates** - After updating the node or container
- **Performance issues** - If the node is running slowly
- **Scheduled maintenance** - To perform maintenance tasks

## Restart Node

To restart the node (stop and start again):

### Using Graphical Interface (Recommended)

1. Open the graphical interface (see [Graphical Interface]({{< relref "graphical-interface" >}}))

2. Navigate: Main Menu → **"Node Operations"** → **"Restart Node"**

   ![Restart Node selected](/images/node-ui-operations-op3-restart.png)

3. The interface will stop and restart the node automatically

### Using Command Line

1. **Stop the node:**
   ```bash
   ./drive.sh exec infinite node-stop
   ```

2. **Wait a few seconds** for the process to close completely (up to 30 seconds)

3. **Start the node again:**
   ```bash
   ./drive.sh exec infinite node-start
   ```

**Complete example:**
```bash
./drive.sh exec infinite node-stop
sleep 5  # Wait 5 seconds
./drive.sh exec infinite node-start
```

## What Happens During Restart

During restart, the system performs the following operations:

1. **Controlled shutdown:**
   - Sends SIGTERM signal to the node process
   - Waits up to 30 seconds for graceful shutdown
   - The node saves its state before stopping

2. **Resource cleanup:**
   - Removes the auto-start flag (temporarily)
   - Stops the supervisor
   - Cleans PID files

3. **Restart:**
   - Starts the node process again
   - Creates new auto-start flag
   - Starts the supervisor again
   - The node begins synchronizing with the network

## Important Considerations

### For Validators

> [!WARNING]
> **⚠️ Warning for Validators**
>
> When restarting a validator node:
> - Make sure the restart is controlled (don't force shutdown)
> - The node may lose some blocks during restart
> - In extreme cases, a poorly executed restart can result in slashing
> - Always use `node-stop` before restarting, never force shutdown

### Restart Time

Restart time depends on:

- **Shutdown time:** Up to 30 seconds for graceful shutdown
- **Start time:** Generally a few seconds
- **Synchronization time:** May take time if the node became desynchronized

### Synchronization Status

After restarting:

- The node will begin synchronizing automatically
- May take time depending on how long it was stopped
- Use `node-process-status` to verify synchronization status

## Verify Restart

After restarting, verify that the node is working correctly:

### 1. Verify Process Status

```bash
./drive.sh exec infinite node-process-status
```

**What to look for:**
- The process is running
- The PID is different from the previous one (restart confirmation)
- The node is synchronizing

### 2. Verify Logs

```bash
./drive.sh exec infinite node-logs -f
```

**What to look for:**
- Successful startup messages
- Connection with peers
- Synchronization process

### 3. Verify Synchronization

See the [Node Monitoring]({{< relref "node-monitoring" >}}) guide to verify synchronization status.

## Troubleshooting

If you encounter problems restarting the node:

- **[Start/Stop Issues]({{< relref "../../troubleshooting/node-start-stop-issues" >}})** - Solutions to common problems
- **[Common Issues]({{< relref "../../troubleshooting/common-issues" >}})** - Other common problems

## Next Steps

After restarting your node:

1. **[Node Monitoring]({{< relref "node-monitoring" >}})** - Monitor status and synchronization
2. **[Graphical Interface]({{< relref "graphical-interface" >}})** - Use the graphical interface to manage your node
3. **[Key Management]({{< relref "keys" >}})** - If you're a validator, manage your cryptographic keys

## See Also

- [Start/Stop Node]({{< relref "start-stop-node" >}}) - How to start and stop the node individually
- [Node Monitoring]({{< relref "node-monitoring" >}}) - Complete guide to monitor status, logs, and synchronization
- [Graphical Interface]({{< relref "graphical-interface" >}}) - Use the graphical interface for all operations
- [Start/Stop Issues]({{< relref "../../troubleshooting/node-start-stop-issues" >}}) - Related troubleshooting

