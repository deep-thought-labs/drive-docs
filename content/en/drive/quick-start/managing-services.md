---
title: "Verify Installation"
weight: 513
---

Before continuing, verify that your system is correctly configured and ready to use Drive. This verification will ensure that all necessary components are working correctly.

## Verify Docker

Confirm that Docker is working correctly:

```bash
docker ps
```

**Expected result:** You should see a list (possibly empty) of containers without errors. If you see an error, Docker is not working correctly.

## Verify Repository Structure

From the root directory of the cloned repository (`drive/`), verify that the `services/` folder exists:

```bash
ls services/
```

**Expected result:** You should see a list of service folders (for example: `node0-infinite`, `node1-infinite-testnet`, etc.).

## Verify Management Script

Enter any service and verify that the `drive.sh` script exists and is executable:

```bash
cd services/node0-infinite  # Or any other available service
ls -la drive.sh
```

**Expected result:** You should see the `drive.sh` file with execute permissions (indicated by the `x` in the permissions).

> [!NOTE]
> **Note on Permissions**
>
> Drive containers run as a user with **UID 1000**. If you are using an Ubuntu system as the host for Drive, make sure to use a user that has **UID 1000** to avoid permission issues. You can verify your UID with the command `id -u`.

## ✅ Verification Complete

If all the above commands worked correctly, your system is configured and ready to use Drive.

## Next Steps

Now that you have completed the Quick Start and verified your installation, you can continue with the following sections according to your needs:

- **[Guides]({{< relref "../guides" >}})** - Learn to perform specific operations
  - [Container Management]({{< relref "../guides/general/container-management" >}}) - Detailed commands for managing services
  - [Blockchain Nodes]({{< relref "../guides/blockchain-nodes" >}}) - Specific guides for working with blockchain nodes

- **[Services]({{< relref "../services" >}})** - Complete technical reference
  - [Service Catalog]({{< relref "../services/catalog" >}}) - Complete list of available services and their configurations
