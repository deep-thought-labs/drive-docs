---
title: "System Update"
weight: 5212
---

How to update the Drive system and Docker images.

This guide explains how to update your Drive system, which consists of multiple Docker Compose containers that may be running. The update process ensures you get the latest code changes and Docker images while avoiding conflicts.

## Update Process Overview

The update process consists of four main steps:

1. **Stop all containers** - Stop all running Docker Compose services
2. **Update Git repository** - Restore and pull latest changes from the repository
3. **Update Docker images** - Pull the latest Docker images used by containers
4. **Restart containers** - Start the services you want to use

## Step 1: Stop All Containers

Before updating, you need to stop and remove all running containers to avoid conflicts and ensure a clean update. Using `down` removes the containers, which is necessary for proper updates.

Navigate to each service directory and stop it:

```bash
# Stop and remove each service individually
cd services/node0-infinite
./drive.sh down

cd ../node1-infinite-testnet
./drive.sh down

cd ../node2-infinite-creative
./drive.sh down

cd ../node3-qom
./drive.sh down
```

**Alternative:** Stop all services at once using a loop:

```bash
# From the drive root directory
for service in services/node*/; do
    cd "$service"
    ./drive.sh down
    cd ../..
done
```

> [!NOTE]
> **Why use `down` instead of `stop`?**
>
> The `down` command stops and removes the containers, which is necessary to update them properly. This ensures that when you restart the services, they will use the updated configuration and images.

## Step 2: Update Git Repository

Once all containers are stopped, update the Git repository to get the latest code changes.

### Restore Repository State

First, restore the repository to avoid conflicts with local changes:

```bash
# Navigate to the drive root directory
cd /path/to/drive  # Replace with your actual drive directory path

# Restore all files to match the remote repository
git restore .
```

This command discards any local changes and ensures your repository matches the remote state, preventing conflicts during the update.

### Pull Latest Changes

After restoring, pull the latest changes from the repository:

```bash
# Pull the latest changes
git pull
```

**Alternative:** If you prefer to specify the branch explicitly:

```bash
# Fetch latest changes
git fetch origin

# Get the current branch name
CURRENT_BRANCH=$(git branch --show-current)

# Restore and reset to match remote
git restore .
git reset --hard origin/$CURRENT_BRANCH

# Pull latest changes
git pull
```

> [!IMPORTANT]
> **Persistent Data Safety**
>
> The `git restore` command only affects files tracked by Git in the repository. Your persistent data (node data, blockchain state, keys, etc.) stored in `persistent-data/` directories is **NOT affected** and will remain intact.

## Step 3: Update Docker Images

After updating the repository, update the Docker images used by your containers.

Navigate to **any service directory** and pull the latest image:

```bash
# Navigate to any service directory
cd services/node0-infinite

# Pull the latest Docker image
docker compose pull
```

**Important:** You only need to run this command **once from any service directory**. All services share the same Docker image, so once you update it, all services will use the updated image when you restart them.

**What this does:**
- Downloads/updates the Docker image specified in your `docker-compose.yml` file
- The image version depends on your configuration (check `docker-compose.yml` to see which version you're using)
- Docker images are shared system-wide, so updating it once updates it for all services

**Verify the image was updated:**

```bash
# Check image details
docker images | grep "deepthoughtlabs/infinite-drive"
```

> [!NOTE]
> **Image Version**
>
> The image version you're using is specified in each service's `docker-compose.yml` file under the `image:` field. Make sure you're pulling the correct version for your environment.

## Step 4: Restart Containers

After updating both the repository and Docker images, you can restart the containers you want to use. You don't need to restart all of them—only the ones you decide to use.

### Restart Individual Services

```bash
# Restart each service you want to use
cd services/node0-infinite
./drive.sh up -d

cd ../node1-infinite-testnet
./drive.sh up -d

# Continue for other services as needed
```

### Restart All Services

If you want to restart all services at once:

```bash
# From the drive root directory
for service in services/node*/; do
    cd "$service"
    ./drive.sh up -d
    cd ../..
done
```

## Complete Update Example

Here's a complete example of the update process:

```bash
# Step 1: Stop and remove all containers
for service in services/node*/; do
    cd "$service"
    ./drive.sh down
    cd ../..
done

# Step 2: Update Git repository (from drive root)
cd /path/to/drive
git restore .
git pull

# Step 3: Update Docker images (from any service directory - only once needed)
cd services/node0-infinite
docker compose pull

# Step 4: Restart containers you want to use
cd ../node0-infinite
./drive.sh up -d

# Only restart the services you need
# cd ../node1-infinite-testnet
# ./drive.sh up -d
```

## Update Checklist

Use this checklist to ensure a complete update:

- [ ] Stop and remove all running services (`./drive.sh down` in each service)
- [ ] Navigate to drive root directory
- [ ] Restore repository state (`git restore .`)
- [ ] Pull latest Git changes (`git pull`)
- [ ] Navigate to any service directory
- [ ] Pull latest Docker image (`docker compose pull`) - only once needed
- [ ] Restart the services you want to use (`./drive.sh up -d`)
- [ ] Verify services are running (`./drive.sh ps`)

## Troubleshooting

For troubleshooting issues related to system updates, see the [Troubleshooting]({{< relref "../../troubleshooting" >}}) section, which covers:

- Common issues and solutions
- Network diagnosis
- Node start/stop issues
- Permission issues
- Key management issues
- Node log issues

## See Also

- [Container Management]({{< relref "container-management" >}}) - General container management commands
- [Start/Stop Node]({{< relref "../blockchain-nodes/start-stop-node" >}}) - Node-specific start/stop operations
