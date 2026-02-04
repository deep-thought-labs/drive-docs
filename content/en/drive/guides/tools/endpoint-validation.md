---
title: "Endpoint Validation Scripts"
weight: 5231
---

Drive includes three validation scripts to check that node endpoints (Cosmos gRPC, Tendermint RPC, and EVM RPC) are reachable and respond correctly. They are useful before connecting a client, after deploying a node, or when troubleshooting connectivity. All three live under `drive/tools/` and share common logic in `tools/common/endpoint-validation-common.sh`.

## Overview

| Script | Endpoint type | Typical port | Purpose |
|--------|----------------|--------------|---------|
| `validate-cosmos-grpc-endpoint.sh` | Cosmos gRPC | 9090 | Application and module queries (balances, staking, account state). Standard way for clients to query chain state in the Cosmos ecosystem. |
| `validate-cosmos-rpc-endpoint.sh` | Tendermint RPC | 26657 | Low-level node/chain data: sync status, chain ID, latest block, consensus. Used by relayers, block explorers, and other Tendermint-layer clients. |
| `validate-evm-rpc-endpoint.sh` | EVM JSON-RPC | 8545 | Ethereum-compatible interface: balances, state, blocks, sending transactions. Used by wallets, dApps, and EVM tooling. |

**About ports:** The "typical port" is the default for that service type. The port actually configured and exposed for your endpoint may be different. In our ecosystem, when using Drive, several nodes or services often run on the same server; thanks to our [port allocation strategy]({{< relref "../../services/ports" >}}), the port exposed on the host can differ from the port the service uses internally. Use the port your administrator has configured or exposed (e.g. in the Service Catalog or in your reverse proxy).

**Expected outcome:** Each script exits with code `0` when all checks pass, and `1` when one or more fail. Output uses colors (✓ passed, ✗ failed, ⚠ warnings) and a final summary; when the endpoint responds, the summary shows chain ID, latest block height, and related info where applicable.

---

## 1. Cosmos gRPC (`validate-cosmos-grpc-endpoint.sh`)

**What it does:** Verifies that the gRPC endpoint is reachable and, when possible, that it exposes the expected gRPC services. Optionally lists services and calls `GetNodeInfo` and `GetLatestBlock` to show chain ID, node version, app name, and latest block.

**Checks:** URL/host:port normalization, DNS resolution, gRPC port connectivity (preferably with `grpcurl`; falls back to TCP probe), SSL certificate for HTTPS, optional gRPC service list and chain info, optional CORS and security headers if the endpoint responds to HTTP.

**Before running:** Change into the folder that contains the script (from the Drive repo root):

```bash
cd drive/tools/validate-cosmos-grpc-endpoint
```

**Usage:**

```bash
./validate-cosmos-grpc-endpoint.sh <URL_or_host:port>
```

**Examples:**

```bash
# With protocol and port
# (typical;
# the actual port may differ depending on your configuration)
./validate-cosmos-grpc-endpoint.sh https://grpc.example.com:9090
./validate-cosmos-grpc-endpoint.sh localhost:9090
./validate-cosmos-grpc-endpoint.sh grpc.example.com:9090

# Domain or subdomain without port
# (server/proxy handles routing;
# common when the administrator points a subdomain to the service port)
./validate-cosmos-grpc-endpoint.sh https://grpc.example.com
```

**Requirements:** `grpcurl` is recommended for full validation; without it, only a TCP connectivity fallback is used. Optional: `openssl` (HTTPS), `curl`, `nc` or `/dev/tcp`, and DNS tools (`host`, `dig`, `nslookup`).

---

## 2. Cosmos (Tendermint) RPC (`validate-cosmos-rpc-endpoint.sh`)

**What it does:** Checks that the Tendermint RPC endpoint is reachable and returns valid data. Calls GET `/status` and validates JSON with `result.node_info` and `result.sync_info`; reports chain ID and latest block height.

**Checks:** URL normalization (protocol added if missing), DNS resolution, port connectivity (or via `/status` if no port given), and Tendermint `/status` response.

**Before running:** Change into the folder that contains the script (from the Drive repo root):

```bash
cd drive/tools/validate-cosmos-rpc-endpoint
```

**Usage:**

```bash
./validate-cosmos-rpc-endpoint.sh <URL>
```

**Examples:**

```bash
# With protocol and port
# (typical;
# the actual port may differ depending on your configuration)
./validate-cosmos-rpc-endpoint.sh https://rpc.example.com:26657
./validate-cosmos-rpc-endpoint.sh http://localhost:26657
./validate-cosmos-rpc-endpoint.sh rpc.example.com:26657

# Domain or subdomain without port
# (server/proxy handles routing;
# common when the administrator points a subdomain to the service port)
./validate-cosmos-rpc-endpoint.sh https://rpc.example.com
```

**Requirements:** `curl` (required); optional `nc` or `/dev/tcp`, and DNS tools.

---

## 3. EVM RPC (`validate-evm-rpc-endpoint.sh`)

**What it does:** Verifies that the EVM JSON-RPC endpoint is reachable and correctly configured. Runs multiple checks including four RPC methods (`web3_clientVersion`, `eth_blockNumber`, `net_version`, `eth_chainId`), plus CORS and security headers for browser/wallet use.

**Checks:** URL normalization, DNS resolution, connectivity, SSL certificate (HTTPS), HTTP/HTTPS response, EVM RPC methods, CORS headers, and security headers. The final summary shows the total number of individual checks (e.g. 12+) and how many passed or failed.

**Before running:** Change into the folder that contains the script (from the Drive repo root):

```bash
cd drive/tools/validate-evm-rpc-endpoint
```

**Usage:**

```bash
./validate-evm-rpc-endpoint.sh <URL>
```

**Examples:**

```bash
# With protocol and port
# (typical;
# the actual port may differ depending on your configuration)
./validate-evm-rpc-endpoint.sh https://rpc.example.com:8545
./validate-evm-rpc-endpoint.sh http://localhost:8545
./validate-evm-rpc-endpoint.sh rpc.example.com:8545

# Domain or subdomain without port
# (server/proxy handles routing;
# common when the administrator points a subdomain to the service port)
./validate-evm-rpc-endpoint.sh https://evmrpc.example.com
```

**Requirements:** `curl` (required); optional `openssl`, `nc` or `/dev/tcp`, and DNS tools.

---

## Common behavior

- **No default ports:** If no port is specified, the URL is left as-is; the server or load balancer handles routing. Scripts do not guess a port.
- **Timeouts:** Default connection timeout is 10 seconds (some steps use shorter timeouts for faster fallbacks).
- **Exit codes:** `0` = all validations passed; `1` = one or more failed or an error occurred.
- **Compatibility:** Linux, macOS, BSD, and Unix-like systems with bash 4.0+.

The scripts source `common/endpoint-validation-common.sh` for shared behavior: colors, print helpers, DNS resolution, timing, and a consistent footer.
