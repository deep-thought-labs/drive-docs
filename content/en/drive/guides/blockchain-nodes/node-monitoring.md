---
title: "Node Monitoring"
weight: 5226
---

Complete guide to monitor the status and activity of your blockchain node. This guide covers all available monitoring options, including logs, process status, synchronization, and network diagnosis.

## Access Monitoring

All monitoring options are available through the graphical interface in the **"Node Monitoring"** submenu.

### Using Graphical Interface (Recommended)

1. Open the graphical interface (see [Graphical Interface]({{< relref "graphical-interface" >}}))

2. Navigate: Main Menu → **"Node Monitoring"**

   ![Node Monitoring submenu](/images/node-ui-monitoring.png)

This submenu contains all options to monitor node status and logs.

## Available Monitoring Options

The **"Node Monitoring"** submenu includes the following options:

1. **Node Status** - Verify the node process status
2. **View Logs** - View the last N lines of logs
3. **Follow Logs** - Follow logs in real-time
4. **Network Diagnosis** - Network diagnosis and system information

## Verify Node Process Status

Verify if the node process is running and get information about the process.

### Using Graphical Interface (Recommended)

1. In the **"Node Monitoring"** submenu, select **"Node Status"** or **"Node Process Status"**

2. The interface will show information about the process status:
   - If running: PID, user, CPU time, and complete command
   - If not running: Message indicating the node is not active

### Using Command Line

**Simplified syntax (recommended):**
```bash
./drive.sh node-process-status
```

**Complete syntax (alternative):**
```bash
./drive.sh exec infinite node-process-status
```

**What it does:** Verifies if the node process is currently running and shows process information.

**Expected output:**
- **If running:** Shows PID, user, CPU time, and complete command
- **If not running:** Shows error message with instructions to start the node

**When to use:** Quick verification that the node process is active, especially useful for troubleshooting or monitoring scripts.

> [!NOTE]
> **Note on Status**
>
> This command verifies process status, not blockchain synchronization status. To verify blockchain synchronization, see the "Verify Synchronization" section below.

## View Node Logs

Node logs contain detailed information about blockchain node activity, including synchronization, block processing, errors, and connection status.

**Log file location:** `/var/log/node/node.log`

### View Last N Lines of Logs

Shows the last N lines of node logs.

#### Using Graphical Interface (Recommended)

1. In the **"Node Monitoring"** submenu, select **"View Logs"**

2. The interface will allow you to specify how many lines you want to see (by default, the last 50 lines)

3. Logs will be displayed on screen with the most recent information

#### Using Command Line

**Simplified syntax (recommended):**
```bash
# Last 50 lines (default)
./drive.sh node-logs

# Last N lines (specify number)
./drive.sh node-logs 100
./drive.sh node-logs 200
```

**Complete syntax (alternative):**
```bash
./drive.sh exec infinite node-logs
./drive.sh exec infinite node-logs 100
./drive.sh exec infinite node-logs 200
```

**What it does:** Shows the last N lines of the node log file (`/var/log/node/node.log`).

**Expected output:** Recent log entries showing:
- Node startup messages
- Synchronization progress
- Block processing
- Errors or warnings
- Connection status

**When to use:** To review recent node activity, verify errors, or check synchronization progress.

### Follow Logs in Real-Time

Shows node logs in real-time, automatically updating as new entries are written.

#### Using Graphical Interface (Recommended)

1. In the **"Node Monitoring"** submenu, select **"Follow Logs"**

2. Logs will begin showing in real-time

3. To stop following, press `Ctrl+C`

#### Using Command Line

**Simplified syntax (recommended):**
```bash
./drive.sh node-logs -f
# or
./drive.sh node-logs --follow
```

**Complete syntax (alternative):**
```bash
./drive.sh exec infinite node-logs -f
# or
./drive.sh exec infinite node-logs --follow
```

> [!TIP]
> **You Don't Need to Specify `-it`**
>
> The `drive.sh` script automatically detects that `node-logs -f` requires interactive mode and adds `-it` for you.

**What it does:** Streams log entries in real-time as they're written to the log file (similar to `tail -f`).

**Expected output:** Shows the message `ℹ️  Following node logs (Ctrl+C to exit)...` followed by a continuous stream of log entries. Press `Ctrl+C` to stop.

**When to use:** Monitor node activity while it's running, observe synchronization progress in real-time, or debug problems as they occur.

## Verify Synchronization

After starting your node, it will begin synchronizing with the blockchain network. You need to verify that synchronization is complete before proceeding with validator operations.

### Using Graphical Interface (Recommended)

1. In the **"Node Monitoring"** submenu, select **"Node Status"** or **"View Logs"**

2. Look for synchronization progress indicators in the logs:
   - Messages about blocks being synchronized
   - Synchronization progress
   - Messages indicating synchronization is complete

### Using Command Line

```bash
./drive.sh exec infinite infinited status
```

**What to look for:**
- **`catching_up: false`** - The node is completely synchronized
- **`catching_up: true`** - The node is still synchronizing (wait until it's `false`)
- **`latest_block_height`** - Current block height that the node has synchronized
- **`earliest_block_height`** - Oldest block the node has

**When synchronization is complete:**
- The node is ready for normal operations
- For validator nodes, you can proceed with creating your validator on the blockchain
- **Note:** Instructions for creating validators on the blockchain will be added to the documentation in a future update

## Network Diagnosis and System Information

The **"Node Monitoring"** submenu also includes options for network diagnosis and system information.

### Using Graphical Interface (Recommended)

1. In the **"Node Monitoring"** submenu, look for options such as:
   - **Network Diagnosis** - Network connectivity diagnosis
   - **System Information** - Information about the system and container

2. Select the desired option to see the corresponding information

### Available Information

Diagnosis and system options may include:

- **Network connection status** - Connectivity verification with other nodes
- **System information** - Details about the container and system resources
- **Network configuration** - Node ports and network configuration
- **Node statistics** - Performance and activity metrics

## Interpreting Logs

Node logs contain valuable information about node status and activity. Here are some common elements you may find:

### Startup Messages

When the node starts, you'll see messages such as:
- Component initialization
- Configuration loading
- Network connection

### Synchronization Progress

During synchronization, you'll see messages about:
- Blocks being downloaded
- Synchronization progress (percentage or block height)
- Estimated synchronization time

### Block Processing

Once synchronized, you'll see messages about:
- New blocks being processed
- Transactions being validated
- Blockchain state being updated

### Errors and Warnings

Logs will also show:
- Connection errors
- Synchronization problems
- Configuration warnings
- Validation errors

### Connection Status

Information about:
- Connections with other nodes (peers)
- P2P network status
- Latency and connection quality

## Troubleshooting Log Issues

If you encounter problems with node logs, see the centralized troubleshooting guide:

- **[Node Log Issues]({{< relref "../../troubleshooting/node-log-issues" >}})** - Solutions to common log-related problems

## Next Steps

After monitoring your node:

1. **[Start/Stop Node]({{< relref "start-stop-node" >}})** - Manage the node lifecycle
2. **[Graphical Interface]({{< relref "graphical-interface" >}})** - Use the graphical interface for all operations
3. **[Key Management]({{< relref "keys" >}})** - If you're a validator, manage your cryptographic keys
4. **[Troubleshooting]({{< relref "../../troubleshooting" >}})** - If you encounter problems, see the troubleshooting guide

## See Also

- [Start/Stop Node]({{< relref "start-stop-node" >}}) - How to start and stop the node
- [Graphical Interface]({{< relref "graphical-interface" >}}) - Complete guide to the graphical interface
- [Container Management]({{< relref "../general/container-management" >}}) - How to manage the Docker container
- [Troubleshooting]({{< relref "../../troubleshooting" >}}) - Troubleshooting guides

