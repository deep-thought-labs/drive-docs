---
title: "drive.sh Script Analysis"
weight: 5362
---

> [!WARNING]
> **⚠️ Documentation Under Construction**
>
> This document is under construction and contains technical analysis in development. It is being used by developers to identify the best solution to the permission problem between the host system and Docker containers.
>
> **Do not take this document as a usage guide yet.** This is a technical analysis that may change significantly while the final solution is being developed.

Complete technical analysis of the `drive.sh` script that manages Drive services.

## Script Location

Each service has its own `drive.sh` script in its directory:

```
services/
└── <service-name>/
    └── drive.sh
```

## Script Purpose

The `drive.sh` script is a wrapper around Docker Compose that:

1. **Manages permissions automatically** - Configures `persistent-data` permissions for the container
2. **Abstracts complexity** - Provides a simple interface for Docker Compose commands
3. **Handles sudo automatically** - Works with or without `sudo`
4. **Shows logs automatically** - When starting services, automatically shows logs

## Script Structure

### 1. Initialization and Validation

```bash
# Gets the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Checks docker-compose availability
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null 2>&1; then
    DOCKER_COMPOSE_CMD="docker compose"
```

**Functionality:**
- Automatically detects whether to use `docker-compose` (legacy) or `docker compose` (new)
- Changes to script directory to execute commands in correct context
- Validates that `docker-compose.yml` exists before continuing

### 2. persistent-data Permission Management

This is the most critical section of the script:

```bash
# Container runs as user 'ubuntu' (UID 1000)
if [ -d "persistent-data" ]; then
    if [ -w "persistent-data" ] || [ -n "$SUDO_USER" ]; then
        # Option 1: Permissions 775/777 (allows write for group/others)
        chmod -R 775 "persistent-data" 2>/dev/null || chmod -R 777 "persistent-data" 2>/dev/null || true
        
        # Option 2: If sudo, change ownership to UID 1000
        if [ -n "$SUDO_USER" ]; then
            chown -R 1000:1000 "persistent-data" 2>/dev/null || true
        fi
    fi
else
    # Create directory with correct permissions
    mkdir -p "persistent-data"
    chmod 775 "persistent-data" 2>/dev/null || chmod 777 "persistent-data" 2>/dev/null || true
    if [ -n "$SUDO_USER" ]; then
        chown -R 1000:1000 "persistent-data" 2>/dev/null || true
    fi
fi
```

**Logic Analysis:**

1. **Execution condition:** Only attempts to change permissions if:
   - Current user can write to `persistent-data`, OR
   - Script was executed with `sudo` (detected by `$SUDO_USER`)

2. **Permission strategy (without sudo):**
   - Attempts `chmod 775` (read/write for owner and group, read for others)
   - If it fails, attempts `chmod 777` (read/write for everyone)
   - Uses `|| true` to prevent script failure if no permissions

3. **Permission strategy (with sudo):**
   - In addition to `chmod`, attempts `chown 1000:1000` to change ownership to UID 1000
   - This is more secure than 777 permissions, but requires sudo

**Identified limitations:**

- If user doesn't have write permissions on `persistent-data` AND doesn't have sudo, script cannot configure permissions
- Commands use `|| true` to not fail, but this can hide permission problems
- Doesn't verify if permissions were applied correctly after attempting to change them

### 3. 'up -d' Command Detection

```bash
SHOW_LOGS=false
if [ "$1" = "up" ]; then
    for arg in "$@"; do
        if [ "$arg" = "-d" ] || [ "$arg" = "--detach" ]; then
            SHOW_LOGS=true
            break
        fi
    done
fi
```

**Functionality:**
- Detects when `./drive.sh up -d` is executed
- Activates automatic log viewing after starting container

### 4. Docker Compose Execution

```bash
if [ -n "$SUDO_USER" ]; then
    sudo -E $DOCKER_COMPOSE_CMD "$@" || EXIT_CODE=$?
else
    $DOCKER_COMPOSE_CMD "$@" || EXIT_CODE=$?
fi
```

**Functionality:**
- If executed with `sudo`, uses `sudo` for Docker Compose too
- `-E` preserves environment variables
- Captures exit code for error handling

### 5. Automatic Log Display

If `up -d` was executed, the script:
- Waits for container to be running
- Verifies logs are available
- Shows logs in real-time with `logs -f`
- Handles Ctrl+C gracefully

## Permission Management Analysis

### Is it working correctly?

**Yes, in most cases:**

1. **Ideal case (UID 1000):** If host user is UID 1000, no problems
2. **Case with write permissions:** If user can write, `chmod 775/777` allows UID 1000 to write
3. **Case with sudo:** If using `sudo`, `chown 1000:1000` changes ownership correctly

**No, in edge cases:**

1. **User without permissions and without sudo:** Script cannot configure permissions
2. **777 permissions:** Although it works, it's less secure
3. **Silent failure:** The `|| true` can hide problems

### Potential Improvements

1. **Post-configuration verification:** Verify that permissions were applied correctly
2. **Warning messages:** Inform user if permissions couldn't be configured
3. **More robust fallback:** Try more strategies before failing silently

## Execution Flow

```
1. Validate environment (docker-compose available, docker-compose.yml exists)
   ↓
2. Configure persistent-data permissions
   ├─ If exists: attempt chmod/chown
   └─ If doesn't exist: create with correct permissions
   ↓
3. Detect command type
   ├─ If 'up -d': activate log viewing
   └─ Others: execute normally
   ↓
4. Execute docker-compose with arguments
   ↓
5. If was 'up -d': show logs automatically
```

## See Also

- [Docker Compose Structure]({{< relref "docker-compose-structure" >}}) - How the container is configured
- [Permission Handling]({{< relref "permission-handling" >}}) - Complete technical documentation on permissions
- [Container Management]({{< relref "../../guides/general/container-management" >}}) - Script usage guide

