---
title: "Git Clone"
weight: 512
---

Clone the Drive repository from GitHub to get the source code on your local system.

## Clone the Repository

Run the following command to clone the repository:

```bash
git clone https://github.com/deep-thought-labs/drive
```

## Navigate to the Repository

Once cloned, enter the repository directory:

```bash
cd drive
```

## Repository Structure

Inside the repository you'll find the `services/` folder, which contains all available services. You can navigate to any subfolder within `services/` to manage each service independently:

```bash
cd services
ls  # See all available services
cd node0-infinite  # Example: enter a specific service
```

**Note:** If you can see the `services/` folder and its contents when running `ls`, this confirms that the repository has been cloned successfully.

## Next Steps

Now that you have the repository cloned, consult the following sections of the documentation:

- [Managing Services]({{< relref "managing-services" >}}) - Learn how to use services in Drive
- [Guides]({{< relref "../guides" >}}) - Specific guides for common operations
- [Service Catalog]({{< relref "../services/catalog" >}}) - Complete list of available services
