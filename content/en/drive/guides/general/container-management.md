---
title: "Container Management"
weight: 5211
---

Learn how to manage Drive containers using the `drive.sh` script. All Drive services use this script for management operations.

## What is drive.sh?

The `drive.sh` script is a **wrapper around `docker compose`**. This means it functions as an abstraction layer that simplifies and improves the use of Docker Compose, while maintaining the same basic syntax.

### Advantages of using drive.sh

- ✅ **Automatic permission handling** - Automatically configures `persistent-data` permissions
- ✅ **Works with or without `sudo`** - Detects and handles both cases automatically
- ✅ **Consistent interface** - The same commands work across all services
- ✅ **Simplified management** - Abstracts Docker Compose complexity
- ✅ **Simplified syntax** - For `node-*` commands, you don't need to specify `exec` or the service name
- ✅ **Automatic interactive mode detection** - Automatically adds `-it` when necessary

{{< callout type="info" >}}
**Simplified Syntax Availability**

The simplified syntax for `node-*` commands (which doesn't require specifying `exec` or the service name) will be available starting from **Drive v0.1.12** in **January 2026**.

If you're using an earlier version, you'll need to use the complete syntax with `exec` and the service name.
{{< /callout >}}

## Script Location

Each service has its own `drive.sh` script in its directory:

```bash
cd services/<service-name>
./drive.sh <command>
```

**Important:** Always navigate to the service directory before executing commands with `drive.sh`.

## Available Commands

### 🚀 Start Service

Start the service in daemon mode (background):

```bash
./drive.sh up -d
```

This command creates and starts the Docker container for the service.

### 📊 Show Container Status

Check the current status of the container:

```bash
./drive.sh ps
```

Shows information about the container: whether it's running, when it started, etc.

### ⏹️ Stop Service

Stop the service gracefully:

```bash
./drive.sh stop
```

The container stops but is not removed, so you can restart it later.

### 🗑️ Stop and Remove Container

Stop the service and remove the container:

```bash
./drive.sh down
```

**Note:** This removes the container but **does not** remove persistent data stored in `persistent-data/`.

### ▶️ Start Service (if stopped)

If the service is stopped but the container still exists, you can start it:

```bash
./drive.sh start
```

### 🔄 Restart Service

Restart a service that is already running:

```bash
./drive.sh restart
```

Useful when you need to apply configuration changes or resolve temporary issues.

### 📋 View Container Logs

Container logs show information about the Docker container itself, including startup messages, Docker errors, and any output from the container's entrypoint or CMD.

> [!NOTE]
> **Difference between Container Logs and Node Logs**
>
> It's important to understand the difference:
> - **Container logs:** Docker logs (container startup, Docker errors, container configuration)
> - **Node logs:** Blockchain process logs (synchronization, blocks, node activity)
>
> To view blockchain node logs, see [Node Monitoring]({{< relref "../blockchain-nodes/node-monitoring" >}}).

#### View All Logs

```bash
cd services/node0-infinite  # Or any other service
./drive.sh logs
```

Shows all container logs from startup.

#### Follow Logs in Real-Time

```bash
cd services/node0-infinite
./drive.sh logs -f
```

Shows container logs in real-time, updating automatically. Press `Ctrl+C` to stop.

#### View Last N Lines

```bash
cd services/node0-infinite
./drive.sh logs --tail=100
```

Shows only the last 100 lines of logs. You can change the number as needed.

#### View Last N Lines and Follow

```bash
cd services/node0-infinite
./drive.sh logs --tail=100 -f
```

Shows the last 100 lines and then continues showing new logs in real-time.

#### Filter Logs by Time

```bash
cd services/node0-infinite
# Logs from the last hour
./drive.sh logs --since=1h

# Logs until 1 hour ago
./drive.sh logs --until=1h
```

**Available options:**
- `-f` or `--follow`: Stream logs in real-time
- `--tail=N`: Show only the last N lines
- `--since=1h`: Show logs from 1 hour ago (you can use `1m`, `1h`, `1d`, etc.)
- `--until=1h`: Show logs until 1 hour ago

**When to use container logs:**
- Debug container startup problems
- View Docker-level errors
- Verify container configuration
- Permission or volume mount issues

**When to use node logs:**
- Monitor blockchain node activity
- View synchronization progress
- Debug blockchain problems
- View block processing

For more information on node logs, see [Node Monitoring]({{< relref "../blockchain-nodes/node-monitoring" >}}).

## Execute Commands Inside Container

To execute commands inside the container, `drive.sh` offers two ways to do it:

### ✨ Simplified Syntax (Recommended)

{{< callout type="info" >}}
**Available from Drive v0.1.12 (January 2026)**

The simplified syntax will be available starting from **Drive v0.1.12** in **January 2026**. If you're using an earlier version, use the complete syntax with `exec` and the service name.
{{< /callout >}}

For commands that start with `node-*` (like `node-init`, `node-ui`, `node-keys`, etc.), you can use the simplified syntax:

```bash
./drive.sh <node-*-command>
```

The script automatically:
- Detects that it's a `node-*` command
- Gets the service name from the `docker-compose.yml` in the current directory
- Adds `exec` and the service name automatically
- Adds `-it` if the command requires interactive mode

**Examples:**
```bash
# Simplified syntax - Script completes automatically
./drive.sh node-ui              # Open graphical interface
./drive.sh node-init            # Initialize node
./drive.sh node-init --recover  # Initialize with recovery
./drive.sh node-keys list       # List keys
./drive.sh node-keys create     # Create new key
./drive.sh node-start           # Start node
./drive.sh node-logs -f         # View logs in real-time
```

> [!TIP]
> **Advantage of Simplified Syntax**
>
> You don't need to remember the service name or specify `exec` or `-it`. The script does it automatically for you.

### Complete Syntax (Alternative)

If you prefer to explicitly specify the service name, you can use the complete syntax:

```bash
./drive.sh exec <container-name> <command>
```

**Examples:**
```bash
# Complete syntax - You specify everything manually
./drive.sh exec infinite node-ui
./drive.sh exec infinite node-init --recover
./drive.sh exec infinite node-keys list
```

**When to use complete syntax:**
- If you want to specify a different service than the current directory
- If you prefer to be explicit about which service you're using
- For commands that are not `node-*` (like `bash`, `sh`, etc.)

**Equivalent to:**
```bash
docker compose exec <container-name> <command>
```

### 💻 Access Container Shell

To access the container shell, you must use the complete syntax (since `bash` is not a `node-*` command):

```bash
./drive.sh exec <container-name> bash
```

**Example:**
```bash
cd services/node0-infinite
./drive.sh exec infinite bash
```

Useful for debugging, inspecting files inside the container, or running manual commands.

> [!NOTE]
> **Commands that Require Complete Syntax**
>
> Some commands always require complete syntax because they are not `node-*` commands:
> - `bash` or `sh` - Access shell
> - System commands like `ls`, `cat`, `grep`, etc.
> - Custom commands that don't follow the `node-*` pattern
>
> For `node-*` commands, you can use simplified syntax. For other commands, use complete syntax with the container name.

## Container Names by Service

> [!IMPORTANT]
> **Simplified Syntax for `node-*` Commands**
>
> {{< callout type="info" >}}
> **Available from Drive v0.1.12 (January 2026)**
>
> This functionality will be available starting from **Drive v0.1.12** in **January 2026**. If you're using an earlier version, you'll need to use the complete syntax specifying the container name.
> {{< /callout >}}
>
> For commands that start with `node-*`, you **DO NOT need** to specify the container name. The script automatically detects it from the `docker-compose.yml` in the current directory.
>
> **Simplified example:**
> ```bash
> cd services/node0-infinite
> ./drive.sh node-ui          # ✅ Works without specifying name
> ./drive.sh node-init         # ✅ Works without specifying name
> ```
>
> **You only need to specify the container name for:**
> - Commands that are NOT `node-*` (like `bash`, `sh`, `ls`, etc.)
> - When you want to use complete syntax explicitly

### Container Name Reference Table

If you need to use complete syntax or access commands that are not `node-*`, here are the container names by service:

| Service | Container Name | Example with Simplified Syntax | Example with Complete Syntax |
|---------|----------------|--------------------------------|------------------------------|
| `node0-infinite` | `infinite` | `./drive.sh node-ui` | `./drive.sh exec infinite bash` |
| `node1-infinite-testnet` | `infinite-testnet` | `./drive.sh node-ui` | `./drive.sh exec infinite-testnet bash` |
| `node2-infinite-creative` | `infinite-creative` | `./drive.sh node-ui` | `./drive.sh exec infinite-creative bash` |
| `node3-qom` | `qom` | `./drive.sh node-ui` | `./drive.sh exec qom bash` |

### Usage Examples

Here are practical examples using both syntaxes:

```bash
# Infinite Mainnet (node0-infinite)
cd services/node0-infinite

# Simplified syntax (recommended for node-* commands)
./drive.sh node-ui              # ✅ Open graphical interface
./drive.sh node-init            # ✅ Initialize node
./drive.sh node-keys list       # ✅ List keys

# Complete syntax (required for non-node-* commands)
./drive.sh exec infinite bash   # Access container shell

# Infinite Testnet (node1-infinite-testnet)
cd services/node1-infinite-testnet
./drive.sh node-ui              # ✅ Simplified syntax
./drive.sh exec infinite-testnet bash  # Complete syntax for bash

# Infinite Creative (node2-infinite-creative)
cd services/node2-infinite-creative
./drive.sh node-ui              # ✅ Simplified syntax
./drive.sh exec infinite-creative bash  # Complete syntax

# QOM Network (node3-qom)
cd services/node3-qom
./drive.sh node-ui              # ✅ Simplified syntax
./drive.sh exec qom bash         # Complete syntax
```

> [!NOTE]
> **Command-Specific Documentation**
>
> For specific commands like blockchain commands (for example, `node-keys`, `node-start`, `node-init`, etc.) and other specialized commands, see the corresponding specific documentation:
>
> - **Blockchain Node Commands**: See guides in [Blockchain Nodes]({{< relref "../../guides/blockchain-nodes" >}}) for specific blockchain node commands
> - **Other specialized commands**: Each type of service may have specific commands documented in its corresponding section

### How to Verify Container Name

If you're not sure of the container name for your service:

1. **Use `./drive.sh ps`**: Shows the container name in the list
   ```bash
   cd services/node0-infinite
   ./drive.sh ps
   ```

2. **Check `docker-compose.yml`**: The name is defined under `container_name`
   ```bash
   cat docker-compose.yml | grep container_name
   ```

**Important:** 
- The container name is defined in each service's `docker-compose.yml` file
- **For `node-*` commands**: You don't need to specify the container name - use simplified syntax
- **For other commands**: You must use complete syntax with the container name
- Most management commands (up, down, stop, start, ps, logs) **DO NOT require** specifying the container name
- The script automatically detects interactive mode and adds `-it` when necessary for `node-*` commands
