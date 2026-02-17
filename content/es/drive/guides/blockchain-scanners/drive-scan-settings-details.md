---
title: Detalles de configuración de Drive Scan
---

Este documento detalla los cambios realizados respecto al Blockscout original y a los archivos de Drive.

## Versiones

- Blockscout (Backend v9.0.2. Frontend v2.3.5)

## 📂 Estructura de directorios

```
/                             ← raíz del host
├─ etc/nginx/
│       ├─ conf.d/            ← directorio de archivos nginx
│		    └─ ssl/               ← directorio de certificados
│
└─ home/ubuntu/
		├─ blockscout/ 
		└─ drive/services/
				     ├─ scan0-infinite/
				     │   ├─ ports.env       ← configuración de puertos
				     │   ├─ db              ← directorios de datos de Blockscout
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

## 🚀 Cambios de configuración de Blockscout

Los cambios realizados en la configuración respecto al repositorio original de Blockscout son:

1. Editar blockscout/docker-compose/proxy/default.conf.template
2. Editar blockscout/docker-compose/proxy/explorer.conf.template
3. Editar blockscout/docker-compose/services/nginx.yml
4. Eliminar container_name de los archivos `.yml` en `blockscout/docker-compose/services`


1️⃣ **Editar blockscout/docker-compose/proxy/default.conf.template**
```bash
cd ~/blockscout/docker-compose/proxy

nano default.conf.template
```

```bash
# Cambiar lo siguiente para los puertos 8080 y 8081:
add_header 'Access-Control-Allow-Origin' 'http://localhost' always;
↓
# ✏️ Después del cambio
add_header 'Access-Control-Allow-Origin' '$http_origin' always;
```

- `default.conf.template`
```bash
# Busca esta sección
server {
    listen       8080;
    .
    .
    # No cambies nada en el medio.
    .
    .
    # Cambia esta línea por la siguiente:
    add_header 'Access-Control-Allow-Origin' '$http_origin' always;
    .
    .
    .
    location / {
      proxy_pass          http://stats:8050/;
      .
      .
      .
        }
}

server {
    listen       8081;
    .
    .
    .
    # Cambia esta línea por la siguiente:
    add_header 'Access-Control-Allow-Origin' '$http_origin' always;
    .
    .
    .
    location / {
      proxy_pass          http://visualizer:8050/;
      .
      .
      .
      }
}
```

> Puedes usar `$http_origin` para permitir simplemente el origen de la petición.


2️⃣ **Editar blockscout/docker-compose/proxy/explorer.conf.template**

```bash
nano explorer.conf.template
```

- `explorer.conf.template`
```nginx
map $http_upgrade $connection_upgrade {
  default upgrade;
  ''      close;
}

  server {
    listen       80;
    # La variable APP_HOST se define en docker-compose.override.yml
    server_name  ${APP_HOST};
    proxy_http_version 1.1;

    # stats (enrutamiento por path)
    location = /stats { return 301 /stats/; }
    location ^~ /stats/ {
        proxy_pass http://stats:8050/;
        proxy_http_version 1.1;
        proxy_set_header Host "$host";
        proxy_set_header X-Real-IP "$remote_addr";
        proxy_set_header X-Forwarded-For "$proxy_add_x_forwarded_for";
        proxy_set_header X-Forwarded-Proto "$scheme";
    }
  
    # stats API (respaldo cuando el frontend llama a /api/v1/...)
    location ^~ /api/v1/ {
        proxy_pass http://stats:8050/api/v1/;
        proxy_http_version 1.1;
        proxy_set_header Host "$host";
        proxy_set_header X-Real-IP "$remote_addr";
        proxy_set_header X-Forwarded-For "$proxy_add_x_forwarded_for";
        proxy_set_header X-Forwarded-Proto "$scheme";
    }

    # visualizer (enrutamiento por path)
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

    # frontend
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
```

3️⃣ **Editar blockscout/docker-compose/services/nginx.yml**
Para evitar conflictos de puertos al lanzar varias instancias de BlockScout, se convierten partes de la plantilla en variables. Los valores se definen en ports.env en el lado de drive.

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


5️⃣ **Eliminar el nombre del contenedor de los archivos yml en blockscout/services**
Si el nombre del contenedor es fijo, habrá conflictos al lanzar varios contenedores; elimina el nombre del contenedor para que Docker asigne el nombre automáticamente.

```bash
cd blockscout/docker-compose/services

# Elimina la línea `container_name: xxxx` de los siguientes archivos

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
# Hay dos líneas, elimina ambas
- stats.yml (stats-db / stats)
- sig-provider.yml
- visualizer.yml
- smart-contract-verifier.yml
- user-ops-indexer.yml
- nft_media_handler.yml

```


Con esto termina la configuración del directorio Blockscout.

---

## 🚀 Cambios de configuración de Drive

Los cambios respecto al drive original son:

1. Añadir la red Docker al archivo docker-compose.yml.
2. Editar el archivo app.toml de cada servicio de nodo.

1️⃣ **Añadir una red al docker-compose.yml de cada servicio blockchain en drive**

Mainnet：
```bash
    cd ~/drive/services/node0-infinite
    
    nano docker-compose.yml
  ```

Añade la siguiente configuración:
```yaml
services:
infinite: 
##################################
###Editable Section Starts Here###
####################################
# Añade estas dos líneas
networks:
- mainnet
・
・
・
・
# Añade las siguientes tres líneas cerca del final
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

Añade la siguiente configuración:
```yaml
services:
infinite-testnet: 
##################################
###Editable Section Starts Here###
####################################
# Añade estas dos líneas
networks:
- testnet
・
・
・
・
# Añade las siguientes tres líneas cerca del final
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

Añade la siguiente configuración:
```yaml
services:
infinite-creative: 
##################################
###Editable Section Starts Here###
####################################
# Añade estas dos líneas
networks:
- creative
・
・
・
・
# Añade las siguientes tres líneas cerca del final
networks:
creative:
external: true

 ### End environment variables
  ### End service qom
### End docker-compose.yml
```

- Simplemente añadir lo anterior no hará que RPC (8545/8546) responda. JSON-RPC está enlazado solo a 127.0.0.1 en el contenedor infinite-creative. Los siguientes cambios permiten el acceso solo desde la misma red. (No se requiere exposición externa.)


2️⃣ **Editar app.toml de cada servicio de nodo**

⚠️Inicializa primero el nodo.

- `~/drive/services/node0-infinite/persistent-data/confog/app.toml`
- `~/drive/services/node1-infinite-testnet/persistent-data/confog/app.toml`
- `~/drive/services/node2-infinite-creative/persistent-data/confog/app.toml`

```toml
** Base Configuration ***
# Para el escáner se recomienda configurarlo en "nothing"
pruning = "nothing"


[json-rpc]
# Enable define si el servidor JSONRPC debe estar habilitado.
enable = true
# Address define la dirección del servidor HTTP EVM RPC a la que enlazar.
address = "0.0.0.0:8545"
# Address define la dirección del servidor WebSocket EVM a la que enlazar.
ws-address = "0.0.0.0:8546"
```

---

**Crear los archivos `docker-compose.override.yml` y `.env`**

`override.yml` es el archivo para sobrescribir la configuración original de blockscout. Aquí se explica cada opción con comentarios. El archivo `ports.env` contiene la configuración de puertos de cada escáner, permitiendo alojar varios escáneres sin conflictos.


```yaml
networks:
  creative:
    external: true
    name: creative

services:
  backend:
    networks: [creative]
    # --- (OPCIONAL) Ajuste de recursos TCP/OS para uso intensivo de RPC de Blockscout ---
    sysctls:
      net.ipv4.ip_local_port_range: "10240 65535"
      net.ipv4.tcp_tw_reuse: "1"
      net.ipv4.tcp_fin_timeout: "15"
    # ---  (OPCIONAL) Límite de descriptores de archivo ---
    ulimits:
      nofile:
        soft: 1048576
        hard: 1048576

    volumes:
      - /home/ubuntu/drive/services/scan2-infinite-creative/logs:/app/logs
      - /home/ubuntu/drive/services/scan2-infinite-creative/dets:/app/dets

    environment:
      ETHEREUM_JSONRPC_HTTP_URL:  "http://infinite-creative:8545/"
      # Para habilitar websocket, establece "wss://infinite-creative:8546/"
      ETHEREUM_JSONRPC_WS_URL:    ""
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
      ### Para habilitar precios de mercado, habilita lo siguiente:
      # DISABLE_MARKET: "false"
      # MARKET_HISTORY_FETCHER_ENABLED: "true"
      # MARKET_NATIVE_COIN_HISTORY_SOURCE: "coin_gecko"
      # MARKET_CAP_HISTORY_SOURCE: "coin_gecko"
      # MARKET_HISTORY_FETCH_INTERVAL: "30m"
      # MARKET_COINGECKO_COIN_ID: ""

      ###############################
      
      # Limita las conexiones concurrentes de Blockscout
      # al endpoint Ethereum JSON-RPC (infinite-creative:8545).
      # Evita agotamiento de puertos efímeros
      # y sockets TIME_WAIT bajo carga alta de indexación.
      POOL_SIZE: "5"
      # Tamaño del pool de conexiones usado por las APIs internas
      # y peticiones a la base de datos de Blockscout.
      # Más pequeño que POOL_SIZE para reducir la concurrencia
      # y la presión sobre recursos del sistema.
      POOL_SIZE_API: "3"
      # URL del servicio indexador de user-ops (ERC-4337) Account Abstraction.
      # Vacío para deshabilitar Account Abstraction,
      # evitando llamadas de red y bucles de reintento
      # cuando el servicio no está desplegado.
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
      ### Para habilitar wallet connect, habilita lo siguiente y define los valores:
      
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
      # Configura el dominio que uses realmente
      APP_HOST: "creative-scan.infinitedrive.xyz"

  # Si la configuración no es correcta, el sistema se reiniciará repetidamente; desactiva explícitamente:
  nft_media_handler: { profiles: ["off"] }
  user-ops-indexer:  { profiles: ["off"] }
  
```

> - NEXT_PUBLIC_APP_HOST:
> - NEXT_PUBLIC_API_HOST:
> - NEXT_PUBLIC_STATS_API_HOST: 
> - NEXT_PUBLIC_VISUALIZE_API_HOST: 
> - APP_HOST:
> Sustituye los valores de las claves anteriores por tu dominio.
>
> nft_media_handler: { profiles: ["off"] }
> user-ops-indexer: { profiles: ["off"] }
> Se recomienda desactivarlos al principio, ya que pueden causar errores.


3️⃣ **Crear un archivo `ports.env`**
```bash
nano ports.env
```

```bash
# Sustituye aquí por tu dominio real
APP_HOST=creative-scan.infinitedrive.xyz

# Configuración de puertos para `~/blockscout/docker-compose/services/db.yml`
# Estrategia: mainnet:+0, testnet:+10, creative-net:+20, qom:+30
POSTGRES_PUBLISHED_PORT=7452

# Configuración de puertos para `~/blockscout/docker-compose/services/stats.yml`
# Estrategia: mainnet:+0, testnet:+10, creative-net:+20, qom:+30
STATS_DB_PUBLISHED_PORT=7453

# Configuración de puertos para `~/blockscout/docker-compose/services/nginx.yml && nginx-explorer.yml`
# IMPORTANTE: NO uses los puertos 80 y 443 aquí; los usa nginx.
# Estrategia: mainnet:81, testnet:82, creative-net:83, qom:84
PROXY_HTTP_PORT=83
# Estrategia: mainnet:+0, testnet:+10, creative-net:+20, qom:+30
PROXY_8080_PORT=8100
PROXY_8081_PORT=8101
```
