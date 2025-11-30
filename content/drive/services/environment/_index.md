---
title: "Environment Variables"
---

# Environment Variables

Environment variables are configuration parameters passed to Docker containers that control how services behave. In Drive, all services can have environment variables, and many services share the same variable names but with different values.

## How Environment Variables Work in Drive

- **Shared Variables**: Many services use the same environment variable names (e.g., `NODE_CHAIN_ID`, `NODE_P2P_SEEDS`)
- **Different Values**: What makes each service unique is the **value** assigned to each variable
- **Service-Specific**: Each service's `docker-compose.yml` file defines the specific values for that service
- **Container Behavior**: The combination of variable names and their values determines how the container runs

## Environment Variable Documentation

### By Service Type

- [Blockchain Nodes]({{< relref "blockchain-nodes" >}}) - Environment variables used by blockchain node services
- [General]({{< relref "general" >}}) - Global environment variables shared across all services

## See Also

- [Service Catalog]({{< relref "../catalog" >}}) - Service-specific configurations with actual values
- [Service Structure]({{< relref "../service-structure" >}}) - How services are configured

