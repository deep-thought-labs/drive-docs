---
title: "Start/Stop Node"
weight: 5224
---

Complete guide to start, stop, and manage the lifecycle of your blockchain node. This guide covers both the **graphical interface (recommended)** and **command line operations (for advanced users)**.

## Start Node

After initializing your node, you need to start it so it begins synchronizing with the blockchain network.

### Using Graphical Interface (Recommended)

1. Open the graphical interface (see [Graphical Interface]({{< relref "graphical-interface" >}}))

2. Navigate: Main Menu → **"Node Operations"** → **"Start Node"**

   ![Start Node selected](/images/node-ui-operations-op1-start.png)

3. The interface will show the startup process and confirm when the node is running

### Using Command Line

#### Simplified Syntax (Recommended)

{{< callout type="info" >}}
**Available from Drive v0.1.12 (January 2026)**

The simplified syntax will be available starting from **Drive v0.1.12** in **January 2026**. If you're using an earlier version, use the complete syntax with `exec` and the service name.
{{< /callout >}}

```bash
./drive.sh node-start
```

#### Complete Syntax (Alternative)

```bash
./drive.sh exec infinite node-start
```

**What it does:** Starts the blockchain node as a daemon process in the background. The node runs continuously until you stop it manually.

**When to use:** After initializing the node, or when you need to start the node after having stopped it.

**Expected output:**
- Shows configuration details: Chain ID, EVM Chain ID, home directory, log location
- Success message: `✅ Node started successfully (PID: 123)`
- Instructions to view logs and stop the node

> [!NOTE]
> **Technical Details**
>
> For detailed information on how node startup works internally, see [Internal Process Management]({{< relref "../../internal-workings/process-management" >}}) and [Supervisor and Auto-Start System]({{< relref "../../internal-workings/supervisor-auto-start" >}}).

**If the node is already running:** The command will show a warning with the existing PID and exit without starting a duplicate instance.

## Stop Node

Stopping the node in a controlled manner is important to maintain data integrity, especially for validators.

### Using Graphical Interface (Recommended)

1. Open the graphical interface (see [Graphical Interface]({{< relref "graphical-interface" >}}))

2. Navigate: Main Menu → **"Node Operations"** → **"Stop Node"**

   ![Stop Node selected](/images/node-ui-operations-op2-stop.png)

3. Confirm the operation

### Using Command Line

#### Simplified Syntax (Recommended)

{{< callout type="info" >}}
**Available from Drive v0.1.12 (January 2026)**

The simplified syntax will be available starting from **Drive v0.1.12** in **January 2026**. If you're using an earlier version, use the complete syntax with `exec` and the service name.
{{< /callout >}}

```bash
./drive.sh node-stop
```

#### Complete Syntax (Alternative)

```bash
./drive.sh exec infinite node-stop
```

**What it does:** Stops the node process in a controlled manner. Sends a termination signal (SIGTERM) and waits for the process to close correctly.

**When to use:** Before making configuration changes, updating the node, or when you need to temporarily stop the node.

**Expected output:**
- Header: `Stopping Infinite Drive Blockchain Node`
- Message: `Stopping node process (PID: 123)...`
- Success: `✅ Node stopped successfully`

**Controlled shutdown:** The node saves its state before stopping, ensuring data integrity. This is important for validators to avoid slashing (penalties).

> [!WARNING]
> **⚠️ Warning for Validators**
>
> Always stop the node in a controlled manner before:
> - Shutting down the server
> - Restarting the container
> - Making configuration changes
>
> An abrupt shutdown can cause synchronization problems and, in extreme cases, can result in slashing for validators.

## Verify Status and Synchronization

To verify node status and synchronization, see the complete [Node Monitoring]({{< relref "node-monitoring" >}}) guide, which includes:

- Verify node process status
- View node logs (last lines and real-time)
- Verify blockchain synchronization
- Network diagnosis and system information

## Restart Node

To restart the node (stop and start again), see the complete guide:

- **[Restart Node]({{< relref "restart-node" >}})** - Complete guide on how to restart the node

## Troubleshooting

If you encounter problems starting or stopping the node, see the centralized troubleshooting guide:

- **[Node Start/Stop Issues]({{< relref "../../troubleshooting/node-start-stop-issues" >}})** - Solutions to common problems related to starting and stopping the node

## Next Steps

After starting your node:

1. **[Node Monitoring]({{< relref "node-monitoring" >}})** - Monitor your node's status, logs, and synchronization
2. **[Graphical Interface]({{< relref "graphical-interface" >}})** - Use the graphical interface to manage your node
3. **[Key Management]({{< relref "keys" >}})** - If you're a validator, manage your cryptographic keys

## See Also

- [Node Monitoring]({{< relref "node-monitoring" >}}) - Complete guide to monitor status, logs, and synchronization
- [Node Initialization]({{< relref "initialization" >}}) - How to initialize a node before starting it
- [Delete Node Data]({{< relref "delete-node-data" >}}) - How to delete node data to reinitialize
- [Graphical Interface]({{< relref "graphical-interface" >}}) - Use the graphical interface to manage your node
- [Container Management]({{< relref "../general/container-management" >}}) - How to manage the Docker container
- [Node Data]({{< relref "../../../../concepts/node-data" >}}) - Understand what node data is and its importance
- [Permission Issues]({{< relref "../../troubleshooting/permission-issues" >}}) - Troubleshooting permission problems
