---
title: "Container Internal Scripts"
weight: 408
---

The Drive container includes a collection of shell scripts that provide all node management functionality. This section documents each script, its purpose, and how they interact with each other.

## Script Architecture

### Configuration Loading

All scripts follow the same loading pattern:

```bash
#!/bin/bash

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load centralized configuration
source "${SCRIPT_DIR}/node-config.sh"

# Load styles (if necessary)
source "${SCRIPT_DIR}/styles.sh"
```

**Advantages:**
- Centralized configuration
- Consistency between scripts
- Easy maintenance

## Configuration and Utility Scripts

### `node-config.sh`

**Purpose:** Centralized system configuration.

**Content:**
- Environment variables with default values
- Fixed and derived paths
- Utility functions (`build_node_start_command`, `validate_node_config`)
- Process detection patterns

**Usage:**
- Loaded by all scripts
- Not executed directly
- Provides shared configuration

**Location:** `/usr/local/bin/node-config.sh`

### `styles.sh`

**Purpose:** Formatting and style functions for terminal output.

**Content:**
- Colors and text formatting
- Print functions (`print_header`, `print_success`, `print_error`, etc.)
- Utility functions (`is_interactive`, `print_code`, etc.)

**Usage:**
- Loaded by scripts that need formatted output
- Provides consistent interface for messages

**Location:** `/usr/local/bin/styles.sh`

### `dialog-theme.sh`

**Purpose:** Theme configuration for the `dialog` graphical interface.

**Usage:**
- Loaded by `node-ui.sh`
- Defines colors and TUI interface style

**Location:** `/usr/local/bin/dialog-theme.sh`

### `container-info.sh`

**Purpose:** Information about the container and system.

**Usage:**
- Provides system information
- Used by diagnostic scripts

**Location:** `/usr/local/bin/container-info.sh`

## Main Management Scripts

### `node-init`

**Purpose:** Initialize the blockchain node.

**Functionality:**
- Verifies if the node is already initialized
- Requests or receives moniker
- Supports simple mode (random keys) and recovery (with seed phrase)
- Downloads and validates official genesis
- Configures the node for use

**Arguments:**
- `[moniker]` - Node name
- `--recover` or `-r` - Recovery mode with seed phrase

**Usage:**
```bash
node-init my-node
node-init --recover my-node
```

**See also:** [Technical Initialization Flow]({{< relref "initialization-flow" >}})

### `node-start`

**Purpose:** Start the blockchain node.

**Functionality:**
- Validates configuration
- Verifies that the node is initialized
- Verifies that the node is not already running
- Builds startup command dynamically
- Starts the node as daemon with `setsid`
- Creates auto-start flag
- Starts the supervisor
- Saves process PID

**Characteristics:**
- Complete process isolation
- Log redirection
- Automatic restart in case of crash

**Usage:**
```bash
node-start
```

**See also:** [Internal Process Management]({{< relref "process-management" >}}), [Supervisor and Auto-Start System]({{< relref "supervisor-auto-start" >}})

### `node-stop`

**Purpose:** Stop the blockchain node gracefully.

**Functionality:**
- Reads PID from file or detects process
- Removes auto-start flag (prevents restart)
- Stops supervisor first
- Sends SIGTERM to the node process
- Waits up to 30 seconds for graceful termination
- If it doesn't terminate, sends SIGKILL
- Cleans PID files

**Characteristics:**
- Graceful shutdown with fallback to forced
- Prevents race conditions
- Complete cleanup of control files

**Usage:**
```bash
node-stop
```

**See also:** [Internal Process Management]({{< relref "process-management" >}})

### `node-logs`

**Purpose:** View node logs.

**Functionality:**
- Verifies that the log file exists
- Shows last N lines (default 50)
- Supports real-time following with `-f` or `--follow`
- Uses `exec tail -f` for signal isolation

**Arguments:**
- `[number]` - Number of lines to show
- `-f` or `--follow` - Follow logs in real-time

**Usage:**
```bash
node-logs          # Last 50 lines
node-logs 100       # Last 100 lines
node-logs -f        # Follow in real-time
```

**See also:** [Internal Logging System]({{< relref "logging-system" >}})

### `node-keys`

**Purpose:** Manage node cryptographic keys.

**Functionality:**
- Create new keys
- Add keys from seed phrase
- List existing keys
- Show key information
- Delete keys
- Reset keyring password

**Subcommands:**
- `create` or `new` - Create new key
- `add` - Add key from seed phrase
- `list` - List all keys
- `show` - Show key information
- `delete` - Delete a key
- `reset-password` - Reset keyring password

**Usage:**
```bash
node-keys create my-key
node-keys add my-key
node-keys list
node-keys show my-key
node-keys delete my-key
node-keys reset-password
```

### `node-clean-data`

**Purpose:** Clean node data.

**Functionality:**
- Verifies that the node is stopped
- Supports cleaning: all, blockchain only, or keyring only
- Creates keyring backup before deleting
- Requests interactive confirmation
- Removes auto-start flag if cleaning all

**Arguments:**
- `all` - Delete all data
- `blockchain` - Delete only blockchain data
- `keyring` - Delete only keyring

**Usage:**
```bash
node-clean-data all
node-clean-data blockchain
node-clean-data keyring
```

## System Scripts

### `node-supervisor`

**Purpose:** Monitor and automatically restart the node if it stops.

**Functionality:**
- Infinite loop with checks every 10 seconds
- Verifies auto-start flag
- Detects if the node process is running
- Restarts the node if it stops and the flag exists
- Logs events to supervisor log
- Stops if the flag is deleted

**Characteristics:**
- Executed in background
- Race condition prevention
- Event logging

**Usage:**
- Started automatically by `node-start`
- Not executed directly by user

**See also:** [Supervisor and Auto-Start System]({{< relref "supervisor-auto-start" >}})

### `node-auto-start`

**Purpose:** Automatically start the node when the container starts.

**Functionality:**
- Verifies if the node is initialized
- Verifies if auto-start flag exists
- Cleans obsolete PIDs from previous instances
- Starts the node if the flag exists

**Characteristics:**
- Executed by the Dockerfile's `CMD`
- Runs only once when the container starts
- Silent (redirects output to `/dev/null`)

**Usage:**
- Executed automatically by Docker
- Not executed directly by user

**See also:** [Supervisor and Auto-Start System]({{< relref "supervisor-auto-start" >}}), [Container Architecture]({{< relref "container-architecture" >}})

## Monitoring and Diagnostic Scripts

### `node-process-status`

**Purpose:** Show node process status.

**Functionality:**
- Verifies if the process is running
- Shows process information (PID, execution time, etc.)
- Shows resource usage (CPU, memory)

**Usage:**
```bash
node-process-status
```

### `node-network-diagnosis`

**Purpose:** Network and connectivity diagnosis.

**Functionality:**
- Verifies connectivity with peers
- Shows network information
- Diagnoses connection problems

**Usage:**
```bash
node-network-diagnosis
```

## Utility Scripts

### `node-update-genesis`

**Purpose:** Update the node's genesis file.

**Functionality:**
- Downloads the latest official genesis
- Validates JSON format
- Replaces current genesis
- Verifies that the node is stopped

**Usage:**
```bash
node-update-genesis
```

### `node-validate-genesis`

**Purpose:** Validate the current genesis file.

**Functionality:**
- Verifies JSON format
- Validates genesis structure
- Shows genesis information

**Usage:**
```bash
node-validate-genesis
```

### `node-help`

**Purpose:** Show help and documentation.

**Functionality:**
- Lists all available commands
- Shows usage and examples
- Provides quick reference information

**Usage:**
```bash
node-help
```

## User Interface Scripts

### `node-ui`

**Purpose:** Terminal graphical interface (TUI) for node management.

**Functionality:**
- Main menu with options
- Submenus for different categories:
  - Key management
  - Node operations
  - Monitoring
  - Help
- Uses `dialog` for the interface
- Calls corresponding scripts based on selection

**Characteristics:**
- Interactive and user-friendly interface
- Menu navigation
- Integration with all scripts

**Usage:**
```bash
node-ui
```

**Requirements:**
- Interactive terminal
- `dialog` installed

## Script Interactions

### Startup Flow

```
node-auto-start (when container starts)
    ↓
node-start
    ↓
    ├─ Creates auto-start flag
    ├─ Starts infinited process
    └─ Starts node-supervisor
```

### Shutdown Flow

```
node-stop
    ↓
    ├─ Removes auto-start flag
    ├─ Stops node-supervisor
    └─ Stops infinited process
```

### Automatic Restart Flow

```
node-supervisor (every 10 seconds)
    ↓
    Does auto-start flag exist?
    ├─ No → Stop supervision
    └─ Yes → Is process running?
        ├─ Yes → Continue monitoring
        └─ No → node-start (restart)
```

### Cleanup Flow

```
node-clean-data
    ↓
    Is node running?
    ├─ Yes → Error (must be stopped)
    └─ No → What to clean?
        ├─ All → Remove auto-start flag
        ├─ Blockchain → Only blockchain data
        └─ Keyring → Only keyring (with backup)
```

## Script Location

All scripts are installed in `/usr/local/bin/`:

```
/usr/local/bin/
├── node-init
├── node-start
├── node-stop
├── node-logs
├── node-keys
├── node-supervisor
├── node-auto-start
├── node-clean-data
├── node-process-status
├── node-network-diagnosis
├── node-update-genesis
├── node-validate-genesis
├── node-help
├── node-ui
├── node-config.sh
├── styles.sh
├── dialog-theme.sh
└── container-info.sh
```

**Note:** Most scripts have the `.sh` extension removed to facilitate their use.

## Permissions and Ownership

All scripts are:
- **Executable:** `chmod +x`
- **Owner:** `ubuntu:ubuntu` (UID 1000:GID 1000)
- **Permissions:** `755` (rwxr-xr-x)

## Interactive vs Non-Interactive Mode

Most scripts support both modes:

### Interactive Mode

- Requests information from user when necessary
- Shows formatted messages
- Confirms destructive actions

### Non-Interactive Mode

- Uses command line arguments
- Doesn't request confirmation
- Suitable for automation

**Detection:**
```bash
is_interactive() {
    [ -t 0 ] && [ -t 1 ]
}
```

## Error Handling

All scripts implement consistent error handling:

1. **Early validation:** Verify requirements before executing
2. **Clear messages:** Provide descriptive error messages
3. **Exit codes:** Use appropriate exit codes
4. **Cleanup:** Clean resources in case of error

## See Also

- [Internal Configuration System]({{< relref "configuration-system" >}}) - How scripts load configuration
- [Internal Process Management]({{< relref "process-management" >}}) - How scripts manage processes
- [Container Architecture]({{< relref "container-architecture" >}}) - How scripts are installed

