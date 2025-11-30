---
title: "Service Catalog"
---

# Service Catalog

Complete catalog of all services currently supported by Drive. Each service entry includes the service name, description, and links to relevant configuration documentation.

## Blockchain Node Services

All blockchain node services share the same Docker image and structure, differing only in configuration values (chain ID, genesis file, ports, etc.).

### node0-infinite (Infinite Mainnet)

**Service Number:** 0  
**Service Name:** `infinite`  
**Container Name:** `infinite`  
**Network:** Infinite Mainnet

**Description:**  
Mainnet blockchain node for the Infinite network. Uses standard/default ports (no offset).

**Configuration:**
- **Ports:** [Port Configuration: Infinite Mainnet]({{< relref "ports/services/node0-infinite" >}}) - Complete port mapping, Docker Compose examples, and firewall configuration
- **Environment Variables:** See [Environment Variables]({{< relref "environment-variables" >}}) for configuration options
- **Port Strategy:** [Port Allocation Strategy]({{< relref "ports/strategy" >}}) - Service #0 (offset: +0)

---

### node1-infinite-testnet (Infinite Testnet)

**Service Number:** 1  
**Service Name:** `infinite-testnet`  
**Container Name:** `infinite-testnet`  
**Network:** Infinite Testnet

**Description:**  
Testnet blockchain node for the Infinite network. All ports have a +10 offset from default ports.

**Configuration:**
- **Ports:** [Port Configuration: Infinite Testnet]({{< relref "ports/services/node1-infinite-testnet" >}}) - Complete port mapping, Docker Compose examples, and firewall configuration
- **Environment Variables:** See [Environment Variables]({{< relref "environment-variables" >}}) for configuration options
- **Port Strategy:** [Port Allocation Strategy]({{< relref "ports/strategy" >}}) - Service #1 (offset: +10)

---

### node2-infinite-creative (Infinite Creative Network)

**Service Number:** 2  
**Service Name:** `infinite-creative`  
**Container Name:** `infinite-creative`  
**Network:** Infinite Creative Network

**Description:**  
Creative Network blockchain node. All ports have a +20 offset from default ports.

**Configuration:**
- **Ports:** [Port Configuration: Infinite Creative Network]({{< relref "ports/services/node2-infinite-creative" >}}) - Complete port mapping, Docker Compose examples, and firewall configuration
- **Environment Variables:** See [Environment Variables]({{< relref "environment-variables" >}}) for configuration options
- **Port Strategy:** [Port Allocation Strategy]({{< relref "ports/strategy" >}}) - Service #2 (offset: +20)

---

### node3-qom (QOM Network)

**Service Number:** 3  
**Service Name:** `qom`  
**Container Name:** `qom`  
**Network:** QOM Network

**Description:**  
QOM Network blockchain node. Uses alternative binary configuration. All ports have a +30 offset from default ports.

**Configuration:**
- **Ports:** [Port Configuration: QOM Network]({{< relref "ports/services/node3-qom" >}}) - Complete port mapping, Docker Compose examples, and firewall configuration
- **Environment Variables:** See [Environment Variables]({{< relref "environment-variables" >}}) for configuration options, including alternative binary settings
- **Port Strategy:** [Port Allocation Strategy]({{< relref "ports/strategy" >}}) - Service #3 (offset: +30)

---

## Service Configuration Reference

For detailed information about:

- **Port Allocation:** See [Port Strategy]({{< relref "ports/strategy" >}}) for the port calculation formula and allocation logic
- **Port Descriptions:** See [Port Reference]({{< relref "ports/reference" >}}) for detailed descriptions of all port types
- **Environment Variables:** See [Environment Variables]({{< relref "environment-variables" >}}) for complete environment variable reference
- **Service Structure:** See [Service Structure]({{< relref "service-structure" >}}) for technical architecture details
