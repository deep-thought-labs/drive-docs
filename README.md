# Documentation Structure

## Proposed Structure for `content/`

```
content/
├── _index.md
├── concepts/
│   ├── _index.md
│   ├── docker.md
│   └── [other atomic concepts]
├── ecosystem/
│   └── [structure to be defined]
├── blockchain/
│   └── [structure to be defined]
└── drive/
    ├── _index.md
    ├── quick-start/
    │   ├── _index.md
    │   ├── installation.md
    │   ├── git-clone.md
    │   └── first-service-nginx.md
    ├── guides/
    │   ├── _index.md
    │   ├── blockchain-nodes/
    │   │   ├── _index.md
    │   │   ├── initialize-node.md
    │   │   ├── start-stop-node.md
    │   │   ├── manage-keys.md
    │   │   └── graphical-interface.md
    │   └── general/
    │       ├── _index.md
    │       ├── container-management.md
    │       └── system-update.md
    ├── services/
    │   ├── _index.md
    │   ├── service-structure.md
    │   ├── ports/
    │   │   ├── _index.md
    │   │   ├── strategy.md
    │   │   └── reference.md
    │   ├── blockchain-nodes/
    │   │   ├── _index.md
    │   │   ├── catalog.md
    │   │   └── environment-variables.md
    │   └── nginx/
    │       ├── _index.md
    │       ├── configuration.md
    │       ├── virtual-hosts.md
    │       ├── ssl-https.md
    │       └── reverse-proxy.md
    └── troubleshooting/
        ├── _index.md
        ├── common-issues.md
        └── network-diagnosis.md
```

## Other Top-Level Sections

The following sections exist at the same level as `drive/`:

- **`concepts/`**: Atomic concept files explaining technologies used across the entire documentation (not just Drive)
- **`ecosystem/`**: General ecosystem documentation
- **`blockchain/`**: Main blockchain documentation

## Section Descriptions

### Drive Overview

**`drive/_index.md`**

Drive is a decentralized infrastructure management tool that enables users to deploy and manage blockchain nodes, services, and protocols on their own systems—whether local machines, personal servers, or their own internet infrastructure. When combined with other independent users running Drive, it creates a synchronized super-mesh of services, protocols, and chains, forming a distributed infrastructure network managed entirely by independent users. Drive empowers individuals to participate in and contribute to a decentralized ecosystem while maintaining full control over their infrastructure.

This page should provide a friendly, concise description of what Drive is, why it exists, its importance, and what users can achieve. It should explain that Drive is a tool users install on their own systems (local machines, servers, or their own internet infrastructure). When combined with other independent users, it creates a synchronized super-mesh of services, protocols, and chains, forming a distributed infrastructure network managed entirely by independent users.

### Quick Start

**`drive/quick-start/`**

Step-by-step instructions to get Drive running. From installing dependencies to deploying your first service. Each step includes brief, practical explanations of what the user is doing and why. Steps must be followed in order.

- **`_index.md`**: Overview of quick start process and recommended path
- **`installation.md`**: Installing technical requirements (Git, Docker, Docker Compose) and system preparation. This must be done first before cloning the repository
- **`git-clone.md`**: Cloning the Drive repository from Git
- **`first-service-nginx.md`**: Deploying Nginx as the first service (recommended starting point). Brief explanations of Docker containers and their importance throughout the process

### Concepts

**`concepts/`** (Top-level section)

Atomic concept files explaining why we use specific technologies and how they fit into our ecosystem. These can be referenced from any part of the documentation (Drive, Blockchain, Ecosystem, etc.).

- **`_index.md`**: Concepts index and navigation
- **`docker.md`**: What Docker is, why it's important, and why it's an excellent choice for our strategy
- **[other atomic concepts]**: Additional concept files as needed (e.g., containerization, service architecture)

### Guides

**`drive/guides/`**

Action-specific guides organized by category. Focused guides for specific operations within the Drive ecosystem.

- **`_index.md`**: Guide index and navigation

**Blockchain Nodes** (`blockchain-nodes/`): Specific guides for blockchain node operations.

- **`_index.md`**: Overview of blockchain node guides
- **`initialize-node.md`**: How to initialize a blockchain node
- **`start-stop-node.md`**: How to start and stop nodes
- **`manage-keys.md`**: Key management within blockchain nodes
- **`graphical-interface.md`**: How to access and use the graphical interface for blockchain nodes. Recommended method for managing nodes, with step-by-step instructions

**General** (`general/`): General guides for system-wide operations.

- **`_index.md`**: Overview of general guides
- **`container-management.md`**: How to manage containers (start, stop, logs, shell access)
- **`system-update.md`**: How to update the Drive system and Docker images

### Services

**`drive/services/`**

Service structure documentation, service type descriptions, and service catalogs. This is the single source of truth for all service information including their configurations, ports, and environment variables.

- **`_index.md`**: Services overview, service types, and navigation to service catalogs
- **`service-structure.md`**: General explanation of service structure, how services work using Docker containers and Docker Compose files, where service definitions are located, and how services are configured

**Ports** (`ports/`): Port allocation strategy and port management documentation.

- **`_index.md`**: Port configuration overview
- **`strategy.md`**: Port allocation strategy, numbering system, and how ports are assigned to services
- **`reference.md`**: Detailed technical reference for the port allocation system, port ranges, and port assignment rules

**Blockchain Nodes** (`blockchain-nodes/`): General documentation for blockchain node services. Since all blockchain nodes share the same structure and image, this focuses on general descriptions rather than individual node documentation.

- **`_index.md`**: Overview of blockchain node services, their common structure, and how they differ only in configuration values
- **`catalog.md`**: Complete catalog of all available blockchain node services. For each service, includes: service name, network/chain, binary download URLs, specific configuration values, and assigned ports (referencing the ports strategy)
- **`environment-variables.md`**: Complete reference of all environment variables used in blockchain node services. Documents all environment variables defined in Docker Compose files for blockchain nodes, their purposes, default values, and how they work

**Nginx** (`nginx/`): Web server service documentation.

- **`_index.md`**: Nginx service overview, use cases, and assigned ports (referencing the ports strategy)
- **`configuration.md`**: Basic Nginx configuration and service setup
- **`virtual-hosts.md`**: Setting up multiple domains and virtual hosts
- **`ssl-https.md`**: SSL/TLS certificate setup and HTTPS configuration
- **`reverse-proxy.md`**: Reverse proxy configuration for APIs and services

### Troubleshooting

**`drive/troubleshooting/`**

Solutions to common problems, diagnostic tools, and recovery procedures. Help users resolve issues quickly.

- **`_index.md`**: Troubleshooting guide index
- **`common-issues.md`**: Frequently encountered problems and their solutions
- **`network-diagnosis.md`**: Network troubleshooting tools and diagnostic procedures
