---
title: "Infinite Creative Scan (scan2-infinite-creative)"
---
## 📂 Estructura de directorios

```
root/etc/nginx/
 ├─ conf.d/                  ← Ubicación de archivos nginx en el host
 │   ├─ creative-scan.conf 
 │   └─ qom-scan.conf  
 └─ ssl/
    ├─ creative-scan.origin.crt
    └─ creative-scan.origin.key

root/home/ubuntu/blockscout/ ← Clonar el repositorio Blockscout en la raíz

root/home/ubuntu/drive/
 └─ services/
     ├─ scan2-infinite-creative/
     │   ├─ ports.env       ← Archivo de configuración de puertos
     │   ├─ db/             ← Directorios de datos de Blockscout     
     │   ├─ stats-db/
     │   ├─ redis/
     │   ├─ dets/
     │   ├─ logs/
     │   └─ docker-compose.override.yml
     │ 
     └─ scan3-qom/
         ├─ ports.env       ← Archivo de configuración de puertos
         ├─ db/             ← Directorios de datos de Blockscout       
         ├─ stats-db/
         ├─ redis/
         ├─ dets/
         ├─ logs/
         └─ docker-compose.override.yml
```

## 🚀 Procedimiento de configuración de Blockscout

### 1️⃣ Clonar el repositorio Blockscout
```bash
cd ~ 
git clone https://github.com/blockscout/blockscout.git
```

### 2️⃣ Modificar la configuración CORS de Nginx (proxy)
```bash
cd ~/blockscout/docker-compose/proxy

nano default.conf.template
```

```bash
# Cambia las siguientes líneas
add_header 'Access-Control-Allow-Origin' 'http://localhost' always;
↓
# ✏️ después de editar
add_header 'Access-Control-Allow-Origin' '$http_origin' always;
```

<details>
<summary><strong>Ver default.conf.template</strong></summary>

(Contenido igual al original; las líneas a cambiar son las de add_header para 8080 y 8081.)
</details>


> Puedes usar `$http_origin` para permitir el origen de la petición tal cual.

A continuación, edita el contenido completo del archivo `explorer.conf.template`.

```bash
nano explorer.conf.template
```
(Ver documento en inglés para el bloque completo de explorer.conf.template.)

### 3️⃣ Reescribir plantillas Nginx (proxy) para varios escáneres
Para evitar conflictos de puertos al lanzar varios Block Scout, se convierten partes de las plantillas en variables. Los valores se definen en ports.env.

```bash
cd ~/blockscout/docker-compose/services

nano nginx.yml
```

(Contenido: mismo nginx.yml que en la versión EN, con ports publicados como variables.)

### 4️⃣ Eliminar el `container name` de los archivos .yml en `blockscout/services`
Si el nombre del contenedor es fijo, habrá conflictos al lanzar varios contenedores; elimínalo para que Docker asigne el nombre automáticamente.

```bash
cd blockscout/docker-compose/services

# Elimina la línea `container_name: xxxx` de: backend.yml, frontend.yml, db.yml, redis.yml, nginx.yml, nginx-explorer.yml, stats.yml (stats-db y stats), sig-provider.yml, visualizer.yml, smart-contract-verifier.yml, user-ops-indexer.yml, nft_media_handler.yml
```

---

## 🚀 Procedimiento de configuración del nodo blockchain

Esta sección explica cómo conectar el nodo y Blockscout solo mediante contenedores Docker (sin exponer el host).

> Los RPC no se exponen al host; solo Blockscout puede alcanzarlos a través de la red dedicada de Docker.

### 1️⃣ Crear una red Docker

```bash
docker network create creative || true
```

Se recomienda unir nodos y escáneres a su red correspondiente.

- **mainnet**: node0-infinite y scan0-infinite
- **testnet**: node1-infinite-testnet y scan1-infinite-testnet
- **creative**: node2-infinite-creative y scan2-infinite-creative
- **qom**: node3-qom y scan3-qom

### 2️⃣ Añadir configuración de red al contenedor infinite-creative

```bash
cd ~/drive/services/node2-infinite-creative
nano docker-compose.yml
```

Añade `networks: - creative` al servicio y al final del archivo:
```yaml
networks:
  creative:
    external: true
```

Solo con lo anterior JSON-RPC (8545/8546) no responderá, porque está enlazado a 127.0.0.1. Los siguientes cambios permiten el acceso solo desde la misma red.

### 3️⃣ Enlazar RPC a `0.0.0.0`

```bash
docker exec -it infinite-creative bash -lc '
CONFIG=/home/ubuntu/.infinited/config/app.toml; [ -f "$CONFIG" ] || CONFIG=/root/.infinited/config/app.toml;
cp "$CONFIG" "${CONFIG}.bak.$(date +%s)";
sed -i -E "s/^(address *= *\").*(:8545\".*)$/\10.0.0.0\2/" "$CONFIG";
sed -i -E "s/^(ws-address *= *\").*(:8546\".*)$/\10.0.0.0\2/" "$CONFIG";
sed -i -E "s/^(enable *= *).*/\1true/" "$CONFIG";
echo UPDATED: $CONFIG
'
```

**Reiniciar el contenedor**
```bash
cd ~/drive/services/node2-infinite-creative
./drive.sh down
./drive.sh up -d
```

### 4️⃣ Comprobación de funcionamiento (desde la red creative)
Comprueba si se puede acceder a la información de bloques desde la red `creative`.

```bash
docker run --rm --network creative curlimages/curl:8.11.1 \
  -v --max-time 5 -H 'Content-Type: application/json' \
  -X POST http://infinite-creative:8545 \
  -d '{"jsonrpc":"2.0","method":"web3_clientVersion","params":[],"id":1}'

docker run --rm --network creative curlimages/curl:8.11.1 \
  -s -H 'Content-Type: application/json' \
  -X POST http://infinite-creative:8545 \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":2}'
```

Si se devuelve JSON como `{"result":"0x...","id":2,"jsonrpc":"2.0"}`, es correcto. El RPC no es accesible desde internet; solo Blockscout puede conectarse a `infinite-creative:8545` a través de la red **creative**.

---

## 🚀 Instrucciones de configuración del servicio Scan

### 1️⃣ Crear directorios en `drive/services`

```bash
mkdir -p ~/drive/services/scan2-infinite-creative 
mkdir -p /home/ubuntu/drive/services/scan2-infinite-creative/{db,stats-db,redis,logs,dets}
sudo chown -R ubuntu:ubuntu /home/ubuntu/drive/services/scan2-infinite-creative/{db,stats-db,redis,logs,dets}
sudo chown -R 2000:2000 ~/drive/services/scan2-infinite-creative/db 
sudo chown -R 2000:2000 ~/drive/services/scan2-infinite-creative/stats-db 
sudo chmod 700 ~/drive/services/scan2-infinite-creative/db 
sudo chmod 700 ~/drive/services/scan2-infinite-creative/stats-db
```

### 2️⃣ Crear el archivo `docker-compose.override.yml`

Configuración equivalente a la versión en inglés: backend, frontend, db, stats-db, redis-db, stats, visualizer, sig-provider, proxy; variables de entorno para CHAIN_ID, NETWORK, SUBNETWORK, COIN, hosts de API/stats/visualizer, APP_HOST. Desactivar nft_media_handler y user-ops-indexer.

Sustituye las claves de dominio (NEXT_PUBLIC_APP_HOST, NEXT_PUBLIC_API_HOST, NEXT_PUBLIC_STATS_API_HOST, NEXT_PUBLIC_VISUALIZE_API_HOST, APP_HOST) por tu dominio.

### 3️⃣ Crear el archivo `ports.env`

```bash
nano ports.env
```

```bash
APP_HOST=creative-scan.infinitedrive.xyz
POSTGRES_PUBLISHED_PORT=7452
STATS_DB_PUBLISHED_PORT=7453
PROXY_HTTP_PORT=83
PROXY_8080_PORT=8100
PROXY_8081_PORT=8101
```

### 4️⃣ Arrancar Blockscout
```bash
docker compose --env-file ~/drive/services/scan2-infinite-creative/ports.env \
  -p scan2-infinite-creative \
  -f ~/blockscout/docker-compose/docker-compose.yml \
  -f ~/drive/services/scan2-infinite-creative/docker-compose.override.yml \
  up -d
```

La indexación comenzará en unos minutos; la interfaz web estará disponible en `http://<IP del servidor>:83`.

---

## 🔍 Comandos de comprobación de estado

- Estado del contenedor y logs: `docker compose ... ps`, `down`, `logs -f backend`
- Comunicación con el backend: `curl -s http://localhost:83/api/v2/config/backend-version`
- Red creative: `docker network ls | grep creative`, `docker network inspect creative`
- Comunicación backend ↔ infinite-creative: ejecutar `curl` hacia `http://infinite-creative:8545` desde el contenedor backend
- Estado de importación en DB: `curl -s http://127.0.0.1:83/api/v2/main-page/indexing-status`, consultas a la base de datos
- Configuración del proxy: `docker exec -it scan2-infinite-creative-proxy-1 ...`

---

## 🚀 Configuración de Cloudflare y Nginx del host

**Requisito: añadir el dominio** en Cloudflare.

### Emitir certificado y colocarlo en el host (p. ej. Cloudflare Origin Cert)

1) Crear certificado de origen en Cloudflare (SSL/TLS → Origin Server → Create Certificate). Guardar certificado (pem) y clave privada (pem).
2) Colocar en el host: `/etc/nginx/ssl/creative-scan.origin.crt` y `creative-scan.origin.key`, `chmod 600` en la clave.

### Configuración del host (servidor o VPS)

1) Abrir puertos 80 y 443 en UFW.
2) Crear `/etc/nginx/conf.d/creative-scan.conf` con server HTTP→HTTPS y server HTTPS que haga proxy a `http://127.0.0.1:83`.
3) Cloudflare SSL/TLS: modo Full (strict); WebSockets: ON.
4) Verificación local y vía Cloudflare con `curl` y desde el navegador.

Para los bloques completos de YAML y nginx, consulta la [versión en inglés](/en/drive/services/blockchain-scanner/scan2-infinite-creative/) del mismo documento.
