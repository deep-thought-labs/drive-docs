---
title: "Supervisor and Auto-Start System"
weight: 401
---

The supervisor and auto-start system is an internal mechanism that ensures the node stays running and automatically restarts when necessary. This system consists of two main components: the **supervisor** and **auto-start**.

## System Components

### 1. Auto-Start Flag

The system uses a flag file (`NODE_AUTO_START_FLAG`) located at `~/.node/auto-start` to indicate that the node should start automatically.

**Location:**
```
/home/ubuntu/.node/auto-start
```

**Purpose:**
- Indicates that the node was manually started by the user
- Allows the node to automatically restart when the container restarts
- Controls whether the supervisor should monitor and restart the node

**Management:**
- Created when the user runs `node-start`
- Deleted when the user runs `node-stop`
- Checked when the container starts (`node-auto-start.sh`)
- Continuously checked by the supervisor (`node-supervisor.sh`)

### 2. Auto-Start Script (`node-auto-start.sh`)

This script runs automatically when the container starts (defined in the Dockerfile's `CMD`).

**Execution Flow:**

1. **Initialization Verification:**
   ```bash
   if [ ! -f "$NODE_GENESIS_FILE" ]; then
       exit 0  # Node not initialized, do nothing
   fi
   ```

2. **Flag Verification:**
   ```bash
   if [ -f "$NODE_AUTO_START_FLAG" ]; then
       # Clean obsolete PIDs from previous instances
       rm -f "$NODE_PID_FILE"
       rm -f "$NODE_SUPERVISOR_PID_FILE"
       
       # Start the node
       /usr/local/bin/node-start
   fi
   ```

**Characteristics:**
- Runs only once when the container starts
- Cleans obsolete PID files from previous container instances
- Only starts the node if the auto-start flag exists
- Executes `node-start` silently (redirects output to `/dev/null`)

### 3. Node Supervisor (`node-supervisor.sh`)

The supervisor is a background process that continuously monitors the node's status and restarts it if it detects that it has stopped unexpectedly.

**Monitoring Flow:**

```bash
while true; do
    # 1. Verify if the auto-start flag exists
    if [ ! -f "$NODE_AUTO_START_FLAG" ]; then
        # Flag deleted, user stopped the node explicitly
        exit 0  # Stop supervision
    fi
    
    # 2. Verify if the node process is running
    if ! pgrep -f "$NODE_PROCESS_PATTERN" > /dev/null; then
        # 3. Double-check the flag (prevent race condition)
        if [ -f "$NODE_AUTO_START_FLAG" ]; then
            # 4. Verify that the node is initialized
            if [ -f "$NODE_GENESIS_FILE" ]; then
                # 5. Restart the node
                /usr/local/bin/node-start
            fi
        fi
    fi
    
    sleep 10  # Wait 10 seconds before next check
done
```

**Characteristics:**
- Runs an infinite loop with checks every 10 seconds
- Verifies the auto-start flag before each action
- Detects if the node process has stopped using `pgrep`
- Prevents race conditions with double flag verification
- Only restarts if the node is initialized
- Logs events to the supervisor log (`/var/log/node/supervisor.log`)

**Supervisor Startup:**

The supervisor starts automatically when the user runs `node-start`:

```bash
# In node-start.sh
if ! pgrep -f "node-supervisor" > /dev/null; then
    nohup /usr/local/bin/node-supervisor > /dev/null 2>&1 &
    SUPERVISOR_PID=$!
    echo "$SUPERVISOR_PID" > "$NODE_SUPERVISOR_PID_FILE"
fi
```

**Supervisor Shutdown:**

The supervisor stops when the user runs `node-stop`:

```bash
# In node-stop.sh
# CRITICAL: Remove flag FIRST to prevent supervisor from restarting
rm -f "$NODE_AUTO_START_FLAG"

# Stop supervisor BEFORE stopping the node
if [ -f "$NODE_SUPERVISOR_PID_FILE" ]; then
    SUPERVISOR_PID=$(cat "$NODE_SUPERVISOR_PID_FILE")
    kill "$SUPERVISOR_PID" 2>/dev/null || true
    rm -f "$NODE_SUPERVISOR_PID_FILE"
fi

# Also remove any remaining supervisor process
pkill -f "node-supervisor" 2>/dev/null || true
```

## Complete System Flow

### Scenario 1: Manual Node Startup

1. User runs `node-start`
2. `node-start.sh` starts the node process
3. `node-start.sh` creates the `NODE_AUTO_START_FLAG` flag
4. `node-start.sh` starts the supervisor
5. Supervisor begins monitoring the node

### Scenario 2: Container Restart

1. Container restarts (for any reason)
2. Docker executes the Dockerfile's `CMD`: `node-auto-start.sh`
3. `node-auto-start.sh` checks if `NODE_AUTO_START_FLAG` exists
4. If it exists, executes `node-start` to restart the node
5. `node-start` creates the flag again and starts the supervisor

### Scenario 3: Unexpected Node Crash

1. The node process stops unexpectedly (crash, error, etc.)
2. Supervisor detects that the process is not running (in the next check, maximum 10 seconds)
3. Supervisor verifies that the auto-start flag exists
4. Supervisor executes `node-start` to restart the node
5. The node restarts automatically

### Scenario 4: Manual Node Shutdown

1. User runs `node-stop`
2. `node-stop.sh` removes the `NODE_AUTO_START_FLAG` flag **FIRST**
3. `node-stop.sh` stops the supervisor
4. `node-stop.sh` stops the node process
5. Supervisor detects that the flag doesn't exist and stops
6. The node will not restart automatically

## Related Files and Variables

**Files:**
- `~/.node/auto-start` - Auto-start flag
- `~/.node/supervisor.pid` - Supervisor process PID
- `/var/log/node/supervisor.log` - Supervisor log

**Configuration Variables:**
- `NODE_AUTO_START_FLAG` - Path to flag file
- `NODE_SUPERVISOR_PID_FILE` - Path to supervisor PID file
- `NODE_SUPERVISOR_LOG_FILE` - Path to supervisor log file
- `NODE_PROCESS_PATTERN` - Pattern to detect the node process

## Design Considerations

### Race Condition Prevention

The system implements several measures to prevent race conditions:

1. **Double flag verification:** The supervisor verifies the flag twice before restarting
2. **Operation order in node-stop:** The flag is removed BEFORE stopping the process
3. **Atomic verification:** Use of flag files for inter-process communication

### Process Isolation

- The supervisor runs with `nohup` to isolate it from the terminal
- The node runs with `setsid` to create a completely isolated session
- Processes are not affected by each other by terminal signals

### Logging

The supervisor logs important events in its log:
- Supervision start
- Node stopped detection
- Restart attempts
- Supervision stop

## See Also

- [Internal Process Management]({{< relref "process-management" >}}) - Details on daemonization and process tracking
- [Internal Configuration System]({{< relref "configuration-system" >}}) - System variables and configuration
- [Container Internal Scripts]({{< relref "internal-scripts" >}}) - Complete description of scripts

