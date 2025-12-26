---
title: "Quick Start"
weight: 51
---

Get Drive up and running quickly. Follow these steps in order:

1. [Architecture Overview]({{< relref "architecture" >}}) - Understand how Drive works
2. [Prerequisites]({{< relref "installation" >}}) - Install technical requirements
3. [Git Clone]({{< relref "git-clone" >}}) - Clone the Drive repository
4. [Verify Installation]({{< relref "managing-services" >}}) - Verify that everything is configured correctly

## Firewall and Port Configuration

Once Drive is installed and running, it's important to configure your system's firewall to allow the necessary connections to Drive services.

**Firewall Configuration:**
- See the [Firewall Configuration Guide]({{< relref "../services/ports/firewall-configuration" >}}) for detailed instructions on how to configure the firewall according to your operating system.

**Ports per Service:**
- Each Drive service has specific ports assigned that must be open in the firewall.
- The port configuration for each service is described in the individual documentation for each service in the [Service Catalog]({{< relref "../services/catalog" >}}).
- **We recommend reading the documentation for each service** you plan to use to learn about the specific ports it needs.

**General Port Information:**
- For general information about port allocation strategy and global configuration, see the [Ports]({{< relref "../services/ports" >}}) section in the Services documentation.
