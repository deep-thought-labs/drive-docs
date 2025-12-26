---
title: "Internal Process Management"
weight: 402
---

The Drive system uses advanced process management techniques to ensure the blockchain node runs stably and isolated. This section documents how daemonization, PID tracking, and signal handling work.

## Node Daemonization

### Main Method: `setsid`

The node is started as a daemon process using `setsid`, which creates a new session completely isolated from the terminal:

```bash
setsid bash -c "eval ${START_CMD} > ${NODE_LOG_FILE} 2>&1" < /dev/null &
```

**`setsid` Characteristics:**

1. **New Session:** Creates a new process session, separated from the terminal
2. **Signal Isolation:** Terminal signals (SIGINT, SIGHUP, etc.) don't affect the process
3. **Process Leader:** The process becomes the leader of its own session
4. **I/O Redirection:** Redirects stdin from `/dev/null` to avoid blocking

**Advantages:**
- The node continues running even if the terminal closes
- Terminal signals don't affect the node process
- The process is completely isolated from the shell that started it

### Alternative Method: `nohup`

If `setsid` is not available, the system uses `nohup` as a fallback:

```bash
eval "nohup ${START_CMD} > ${NODE_LOG_FILE} 2>&1 &"
NODE_PID=$!
disown $NODE_PID 2>/dev/null || true
```

**`nohup` Characteristics:**
- Prevents the process from receiving SIGHUP when the terminal closes
- Redirects output to a log file
- `disown` removes the process from the shell's job table

## PID Tracking

### PID Files

The system maintains PID files to track important processes:

**Files:**
- `~/.node/node.pid` - PID of the blockchain node process
- `~/.node/supervisor.pid` - PID of the supervisor process

**Location:**
```
/home/ubuntu/.node/node.pid
/home/ubuntu/.node/supervisor.pid
```

### PID Retrieval

The system uses multiple methods to get the node's PID:

1. **From PID file:**
   ```bash
   PID=$(cat "$NODE_PID_FILE")
   ```

2. **From running process (using `pgrep`):**
   ```bash
   PID=$(pgrep -f "$NODE_PROCESS_PATTERN" | head -1)
   ```

3. **Existence verification:**
   ```bash
   if ps -p $PID > /dev/null; then
       # Process exists
   fi
   ```

### Process Detection Pattern

The system uses a specific pattern to identify the node process:

```bash
NODE_PROCESS_PATTERN="${NODE_BINARY_PATH} start.*--chain-id ${NODE_CHAIN_ID}"
```

**Example:**
```
/usr/local/bin/infinited start.*--chain-id infinite_421018-1
```

**Advantages:**
- Allows multiple nodes on the same host (different chain-id)
- Specifically identifies the node process, not other processes
- Avoids false positives with other processes using the binary

## Signal Handling

### Graceful Shutdown (SIGTERM)

When the user runs `node-stop`, the system first attempts to stop the node gracefully:

```bash
kill -TERM $PID
```

**Process:**
1. SIGTERM is sent to the process
2. The process has up to 30 seconds to terminate gracefully
3. The system checks every second if the process still exists
4. If the process terminates within the time, it's considered successful

**Code:**
```bash
kill -TERM $PID

# Wait until it terminates (maximum 30 seconds)
for i in {1..30}; do
    if ! ps -p $PID > /dev/null; then
        print_success "Node stopped successfully"
        rm -f "$NODE_PID_FILE"
        exit 0
    fi
    sleep 1
done
```

### Forced Termination (SIGKILL)

If the process doesn't respond to SIGTERM within 30 seconds, termination is forced:

```bash
if ps -p $PID > /dev/null; then
    print_warning "Forcing termination..."
    kill -KILL $PID
    rm -f "$NODE_PID_FILE"
    print_success "Node stopped (forced)"
fi
```

**Considerations:**
- SIGKILL cannot be ignored by the process
- May result in data loss if the node was writing
- Only used as a last resort

## Process Status Verification

### Running Process Verification

Before starting the node, the system verifies if it's already running:

```bash
if pgrep -f "$NODE_PROCESS_PATTERN" > /dev/null; then
    local_pid=$(pgrep -f "$NODE_PROCESS_PATTERN" | head -1)
    print_warning "The node is already running (PID: $local_pid)"
    exit 1
fi
```

### Post-Startup Verification

After starting the node, the system verifies that it actually started:

```bash
# Wait a moment for the process to start
sleep 2

# Verify that the process exists
if [ -n "$NODE_PID" ] && ps -p $NODE_PID > /dev/null; then
    print_success "Node started successfully (PID: $NODE_PID)"
    # Save PID to file
    echo "$NODE_PID" > "$NODE_PID_FILE"
else
    print_error "The node could not start"
    exit 1
fi
```

## Process Isolation

### Node Isolation

The node process is completely isolated:

1. **Isolated Session:** `setsid` creates a new session
2. **Redirected I/O:** stdin, stdout, stderr redirected to files/logs
3. **No Terminal Control:** Doesn't respond to terminal signals
4. **Background Process:** Executed as a background process

### Supervisor Isolation

The supervisor is also isolated:

```bash
nohup /usr/local/bin/node-supervisor > /dev/null 2>&1 &
SUPERVISOR_PID=$!
echo "$SUPERVISOR_PID" > "$NODE_SUPERVISOR_PID_FILE"
```

**Characteristics:**
- Executed with `nohup` to avoid SIGHUP
- Output redirected to `/dev/null` (logs are written directly to file)
- PID saved to file for future reference

## Obsolete PID Cleanup

When restarting the container, the system cleans obsolete PID files:

```bash
# In node-auto-start.sh
rm -f "$NODE_PID_FILE"
rm -f "$NODE_SUPERVISOR_PID_FILE"
```

**Reason:**
- PIDs from previous container instances are no longer valid
- Previous processes were terminated when the container stopped
- New processes will have new PIDs

## Complete Process Management Flow

### Node Startup

1. Verify that the node is not already running
2. Build startup command with dynamic arguments
3. Start process with `setsid` (or `nohup` as fallback)
4. Wait 2 seconds for the process to start
5. Verify that the process exists using `pgrep`
6. Save PID to file `~/.node/node.pid`
7. Start supervisor if not running

### Node Shutdown

1. Read PID from file or detect with `pgrep`
2. Verify that the process exists
3. Remove auto-start flag (prevents restart)
4. Stop supervisor first (prevents race condition)
5. Send SIGTERM to the node process
6. Wait up to 30 seconds for graceful termination
7. If it doesn't terminate, send SIGKILL
8. Remove PID file

### Node Monitoring

1. Supervisor checks every 10 seconds
2. Uses `pgrep` with pattern to detect process
3. If process doesn't exist and flag exists, restarts
4. Logs events to supervisor log

## Related Variables and Files

**Variables:**
- `NODE_PID_FILE` - Path to node PID file
- `NODE_SUPERVISOR_PID_FILE` - Path to supervisor PID file
- `NODE_PROCESS_PATTERN` - Pattern to detect the process
- `NODE_BINARY_PATH` - Path to node binary

**Files:**
- `~/.node/node.pid` - Node PID
- `~/.node/supervisor.pid` - Supervisor PID

## See Also

- [Supervisor and Auto-Start System]({{< relref "supervisor-auto-start" >}}) - How the monitoring system works
- [Internal Configuration System]({{< relref "configuration-system" >}}) - Related configuration variables
- [Container Internal Scripts]({{< relref "internal-scripts" >}}) - Scripts that implement this functionality

