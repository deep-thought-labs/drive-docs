---
title: "Permission Handling"
weight: 5363
---

> [!WARNING]
> **⚠️ Documentation Under Construction**
>
> This document is under construction and contains technical analysis in development. It is being used by developers to identify the best solution to the permission problem between the host system and Docker containers.
>
> **Do not take this document as a usage guide yet.** This is a technical analysis that may change significantly while the final solution is being developed.

Complete technical documentation on how Drive handles file permissions between the host system and Docker containers.

## The Fundamental Problem

Docker maps file permissions using **numeric UIDs/GIDs**, not usernames. This means:

- Container runs as UID 1000 (user `ubuntu`)
- Host system may have a different user with a different UID
- Bind mounts preserve UIDs from the host filesystem
- If host UID doesn't match container UID, there will be permission problems

## Current Drive Configuration

### Container User

- **User:** `ubuntu`
- **UID:** 1000
- **GID:** 1000
- **Definition:** Set in the image's Dockerfile, not in `docker-compose.yml`

### Permission Strategy in drive.sh

The `drive.sh` script attempts to resolve permission problems in two ways:

#### Strategy 1: Broad Permissions (without sudo)

```bash
chmod -R 775 "persistent-data"  # Or 777 if 775 fails
```

**How it works:**
- Permissions 775: `rwxrwxr-x` (owner and group can write, others read-only)
- Permissions 777: `rwxrwxrwx` (everyone can write)
- Allows UID 1000 (container) to write even if owner is a different UID

**Advantages:**
- Doesn't require sudo
- Works if user has write permissions on parent directory

**Disadvantages:**
- 777 permissions are less secure (any user can write)
- Doesn't change ownership, only permissions

#### Strategy 2: Ownership Change (with sudo)

```bash
chown -R 1000:1000 "persistent-data"
```

**How it works:**
- Changes directory ownership to UID 1000:GID 1000
- Container (UID 1000) is now the owner
- Doesn't need broad permissions (can use 755 or 700)

**Advantages:**
- More secure (doesn't require broad permissions)
- Permanent solution (ownership persists)

**Disadvantages:**
- Requires sudo
- Host user may lose direct access if not UID 1000

## Use Cases and Solutions

### Case 1: Host User is UID 1000

**Situation:** Host user has UID 1000 (e.g., `kvm` user on InterServer)

**Behavior:**
- ✅ No permission problems
- ✅ Container can write
- ✅ Host user can write
- ✅ No permission changes required

**Example:**
```bash
$ id -u
1000
# Everything works without additional configuration
```

### Case 2: Host User is NOT UID 1000, but has write permissions

**Situation:** Host user has a different UID but can write to the directory

**Script behavior:**
1. Detects it can write (`[ -w "persistent-data" ]`)
2. Applies `chmod 775` or `777`
3. ✅ Container (UID 1000) can write thanks to broad permissions

**Example:**
```bash
$ id -u
1001
$ ls -ld persistent-data
drwxrwxrwx  alberto alberto  persistent-data
# Container can write due to 777 permissions
```

### Case 3: Host User is NOT UID 1000 and does NOT have write permissions

**Situation:** User cannot write and doesn't have sudo

**Script behavior:**
- ⚠️ Cannot configure permissions
- ⚠️ `chmod`/`chown` commands fail silently (`|| true`)
- ❌ Container will not be able to write
- ❌ Permission errors will occur

**Manual solution required:**
```bash
# Option 1: Use sudo
sudo chown -R 1000:1000 persistent-data

# Option 2: Switch to a user with UID 1000
su - user-with-uid-1000

# Option 3: Configure permissions manually
sudo chmod -R 775 persistent-data
```

### Case 4: Host User executes with sudo

**Situation:** Script is executed with `sudo ./drive.sh up -d`

**Script behavior:**
1. Detects `$SUDO_USER` (user who executed sudo)
2. Applies `chown -R 1000:1000` to change ownership
3. ✅ Container (UID 1000) is now the owner
4. ✅ Can write without problems

**Example:**
```bash
$ sudo ./drive.sh up -d
# Script changes ownership to 1000:1000 automatically
# Container can write correctly
```

## Reported Problem Analysis

### User Scenario

- **VPS Provider:** InterServer
- **Default user:** `kvm` (UID 1000)
- **Attempted user:** `ubuntu` (different UID, not 1000)
- **Problem:** Container couldn't write to `persistent-data`

### Why did it fail?

1. User `ubuntu` was not UID 1000
2. `drive.sh` script probably couldn't configure permissions (without sudo or without write permissions)
3. Docker created files as UID 1001 (next available UID)
4. Neither host nor container could write (permission deadlock)

### Why did it work with `kvm`?

- User `kvm` is UID 1000
- Matches container UID
- No permission changes required
- Everything works automatically

### Is the drive.sh script working correctly?

**Partially:**

✅ **Works when:**
- User is UID 1000
- User has write permissions and script can apply chmod
- User executes with sudo and script can apply chown

❌ **Doesn't work when:**
- User is not UID 1000
- User doesn't have write permissions
- User doesn't have sudo
- Script fails silently (`|| true` hides errors)

## Recommended Improvements

### 1. Post-Configuration Verification

Script should verify that permissions were applied correctly:

```bash
# After chmod/chown, verify:
if [ -d "persistent-data" ]; then
    PERMS=$(stat -c "%a" persistent-data 2>/dev/null || stat -f "%OLp" persistent-data)
    OWNER=$(stat -c "%u" persistent-data 2>/dev/null || stat -f "%u" persistent-data)
    
    if [ "$OWNER" != "1000" ] && [ "$PERMS" != "775" ] && [ "$PERMS" != "777" ]; then
        echo "⚠️  Warning: Could not configure permissions correctly"
        echo "   Container (UID 1000) may not be able to write"
    fi
fi
```

### 2. Informative Messages

Script should inform user about permission status:

```bash
if [ "$OWNER" = "1000" ]; then
    echo "✅ Permissions configured: persistent-data is owned by UID 1000"
elif [ "$PERMS" = "775" ] || [ "$PERMS" = "777" ]; then
    echo "✅ Permissions configured: persistent-data has broad permissions (775/777)"
else
    echo "⚠️  Warning: Permissions may not be compatible with container"
fi
```

### 3. More Robust Fallback

If `chmod` fails, try other strategies before continuing:

```bash
# Try multiple strategies
if ! chmod 775 persistent-data 2>/dev/null; then
    if ! chmod 777 persistent-data 2>/dev/null; then
        if [ -n "$SUDO_USER" ]; then
            if ! sudo chown 1000:1000 persistent-data 2>/dev/null; then
                echo "❌ Error: Could not configure permissions"
                exit 1
            fi
        else
            echo "⚠️  Warning: Could not configure permissions. May require sudo."
        fi
    fi
fi
```

## Summary

### Current Status

- ✅ Works in most common cases
- ⚠️ Has limitations in edge cases (user without permissions and without sudo)
- ⚠️ Fails silently in some cases (`|| true`)

### Recommendations

1. **For users:** Verify UID before using Drive (see [Verify Installation]({{< relref "../../quick-start/managing-services" >}}))
2. **For development:** Improve script with verifications and more informative messages
3. **For documentation:** Clearly explain permission requirements

## See Also

- [Docker Compose Structure]({{< relref "docker-compose-structure" >}}) - How the container is configured
- [drive.sh Script Analysis]({{< relref "drive-script-analysis" >}}) - Current script implementation
- [Verify Installation]({{< relref "../../quick-start/managing-services" >}}) - How to verify permissions before using Drive
- [Common Issues]({{< relref "../../troubleshooting/common-issues" >}}) - Solutions to permission problems

