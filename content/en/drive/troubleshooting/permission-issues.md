---
title: "Permission Issues"
weight: 543
---

Guide to identify and resolve permission problems related to the `persistent-data` folder and Docker containers.

> [!NOTE]
> **Work in Progress**
>
> We are actively working on improving automatic permission handling so that Drive works correctly **regardless of which user you are using** on the host system. This includes:
>
> - Improvements to the `drive.sh` script to detect and resolve permission problems more robustly
> - Post-configuration verifications to ensure permissions were applied correctly
> - Clearer informative messages when there are permission problems
> - Possible changes to Docker Compose configuration to support different UIDs
>
> For now, **it is recommended that the user running Drive on the host system has UID 1000** to avoid permission issues.

## Problem Symptoms

If you experience any of these errors, you likely have a permission problem:

- `permission denied` when starting a service
- `cannot write to /home/ubuntu/.infinited`
- `operation not permitted`
- `cannot chown`
- Container cannot create or modify files in `persistent-data`
- Files created by the container are not accessible from the host

## Problem Cause

The problem arises from how Docker handles permissions between the host system and containers:

### The Fundamental Problem

Docker maps file permissions using **numeric UIDs/GIDs**, not usernames. This means:

- Drive containers run as a user with **UID 1000** (defined in the Dockerfile)
- The host system may have a different user with a different UID
- Bind mounts (like `./persistent-data:/home/ubuntu/.infinited`) preserve UIDs from the host filesystem
- If the host user's UID doesn't match the container's UID (1000), there will be permission problems

### Problem Example

If you run Drive as a user with UID 1001 on the host:
- Container tries to write files as UID 1000
- Files are created with UID 1000 on the host system
- Host user (UID 1001) cannot modify these files
- Container may have problems if the directory doesn't have adequate permissions

## Current Solution

### Recommended Solution: Use User with UID 1000

**The simplest and recommended solution is to use a user with UID 1000 on the host system.**

#### Verify Your Current UID

```bash
id -u
```

#### If Your UID is NOT 1000

You have several options:

**Option 1: Switch to the correct user (Recommended)**

If you have a user with UID 1000 on your system (common in Ubuntu, may be `ubuntu`, `kvm`, or another):

```bash
# Verify which user has UID 1000
getent passwd 1000

# Switch to that user
su - <user-with-uid-1000>
```

**Option 2: Use sudo to change ownership**

If you need to use your current user, you can use `sudo` to change `persistent-data` ownership:

```bash
cd services/<service-name>
sudo chown -R 1000:1000 persistent-data
```

Then run Drive commands normally.

**Option 3: Configure broad permissions (less secure)**

If you can't use sudo and can't switch users, the `drive.sh` script will attempt to configure broad permissions automatically, but this is less secure:

```bash
chmod -R 775 persistent-data  # Or 777 if 775 fails
```

### How the drive.sh Script Currently Works

The `drive.sh` script attempts to resolve permission problems automatically:

1. **If you run without sudo:**
   - Attempts to apply `chmod 775` or `777` to `persistent-data`
   - This allows UID 1000 to write even if the owner is a different UID
   - Only works if you have write permissions on the directory

2. **If you run with sudo:**
   - In addition to `chmod`, attempts to change ownership to `1000:1000` with `chown`
   - This is more secure and permanent

**Current limitation:** If you don't have write permissions AND don't have sudo, the script cannot configure permissions automatically.

For more technical details on how the permission system currently works, see the [Permission Handling technical documentation]({{< relref "../services/technical/permission-handling" >}}).

## Summary

**To avoid permission problems:**

1. ✅ **Recommended:** Use a user with UID 1000 on your host system
2. ✅ **Alternative:** Use `sudo ./drive.sh` to allow the script to configure permissions automatically
3. ⚠️ **Temporary:** The script will attempt to configure broad permissions if you have write permissions

**If you encounter permission problems:**

1. Verify your UID with `id -u`
2. If it's not 1000, switch to a user with UID 1000 or use `sudo`
3. Consult the [technical documentation]({{< relref "../services/technical/permission-handling" >}}) to better understand the problem

## See Also

- [Permission Handling (Technical Documentation)]({{< relref "../services/technical/permission-handling" >}}) - Complete technical analysis of the permission problem
- [Verify Installation]({{< relref "../quick-start/managing-services" >}}) - Basic system verifications

