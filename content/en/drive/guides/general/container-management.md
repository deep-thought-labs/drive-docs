---
title: "Container Management"
weight: 5211
---

Learn how to manage Drive containers using the `drive.sh` script. All Drive services use this script for management operations.

## Script Location

Each service has its own `drive.sh` script in its directory:

```bash
cd services/<service-name>
./drive.sh <command>
```

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

View the container logs in real-time:

```bash
./drive.sh logs
```

To see the latest logs and exit, press `Ctrl+C`.

### 💻 Access Container Shell

Open a shell session inside the container:

```bash
./drive.sh bash
```

Useful for debugging, inspecting files inside the container, or running manual commands.

## Script Features

- **Automatic permission handling** - Works with or without `sudo`
- **Consistent interface** - The same commands work across all services
- **Simplified management** - Abstracts Docker Compose complexity
