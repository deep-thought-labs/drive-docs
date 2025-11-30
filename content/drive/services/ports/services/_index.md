---
title: "Service Port Configurations"
---

# Service Port Configurations

Complete port configurations for each service, including port mappings, Docker Compose examples, and firewall configurations.

## Available Service Configurations

- [Infinite Mainnet (node0-infinite)]({{< relref "node0-infinite" >}}) - Service #0, standard ports
- [Infinite Testnet (node1-infinite-testnet)]({{< relref "node1-infinite-testnet" >}}) - Service #1, +10 offset
- [Infinite Creative Network (node2-infinite-creative)]({{< relref "node2-infinite-creative" >}}) - Service #2, +20 offset
- [QOM Network (node3-qom)]({{< relref "node3-qom" >}}) - Service #3, +30 offset

## What's Included

Each service configuration document includes:

- **Quick Reference** - Table of all port mappings
- **Port Calculation** - How ports are calculated using the service number
- **Required Ports** - Ports that must be configured
- **Optional Ports** - Additional ports for specific use cases
- **Docker Compose Configuration** - Ready-to-use examples (minimal and full)
- **Firewall Configuration** - UFW commands for each port

## See Also

- [Port Strategy]({{< relref ".." >}}) - Port allocation strategy and general information
- [Port Reference: Blockchain Nodes]({{< relref "../blockchain-nodes" >}}) - Detailed port descriptions
- [Service Catalog]({{< relref "../../catalog" >}}) - Complete service listings

