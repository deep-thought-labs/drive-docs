---
title: Drive Scan Startup Guide
---
## Drive-Scan

Drive-Scan is a configuration repository optimized for efficient operation of **Blockscout**, an EVM-based blockchain explorer, in the Drive environment.

[This repository](https://github.com/deep-thought-labs/drive-scan) is based on the open source project Blockscout, and its configuration and settings have been adapted and extended for the Drive infrastructure. 
The Blockscout implementation itself relies on the official project, and the drive-scan repository mainly provides:

- Docker/docker-compose configuration for a Drive environment

- Configuration template for running multiple scanners in parallel

- Nginx/domain configuration integration example

- Configuration files and instructions modified and added for Drive


Details of the changes and additional settings are clearly stated in the [documentation](../drive-scan-settings-details).

Users can quickly host multiple blockchain scanners with minimal environment variables and domain configuration.

---

## Prerequisites

To use this repository, you need the following:

- Docker and Docker Compose must be installed.[Quick Start Guide](https://docs.infinitedrive.xyz/en/drive/quick-start/installation/)

- The ports required for blockchain node operation must be open.

- A domain for the scanner must be obtained.

## Step 1: Clone the repository

```bash
git clone https://github.com/deep-thought-labs/drive-scan.git

cd drive-scan
```

## Step 2: Configure the node and scanner

<details>
<summary><strong>Mainnet Scanner Setup Instructions</strong></summary>

### **Create a Docker shared network**

This section explains the setup procedure for connecting nodes and Blockscout only between Docker containers (without exposing the host).

> RPCs are not exposed to the host, meaning they cannot be accessed from the outside. This means that only Blockscout can reach them via Docker's dedicated network.

1. Create a Docker network
2. Edit the `app.toml` created after each node is initialized

```bash
docker network create mainnet || true
```

---

### **Edit Node `app.toml`**

After initializing the blockchain node, edit the `[json-rpc]`  section and pruning settings in `app.toml`.

- `~/drive-scan/drive/services/node0-infinite/persistent-data/config/app.toml`
```toml
### Base Configuration ###
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

After editing the toml file, restart the service container and blockchain node.

**Restart container**
```bash
./drive.sh down

./drive.sh up -d

# ⚠️ After restarting the container, restart the node from the GUI.
./drive.sh node-ui
```


3️⃣ **Operation check (from the Docker network side)**

Check whether you can access the block information from the Docker network you just set up.

```bash
# Name resolution + HTTP JSON-RPC response (5-second timeout, verbose)
docker run --rm --network mainnet curlimages/curl:8.11.1 \
-v --max-time 5 -H 'Content-Type: application/json' \
-X POST http://infinite:8545 \
-d '{"jsonrpc":"2.0","method":"web3_clientVersion","params":[],"id":1}'

# Get block height
docker run --rm --network mainnet curlimages/curl:8.11.1 \
-s -H 'Content-Type: application/json' \
-X POST http://infinite:8545 \
-d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":2}'
```

It's OK if JSON like `{"result":"0x...","id":2,"jsonrpc":"2.0"}` is returned.

> Now **the RPC is unreachable from the external internet, only Blockscout can connect directly to `infinite:8545` through the network.**


---

### Change permissions for the blockscout directory

Change the permissions of the blockscout database directory to avoid permission errors.

```bash
# Create directories for blockscout
sudo mkdir -p /home/ubuntu/drive-scan/drive/services/scan0-infinite/{db,stats-db,redis,logs,dets}

# Grant write permission
sudo chown -R ubuntu:ubuntu /home/ubuntu/drive-scan/drive/services/scan0-infinite/{db,stats-db,redis,logs,dets}

# Set owner to 2000:2000
sudo chown -R 2000:2000 ~/drive-scan//drive/services/scan0-infinite/db 
sudo chown -R 2000:2000 ~/drive-scan/drive/services/scan0-infinite/stats-db 
sudo chmod 700 ~/drive-scan/drive/services/scan0-infinite/db 
sudo chmod 700 ~/drive-scan/drive/services/scan0-infinite/stats-db
```

---

### Edit `docker-compose.override.yml` and `ports.env` for the scan service

Edit the frontend > environment and proxy > environment sections of the override.yml file to include the domain names you actually use.

```bash
nano ~/drive-scan/drive/services/scan0-infinite/docker-compose.override.yml
```

```yaml
frontend:
    networks: [mainnet]
    environment:
      NEXT_PUBLIC_APP_HOST: "xxxx-scan.infinitedrive.xyz"
      NEXT_PUBLIC_API_HOST: "xxxx-scan.infinitedrive.xyz"
      NEXT_PUBLIC_STATS_API_HOST: "https://xxxx-scan.infinitedrive.xyz/stats"
      NEXT_PUBLIC_VISUALIZE_API_HOST: "https://xxxx-scan.infinitedrive.xyz/visualizer"
      
proxy:
    environment:
      # Please set the domain you actually use
      APP_HOST: "xxx-scan.infinitedrive.xyz"
```


- Editing `ports.env`
```bash
nano ~/drive-scan/drive/services/scan0-infinite/ports.env
```

Replace the `APP_HOST` value `xxxx-scan.infinitedrive.xyz` with the actual domain you want to use.
```
# Please replace your actual domain here
APP_HOST=xxxx-scan.infinitedrive.xyz
```
</details>

<details>
<summary><strong>Testnet Scanner Setup Instructions</strong></summary>

### **Create a Docker shared network**

This section explains the setup procedure for connecting nodes and Blockscout only between Docker containers (without exposing the host).

> RPCs are not exposed to the host, meaning they cannot be accessed from the outside. This means that only Blockscout can reach them via Docker's dedicated network.

1. Create a Docker network
2. Edit the `app.toml` created after each node is initialized

```bash
docker network create testnet || true
```


---

### **Edit Node `app.toml`**

After initializing the blockchain node, edit the `[json-rpc]` section and pruning settings in `app.toml`.

- `~/drive-scan/drive/services/node1-infinite-testnet/persistent-data/config/app.toml`
```toml
### Base Configuration ###
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

After editing the toml file, restart the service container and blockchain node.

**Restart container**
```bash
./drive.sh down

./drive.sh up -d

# ⚠️ After restarting the container, restart the node from the GUI.
./drive.sh node-ui
```


3️⃣ **Operation check (from the Docker network side)**


```bash
# Name resolution + HTTP JSON-RPC response (5-second timeout, verbose)
docker run --rm --network testnet curlimages/curl:8.11.1 \
-v --max-time 5 -H 'Content-Type: application/json' \
-X POST http://infinite-testnet:8545 \
-d '{"jsonrpc":"2.0","method":"web3_clientVersion","params":[],"id":1}'

# Get block height
docker run --rm --network testnet curlimages/curl:8.11.1 \
-s -H 'Content-Type: application/json' \
-X POST http://infinite-testnet:8545 \
-d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":2}'
```

It's OK if JSON like `{"result":"0x...","id":2,"jsonrpc":"2.0"}` is returned.

> Now **RPC is unreachable from the external internet, only Blockscout can connect directly to `infinite-testnet:8545` through the network.**

---

### Change permissions for the blockscout directory

Change the permissions of the blockscout database directory to avoid permission errors.

```bash
# Create directories for blockscout
sudo mkdir -p /home/ubuntu/drive-scan/drive/services/scan1-infinite-testnet/{db,stats-db,redis,logs,dets}

# Grant write permission
sudo chown -R ubuntu:ubuntu /home/ubuntu/drive-scan/drive/services/scan1-infinite-testnet/{db,stats-db,redis,logs,dets}

# Set owner to 2000:2000
sudo chown -R 2000:2000 ~/drive-scan//drive/services/scan1-infinite-testnet/db 
sudo chown -R 2000:2000 ~/drive-scan/drive/services/scan1-infinite-testnet/stats-db 
sudo chmod 700 ~/drive-scan/drive/services/scan1-infinite-testnet/db 
sudo chmod 700 ~/drive-scan/drive/services/scan1-infinite-testnet/stats-db
```

---

### Edit `docker-compose.override.yml` and `ports.env` for the scan service

Edit the frontend > environment and proxy > environment sections of the override.yml file to include the domain names you actually use.

```bash
nano ~/drive-scan/drive/services/scan1-infinite-testnet/docker-compose.override.yml
```

```yaml
frontend:
    networks: [testnet]
    environment:
      NEXT_PUBLIC_APP_HOST: "xxxx-scan.infinitedrive.xyz"
      NEXT_PUBLIC_API_HOST: "xxxx-scan.infinitedrive.xyz"
      NEXT_PUBLIC_STATS_API_HOST: "https://xxxx-scan.infinitedrive.xyz/stats"
      NEXT_PUBLIC_VISUALIZE_API_HOST: "https://xxxx-scan.infinitedrive.xyz/visualizer"
      
proxy:
    environment:
      # Please set the domain you actually use
      APP_HOST: "xxx-scan.infinitedrive.xyz"
```


- Editing `ports.env`
```bash
nano ~/drive-scan/drive/services/scan1-infinite-testnet/ports.env
```

Replace the `APP_HOST` value `xxxx-scan.infinitedrive.xyz` with the actual domain you want to use.
```
# Please replace your actual domain here
APP_HOST=xxxx-scan.infinitedrive.xyz
```
</details>

<details>
<summary><strong>Creative Scanner Setup Instructions</strong></summary>


## **Create a Docker shared network**

This section explains the setup procedure for connecting nodes and Blockscout only between Docker containers (without exposing the host).

> RPCs are not exposed to the host, meaning they cannot be accessed from the outside. This means that only Blockscout can reach them via Docker's dedicated network.

1. Create a Docker network
2. Edit the `app.toml` created after each node is initialized

```bash
docker network create creative || true
```

---

### **Edit Node `app.toml`**

After initializing the blockchain node, edit the `[json-rpc]` section and pruning settings in `app.toml`.

- `~/drive-scan/drive/services/node2-infinite-creative/persistent-data/config/app.toml`

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


After editing the toml file, please restart the service container and blockchain node.

**Restart container**
```bash
./drive.sh down

./drive.sh up -d

# ⚠️ After restarting the container, restart the node from the GUI.
./drive.sh node-ui
```


3️⃣ **Operation check (from the Docker network side)**

Check whether you can access the block information from the Docker network you just set up.

```bash
# Name resolution + HTTP JSON-RPC response (5-second timeout, verbose)
docker run --rm --network creative curlimages/curl:8.11.1 \
-v --max-time 5 -H 'Content-Type: application/json' \
-X POST http://infinite-creative:8545 \
-d '{"jsonrpc":"2.0","method":"web3_clientVersion","params":[],"id":1}'

# Get block height
docker run --rm --network testnet curlimages/curl:8.11.1 \
-s -H 'Content-Type: application/json' \
-X POST http://infinite-creative:8545 \
-d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":2}'
```

It's OK if JSON like `{"result":"0x...","id":2,"jsonrpc":"2.0"}` is returned.

> Now the RPC is unreachable from the external internet, only Blockscout can connect directly to `infinite-creative:8545` through the network.

---

## Change permissions for the blockscout directory

Change the permissions of the blockscout database directory to make it work.

```bash
# Create directories for blockscout
sudo mkdir -p /home/ubuntu/drive-scan/drive/services/scan2-infinite-creative/{db,stats-db,redis,logs,dets}

# Grant write permission
sudo chown -R ubuntu:ubuntu /home/ubuntu/drive-scan/drive/services/scan2-infinite-creative/{db,stats-db,redis,logs,dets}

# Set owner to 2000:2000
sudo chown -R 2000:2000 ~/drive-scan//drive/services/scan2-infinite-creative/db 
sudo chown -R 2000:2000 ~/drive-scan/drive/services/scan2-infinite-creative/stats-db 
sudo chmod 700 ~/drive-scan/drive/services/scan2-infinite-creative/db 
sudo chmod 700 ~/drive-scan/drive/services/scan2-infinite-creative/stats-db
```

---

### Edit `docker-compose.override.yml` and `ports.env` for the scan service

Edit the frontend > environment and proxy > environment sections of the override.yml file to include the domain names you actually use.

```bash
nano ~/drive-scan/drive/services/scan2-infinite-creative/docker-compose.override.yml
```

```yaml
frontend:
    networks: [creative]
    environment:
      NEXT_PUBLIC_APP_HOST: "xxxx-scan.infinitedrive.xyz"
      NEXT_PUBLIC_API_HOST: "xxxx-scan.infinitedrive.xyz"
      NEXT_PUBLIC_STATS_API_HOST: "https://xxxx-scan.infinitedrive.xyz/stats"
      NEXT_PUBLIC_VISUALIZE_API_HOST: "https://xxxx-scan.infinitedrive.xyz/visualizer"
      
proxy:
    environment:
      # Please set the domain you actually use
      APP_HOST: "xxx-scan.infinitedrive.xyz"
```


- Editing `ports.env`
```bash
nano ~/drive-scan/drive/services/scan2-infinite-creative/ports.env
```

Replace the `APP_HOST` value `xxxx-scan.infinitedrive.xyz` with the actual domain you will be using.
```
# Please replace your actual domain here
APP_HOST=xxxx-scan.infinitedrive.xyz
```

</details>

<details>
<summary><strong>Note: How to obtain a CloudFlare certificate</strong></summary>

### Issue and deploy a certificate (e.g., Cloudflare Origin Cert)

1️⃣ **Create a Cloudflare Origin Cert (Cloudflare Dashboard)**

Cloudflare Dashboard → Your Domain → **SSL/TLS** → **Origin Server** → **Create Certificate**

- Hostnames: `xxxx-scan.yourdomain.example` (or `*.yourdomain.example` if necessary)

- Key type: RSA 2048

- Validity: As desired (longer is fine)


Please keep the following two items that were issued:

- **Origin Certificate（pem）**
    
- **Private key（pem）**  

</details>

## Step 3: Place the certificate and vhost files

1️⃣ **Install nginx**

```bash
sudo apt update
sudo apt install -y nginx
sudo systemctl enable --now nginx

# Check if the installation was successful
sudo systemctl status nginx --no-pager
```


2️⃣ **Create a directory for placing certificates and paste the contents**

Please obtain the certificate from Let's encrypt or the Cloudflare dashboard.

```bash
# make directory if there aren't
sudo mkdir -p /etc/nginx/{ssl,conf.d}
# copy the nginx directory
sudo cp -ri ~/drive-scan/nginx/* /etc/nginx/
# Paste the contents of the origin certificate issued by Cloudflare.
sudo nano /etc/nginx/ssl/example.origin.crt
# Paste the contents of the private key issued by Cloudflare.
sudo nano /etc/nginx/ssl/example.origin.key
# Grant permissions.
sudo chmod 600 /etc/nginx/ssl/example.origin.key
```


3️⃣ **Edit the `.conf` file and enter the actual domain name you want to use**

Replace the `server_name` value in the `.conf` file with the actual domain name you want to use (there are two places).

Mainnet:
```bash
sudo nano /etc/nginx/conf.d/mainnet-scan.conf
```

Testnet:
```bash
sudo nano /etc/nginx/conf.d/testnet-scan.conf 
```

Creative:
```bash
sudo nano /etc/nginx/conf.d/creative-scan.conf 
```

qom:
```bash
sudo nano /etc/nginx/conf.d/qom-scan.conf 
```

> [!important]
> Please remove any files for scanners you do not intend to host, as unnecessary files will cause errors when you run `nginx -t` in the next step.


```bash
# e.g.) when you remove creative-scan.conf
sudo rm /etc/nginx/conf.d/creative-scan.conf
```

After editing or removing the above file, test and reload nginx:
```bash
sudo nginx -t
sudo systemctl reload nginx
```

Expected output:
```txt
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```


**4️⃣ Open ports 80 and 443 in Ubuntu UFW (or Firewall)**

**Check the current UFW status:**
```bash
sudo ufw status
```

If ports 80 and 443 are not open, please do the following:

**Allow ports 80 and 443 (required)**
```bash
sudo ufw allow 80/tcp 
sudo ufw allow 443/tcp

# Apply
sudo ufw reload
```

**Check if port 80 is free:**
```bash
# Verify that port 80 is free (first time only)
sudo ss -lntp | egrep ':(80)\b' || echo "OK: 80 is free"

# Or, verify that nginx is listening on ports 80 and 443.
sudo ss -lntp | egrep ':(80|443)\b' || true sudo systemctl status nginx --no-pager
```

---

## Step 4: **Launch Blockscout**


```bash
# mainnet scan
docker compose --env-file ~/drive-scan/drive/services/scan0-infinite/ports.env \
  -p scan0-infinite \
  -f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
  -f ~/drive-scan/drive/services/scan0-infinite/docker-compose.override.yml \
  up -d


# testnet scan
docker compose --env-file ~/drive-scan/drive/services/scan1-infinite-testnet/ports.env \
  -p scan1-infinite-testnet \
  -f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
  -f ~/drive-scan/drive/services/scan1-infinite-testnet/docker-compose.override.yml \
  up -d


# creative scan
docker compose --env-file ~/drive-scan/drive/services/scan2-infinite-creative/ports.env \
  -p scan2-infinite-creative \
  -f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
  -f ~/drive-scan/drive/services/scan2-infinite-creative/docker-compose.override.yml \
  up -d  
```


> Run the startup command by specifying the `project name`, `docker-compose.yml`, `docker-compose.override.yml`, and `ports.env` paths.
> Indexing will begin within a few minutes to a dozen minutes, and the Web UI will be displayed when you access `https://xxxx-scan.yourdomain.example`.

If the page does not display correctly after a few minutes or even several tens of minutes have passed, please use the [status check commands](../status-check-commands-for-scanners) below to identify the problem.