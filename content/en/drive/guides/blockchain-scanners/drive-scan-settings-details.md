---
title: Drive Scan Settings Details
---

This document details the changes made to the original Blockscout and Drive files.

## Versions

- Blockscout (Backend v9.0.2. Frontend v2.3.5)

## 📂 Directory Structure

```
/                             ← host root
├─ etc/nginx/
│       ├─ conf.d/            ← nginx files directory
│		    └─ ssl/               ← certs directory
│
└─ home/ubuntu/
		├─ blockscout/ 
		└─ drive/services/
				     ├─ scan0-infinite/
				     │   ├─ ports.env       ← ports configuration
				     │   ├─ db              ← Blockscout data directories
				     │   ├─ stats-db
				     │   ├─ redis
				     │   ├─ dets
				     │   ├─ logs
				     │   └─ docker-compose.override.yml
				     │ 
				     ├─ scan1-infinite-testnet/
				     │   ├─ ports.env
				     │   ├─ db
				     │   ├─ stats-db
				     │   ├─ redis
				     │   ├─ dets
				     │   ├─ logs
				     │   └─ docker-compose.override.yml
				     │ 
				     ├─ scan2-infinite-creative/
				     │   ├─ ports.env
				     │   ├─ db
				     │   ├─ stats-db
				     │   ├─ redis
				     │   ├─ dets
				     │   ├─ logs
				     │   └─ docker-compose.override.yml
				     │ 
				     └─ scan3-qom/
				         ├─ ports.env
				         ├─ db
				         ├─ stats-db
				         ├─ redis
				         ├─ dets
				         ├─ logs
				         └─ docker-compose.override.yml
```

## 🚀 Blockscout settings changes

The changes made to the configuration from the original Blockscout repository are as follows:

1. Edit blockscout/docker-compose/proxy/default.conf.template
2. Edit blockscout/docker-compose/proxy/explorer.conf.template
3. Edit blockscout/docker-compose/services/nginx.yml
4. Delete container_name from the `.yml` file under `blockscout/docker-compose/services`


1️⃣ **Edit blockscout/docker-compose/proxy/default.conf.template**
```bash
cd ~/blockscout/docker-compose/proxy

nano default.conf.template
```

```bash
# Change the following for ports 8080 and 8081:
add_header 'Access-Control-Allow-Origin' 'http://localhost' always;
↓
# ✏️After change
add_header 'Access-Control-Allow-Origin' '$http_origin' always;
```

- `default.conf.template`
```bash
# Look for this section
server {
    listen       8080;
    .
    .
    # Do not change anything in the middle.
    .
    .
    # Change this line to the following:
    add_header 'Access-Control-Allow-Origin' '$http_origin' always;
    .
    .
    .
    location / {
      proxy_pass          http://stats:8050/;
      .
      .
      .
        }
}

server {
    listen       8081;
    .
    .
    .
    # Change this line to the following:
    add_header 'Access-Control-Allow-Origin' '$http_origin' always;
    .
    .
    .
    location / {
      proxy_pass          http://visualizer:8050/;
      .
      .
      .
      }
}
```

> You can use `$http_origin` to simply allow the origin of the request.


2️⃣ **Edit blockscout/docker-compose/proxy/explorer.conf.template**

```bash
nano explorer.conf.template
```

- `explorer.conf.template`
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

3️⃣ **Edit blockscout/docker-compose/services/nginx.yml**
To avoid port conflicts when multiple instances of BlockScout are launched, we will convert some of the template to variables. We will set the values of these variables in ports.env on the drive side.

```bash
cd ~/blockscout/docker-compose/services

nano nginx.yml
```

- `nginx.yml`
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


5️⃣ **Remove the container name from the yml file under blockscout/services**
If the container name is fixed, name conflicts will occur when multiple containers are launched, so delete the container name. This will allow the Docker system to automatically name the container according to the naming convention.

```bash
cd blockscout/docker-compose/services

# Delete the `container_name: xxxx` line from the following file

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
# stats & stats-db
# There are two lines, delete both
- stats.yml (stats-db / stats)
- sig-provider.yml
- visualizer.yml
- smart-contract-verifier.yml
- user-ops-indexer.yml
- nft_media_handler.yml

```


That's it for setting up the Blockscout directory.

---

## 🚀 Drive setting changes

The settings changed from the original drive are as follows:

1. Add the Docker network to the docker-compose.yml compose file.
2. Edit the app.toml file for each node service.

1️⃣ **Add a network to the `docker-compose.yml` compose for each blockchain service in drive**

Mainnet：
```bash
    cd ~/drive/services/node0-infinite
    
    nano docker-compose.yml
  ```

Add the following configuration:
```yaml
services:
infinite: 
##################################
###Editable Section Starts Here###
####################################
# Add these two lines
networks:
- mainnet
・
・
・
・
# Add the following three lines near the end
networks:
mainnet:
external: true

 ### End environment variables
  ### End service qom
### End docker-compose.yml
```


Testnet：
```bash
    cd ~/drive/services/node1-infinite-testnet
    
    nano docker-compose.yml
  ```

Add the following configuration:
```yaml
services:
infinite-testnet: 
##################################
###Editable Section Starts Here###
####################################
# Add these two lines
networks:
- testnet
・
・
・
・
# Add the following three lines near the end
networks:
testnet:
external: true

 ### End environment variables
  ### End service qom
### End docker-compose.yml
```


 Creative：
```bash
    cd ~/drive/services/node2-infinite-creative
    
    nano docker-compose.yml
  ```

Add the following settings:
```yaml
services:
infinite-creative: 
##################################
###Editable Section Starts Here###
####################################
# Add these two lines
networks:
- creative
・
・
・
・
# Add the following three lines near the end
networks:
creative:
external: true

 ### End environment variables
  ### End service qom
### End docker-compose.yml
```

- Simply adding the above settings will not result in RPC (8545/8546) responding. This is because JSON-RPC is bound only to 127.0.0.1 in the infinite-creative container. The following changes will allow access only from within the same network. (External exposure is not required.)


2️⃣ **Edit app.toml for each node service**

⚠️Please initialize the node first.

- `~/drive/services/node0-infinite/persistent-data/confog/app.toml`
- `~/drive/services/node1-infinite-testnet/persistent-data/confog/app.toml`
- `~/drive/services/node2-infinite-creative/persistent-data/confog/app.toml`

```toml
** Base Configuration ***
# For scanner operation, it is recommended to set it to "nothing"
pruning = "nothing"


[json-rpc]
# Enable defines if the JSONRPC server should be enabled.
enable = true
# Address defines the EVM RPC HTTP server address to bind to.
address = "0.0.0.0:8545"
# Address defines the EVM WebSocket server address to bind to.
ws-address = "0.0.0.0:8546"
```

---

**Create the `docker-compose.override.yml` and `.env` files**

`override.yml` is a file to override the original blockscout settings. Here we will explain each setting in detail with comments. The `ports.env` file contains the port settings for each scanner, allowing you to host multiple scanners without conflicting settings.


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
      # to the Ethereum JSON-RPC endpoint (infinite-creative:8545).
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
      NEXT_PUBLIC_NETWORK_NAME: "Infinite Improbability Drive - Creative"
      NEXT_PUBLIC_NETWORK_SHORT_NAME: "Infinite Creative"
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
      # NEXT_PUBLIC_BLOCKSCOUT_URL: "http://infinite-creative.infinitedrive.xyz"
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

> - NEXT_PUBLIC_APP_HOST:
> - NEXT_PUBLIC_API_HOST:
> - NEXT_PUBLIC_STATS_API_HOST: 
> - NEXT_PUBLIC_VISUALIZE_API_HOST: 
> - APP_HOST:
> Replace the values of the above keys with your domain.
>
> nft_media_handler: { profiles: ["off"] }
> user-ops-indexer: { profiles: ["off"] }
> We recommend turning these off initially, as they may cause errors.


3️⃣ **Create a `ports.env` file**
```bash
nano ports.env
```

```bash
# Please replace your actual domain here
APP_HOST=creative-scan.infinitedrive.xyz

# Port Settings for　`~/blockscout/docker-compose/services/db.yml`
# Port Allocation Strategy：mainnet:+0,testnet:+10,creative-net:+20,qom:+30
POSTGRES_PUBLISHED_PORT=7452

# Port Settings for　`~/blockscout/docker-compose/services/stats.yml`
# Port Allocation Strategy：mainnet:+0,testnet:+10,creative-net:+20,qom:+30
STATS_DB_PUBLISHED_PORT=7453

# Port Settings for　`~/blockscout/docker-compose/services/nginx.yml && nginx-explorer.yml`
# IMPORTANT: **DO NOT** use ports 80 and 443 here as they are used by nginx.
# Port Allocation Strategy：mainnet:81,testnet:82,creative-net:83,qom:84
PROXY_HTTP_PORT=83
# Port Allocation Strategy：mainnet:+0,testnet:+10,creative-net:+20,qom:+30
PROXY_8080_PORT=8100
PROXY_8081_PORT=8101
```
