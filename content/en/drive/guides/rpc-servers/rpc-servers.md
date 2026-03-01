---
title: "RPC Servers Set Up Guide"
---

## Step 1: Expose RPC ports to localhost

We recommend that you first change the ports in `drive/services/node0-infinite/docker-compose.yml` as follows:

### ✅ Configuration example (limit RPC exposure to localhost, WS optional)

```yaml
ports:
# P2P
- "26656:26656"
# CometBFT RPC HTTP (expose only to localhost)
- "127.0.0.1:26657:26657"
# GRPC HTTP (expose only to localhost)
- "127.0.0.1:9090:9090"
# EVM JSON-RPC HTTP (expose only to localhost)
- "127.0.0.1:8545:8545"
# WebSocket (if used, expose only to localhost)
# - "127.0.0.1:8546:8546"
```

**Q. Why limit RPC port exposure to localhost?**

- Ports such as `8545/8546 (EVM JSON RPC)` and `26657 (COMET RPC)` should not be exposed directly to the outside world, but should be reachable only by Nginx on the host. This reduces the risk of external DoS attacks.

- Requests are accepted via the following flow: "Nginx (443) → 127.0.0.1:8545 (localhost) → Docker container:8545," allowing the security boundary to be consolidated at Nginx.

**Image:**
```
			  Internet
				    ↓
			  Nginx (443)
				    ↓
		    localhost
127.0.0.1:8545      127.0.0.1:26657
		    ↓                ↓
Docker EVM RPC      Docker COMET RPC
```

> Note: The P2P port (26656) is made public in order to contribute to the network and ensure stable connections.

---
## Step 2: app.toml (enable JSON-RPC)

File: 
`drive/services/node0-infinite/persistent-data/config/app.toml`

Change the following:
```toml
[json-rpc]
enable = true
address = "0.0.0.0:8545"
ws-address = "0.0.0.0:8546"
allow-insecure-unlock = false

# Optional (If you want to expose Grpc, configure the following settings.)
[grpc]
enable = true
address = "0.0.0.0:9090"
```

## Step 3: config.toml (enable COMET-RPC)

File: 
`drive/services/node0-infinite/persistent-data/config/config.toml`

Change the following:
```toml
[rpc]
laddr = "tcp://0.0.0.0:26657"
```

**Q. Why bind to 0.0.0.0?**

If you leave the port `127.0.0.1:8545` in the container, Docker's port forwarding will be difficult to reach from outside the container (localhost). External exposure is limited to localhost on the Docker ports side, so set the port inside the container to `0.0.0.0`.


**Apply and restart the node:**
```bash
./drive.sh down
./drive.sh up -d

# After restarting the container, restart the node from the GUI.
./drive.sh node-ui
```


## Step 4: Nginx configuration

### 4-A) Rate limiting and simultaneous connection limiting settings (optional but recommended)

File: `/etc/nginx/conf.d/00_rpc_limits.conf`

```
# ==========================
# EVM RPC limits
# ==========================
limit_req_zone  $binary_remote_addr zone=rpc_req:10m rate=10r/s;
limit_conn_zone $binary_remote_addr zone=rpc_conn:10m;

# ==========================
# Comet (Tendermint) RPC limits
# ==========================
limit_req_zone  $binary_remote_addr zone=comet_req:10m rate=20r/s;
limit_conn_zone $binary_remote_addr zone=comet_conn:10m;

# ==========================
# WebSocket（Tendermint: Optional）
# ==========================
limit_conn_zone $binary_remote_addr zone=comet_ws_conn:10m;
```

> Rate limiting and concurrent connection limits on public RPC endpoints are basic protective measures to maintain the stability and availability of the overall service by preventing node overload and DoS attacks, and avoiding CPU, memory, and I/O resource depletion. This prevents resource monopolization by specific users or bots, ensuring a fair and stable RPC environment for general users and relayers.

### 4-B) vhost nginx

#### EVM-RPC settings

File: `/etc/nginx/conf.d/evm-rpc.conf`

```nginx
server {
    listen 80;
    listen [::]:80;
    # Please use your domain here
    server_name evm-rpc.infinitedrive.xyz;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;

    # Please use your domain here
    server_name evm-rpc.infinitedrive.xyz;

    # ---- Security headers ----
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer" always;
    add_header X-Frame-Options "DENY" always;
    add_header Permissions-Policy "interest-cohort=()" always;
    # Optional: HSTS (ONLY if you will keep HTTPS permanently)
    # add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    # Place a valid certificate and key (fullchain.pem is recomended)
    ssl_certificate     /etc/nginx/ssl/infinitedrive.xyz.crt;
    ssl_certificate_key /etc/nginx/ssl/infinitedrive.xyz.key;

    client_max_body_size 1m;

    # ---- CORS (apply at SERVER level so it also works for 204/return) ----
    add_header Access-Control-Allow-Origin "*" always;
    add_header Access-Control-Allow-Methods "POST, GET, OPTIONS" always;
    add_header Access-Control-Allow-Headers "Content-Type, Authorization, Accept, Origin, User-Agent, X-Requested-With" always;
    add_header Access-Control-Expose-Headers "Content-Length, Content-Type" always;
    add_header Access-Control-Max-Age 86400 always;

    location / {
        # Fast response for preflight (explicitly add headers here too)
        if ($request_method = OPTIONS) {
            add_header Access-Control-Allow-Origin "*" always;
            add_header Access-Control-Allow-Methods "POST, GET, OPTIONS" always;
            add_header Access-Control-Allow-Headers "Content-Type, Authorization, Accept, Origin, User-Agent, X-Requested-With" always;
            add_header Access-Control-Max-Age 86400 always;
            add_header Content-Length 0;
            add_header Content-Type text/plain;
            return 204;
        }

        # ---- Basic abuse protection ----
        limit_req zone=rpc_req burst=30 nodelay;
        limit_conn rpc_conn 20;

        # Prevent duplicate CORS headers if upstream adds any
        proxy_hide_header Access-Control-Allow-Origin;
        proxy_hide_header Access-Control-Allow-Methods;
        proxy_hide_header Access-Control-Allow-Headers;
        proxy_hide_header Access-Control-Expose-Headers;
        proxy_hide_header Access-Control-Max-Age;

        # ---- Reverse proxy to EVM JSON-RPC ----
        proxy_pass http://127.0.0.1:8545;
        proxy_http_version 1.1;

        # Keepalive / upstream stability
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        proxy_connect_timeout 10s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        proxy_intercept_errors off;
    }
}
```

#### Comet-rpc configuration

- `/etc/nginx/conf.d/comet-rpc.conf`
```nginx
server {
  listen 80;
  listen [::]:80;
  # Use your domain here
  server_name comet-rpc.infinitedrive.xyz;
  return 301 https://$host$request_uri;
}

# 2) HTTPS -> Tendermint RPC (localhost:26657)
server {
  listen 443 ssl http2;
  listen [::]:443 ssl http2;
  
  # Use your domain here
  server_name comet-rpc.infinitedrive.xyz;
  
  # Place a valid certificate and key (fullchain.pem is recomended)
  ssl_certificate /etc/nginx/ssl/infinitedrive.xyz.crt;
  ssl_certificate_key /etc/nginx/ssl/infinitedrive.xyz.key;

  client_max_body_size 1m;

  # Tendermint RPC (HTTP)
  location / {
    limit_conn comet_conn 20;
    limit_conn_status 429;
    
    limit_req  zone=comet_req burst=40 nodelay;
    limit_req_status 429;
  
    proxy_pass http://127.0.0.1:26657;
    proxy_http_version 1.1;

    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header Connection "";

    proxy_connect_timeout 10s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;
  }

  # Tendermint WebSocket endpoint (required by some relayers / subscriptions)
  location /websocket {
    limit_conn comet_ws_conn 20;
    limit_conn_status 429;
    
    proxy_pass http://127.0.0.1:26657/websocket;
    proxy_http_version 1.1;

    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";

    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

    proxy_read_timeout 3600s;
    proxy_send_timeout 3600s;
  }
}
```

#### Grpc settings

File: `/etc/nginx/conf.d/grpc.conf`

```nginx
server {
  listen 443 ssl http2;
  listen [::]:443 ssl http2;

  # Use your domain here
  server_name grpc.infinitedrive.xyz;

  # Place a valid certificate and key (fullchain.pem is recomended)
  ssl_certificate     /etc/nginx/ssl/infinitedrive.xyz.crt;
  ssl_certificate_key /etc/nginx/ssl/infinitedrive.xyz.key;

  # gRPC to local node
  location / {
    grpc_pass grpc://127.0.0.1:9090;

    # optional but often helpful
    grpc_set_header Host $host;
    grpc_set_header X-Real-IP $remote_addr;
    grpc_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

    # gRPC can be long-lived
    grpc_read_timeout 300s;
    grpc_send_timeout 300s;
  }
}
```


Installing nginx (first time only)
```bash
sudo apt update
sudo apt install -y nginx
sudo systemctl enable --now nginx
sudo systemctl status nginx --no-pager
```

Apply the settings:
```bash
# Verify that the test result is `success`
sudo nginx -t
# Apply the settings
sudo systemctl reload nginx
```

---

## Step 5: Check operation

### 5-A) Check from localhost without Nginx
```bash
# (EVM) Get latest block
curl -s -H 'Content-Type: application/json' \
-d '{"jsonrpc":"2.0","id":1,"method":"eth_blockNumber","params":[]}' \
http://127.0.0.1:8545

# (EVM) Check synchronization status
curl -s -H 'Content-Type: application/json' \
-d '{"jsonrpc":"2.0","id":1,"method":"eth_syncing","params":[]}' \
http://127.0.0.1:8545

# Check Tendermint synchronization status
curl -s http://127.0.0.1:26657/status | head
```


### 5-B) Check via Nginx
```bash
# (EVM) Get the latest block
curl -sk -H 'Content-Type: application/json' \
-d '{"jsonrpc":"2.0","id":1,"method":"eth_blockNumber","params":[]}' \
https://your-evm-rpc.example.com

# Check the (EVM) synchronization status
curl -sk -H 'Content-Type: application/json' \
-d '{"jsonrpc":"2.0","id":1,"method":"eth_syncing","params":[]}' \
https://your-evm-rpc.example.com

# Check the Tendermint synchronization status
curl -sk https://your-comet-rpc.example.com/status | head
```

### 5-C)Check GRPC communication:
```bash
grpcurl -insecure your-grpc.example.com:443 list | head

grpcurl -insecure your-grpc.example.com:443 \
  cosmos.base.tendermint.v1beta1.Service/GetLatestBlock
```
> [!important]
> ⚠️ **Cloudflare Proxy and Comet-RPC/gRPC**
>
> Streaming Comet-RPC websocket or gRPC through Cloudflare's "Orange Cloud (Proxy)" may be subject to configuration and plan restrictions.
> 
> Safety measures include:
> 
> - Use DNS only (gray cloud) for the Comet-RPC/gRPC subdomain.
> (TLS terminates at Nginx, and comes directly over 443.)
> 
> - Or, configure Cloudflare to ensure Comet-RPC/gRPC is passed through.
> 
> Either option is acceptable.

We also recommend using a tool such as cerbot to obtain a **fullchain pem** certificate.

<details>

<summary><strong>📗Step by step guide installing Certbot and verify</strong></summary>

**1. Install cerbot on Ubuntu:**
```
sudo apt update
sudo apt install -y certbot python3-certbot-nginx
```

**2. Obtaining a Certificate**

If Nginx is already running:
```
sudo certbot --nginx -d grpc.infinitedrive.xyz
```

If successful:
`/etc/letsencrypt/live/grpc.infinitedrive.xyz/`
will be created.


**3. Check your Nginx configuration**

example:
```bash
sudo nano /etc/nginx/conf.d/grpc.conf

```

Check if `ssl_certificate` and `ssl_certificate_key` is like below:
```nginx
ssl_certificate /etc/letsencrypt/live/grpc.infinitedrive.xyz/fullchain.pem;

ssl_certificate_key /etc/letsencrypt/live/grpc.infinitedrive.xyz/privkey.pem;
```

**Q.Why fullchain.pem?**

If you don't use fullchain.pem certificate, you'll get the following error:
```nginx
x509: certificate signed by unknown authority
```

**4. Nginx reload**

```
sudo nginx -t
sudo systemctl reload nginx
```

**5. Verification**

TLS verification:

```bash
curl -I https://grpc.infinitedrive.xyz
```

</details>

---
## Step 6: Verify with the Drive Verification Tool

Use the validation tool in the drive repository to verify that the RPC server is running correctly.

```bash
cd ~/drive/tools/validate-evm-rpc-endpoint
./validate-evm-rpc-endpoint.sh https://your-evm-rpc.example.com

cd ~/drive/tools/validate-cosmos-rpc-endpoint
./validate-cosmos-rpc-endpoint.sh https://your-comet-rpc.example.com

cd ~/drive/tools/validate-cosmos-grpc-endpoint
./validate-cosmos-grpc-endpoint.sh https://your-grpc.example.com
```
