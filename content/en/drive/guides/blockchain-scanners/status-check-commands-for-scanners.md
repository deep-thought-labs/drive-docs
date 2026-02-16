---
title: Status Check Commands For Scanners
---

## 🔍Container status check command

Mainnet:
```bash
# Check container status
docker compose --env-file ~/drive-scan/drive/services/scan0-infinite/ports.env \
-p scan0-infinite \
-f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
-f ~/drive-scan/drive/services/scan0-infinite/docker-compose.override.yml \
ps

# Stop container
docker compose --env-file ~/drive-scan/drive/services/scan0-infinite/ports.env \
-p scan0-infinite \
-f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
-f ~/drive-scan/drive/services/scan0-infinite/docker-compose.override.yml \
down

# Check communication with the backend
curl -s http://localhost:81/api/v2/config/backend-version

# Display backend logs (press `ctrl + c` to stop)
docker compose --env-file ~/drive-scan/drive/services/scan0-infinite/ports.env \
  -p scan0-infinite \
  -f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
  -f ~/drive-scan/drive/services/scan0-infinite/docker-compose.override.yml \
  logs -f backend
```


Testnet:
```bash
# Check container status
docker compose --env-file ~/drive-scan/drive/services/scan1-infinite-testnet/ports.env \
-p scan1-infinite-testnet \
-f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
-f ~/drive-scan/drive/services/scan1-infinite-testnet/docker-compose.override.yml \
ps

# Stop container
docker compose --env-file ~/drive-scan/drive/services/scan0-infinite/ports.env \
-p scan1-infinite-testnet \
-f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
-f ~/drive-scan/drive/services/scan1-infinite-testnet/docker-compose.override.yml \
  down

# Check communication with the backend
curl -s http://localhost:82/api/v2/config/backend-version

# Display backend logs (press `ctrl + c` to stop)
docker compose --env-file ~/drive-scan/drive/services/scan1-infinite-testnet/ports.env \
-p scan1-infinite-testnet \
-f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
-f ~/drive-scan/drive/services/scan1-infinite-testnet/docker-compose.override.yml \
logs -f backend
```


Creative:
```bash
# Check container status
docker compose --env-file ~/drive-scan/drive/services/scan2-infinite-creative/ports.env \
-p scan2-infinite-creative \
-f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
-f ~/drive-scan/drive/services/scan2-infinite-creative/docker-compose.override.yml \
ps

# Stop container
docker compose --env-file ~/drive-scan/drive/services/scan2-infinite-creative/ports.env \
-p scan2-infinite-creative \
-f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
-f ~/drive-scan/drive/services/scan2-infinite-creative/docker-compose.override.yml \
  down

# Check communication with the backend
curl -s http://localhost:83/api/v2/config/backend-version

# Display backend logs (press `ctrl + c` to stop)
docker compose --env-file ~/drive-scan/drive/services/scan2-infinite-creative/ports.env \
  -p scan2-infinite-creative \
  -f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
  -f ~/drive-scan/drive/services/scan2-infinite-creative/docker-compose.override.yml \
  logs -f backend
```


---

## 🔍Command to check network connection status

Mainnet
```bash
# mainnet network presence
docker network ls | grep mainnet || true

# Is infinite (node) participating in mainnet?
docker network inspect mainnet | jq -r '.[0].Containers | to_entries[] | .value.Name' | grep -E '^infinite$' || true

# Is the Blockscout backend participating in mainnet?
docker network inspect mainnet | jq -r '.[0].Containers | to_entries[] | .value.Name' | grep -E '^scan0-infinite-backend-1$' || true
```

Testnet
```bash
# testnet network presence
docker network ls | grep testnet || true

# Is infinite-testnet (node) participating in testnet?
docker network inspect testnet | jq -r '.[0].Containers | to_entries[] | .value.Name' | grep -E '^infinite-testnet$' || true

# Is the Blockscout backend participating in testnet?
docker network inspect testnet | jq -r '.[0].Containers | to_entries[] | .value.Name' | grep -E '^scan1-infinite-testnet-backend-1$' || true
```

Creativenet
```bash
# testnet network presence
docker network ls | grep creative || true

# Is infinite-testnet (node) participating in the testnet?
docker network inspect creative | jq -r '.[0].Containers | to_entries[] | .value.Name' | grep -E '^infinite-creative$' || true

# Is the Blockscout backend participating in the testnet?
docker network inspect creative | jq -r '.[0].Containers | to_entries[] | .value.Name' | grep -E '^scan2-infinite-creative-backend-1$' || true
```

---

## 🔍Blockscout backend → Check communication between nodes

Mainnet:
```bash
# Obtain eth_blockNumber
docker compose \
  --env-file ~/drive-scan/drive/services/scan0-infinite/ports.env \
  -p scan0-infinite \
  -f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
  -f ~/drive-scan/drive/services/scan0-infinite/docker-compose.override.yml \
  exec -T backend \
  curl -s -H 'Content-Type: application/json' \
       -d '{"jsonrpc":"2.0","id":1,"method":"eth_blockNumber","params":[]}' \
       http://infinite:8545

# Obtain latest blocks
docker compose \
  --env-file ~/drive-scan/drive/services/scan0-infinite/ports.env \
  -p scan0-infinite \
  -f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
  -f ~/drive-scan/drive/services/scan0-infinite/docker-compose.override.yml \
  exec -T backend \
  curl -s -H 'Content-Type: application/json' \
       -d '{"jsonrpc":"2.0","id":2,"method":"eth_getBlockByNumber","params":["latest",true]}' \
       http://infinite:8545
```

> If `result: "0x..."` is returned, **backend can reach infinite via the mainnet network**.


Testnet
```bash
# Obtain eth_blockNumber
docker compose \
  --env-file ~/drive-scan/drive/services/scan1-infinite-testnet/ports.env \
  -p scan1-infinite-testnet \
  -f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
  -f ~/drive-scan/drive/services/scan1-infinite-testnet/docker-compose.override.yml \
  exec -T backend \
  curl -s -H 'Content-Type: application/json' \
       -d '{"jsonrpc":"2.0","id":1,"method":"eth_blockNumber","params":[]}' \
       http://infinite-testnet:8545

# Obtain latest blocks
docker compose \
  --env-file ~/drive-scan/drive/services/scan1-infinite-testnet/ports.env \
  -p scan1-infinite-testnet \
  -f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
  -f ~/drive-scan/drive/services/scan1-infinite-testnet/docker-compose.override.yml \
  exec -T backend \
  curl -s -H 'Content-Type: application/json' \
       -d '{"jsonrpc":"2.0","id":2,"method":"eth_getBlockByNumber","params":["latest",true]}' \
       http://infinite-testnet:8545
```

> If `result: "0x..."` is returned, **backend can reach infinite-testnet via the testnet network**.

Creative:
```bash
# Obtain eth_blockNumber
docker compose \
  --env-file ~/drive-scan/drive/services/scan2-infinite-creative/ports.env \
  -p scan2-infinite-creative \
  -f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
  -f ~/drive-scan/drive/services/scan2-infinite-creative/docker-compose.override.yml \
  exec -T backend \
  curl -s -H 'Content-Type: application/json' \
       -d '{"jsonrpc":"2.0","id":1,"method":"eth_blockNumber","params":[]}' \
       http://infinite-creative:8545

# Obtain latest blocks
docker compose \
  --env-file ~/drive-scan/drive/services/scan2-infinite-creative/ports.env \
  -p scan2-infinite-creative \
  -f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
  -f ~/drive-scan/drive/services/scan2-infinite-creative/docker-compose.override.yml \
  exec -T backend \
  curl -s -H 'Content-Type: application/json' \
       -d '{"jsonrpc":"2.0","id":2,"method":"eth_getBlockByNumber","params":["latest",true]}' \
       http://infinite-creative:8545
```

> If `result: "0x..."` is returned, **backend can reach infinite-creative via the creative network**.


---

## 🔍Check the status of block import into the blockscout database

Mainnet:
```bash
# Indexer status (the closer to 1, the more progress has been made in the database)
curl -s http://127.0.0.1:81/api/v2/main-page/indexing-status | jq .

# Most recent block
curl -s "http://127.0.0.1:81/api/v2/blocks?type=block&limit=5" | jq .

# Number of blocks stored in the DB
docker compose \
--env-file ~/drive-scan/drive/services/scan0-infinite/ports.env \
-p scan0-infinite \
-f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
-f ~/drive-scan/drive/services/scan0-infinite/docker-compose.override.yml exec db \
psql -U blockscout -d blockscout -c \
"SELECT COUNT(*) AS blocks, MAX(number) AS max_block FROM blocks;"
```

**Expected Results**
- `eth_blockNumber` in the backend responds.

- `blocks` starts to increase after a few minutes (`indexing-status` progresses).

If `eth_blockNumber` is not returned, it may be that the network is not yet connected (`backend` is not in `mainnet`) or the node-side RPC is closed. In that case, please recheck that **`backend` is listed** with `docker network inspect mainnet`.


Testnet:
```bash
# Indexer status (the closer to 1, the more progress has been made in the database)
curl -s http://127.0.0.1:82/api/v2/main-page/indexing-status | jq .

# Most recent block
curl -s "http://127.0.0.1:82/api/v2/blocks?type=block&limit=5" | jq .

# Number of blocks stored in the DB
docker compose \
--env-file ~/drive-scan/drive/services/scan1-infinite-testnet/ports.env \
-p scan1-infinite-testnet \
-f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
-f ~/drive-scan/drive/services/scan1-infinite-testnet/docker-compose.override.yml exec db \
psql -U blockscout -d blockscout -c \
"SELECT COUNT(*) AS blocks, MAX(number) AS max_block FROM blocks;"
```
**Expected value**
- `eth_blockNumber` in the backend responds

- `blocks` starts to increase after a few minutes (`indexing-status` progresses)

If `eth_blockNumber` is not returned, it may be because the network is not yet connected (`backend` is not in `testnet`) or the node-side RPC is closed. In that case, please double-check that **`backend` is listed** with `docker network inspect testnet`.


Creative:
```bash
# Indexer status (the closer to 1, the more progress has been made in the database)
curl -s http://127.0.0.1:83/api/v2/main-page/indexing-status | jq .

# Most recent block
curl -s "http://127.0.0.1:83/api/v2/blocks?type=block&limit=5" | jq .

# Number of blocks stored in the DB
docker compose \
--env-file ~/drive-scan/drive/services/scan2-infinite-creative/ports.env \
-p scan2-infinite-creative \
-f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
-f ~/drive-scan/drive/services/scan2-infinite-creative/docker-compose.override.yml exec db \
psql -U blockscout -d blockscout -c \
"SELECT COUNT(*) AS blocks, MAX(number) AS max_block FROM blocks;"
```

**Expected Results**
- `eth_blockNumber` in the backend responds.

- `blocks` starts to increase after a few minutes (`indexing-status` progresses).

If `eth_blockNumber` is not returned, it may be because the network is not yet connected (`backend` is not in `creative`) or the node-side RPC is closed. In that case, please double-check that **`backend` is listed** with `docker network inspect creative`.

---

## 🔍Check the BlockScout proxy configuration file

Use this to check whether the traffic is flowing to the intended port and whether the domain settings are correct.

Mainnet:
```bash
# Check the final merge of the proxy configuration file
docker exec -it scan0-infinite-proxy-1 sh -lc '
ls -l /etc/nginx/conf.d &&
echo "---- explorer.conf ----" &&
sed -n "1,120p" /etc/nginx/conf.d/explorer.conf
'
```

Testnet:
```bash
# Check the final merge of the proxy configuration file
docker exec -it scan1-infinite-testnet-proxy-1 sh -lc '
ls -l /etc/nginx/conf.d &&
echo "---- explorer.conf ----" &&
sed -n "1,120p" /etc/nginx/conf.d/explorer.conf
'
```

Creative:
```bash
# Check the final merge of the proxy configuration file
docker exec -it scan2-infinite-creative-proxy-1 sh -lc '
ls -l /etc/nginx/conf.d &&
echo "---- explorer.conf ----" &&
sed -n "1,120p" /etc/nginx/conf.d/explorer.conf
'
```

---
