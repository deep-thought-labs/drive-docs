---
title: "Internal Logging System"
weight: 405
---

The Drive system implements a structured logging system to facilitate monitoring, debugging, and problem diagnosis. This section documents how the logging system works internally.

## Logging System Architecture

### Log Types

The system maintains two main types of logs:

1. **Node Logs** - Output from the blockchain process
2. **Supervisor Logs** - Events from the monitoring system

### Log Location

All logs are stored in `/var/log/node/`:

```
/var/log/node/
├── node.log          # Main blockchain node log
└── supervisor.log    # Supervisor log
```

## Node Log (`node.log`)

### Location and Configuration

**Path:**
```
/var/log/node/node.log
```

**Variable:**
```bash
NODE_LOG_FILE="/var/log/node/node.log"
```

### Content

The node log contains all output from the `infinited` process:

- **Standard output (stdout):** Informative messages from the node
- **Error output (stderr):** Errors and warnings

### Redirection

The log is created via I/O redirection when the node starts:

```bash
# In node-start.sh
setsid bash -c "eval ${START_CMD} > ${NODE_LOG_FILE} 2>&1" < /dev/null &
```

**Explanation:**
- `> ${NODE_LOG_FILE}` - Redirects stdout to the log file
- `2>&1` - Redirects stderr to stdout (both go to the same file)
- `< /dev/null` - Redirects stdin from /dev/null (avoids blocking)

### Characteristics

1. **Append Mode:** Logs are appended to the file (not overwritten)
2. **Text Format:** Logs in plain text format
3. **Size:** The file grows continuously while the node is running
4. **Rotation:** No automatic rotation implemented (can be added externally)

### Viewing

#### View Last N Lines

```bash
node-logs [number]
```

**Example:**
```bash
node-logs 100    # Last 100 lines
node-logs        # Last 50 lines (default)
```

**Implementation:**
```bash
if [ -n "$1" ]; then
    tail -n "$1" "$NODE_LOG_FILE"
else
    tail -n 50 "$NODE_LOG_FILE"
fi
```

#### Real-Time Following

```bash
node-logs -f
# or
node-logs --follow
```

**Implementation:**
```bash
if [ "$1" = "-f" ] || [ "$1" = "--follow" ]; then
    # Use exec to replace the script process with tail
    exec tail -f "$NODE_LOG_FILE"
fi
```

**Characteristics:**
- Uses `exec tail -f` to replace the script process
- Allows Ctrl+C to only affect `tail`, not the node
- Shows logs in real-time as they're generated

### Signal Isolation

The system is designed so that terminal signals don't affect the node process:

```bash
# The node runs with setsid, in an isolated session
setsid bash -c "eval ${START_CMD} > ${NODE_LOG_FILE} 2>&1" < /dev/null &

# tail also runs with exec to isolate signals
exec tail -f "$NODE_LOG_FILE"
```

**Advantages:**
- Ctrl+C in `node-logs -f` only stops `tail`, not the node
- The node continues running independently
- No interference between viewing and execution

## Supervisor Log (`supervisor.log`)

### Location and Configuration

**Path:**
```
/var/log/node/supervisor.log
```

**Variable:**
```bash
NODE_SUPERVISOR_LOG_FILE="${NODE_SUPERVISOR_LOG_FILE:-/var/log/node/supervisor.log}"
```

### Content

The supervisor log contains events from the monitoring system:

- Supervision start
- Node stopped detection
- Restart attempts
- Supervision stop
- Errors or problems detected

### Entry Format

Each entry includes a timestamp:

```
[2024-01-15 10:30:45] Node not detected, attempting to restart...
[2024-01-15 10:30:50] Auto-start flag removed, stopping supervision...
```

**Format:**
```bash
echo "[$(date +"%Y-%m-%d %H:%M:%S")] Message..." >> "$NODE_SUPERVISOR_LOG_FILE"
```

### Writing

The supervisor writes directly to the file using append (`>>`):

```bash
# In node-supervisor.sh
echo "[$(date +"%Y-%m-%d %H:%M:%S")] Node not detected, attempting to restart..." >> "$NODE_SUPERVISOR_LOG_FILE"
```

**Characteristics:**
- Append mode (doesn't overwrite)
- Consistent format with timestamps
- Only writes when there are important events

### Directory Creation

The log directory is created automatically if it doesn't exist:

```bash
# In node-supervisor.sh
mkdir -p "$(dirname "$NODE_SUPERVISOR_LOG_FILE")"
```

## Difference between Node Logs and Container Logs

### Node Logs

- **Origin:** `infinited` process inside the container
- **Location:** `/var/log/node/node.log` (inside container)
- **Content:** Specific output from the blockchain node
- **Access:** `node-logs` or `docker compose exec infinite-drive node-logs`

### Container Logs

- **Origin:** Output from all container processes
- **Location:** Docker management (not in container filesystem)
- **Content:** Output from `node-auto-start.sh`, startup errors, etc.
- **Access:** `docker compose logs infinite-drive`

**Note:** Container logs may include initial output from `node-auto-start.sh`, but once the node is running, node logs are more relevant.

## Log Management

### Directory Creation

Log directories are created automatically:

**In the Dockerfile:**
```dockerfile
RUN mkdir -p /home/ubuntu/.infinited /var/log/node /home/ubuntu/.node && \
    chown -R 1000:1000 /home/ubuntu /var/log/node
```

**In scripts:**
```bash
# Create directory if it doesn't exist
mkdir -p "$(dirname "$NODE_LOG_FILE")"
mkdir -p "$(dirname "$NODE_SUPERVISOR_LOG_FILE")"
```

### Permissions

Logs have standard permissions:

- **Owner:** `ubuntu` (UID 1000)
- **Group:** `ubuntu` (GID 1000)
- **Permissions:** `644` (rw-r--r--)

### Persistence

Logs are stored in persistent volumes in Docker:

```yaml
volumes:
  - ./persistent-data/logs:/var/log/node
```

**Advantages:**
- Logs persist between container restarts
- Accessible from the host
- Not lost when recreating the container

## Log Rotation

### Current State

The system **does not implement automatic log rotation** internally.

### Considerations

1. **Continuous Growth:** Logs grow indefinitely
2. **Disk Space:** Can consume significant space over time
3. **Performance:** Very large files can affect performance

### External Solutions

External solutions can be implemented:

1. **logrotate:** Configure logrotate on the host
2. **Custom scripts:** Create scripts that rotate logs periodically
3. **Manual management:** Clean logs manually when necessary

**Example with logrotate:**
```
/var/log/node/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    missingok
}
```

## Log Verification

### Verify if Log Exists

```bash
if [ ! -f "$NODE_LOG_FILE" ]; then
    print_error "Log file not found: $NODE_LOG_FILE"
    echo "   The node may not have been started yet."
    exit 1
fi
```

### Verify if Node is Running

Before following logs, status can be verified:

```bash
if ! pgrep -f "$NODE_PROCESS_PATTERN" > /dev/null; then
    print_warning "Node is not currently running, but showing logs..."
fi
```

## Log Interpretation

### Node Logs

Node logs contain information about:

- **Synchronization:** Progress synchronizing with the network
- **Connections:** Peer connection and disconnection
- **Blocks:** Block download and processing
- **Errors:** Connection errors, validation, etc.
- **Status:** General node status

### Supervisor Logs

Supervisor logs contain information about:

- **Monitoring:** Node monitoring events
- **Restarts:** Automatic restart attempts
- **Shutdown:** Supervision stop
- **Problems:** Problems detected by the supervisor

## Related Variables

```bash
NODE_LOG_FILE="/var/log/node/node.log"
NODE_SUPERVISOR_LOG_FILE="/var/log/node/supervisor.log"
```

## See Also

- [Internal Directory Structure]({{< relref "directory-structure" >}}) - Log file locations
- [Internal Process Management]({{< relref "process-management" >}}) - How logs are redirected
- [Node Monitoring Guide]({{< relref "../guides/blockchain-nodes/node-monitoring" >}}) - How to use logs from the user perspective

