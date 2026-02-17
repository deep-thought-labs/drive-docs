---
title: "Guía de configuración de servidores RPC"
---

# Paso A: Exponer los puertos RPC en localhost

Recomendamos cambiar primero los puertos en `drive/services/node0-infinite/docker-compose.yml` como se indica a continuación:

## ✅ Ejemplo de configuración (limitar la exposición RPC a localhost, WS opcional)

```yaml
ports:
# P2P
- "26656:26656"
# CometBFT RPC HTTP (solo localhost)
- "127.0.0.1:26657:26657"
# GRPC HTTP (solo localhost)
- "127.0.0.1:9090:9090"
# EVM JSON-RPC HTTP (solo localhost)
- "127.0.0.1:8545:8545"
# WebSocket (si se usa, solo localhost)
# - "127.0.0.1:8546:8546"
```

**P. ¿Por qué limitar la exposición de los puertos RPC a localhost?**

- Puertos como `8545/8546 (EVM JSON RPC)` y `26657 (COMET RPC)` no deben exponerse directamente al exterior, sino ser accesibles solo desde Nginx en el host. Así se reduce el riesgo de ataques DoS externos.

- Las peticiones se aceptan con el flujo: "Nginx (443) → 127.0.0.1:8545 (localhost) → contenedor Docker:8545", concentrando el límite de seguridad en Nginx.

**Esquema:**
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

> Nota: El puerto P2P (26656) se hace público para contribuir a la red y mantener conexiones estables.

---
# Paso A: app.toml (habilitar JSON-RPC)

Archivo: 
`drive/services/node0-infinite/persistent-data/config/app.toml`

Cambia lo siguiente:
```toml
[json-rpc]
enable = true
address = "0.0.0.0:8545"
ws-address = "0.0.0.0:8546"
allow-insecure-unlock = false

# Opcional (si quieres exponer Grpc, configura lo siguiente.)
[grpc]
enable = true
address = "0.0.0.0:9090"
```

## Paso B: config.toml (habilitar COMET-RPC)

Archivo: 
`drive/services/node0-infinite/persistent-data/config/config.toml`

Cambia lo siguiente:
```toml
[rpc]
laddr = "tcp://0.0.0.0:26657"
```

**P. ¿Por qué enlazar a 0.0.0.0?**

Si dejas el puerto `127.0.0.1:8545` en el contenedor, el reenvío de puertos de Docker no permitirá alcanzarlo desde fuera del contenedor (localhost). La exposición externa se limita a localhost en el lado de los puertos de Docker, así que dentro del contenedor configura el puerto en `0.0.0.0`.


**Aplicar y reiniciar el nodo:**
```bash
./drive.sh down
./drive.sh up -d

# Tras reiniciar el contenedor, reinicia el nodo desde la GUI.
./drive.sh node-ui
```


# Paso 3: Configuración de Nginx

## 3-A) Límites de tasa y conexiones simultáneas (opcional pero recomendado)

Archivo: `/etc/nginx/conf.d/00_rpc_limits.conf`

```
# ==========================
# Límites EVM RPC
# ==========================
limit_req_zone  $binary_remote_addr zone=rpc_req:10m rate=10r/s;
limit_conn_zone $binary_remote_addr zone=rpc_conn:10m;

# ==========================
# Límites Comet (Tendermint) RPC
# ==========================
limit_req_zone  $binary_remote_addr zone=comet_req:10m rate=20r/s;
limit_conn_zone $binary_remote_addr zone=comet_conn:10m;

# ==========================
# WebSocket (Tendermint: opcional)
# ==========================
limit_conn_zone $binary_remote_addr zone=comet_ws_conn:10m;
```

> Los límites de tasa y de conexiones simultáneas en los endpoints RPC públicos son medidas básicas para mantener la estabilidad y disponibilidad del servicio, evitar sobrecarga del nodo y ataques DoS, y no agotar CPU, memoria e I/O. Así se evita que usuarios o bots monopolicen recursos y se ofrece un entorno RPC estable para usuarios y relayers.

## 3-B) vhost nginx

### Configuración EVM-RPC

Archivo: `/etc/nginx/conf.d/evm-rpc.conf`

```
server {
  listen 80;
  listen [::]:80;
  # Usa aquí tu dominio
  server_name evm-rpc.infinitedrive.xyz;
  return 301 https://$host$request_uri;
}

server {
  listen 443 ssl http2;
  listen [::]:443 ssl http2;  

  # Usa aquí tu dominio
  server_name evm-rpc.infinitedrive.xyz;
  # ---- Cabeceras de seguridad ----
  add_header X-Content-Type-Options "nosniff" always;
  add_header Referrer-Policy "no-referrer" always;
  add_header X-Frame-Options "DENY" always;
  add_header Permissions-Policy "interest-cohort=()" always;
  # Opcional: HSTS (solo si mantendrás HTTPS de forma permanente)
  # add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

  # Coloca un certificado y clave válidos
  ssl_certificate     /etc/nginx/ssl/infinitedrive.xyz.crt;
  ssl_certificate_key /etc/nginx/ssl/infinitedrive.xyz.key;

  client_max_body_size 1m;
    location / {
    # ---- CORS (necesario para wallets en navegador como MetaMask) ----
    add_header Access-Control-Allow-Origin "*" always;
    add_header Access-Control-Allow-Methods "POST, OPTIONS" always;
    add_header Access-Control-Allow-Headers "Content-Type, Authorization" always;
    add_header Access-Control-Max-Age 86400 always;

    # Respuesta rápida para preflight CORS
    if ($request_method = OPTIONS) {
      add_header Content-Length 0;
      add_header Content-Type text/plain;
      return 204;
    }

    # ---- Protección básica contra abuso ----
    limit_req zone=rpc_req burst=30 nodelay;
    limit_conn rpc_conn 20;
    
    # ---- Proxy inverso al EVM JSON-RPC ----
    proxy_pass http://127.0.0.1:8545;
    proxy_http_version 1.1;

    # Estabilidad keepalive / upstream
    proxy_set_header Connection "";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  
    proxy_connect_timeout 10s;
    proxy_send_timeout 30s;
    proxy_read_timeout 30s;

    # Si hay errores upstream, no cachear ni servir contenido obsoleto
    proxy_intercept_errors off;
  }
}
```

### Configuración Comet-rpc

- `/etc/nginx/conf.d/comet-rpc.conf`
```
server {
  listen 80;
  listen [::]:80;
  # Usa aquí tu dominio
  server_name comet-rpc.infinitedrive.xyz;
  return 301 https://$host$request_uri;
}

# 2) HTTPS -> Tendermint RPC (localhost:26657)
server {
  listen 443 ssl http2;
  listen [::]:443 ssl http2;
  
  # Usa aquí tu dominio
  server_name comet-rpc.infinitedrive.xyz;
  
  # Coloca certificado y clave válidos
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

  # Endpoint WebSocket Tendermint (requerido por algunos relayers / suscripciones)
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

### Configuración Grpc

Archivo: `/etc/nginx/conf.d/grpc.conf`

```nginx
server {
  listen 443 ssl http2;
  listen [::]:443 ssl http2;

  # Usa aquí tu dominio
  server_name grpc.infinitedrive.xyz;

  # Coloca certificado y clave válidos
  ssl_certificate     /etc/nginx/ssl/infinitedrive.xyz.crt;
  ssl_certificate_key /etc/nginx/ssl/infinitedrive.xyz.key;

  # gRPC al nodo local
  location / {
    grpc_pass grpc://127.0.0.1:9090;

    # opcional pero útil
    grpc_set_header Host $host;
    grpc_set_header X-Real-IP $remote_addr;
    grpc_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

    # gRPC puede ser de larga duración
    grpc_read_timeout 300s;
    grpc_send_timeout 300s;
  }
}
```


Instalación de nginx (solo la primera vez)
```bash
sudo apt update
sudo apt install -y nginx
sudo systemctl enable --now nginx
sudo systemctl status nginx --no-pager
```

Aplicar la configuración:
```bash
# Comprobar que el resultado del test sea `success`
sudo nginx -t
# Aplicar la configuración
sudo systemctl reload nginx
```

---

# Paso 4: Comprobar el funcionamiento

**4-A) Comprobar desde localhost sin Nginx:**
```bash
# (EVM) Obtener último bloque
curl -s -H 'Content-Type: application/json' \
-d '{"jsonrpc":"2.0","id":1,"method":"eth_blockNumber","params":[]}' \
http://127.0.0.1:8545

# (EVM) Estado de sincronización
curl -s -H 'Content-Type: application/json' \
-d '{"jsonrpc":"2.0","id":1,"method":"eth_syncing","params":[]}' \
http://127.0.0.1:8545

# Estado de sincronización Tendermint
curl -s http://127.0.0.1:26657/status | head
```


**4-B) Comprobar vía Nginx:**
```bash
# (EVM) Obtener último bloque
curl -sk -H 'Content-Type: application/json' \
-d '{"jsonrpc":"2.0","id":1,"method":"eth_blockNumber","params":[]}' \
https://tu-evm-rpc.ejemplo.com

# Estado de sincronización (EVM)
curl -sk -H 'Content-Type: application/json' \
-d '{"jsonrpc":"2.0","id":1,"method":"eth_syncing","params":[]}' \
https://tu-evm-rpc.ejemplo.com

# Estado de sincronización Tendermint
curl -sk https://tu-comet-rpc.ejemplo.com/status | head
```

### Comprobar comunicación GRPC:
```bash
grpcurl -insecure tu-grpc.ejemplo.com:443 list | head

grpcurl -insecure tu-grpc.ejemplo.com:443 \
  cosmos.base.tendermint.v1beta1.Service/GetLatestBlock
```

⚠️Nota (proxy Cloudflare y gRPC)

gRPC en streaming a través del "Orange Cloud (Proxy)" de Cloudflare puede estar sujeto a restricciones de configuración y plan.

Medidas de seguridad:

- Usar solo DNS (nube gris) para el subdominio gRPC.
(TLS termina en Nginx y llega directamente por 443.)

- O configurar Cloudflare para que gRPC se reenvíe correctamente.

Cualquiera de las dos opciones es válida.

---
## Paso 4: Verificar con la herramienta de validación de Drive

Usa la herramienta de validación del repositorio drive para comprobar que el servidor RPC funciona correctamente.

```bash
cd drive/tools/validate-evm-rpc-endpoint
./validate-evm-rpc-endpoint.sh https://tu-evm-rpc.ejemplo.com

cd ../validate-cosmos-rpc-endpoint
./validate-cosmos-rpc-endpoint.sh https://tu-comet-rpc.ejemplo.com

cd ../validate-cosmos-grpc-endpoint
./validate-cosmos-grpc-endpoint.sh https://tu-grpc.ejemplo.com
```
