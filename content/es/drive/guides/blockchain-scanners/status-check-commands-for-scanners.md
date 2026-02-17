---
title: Comandos de comprobación de estado para escáneres
---

## 🔍 Comando de comprobación de estado del contenedor

Mainnet:
```bash
# Comprobar estado del contenedor
docker compose --env-file ~/drive-scan/drive/services/scan0-infinite/ports.env \
-p scan0-infinite \
-f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
-f ~/drive-scan/drive/services/scan0-infinite/docker-compose.override.yml \
ps

# Detener contenedor
docker compose --env-file ~/drive-scan/drive/services/scan0-infinite/ports.env \
-p scan0-infinite \
-f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
-f ~/drive-scan/drive/services/scan0-infinite/docker-compose.override.yml \
down

# Comprobar comunicación con el backend
curl -s http://localhost:81/api/v2/config/backend-version

# Mostrar logs del backend (pulsa `ctrl + c` para detener)
docker compose --env-file ~/drive-scan/drive/services/scan0-infinite/ports.env \
  -p scan0-infinite \
  -f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
  -f ~/drive-scan/drive/services/scan0-infinite/docker-compose.override.yml \
  logs -f backend
```


Testnet:
```bash
# Comprobar estado del contenedor
docker compose --env-file ~/drive-scan/drive/services/scan1-infinite-testnet/ports.env \
-p scan1-infinite-testnet \
-f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
-f ~/drive-scan/drive/services/scan1-infinite-testnet/docker-compose.override.yml \
ps

# Detener contenedor
docker compose --env-file ~/drive-scan/drive/services/scan0-infinite/ports.env \
-p scan1-infinite-testnet \
-f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
-f ~/drive-scan/drive/services/scan1-infinite-testnet/docker-compose.override.yml \
  down

# Comprobar comunicación con el backend
curl -s http://localhost:82/api/v2/config/backend-version

# Mostrar logs del backend (pulsa `ctrl + c` para detener)
docker compose --env-file ~/drive-scan/drive/services/scan1-infinite-testnet/ports.env \
-p scan1-infinite-testnet \
-f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
-f ~/drive-scan/drive/services/scan1-infinite-testnet/docker-compose.override.yml \
logs -f backend
```


Creative:
```bash
# Comprobar estado del contenedor
docker compose --env-file ~/drive-scan/drive/services/scan2-infinite-creative/ports.env \
-p scan2-infinite-creative \
-f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
-f ~/drive-scan/drive/services/scan2-infinite-creative/docker-compose.override.yml \
ps

# Detener contenedor
docker compose --env-file ~/drive-scan/drive/services/scan2-infinite-creative/ports.env \
-p scan2-infinite-creative \
-f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
-f ~/drive-scan/drive/services/scan2-infinite-creative/docker-compose.override.yml \
  down

# Comprobar comunicación con el backend
curl -s http://localhost:83/api/v2/config/backend-version

# Mostrar logs del backend (pulsa `ctrl + c` para detener)
docker compose --env-file ~/drive-scan/drive/services/scan2-infinite-creative/ports.env \
  -p scan2-infinite-creative \
  -f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
  -f ~/drive-scan/drive/services/scan2-infinite-creative/docker-compose.override.yml \
  logs -f backend
```


---

## 🔍 Comando para comprobar el estado de la conexión de red

Mainnet
```bash
# Presencia de la red mainnet
docker network ls | grep mainnet || true

# ¿Participa infinite (nodo) en mainnet?
docker network inspect mainnet | jq -r '.[0].Containers | to_entries[] | .value.Name' | grep -E '^infinite$' || true

# ¿Participa el backend de Blockscout en mainnet?
docker network inspect mainnet | jq -r '.[0].Containers | to_entries[] | .value.Name' | grep -E '^scan0-infinite-backend-1$' || true
```

Testnet
```bash
# Presencia de la red testnet
docker network ls | grep testnet || true

# ¿Participa infinite-testnet (nodo) en testnet?
docker network inspect testnet | jq -r '.[0].Containers | to_entries[] | .value.Name' | grep -E '^infinite-testnet$' || true

# ¿Participa el backend de Blockscout en testnet?
docker network inspect testnet | jq -r '.[0].Containers | to_entries[] | .value.Name' | grep -E '^scan1-infinite-testnet-backend-1$' || true
```

Creativenet
```bash
# Presencia de la red creative
docker network ls | grep creative || true

# ¿Participa infinite-creative (nodo) en la red creative?
docker network inspect creative | jq -r '.[0].Containers | to_entries[] | .value.Name' | grep -E '^infinite-creative$' || true

# ¿Participa el backend de Blockscout en la red creative?
docker network inspect creative | jq -r '.[0].Containers | to_entries[] | .value.Name' | grep -E '^scan2-infinite-creative-backend-1$' || true
```

---

## 🔍 Blockscout backend → Comprobar comunicación con los nodos

Mainnet:
```bash
# Obtener eth_blockNumber
docker compose \
  --env-file ~/drive-scan/drive/services/scan0-infinite/ports.env \
  -p scan0-infinite \
  -f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
  -f ~/drive-scan/drive/services/scan0-infinite/docker-compose.override.yml \
  exec -T backend \
  curl -s -H 'Content-Type: application/json' \
       -d '{"jsonrpc":"2.0","id":1,"method":"eth_blockNumber","params":[]}' \
       http://infinite:8545

# Obtener últimos bloques
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

> Si se devuelve `result: "0x..."`, **el backend puede alcanzar infinite a través de la red mainnet**.


Testnet
```bash
# Obtener eth_blockNumber
docker compose \
  --env-file ~/drive-scan/drive/services/scan1-infinite-testnet/ports.env \
  -p scan1-infinite-testnet \
  -f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
  -f ~/drive-scan/drive/services/scan1-infinite-testnet/docker-compose.override.yml \
  exec -T backend \
  curl -s -H 'Content-Type: application/json' \
       -d '{"jsonrpc":"2.0","id":1,"method":"eth_blockNumber","params":[]}' \
       http://infinite-testnet:8545

# Obtener últimos bloques
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

> Si se devuelve `result: "0x..."`, **el backend puede alcanzar infinite-testnet a través de la red testnet**.

Creative:
```bash
# Obtener eth_blockNumber
docker compose \
  --env-file ~/drive-scan/drive/services/scan2-infinite-creative/ports.env \
  -p scan2-infinite-creative \
  -f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
  -f ~/drive-scan/drive/services/scan2-infinite-creative/docker-compose.override.yml \
  exec -T backend \
  curl -s -H 'Content-Type: application/json' \
       -d '{"jsonrpc":"2.0","id":1,"method":"eth_blockNumber","params":[]}' \
       http://infinite-creative:8545

# Obtener últimos bloques
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

> Si se devuelve `result: "0x..."`, **el backend puede alcanzar infinite-creative a través de la red creative**.


---

## 🔍 Comprobar el estado de la importación de bloques en la base de datos de blockscout

Mainnet:
```bash
# Estado del indexador (cuanto más cerca de 1, más progreso en la base de datos)
curl -s http://127.0.0.1:81/api/v2/main-page/indexing-status | jq .

# Bloque más reciente
curl -s "http://127.0.0.1:81/api/v2/blocks?type=block&limit=5" | jq .

# Número de bloques almacenados en la DB
docker compose \
--env-file ~/drive-scan/drive/services/scan0-infinite/ports.env \
-p scan0-infinite \
-f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
-f ~/drive-scan/drive/services/scan0-infinite/docker-compose.override.yml exec db \
psql -U blockscout -d blockscout -c \
"SELECT COUNT(*) AS blocks, MAX(number) AS max_block FROM blocks;"
```

**Resultados esperados**
- `eth_blockNumber` responde en el backend.

- `blocks` empieza a aumentar tras unos minutos (avanza `indexing-status`).

Si no se devuelve `eth_blockNumber`, puede que la red no esté conectada (`backend` no está en `mainnet`) o que el RPC del nodo esté cerrado. En ese caso, comprueba de nuevo que **`backend` aparezca** con `docker network inspect mainnet`.


Testnet:
```bash
# Estado del indexador (cuanto más cerca de 1, más progreso en la base de datos)
curl -s http://127.0.0.1:82/api/v2/main-page/indexing-status | jq .

# Bloque más reciente
curl -s "http://127.0.0.1:82/api/v2/blocks?type=block&limit=5" | jq .

# Número de bloques almacenados en la DB
docker compose \
--env-file ~/drive-scan/drive/services/scan1-infinite-testnet/ports.env \
-p scan1-infinite-testnet \
-f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
-f ~/drive-scan/drive/services/scan1-infinite-testnet/docker-compose.override.yml exec db \
psql -U blockscout -d blockscout -c \
"SELECT COUNT(*) AS blocks, MAX(number) AS max_block FROM blocks;"
```
**Valor esperado**
- `eth_blockNumber` responde en el backend

- `blocks` empieza a aumentar tras unos minutos (avanza `indexing-status`)

Si no se devuelve `eth_blockNumber`, puede que la red no esté conectada (`backend` no está en `testnet`) o que el RPC del nodo esté cerrado. En ese caso, comprueba que **`backend` aparezca** con `docker network inspect testnet`.


Creative:
```bash
# Estado del indexador (cuanto más cerca de 1, más progreso en la base de datos)
curl -s http://127.0.0.1:83/api/v2/main-page/indexing-status | jq .

# Bloque más reciente
curl -s "http://127.0.0.1:83/api/v2/blocks?type=block&limit=5" | jq .

# Número de bloques almacenados en la DB
docker compose \
--env-file ~/drive-scan/drive/services/scan2-infinite-creative/ports.env \
-p scan2-infinite-creative \
-f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
-f ~/drive-scan/drive/services/scan2-infinite-creative/docker-compose.override.yml exec db \
psql -U blockscout -d blockscout -c \
"SELECT COUNT(*) AS blocks, MAX(number) AS max_block FROM blocks;"
```

**Resultados esperados**
- `eth_blockNumber` responde en el backend.

- `blocks` empieza a aumentar tras unos minutos (avanza `indexing-status`).

Si no se devuelve `eth_blockNumber`, puede que la red no esté conectada (`backend` no está en `creative`) o que el RPC del nodo esté cerrado. En ese caso, comprueba que **`backend` aparezca** con `docker network inspect creative`.

---

## 🔍 Comprobar el archivo de configuración del proxy de BlockScout

Sirve para comprobar si el tráfico llega al puerto correcto y si la configuración del dominio es correcta.

Mainnet:
```bash
# Comprobar la fusión final del archivo de configuración del proxy
docker exec -it scan0-infinite-proxy-1 sh -lc '
ls -l /etc/nginx/conf.d &&
echo "---- explorer.conf ----" &&
sed -n "1,120p" /etc/nginx/conf.d/explorer.conf
'
```

Testnet:
```bash
# Comprobar la fusión final del archivo de configuración del proxy
docker exec -it scan1-infinite-testnet-proxy-1 sh -lc '
ls -l /etc/nginx/conf.d &&
echo "---- explorer.conf ----" &&
sed -n "1,120p" /etc/nginx/conf.d/explorer.conf
'
```

Creative:
```bash
# Comprobar la fusión final del archivo de configuración del proxy
docker exec -it scan2-infinite-creative-proxy-1 sh -lc '
ls -l /etc/nginx/conf.d &&
echo "---- explorer.conf ----" &&
sed -n "1,120p" /etc/nginx/conf.d/explorer.conf
'
```

---
