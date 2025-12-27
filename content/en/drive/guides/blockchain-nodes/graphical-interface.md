---
title: "Graphical Interface"
weight: 5221
---

The graphical interface (node-ui) is the recommended method to manage your blockchain nodes. It provides visual access to all operations without needing to remember commands.

## Open the Graphical Interface

To access the graphical interface:

### Simplified Syntax (Recommended)

```bash
cd services/node0-infinite  # Or any other service
./drive.sh up -d            # Make sure the container is running
./drive.sh node-ui          # ✅ Simplified syntax - no need to specify exec or name
```

The script automatically:
- Detects that it's a `node-ui` command
- Gets the service name from the `docker-compose.yml` in the current directory
- Adds `exec` and the service name
- Adds `-it` automatically (since `node-ui` requires interactive mode)

### Complete Syntax (Alternative)

If you prefer to explicitly specify the service name:

```bash
cd services/node0-infinite
./drive.sh exec infinite node-ui
```

**Examples for different services using simplified syntax:**

```bash
# Infinite Mainnet
cd services/node0-infinite
./drive.sh node-ui          # ✅ Simplified syntax

# Infinite Testnet
cd services/node1-infinite-testnet
./drive.sh node-ui          # ✅ Simplified syntax

# Infinite Creative
cd services/node2-infinite-creative
./drive.sh node-ui          # ✅ Simplified syntax

# QOM Network
cd services/node3-qom
./drive.sh node-ui          # ✅ Simplified syntax
```

> [!TIP]
> **Advantage of Simplified Syntax**
>
> You don't need to remember the service name. The script automatically detects it from the `docker-compose.yml` in the current directory. Simply navigate to the service directory and run `./drive.sh node-ui`.

## Interface Structure

The graphical interface is organized in **submenus** that you can navigate using arrow keys and Enter. The main menu has **four main options**, each with its own submenu or function:

### Main Menu

The main menu contains the following options:

![node-ui Main Menu](/images/node-ui.png)

1. **Key Management** (Key Management)
2. **Node Operations** (Node Operations)
3. **Node Monitoring** (Node Monitoring)
4. **Help and Documentation** (Help and Documentation)

### Key Management

When selecting "Key Management" from the main menu, you'll access the key management submenu:

![Key Management submenu](/images/node-ui-keys.png)

This submenu contains all options related to cryptographic key management.

### Node Operations

When selecting "Node Operations" from the main menu, you'll access the node operations submenu:

![Node Operations submenu](/images/node-ui-operations.png)

This submenu contains basic node operations.

#### Node Operations Advanced

Within the "Node Operations" submenu, you'll find the "Node Operations Advanced" option that takes you to more advanced operations:

![Node Operations Advanced submenu](/images/node-ui-operations-advanced.png)

This submenu contains advanced operations such as node initialization and other configurations.

### Node Monitoring

When selecting "Node Monitoring" from the main menu, you'll access the monitoring submenu:

![Node Monitoring submenu](/images/node-ui-monitoring.png)

This submenu contains all options to monitor node status and logs.

### Help and Documentation

The "Help and Documentation" option prints essential information in the console about how to use commands directly without needing to use the graphical interface. It works as a help system for node options, providing examples and explanations about available commands.

> [!NOTE]
> **Note on Help Information**
>
> Some command examples shown in the "Help and Documentation" output may not be completely up-to-date, especially regarding:
> - Service names to call
> - Specific names of some commands
>
> However, the general explanation and command structure is correct and useful as a reference.

## How to Navigate

### Moving Between Options

- Use **arrow keys (↑↓)** to move between options
- Press **Enter** to select an option and enter a submenu
- You can navigate freely between submenus as needed

### Back Navigation

To return to the previous menu, you have two options:

- **"Back" option**: Each submenu has a "Back" option that you can select with arrows and Enter to return to the previous menu
- **Esc key**: Press the **Esc** key to return to the previous menu without needing to select the "Back" option

**Tip:** Don't worry about getting lost - you can always navigate back to the main menu using the "Back" option or the Esc key.

### Exit the Graphical Interface

To completely exit the graphical interface and terminate the process, you have two options:

- **Esc key (from main menu)**: If you're in the main menu, you can press the **Esc** key to exit the graphical interface
- **Ctrl+C**: Press the **Ctrl+C** key combination to terminate the process and completely exit the graphical interface from any menu or submenu

**Note about Ctrl+C:**
- The **Ctrl+C** combination works the same on macOS, Windows, and Linux
- **Cmd+C** is not enabled to exit the interface
- This is the standard way to terminate processes in terminal, similar to any other process you run on the command line

When exiting, the interface will close immediately and you'll return to your terminal's command line.

## See Also

- [Key Management]({{< relref "keys" >}}) - Complete guide on key management using the interface
- [Node Initialization]({{< relref "initialization" >}}) - How to initialize a node using the interface
- [Start/Stop Node]({{< relref "start-stop-node" >}}) - Basic node operations
