---
title: "Infinite Creative Scan (scan2-infinite-creative)"
---
## 📂 Directory structure

```
root/etc/nginx/
 ├─ conf.d/                  ← Host nginx file location
 │   ├─ creative-scan.conf 
 │   └─ qom-scan.conf  
 └─ ssl/
    ├─ creative-scan.origin.crt
    └─ creative-scan.origin.key

root/home/ubuntu/blockscout/ ← Clone the Blockscout repository to the root

root/home/ubuntu/drive/
 └─ services/
     ├─ scan2-infinite-creative/
     │   ├─ ports.env       ← Port setting file
     │   ├─ db/             ← Data directories for Blockscout     
     │   ├─ stats-db/
     │   ├─ redis/
     │   ├─ dets/
     │   ├─ logs/
     │   └─ docker-compose.override.yml
     │ 
     └─ scan3-qom/
         ├─ ports.env       ← Port setting file
         ├─ db/             ← Data directories for Blockscout       
         ├─ stats-db/
         ├─ redis/
         ├─ dets/
         ├─ logs/
         └─ docker-compose.override.yml
```

## 🚀 Blockscout setup procedure

### 1️⃣ Clone Blockscout repository
```bash
cd ~ 
git clone https://github.com/blockscout/blockscout.git
```

### 2️⃣ Rewrite CORS settings for Nginx(proxy)
```bash
cd ~/blockscout/docker-compose/proxy

nano default.conf.template
```

```bash
# Change the following lines
add_header 'Access-Control-Allow-Origin' 'http://localhost' always;
↓
# ✏️ after editted
add_header 'Access-Control-Allow-Origin' '$http_origin' always;
```

<details>
<summary><strong>Click to see default.conf.template</strong></summary>

```bash
map $http_upgrade $connection_upgrade {

  default upgrade;
  ''      close;
}

server {
    listen       80;
    server_name  localhost;
    proxy_http_version 1.1;

    location ~ ^/(api(?!-docs$)|socket|sitemap.xml|auth/auth0|auth/auth0/callback|auth/logout) {
        proxy_pass            ${BACK_PROXY_PASS};
        proxy_http_version    1.1;
        proxy_set_header      Host "$host";
        proxy_set_header      X-Real-IP "$remote_addr";
        proxy_set_header      X-Forwarded-For "$proxy_add_x_forwarded_for";
        proxy_set_header      X-Forwarded-Proto "$scheme";
        proxy_set_header      Upgrade "$http_upgrade";
        proxy_set_header      Connection $connection_upgrade;
        proxy_cache_bypass    $http_upgrade;
    }
    location / {
        proxy_pass            ${FRONT_PROXY_PASS};
        proxy_http_version    1.1;
        proxy_set_header      Host "$host";
        proxy_set_header      X-Real-IP "$remote_addr";
        proxy_set_header      X-Forwarded-For "$proxy_add_x_forwarded_for";
        proxy_set_header      X-Forwarded-Proto "$scheme";
        proxy_set_header      Upgrade "$http_upgrade";
        proxy_set_header      Connection $connection_upgrade;
        proxy_cache_bypass    $http_upgrade;
    }
}
server {
    listen       8080;
    server_name  localhost;
    proxy_http_version 1.1;
    proxy_hide_header Access-Control-Allow-Origin;
    proxy_hide_header Access-Control-Allow-Methods;
    # Please edit the line as below
    add_header 'Access-Control-Allow-Origin' '$http_origin' always;
    add_header 'Access-Control-Allow-Credentials' 'true' always;
    add_header 'Access-Control-Allow-Methods' 'PUT, GET, POST, OPTIONS, DELETE, PATCH' always;

    location / {
        proxy_pass            http://stats:8050/;
        proxy_http_version    1.1;
        proxy_set_header      Host "$host";
        proxy_set_header      X-Real-IP "$remote_addr";
        proxy_set_header      X-Forwarded-For "$proxy_add_x_forwarded_for";
        proxy_set_header      X-Forwarded-Proto "$scheme";
        proxy_set_header      Upgrade "$http_upgrade";
        proxy_set_header      Connection $connection_upgrade;
        proxy_cache_bypass    $http_upgrade;
    }
}
server {
    listen       8081;
    server_name  localhost;
    proxy_http_version 1.1;
    proxy_hide_header Access-Control-Allow-Origin;
    proxy_hide_header Access-Control-Allow-Methods;
    # Please edit the line as below
    add_header 'Access-Control-Allow-Origin' '$http_origin' always;
    add_header 'Access-Control-Allow-Credentials' 'true' always;
    add_header 'Access-Control-Allow-Methods' 'PUT, GET, POST, OPTIONS, DELETE, PATCH' always;
    add_header 'Access-Control-Allow-Headers' 'DNT,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization,x-csrf-token' always;

    location / {
        proxy_pass            http://visualizer:8050/;
        proxy_http_version    1.1;
        proxy_buffering       off;
        proxy_set_header      Host "$host";
        proxy_set_header      X-Real-IP "$remote_addr";
        proxy_connect_timeout 30m;
        proxy_read_timeout    30m;
        proxy_send_timeout    30m;
        proxy_set_header      X-Forwarded-For "$proxy_add_x_forwarded_for";
        proxy_set_header      X-Forwarded-Proto "$scheme";
        proxy_set_header      Upgrade "$http_upgrade";
        proxy_set_header      Connection $connection_upgrade;
        proxy_cache_bypass    $http_upgrade;
        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' 'http://localhost' always;
            add_header 'Access-Control-Allow-Credentials' 'true' always;
            add_header 'Access-Control-Allow-Methods' 'PUT, GET, POST, OPTIONS, DELETE, PATCH' always;
            add_header 'Access-Control-Allow-Headers' 'DNT,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization,x-csrf-token' always;
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Content-Type' 'text/plain charset=UTF-8';
            add_header 'Content-Length' 0;
            return 204;
        }
    }
}

```

</details>


>  You can use `$http_origin` to allow the origin of the request as is.

Next, edit the entire contents of the `explorer.conf.template` file.

```bash
nano explorer.conf.template
```
<details>
<summary><strong>Click to see explorer.conf.template</strong></summary>

```nginx
map $http_upgrade $connection_upgrade {
  default upgrade;
  ''      close;
}

  server {
    listen       80;
    # APP_HOST variable is defined in the docker-compose.override.yml
    server_name  ${APP_HOST};
    proxy_http_version 1.1;

    # stats (path-based routing)
    location = /stats { return 301 /stats/; }
    location ^~ /stats/ {
        proxy_pass http://stats:8050/;
        proxy_http_version 1.1;
        proxy_set_header Host "$host";
        proxy_set_header X-Real-IP "$remote_addr";
        proxy_set_header X-Forwarded-For "$proxy_add_x_forwarded_for";
        proxy_set_header X-Forwarded-Proto "$scheme";
    }
  
    # stats API (fallback when frontend calls /api/v1/...)
    location ^~ /api/v1/ {
        proxy_pass http://stats:8050/api/v1/;
        proxy_http_version 1.1;
        proxy_set_header Host "$host";
        proxy_set_header X-Real-IP "$remote_addr";
        proxy_set_header X-Forwarded-For "$proxy_add_x_forwarded_for";
        proxy_set_header X-Forwarded-Proto "$scheme";
    }

    # visualizer (path-based routing)
    location = /visualizer { return 301 /visualizer/; }
    location ^~ /visualizer/ {
        proxy_pass http://visualizer:8050/;
        proxy_http_version 1.1;
        proxy_set_header Host "$host";
        proxy_set_header X-Real-IP "$remote_addr";
        proxy_set_header X-Forwarded-For "$proxy_add_x_forwarded_for";
        proxy_set_header X-Forwarded-Proto "$scheme";
    }

    # backend
    location ~ ^/(api(?!-docs$)|socket|sitemap.xml|auth/auth0|auth/auth0/callback|auth/logout) {
        proxy_pass            ${BACK_PROXY_PASS};
        proxy_http_version    1.1;
        proxy_set_header      Host "$host";
        proxy_set_header      X-Real-IP "$remote_addr";
        proxy_set_header      X-Forwarded-For "$proxy_add_x_forwarded_for";
        proxy_set_header      X-Forwarded-Proto "$scheme";
        proxy_set_header      Upgrade "$http_upgrade";
        proxy_set_header      Connection $connection_upgrade;
        proxy_cache_bypass    $http_upgrade;
    }

    # frontend
    location / {
        proxy_pass            ${FRONT_PROXY_PASS};
        proxy_http_version    1.1;
        proxy_set_header      Host "$host";
        proxy_set_header      X-Real-IP "$remote_addr";
        proxy_set_header      X-Forwarded-For "$proxy_add_x_forwarded_for";
        proxy_set_header      X-Forwarded-Proto "$scheme";
        proxy_set_header      Upgrade "$http_upgrade";
        proxy_set_header      Connection $connection_upgrade;
        proxy_cache_bypass    $http_upgrade;
    }
}
```
</details>

### 3️⃣ Rewrite Nginx (proxy) templates for multiple scanners
To avoid port conflicts when multiple Block Scouts are launched, we will convert some of the templates to variables. We will set the values for these variables in ports.env.

```bash
cd ~/blockscout/docker-compose/services

nano nginx.yml
```

<details>
<summary><strong>Click to see nginx.yml</strong></summary>

```yaml
version: '3.9'

services:
  proxy:
    image: nginx
    # container_name: proxy
    extra_hosts:
      - 'host.docker.internal:host-gateway'

    volumes:
      - "../proxy:/etc/nginx/templates"

    environment:
      BACK_PROXY_PASS: ${BACK_PROXY_PASS:-http://backend:4000}
      FRONT_PROXY_PASS: ${FRONT_PROXY_PASS:-http://frontend:3000}

    ports:
      - target: 80
        published: ${PROXY_HTTP_PORT}

      - target: 8080
        published: ${PROXY_8080_PORT}

      - target: 8081
        published: ${PROXY_8081_PORT}
```
</details>

### 4️⃣ Remove the `container name` from the .yml file under `blockscout/services`
If the container name is fixed, name conflicts will occur when multiple containers are launched, so remove the container name. This will allow the Docker system to automatically name the container according to the naming convention.


```bash
cd blockscout/docker-compose/services

# Please delete the line `container_name: xxxx` from the following file

  # backend
- backend.yml
  # frontend
- frontend.yml
  # db
- db.yml
  # redis-db
- redis.yml
  # proxy
- nginx.yml
- nginx-explorer.yml
  # stats & stats-db ⚠️There are two lines, please delete both
- stats.yml（stats-db / stats）
- sig-provider.yml
- visualizer.yml
- smart-contract-verifier.yml
- user-ops-indexer.yml
- nft_media_handler.yml

```

---

## 🚀 Blockchain Node Setup Procedure

This section explains the setup procedure for connecting the node and Blockscout via Docker containers only (without exposing the host).

> RPCs are not exposed to the host, meaning they cannot be accessed from the outside. This means that **only Blockscout can reach them via Docker's dedicated network.**

### 1️⃣ Create a Docker network

```bash
docker network create creative || true
```

It is recommended to join nodes and scans to their corresponding networks to avoid confusion within the system.

- **(example network): (participants)**
- **mainnet**: node0-infinite and scan0-infinite
- **testnet**: node1-infinite-testnet and scan1-infinite-testnet
- **creative**: node2-infinite-creative and scan2-infinite-creative
- **qom**: node3-qom and scan3-qom

### 2️⃣ Add network configuration to infinite-creative container

```bash
    cd ~/drive/services/node2-infinite-creative
    
    nano docker-compose.yml
  ```

<details>

<summary><strong>Click to see docker-compose.yml</strong></summary>

```yaml
services:
  infinite-creative:
    # Core service settings (image, name, user, restart) - not expected to be modified by users
    image: deepthoughtlabs/infinite-drive:latest
    container_name: infinite-creative
    restart: unless-stopped

    ##################################################################################
    #                       Editable Section Starts Here                             #
    # Customize ports, volumes, and environment variables as needed below.           #
    ##################################################################################
	  # Please add these two lines
    networks:
      - creative
    ports:
      # See ../../config/ports/strategy.md for port allocation strategy and conflict resolution
      # See ../../config/ports/services/node2-infinite-creative.md for complete port configuration
      # Required ports
      - "26676:26656"  # P2P
      - "26677:26657"  # RPC
      
      # Optional ports (uncomment if needed)
      # - "9110:9090"    # gRPC
      # - "9111:9091"    # gRPC-Web
      # - "1337:1317"    # REST API
      # - "8565:8545"    # JSON-RPC HTTP
      # - "8566:8546"    # JSON-RPC WebSocket
      # - "26680:26660"  # Prometheus
      # - "6085:6065"    # EVM Metrics
      # - "8120:8100"    # Geth Metrics

・
・
# No changes need to be made to the lines in between.
・
・
# Please add the following three lines near the end:
networks:
  creative:
    external: true
    
     ### End environment variables
  ### End service qom
### End docker-compose.yml

```

</details>

Simply adding the above settings will not result in JSON-RPC (8545/8546) responding. This is because JSON-RPC is bound only to 127.0.0.1 in the infinite-creative container. The following changes will allow access only from within the same network. (External exposure is not required.)

### 3️⃣ Bind RPC to `0.0.0.0`

```bash
# The following command will automatically detect and rewrite the relevant part of `~/drive/servies/node2-infinite-creative/persistent-data/config/app.toml`

docker exec -it infinite-creative bash -lc '
CONFIG=/home/ubuntu/.infinited/config/app.toml; [ -f "$CONFIG" ] || CONFIG=/root/.infinited/config/app.toml;
cp "$CONFIG" "${CONFIG}.bak.$(date +%s)";
sed -i -E "s/^(address *= *\").*(:8545\".*)$/\10.0.0.0\2/" "$CONFIG";
sed -i -E "s/^(ws-address *= *\").*(:8546\".*)$/\10.0.0.0\2/" "$CONFIG";
sed -i -E "s/^(enable *= *).*/\1true/" "$CONFIG";
echo UPDATED: $CONFIG
'
```


**Restart the container**

```bash
cd ~/drive/services/node2-infinite-creative

./drive.sh down

./drive.sh up -d
```


### 4️⃣ Operation check (from the creative network side)
Check whether block information can be accessed from the `creative` network you just set up.

```bash
# Name resolution + HTTP JSON-RPC response (5-second timeout, detailed display)
docker run --rm --network creative curlimages/curl:8.11.1 \
  -v --max-time 5 -H 'Content-Type: application/json' \
  -X POST http://infinite-creative:8545 \
  -d '{"jsonrpc":"2.0","method":"web3_clientVersion","params":[],"id":1}'

# Get block height
docker run --rm --network creative curlimages/curl:8.11.1 \
  -s -H 'Content-Type: application/json' \
  -X POST http://infinite-creative:8545 \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":2}'

# Websocket response
docker run --rm -it --network creative node:20-alpine sh -lc '
npm -g i wscat >/dev/null 2>&1
wscat -c ws://infinite-creative:8546/
'

# then, throw
{"jsonrpc":"2.0","id":1,"method":"eth_chainId","params":[]}
```

It's OK if JSON like `{"result":"0x...","id":2,"jsonrpc":"2.0"}` or `{"jsonrpc":"2.0","id":1,"result":"0x19183992"}` is returned.

> Now the RPC is unreachable from the external internet, only Blockscout can connect directly to `infinite-creative:8545` through the **creative network**.

---

## 🚀 Scan Service Setup Instructions


### 1️⃣ Create directories under `drive/services` directory

```bash
mkdir -p ~/drive/services/scan2-infinite-creative 

# Create db, stats-db, redis, logs, and dets in the scan2-infinite-creative directory.
mkdir -p /home/ubuntu/drive/services/scan2-infinite-creative/{db,stats-db,redis,logs,dets}

# Change owner of directories to avoid permission errors
sudo chown -R ubuntu:ubuntu /home/ubuntu/drive/services/scan2-infinite-creative/{db,stats-db,redis,logs,dets}

# Set owner to 2000:2000
sudo chown -R 2000:2000 ~/drive/services/scan2-infinite-creative/db 
sudo chown -R 2000:2000 ~/drive/services/scan2-infinite-creative/stats-db 
sudo chmod 700 ~/drive/services/scan2-infinite-creative/db 
sudo chmod 700 ~/drive/services/scan2-infinite-creative/stats-db
```

### 2️⃣ Create a `docker-compose.override.yml` file

```bash
cd ~/drive/services/scan2-infinite-creative

nano docker-compose.override.yml
```

<details>
<summary><strong>Click to see docker-compose.override.yml</strong></summary>

```yaml
networks:
  creative:
    external: true
    name: creative

services:
  backend:
    networks: [creative]
    # --- (OPTIONAL) TCP / OS resource tuning for high-load Blockscout RPC usage ---
    sysctls:
      net.ipv4.ip_local_port_range: "10240 65535"
      net.ipv4.tcp_tw_reuse: "1"
      net.ipv4.tcp_fin_timeout: "15"
    # ---  (OPTIONAL) File descriptor limit tuning ---
    ulimits:
      nofile:
        soft: 1048576
        hard: 1048576

    volumes:
      - /home/ubuntu/drive/services/scan2-infinite-creative/logs:/app/logs
      - /home/ubuntu/drive/services/scan2-infinite-creative/dets:/app/dets

    environment:
      ETHEREUM_JSONRPC_HTTP_URL:  "http://infinite-creative:8545/"
      # To enable websocket, set the value "wss://infinite-creative:8546/"
      ETHEREUM_JSONRPC_WS_URL:    ""
      ETHEREUM_JSONRPC_TRACE_URL: ""
      NFT_MEDIA_HANDLER_ENABLED: "false"
      NFT_MEDIA_HANDLER_BACKFILL_ENABLED: "false"
      NFT_MEDIA_HANDLER_REMOTE_DISPATCHER_NODE_MODE_ENABLED: "false"
      INDEXER_DISABLE_PENDING_TRANSACTIONS_FETCHER: "true"
      CHAIN_ID: "421018002"
      NETWORK: "INFINITE-CREATIVE"
      SUBNETWORK: "scan2-infinite-creative"
      COIN: "CRE42"
      COIN_NAME: "Creative Improbability"
      
      ###############################
      ### To enable market prices, please enable the following:
      # DISABLE_MARKET: "false"
      # MARKET_HISTORY_FETCHER_ENABLED: "true"
      # MARKET_NATIVE_COIN_HISTORY_SOURCE: "coin_gecko"
      # MARKET_CAP_HISTORY_SOURCE: "coin_gecko"
      # MARKET_HISTORY_FETCH_INTERVAL: "30m"
      # MARKET_COINGECKO_COIN_ID: ""

      ###############################
      
      # Limits the number of concurrent connections from Blockscout
      # to the Ethereum JSON-RPC endpoint (qom:8545).
      # This is to prevent ephemeral port exhaustion
      # and excessive TIME_WAIT sockets under high indexing load.
      POOL_SIZE: "5"
      # Controls the connection pool size used by Blockscout’s
      # internal APIs and database-related requests.
      # Kept smaller than POOL_SIZE to reduce overall concurrency
      # and system resource pressure.
      POOL_SIZE_API: "3"
      # URL of the Account Abstraction (ERC-4337) user-ops indexer service.
      # Left empty to fully disable Account Abstraction features,
      # avoiding unnecessary network calls and retry loops
      # when the service is not deployed.
      MICROSERVICE_ACCOUNT_ABSTRACTION_URL: ""

  frontend:
    networks: [creative]
    environment:
      NEXT_PUBLIC_NETWORK_ID: "421018002"
      NEXT_PUBLIC_NETWORK_NAME: "Infinite Improbability Drive - Creative(For Testing)"
      NEXT_PUBLIC_NETWORK_SHORT_NAME: "Creative Net"
      NEXT_PUBLIC_NETWORK_CURRENCY_SYMBOL: "CRE42"
      NEXT_PUBLIC_NETWORK_CURRENCY_NAME: "Creative Improbability"
      NEXT_PUBLIC_APP_PROTOCOL: "https"
      NEXT_PUBLIC_APP_HOST: "creative-scan.infinitedrive.xyz"
      NEXT_PUBLIC_API_PROTOCOL: "https"
      NEXT_PUBLIC_API_HOST: "creative-scan.infinitedrive.xyz"
      NEXT_PUBLIC_API_WEBSOCKET_PROTOCOL: "wss"
      NEXT_PUBLIC_IS_TESTNET: "true"
      NEXT_PUBLIC_STATS_API_HOST: "https://creative-scan.infinitedrive.xyz/stats"
      NEXT_PUBLIC_VISUALIZE_API_HOST: "https://creative-scan.infinitedrive.xyz/visualizer"
      
      ###############################
      ### To enable wallet connect, please enable the following and set the values:
      
      # NEXT_PUBLIC_NETWORK_RPC_URL: ""
      # NEXT_PUBLIC_BLOCKSCOUT_URL: "http://infinite-creative"
      # NEXT_PUBLIC_WALLET_CONNECT_PROJECT_ID: ""

  db:
    networks: [creative]
    volumes:
      - /home/ubuntu/drive/services/scan2-infinite-creative/db:/var/lib/postgresql/data

  stats-db:
    networks: [creative]
    volumes:
      - /home/ubuntu/drive/services/scan2-infinite-creative/stats-db:/var/lib/postgresql/data

  redis-db:
    networks: [creative]
    volumes:
      - /home/ubuntu/drive/services/scan2-infinite-creative/redis:/data

  stats:
    networks: [creative]
    environment:
      STATS__BLOCKSCOUT_API_URL: http://backend:4000

  visualizer:
    networks: [creative]

  sig-provider:
    networks: [creative]

  proxy:
    networks: [creative]
    environment:
    　# Please set the domain you actually use
      APP_HOST: "creative-scan.infinitedrive.xyz"

  #If the settings are not configured properly, the system will restart repeatedly, so explicitly stop folloings.
  nft_media_handler: { profiles: ["off"] }
  user-ops-indexer:  { profiles: ["off"] }
```

</details>

Please replace the key values below with your domain.
- NEXT_PUBLIC_APP_HOST:
- NEXT_PUBLIC_API_HOST:
- NEXT_PUBLIC_STATS_API_HOST: 
- NEXT_PUBLIC_VISUALIZE_API_HOST: 
- APP_HOST:
　
> nft_media_handler:      { profiles: ["off"] }
> user-ops-indexer:       { profiles: ["off"] }
> These can cause errors so it is recommended to leave them off initially.


### 3️⃣ Create a `ports.env` file
```bash
nano ports.env
```

```bash
# Please replace your actual domain here
APP_HOST=creative-scan.infinitedrive.xyz

# Port Settings for `~/blockscout/docker-compose/services/db.yml`
# Port Allocation Strategy：mainnet:+0,testnet:+10,creative-net:+20,qom:+30
POSTGRES_PUBLISHED_PORT=7452

# Port Settings for `~/blockscout/docker-compose/services/stats.yml`
# Port Allocation Strategy：mainnet:+0,testnet:+10,creative-net:+20,qom:+30
STATS_DB_PUBLISHED_PORT=7453

# Port Settings for `~/blockscout/docker-compose/services/nginx.yml && nginx-explorer.yml`
# IMPORTANT: **DO NOT** use ports 80 and 443 here as they are used by nginx.
# Port Allocation Strategy：mainnet:81,testnet:82,creative-net:83,qom:84
PROXY_HTTP_PORT=83
# Port Allocation Strategy：mainnet:+0,testnet:+10,creative-net:+20,qom:+30
PROXY_8080_PORT=8100
PROXY_8081_PORT=8101
```

> Replace the APP_HOST value with the actual domain name you use.

### 4️⃣ Start Blockscout
```bash
docker compose --env-file ~/drive/services/scan2-infinite-creative/ports.env \
  -p scan2-infinite-creative \
  -f ~/blockscout/docker-compose/docker-compose.yml \
  -f ~/drive/services/scan2-infinite-creative/docker-compose.override.yml \
  up -d
```

> Please execute the startup command, specifying the `project name`, `docker-compose.yml`, `docker-compose.override.yml`, and `ports.env` paths.
> Indexing will begin within a few minutes to a dozen minutes, and the Web UI will be displayed when you access `http://<server IP>:83`.

### Check the front-end display

From your browser, access to:
```
http://<Your IP>:83
```

### 🧠 memo

- The initial indexing will take some time. Don't worry if CPU and I/O are at 100%.

- DB capacity will increase dramatically as the index progresses, so NVMe disks are recommended.

- You can monitor the load on each container with `docker stats`.

- The next time you start `node0-infinite`, simply create `scan0-infinite/` using the same procedure and change `ports.env` and the port number.

---

## 🔍 Status check commands

<details>
<summary><strong>Click to see commands</strong></summary>

### Checking the container status and logs
```bash
# Checking the running status of the container
docker compose --env-file ~/drive/services/scan2-infinite-creative/ports.env \
  -p scan2-infinite-creative \
  -f ~/blockscout/docker-compose/docker-compose.yml \
  -f ~/drive/services/scan2-infinite-creative/docker-compose.override.yml \
  ps
  
# Stop the container
docker compose --env-file ~/drive/services/scan2-infinite-creative/ports.env \
  -p scan2-infinite-creative \
  -f ~/blockscout/docker-compose/docker-compose.yml \
  -f ~/drive/services/scan2-infinite-creative/docker-compose.override.yml \
  down

# Checking communication with the Blockscout backend
curl -s http://localhost:83/api/v2/config/backend-version

# Display backend log (stop with ctrl + c)
docker compose --env-file ~/drive/services/scan2-infinite-creative/ports.env \
  -p scan2-infinite-creative \
  -f ~/blockscout/docker-compose/docker-compose.yml \
  -f ~/drive/services/scan2-infinite-creative/docker-compose.override.yml \
  logs -f backend
```


### Checking creative network connection status
```bash
# check creative network presence
docker network ls | grep creative || true

# Is infinite-creative participating in creative?
docker network inspect creative | jq -r '.[0].Containers | to_entries[] | .value.Name' | grep -E '^infinite-creative$' || true

# Is the Blockscout backend participating in creative network?
docker network inspect creative | jq -r '.[0].Containers | to_entries[] | .value.Name' | grep -E '^backend$' || true
```


### Check communication between Blockscout backend and infinite-creative
```bash
# Get eth_blockNumber
docker compose \
  --env-file ~/drive/services/scan2-infinite-creative/ports.env \
  -p scan2-infinite-creative \
  -f ~/blockscout/docker-compose/docker-compose.yml \
  -f ~/drive/services/scan2-infinite-creative/docker-compose.override.yml \
  exec -T backend \
  curl -s -H 'Content-Type: application/json' \
       -d '{"jsonrpc":"2.0","id":1,"method":"eth_blockNumber","params":[]}' \
       http://infinite-creative:8545

# Get latest blocks
docker compose \
  --env-file ~/drive/services/scan2-infinite-creative/ports.env \
  -p scan2-infinite-creative \
  -f ~/blockscout/docker-compose/docker-compose.yml \
  -f ~/drive/services/scan2-infinite-creative/docker-compose.override.yml \
  exec -T backend \
  curl -s -H 'Content-Type: application/json' \
       -d '{"jsonrpc":"2.0","id":2,"method":"eth_getBlockByNumber","params":["latest",true]}' \
       http://infinite-creative:8545
```

> If `result: "0x..."` is returned, **backend can reach infinite-creative node via the creative network**.

### Checking the status of block import into DB
```bash
# ndexer Status
curl -s http://127.0.0.1:83/api/v2/main-page/indexing-status | jq .

# Latest blocks
curl -s "http://127.0.0.1:83/api/v2/blocks?type=block&limit=5" | jq .

# How many blocks are in the DB?
docker compose \
  --env-file ~/drive/services/scan2-infinite-creative/ports.env \
  -p scan2-infinite-creative \
  -f ~/blockscout/docker-compose/docker-compose.yml \
  -f ~/drive/services/scan2-infinite-creative/docker-compose.override.yml exec db \
  psql -U blockscout -d blockscout -c \
  "SELECT COUNT(*) AS blocks, MAX(number) AS max_block FROM blocks;"
```

**Expected Value**
- `eth_blockNumber` in the backend responds.

- `blocks` will start to increase after a few minutes (`indexing-status` will progress).

If `eth_blockNumber` is not returned, the network may still not be connected (`backend` is not included in `creative`) or the `infinite-creative` RPC may be closed. In this case, use `docker network inspect creative` to double-check that `backend` is listed.


### Checking the BlockScout proxy configuration file

```bash
# Checking the final merge of the proxy configuration file
docker exec -it scan2-infinite-creative-proxy-1 sh -lc '
ls -l /etc/nginx/conf.d &&
echo "---- explorer.conf ----" &&
sed -n "1,120p" /etc/nginx/conf.d/explorer.conf
'
```

> Use this to check whether the settings in the `override.yml` and `ports.env` files are correctly reflected to Blockscout.

</details>

---

## 🚀Cloudflare and Host Nginx Configuration

**Prerequisite: Adding a Domain**
Add the domain you want to use for the scanner to Cloudflare.

### Issue a certificate and place it on the host (e.g. Cloudflare Origin Cert)

#### 1) Create a Cloudflare Origin Certificate (Cloudflare Dashboard)

Cloudflare Dashboard → Domain → **SSL/TLS** → **Origin Server** → **Create Certificate**

- **Hostnames:** e.g. )`creative-scan.infinitedrive.xyz` (or `*.infinitedrive.xyz` if necessary)

- **Key type:** RSA 2048

- **Validity:** As desired (longer is fine)

Keep a record of the following two issued documents:

- **Origin Certificate (pem)**

- **Private key (pem)**


#### 2) Place on the host (server or VPS)

Place it in the following location:
``` bash
sudo mkdir -p /etc/nginx/ssl
# Paste the contents of the origin certificate issued by Cloudflare
sudo nano /etc/nginx/ssl/creative-scan.origin.crt
# Paste the contents of the private key issued by Cloudflare
sudo nano /etc/nginx/ssl/creative-scan.origin.key
# Grant permissions
sudo chmod 600 /etc/nginx/ssl/creative-scan.origin.key
```

---

### Host (server or VPS) settings
#### 1) Open ports 80 and 443 in Ubuntu's UFW (or Firewall)

**Check the current UFW status**
```bash
sudo ufw status
```

If ports 80 and 443 are not open, run the following:

**Allow ports 80 and 443 (required)**
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Apply
sudo ufw reload
```

**Check if port 80 is available**
```bash
# Verify that port 80 is open (first time only)
sudo ss -lntp | egrep ':(80)\b' || echo "OK: 80 is free"

# Or, verify that nginx is using ports 80 and 443
sudo ss -lntp | egrep ':(80|443)\b' || true sudo systemctl status nginx --no-pager
````

> Cloudflare grabs ports 80(http) and 443(https), so you need to make sure those ports are not occupied by other processes.
 
 ---
#### 2) Make the host nginx compatible with both 80 and 443

Create `/etc/nginx/conf.d/creative-scan.conf`.

```bash
sudo tee /etc/nginx/conf.d/creative-scan.conf >/dev/null <<'NGINX'
# Infinite Improbability Drive scanners (host nginx entry)

# 1) HTTP -> HTTPS
server {
  listen 80;
  listen [::]:80;
  server_name creative-scan.infinitedrive.xyz;

  return 301 https://$host$request_uri;
}

# 2) HTTPS -> Blockscout container (localhost:83)
server {
  listen 443 ssl http2;
  listen [::]:443 ssl http2;
  server_name creative-scan.infinitedrive.xyz;
  
  # Certificate placement directory
  ssl_certificate     /etc/nginx/ssl/creative-scan.origin.crt;
  ssl_certificate_key /etc/nginx/ssl/creative-scan.origin.key;

  # (Optional) If you want to make TLS a bit more robust
  ssl_protocols TLSv1.2 TLSv1.3;

  # Blockscout  
  location / {
    proxy_pass http://127.0.0.1:83;
    proxy_http_version 1.1;

    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto https;

    # WebSocket
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";

    # (Optional) It is recommended to set a longer waiting time for websocket.
    proxy_read_timeout 3600;
    proxy_send_timeout 3600;
  }
}
NGINX
```

Apply：
```bash
# Start the host nginx
sudo systemctl enable --now nginx
sudo systemctl status nginx --no-pager
```

If it is already running, please reload it:
```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

### 3) Cloudflare SSL/TLS Settings (Important)

Cloudflare Dashboard → Left Menu: SSL/TLS → Overview

- **Encryption mode: Full (strict)**

Cloudflare Dashboard → Network

- **WebSockets: ON**

Cloudflare Dashboard → Left Menu: SSL/TLS → Edge Certificates

- “Always Use HTTPS” is your preference (ON is fine)

- “Automatic HTTPS Rewrites” is your preference (ON is fine)

---

### 4) Operational Verification (Local & External)

**4-A) Check the Response from the Server(Local, no DNS / no Cloudflare)**

```bash
# Check which virtual host responds when accessed locally with a specific Host header (HTTP)
curl -I http://127.0.0.1/ -H 'Host: <your-domain>' | head

# Check HTTPS, TLS certificate, and SNI locally by forcing DNS resolution to 127.0.0.1
curl -Ik https://<your-domain> --resolve <your-domain>:443:127.0.0.1 | head
```


**4-B) Check the Response via Cloudflare**

```bash
# Check the response through Cloudflare using real DNS resolution and HTTPS
curl -Ik https://<your-domain> | head
```

If you get an **HTTP/2 200 or 301 response, it's OK**.

**4-C) Check from your browser**

```bash
https://<your-domain>/
```

---