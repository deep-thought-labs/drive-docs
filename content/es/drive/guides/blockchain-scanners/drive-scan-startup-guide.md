---
title: Guía de arranque de Drive Scan
---
## Drive-Scan

Drive-Scan es un repositorio de configuración optimizado para el funcionamiento eficiente de **Blockscout**, un explorador de blockchain basado en EVM, en el entorno Drive.

[Este repositorio](https://github.com/deep-thought-labs/drive-scan) está basado en el proyecto de código abierto Blockscout, y su configuración y ajustes han sido adaptados y ampliados para la infraestructura Drive. 
La implementación de Blockscout en sí se basa en el proyecto oficial, y el repositorio drive-scan proporciona principalmente:

- Configuración Docker/docker-compose para un entorno Drive

- Plantilla de configuración para ejecutar varios escáneres en paralelo

- Ejemplo de integración de configuración Nginx/dominio

- Archivos de configuración e instrucciones modificados y añadidos para Drive


Los detalles de los cambios y la configuración adicional se indican claramente en la [documentación](../drive-scan-settings-details).

Los usuarios pueden alojar rápidamente varios escáneres de blockchain con un mínimo de variables de entorno y configuración de dominio.

---

## Requisitos previos

Para usar este repositorio necesitas:

- Docker y Docker Compose instalados. [Guía de inicio rápido](https://docs.infinitedrive.xyz/es/drive/quick-start/installation/)

- Los puertos necesarios para el funcionamiento del nodo blockchain deben estar abiertos.

- Debe obtenerse un dominio para el escáner.

## Paso 1: Clonar el repositorio

```bash
git clone https://github.com/deep-thought-labs/drive-scan.git

cd drive-scan
```

## Paso 2: Configurar el nodo y el escáner

<details>
<summary><strong>Instrucciones de configuración del escáner Mainnet</strong></summary>

### **Crear una red compartida de Docker**

Esta sección explica el procedimiento para conectar nodos y Blockscout solo entre contenedores Docker (sin exponer el host).

> Los RPC no se exponen al host, por lo que no son accesibles desde el exterior. Solo Blockscout puede alcanzarlos mediante la red dedicada de Docker.

1. Crear una red Docker
2. Editar el `app.toml` creado tras inicializar cada nodo

```bash
docker network create mainnet || true
```

---

### **Editar el `app.toml` del nodo**

Tras inicializar el nodo blockchain, edita la sección `[json-rpc]` y la configuración de pruning en `app.toml`.

- `~/drive-scan/drive/services/node0-infinite/persistent-data/config/app.toml`
```toml
### Base Configuration ###
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

Tras editar el archivo toml, reinicia el contenedor del servicio y el nodo blockchain.

**Reiniciar contenedor**
```bash
./drive.sh down

./drive.sh up -d

# ⚠️ Tras reiniciar el contenedor, reinicia el nodo desde la GUI.
./drive.sh node-ui
```


3️⃣ **Comprobación de funcionamiento (desde el lado de la red Docker)**

Comprueba si puedes acceder a la información de bloques desde la red Docker que acabas de configurar.

```bash
# Resolución de nombres + respuesta HTTP JSON-RPC (timeout 5 s, verbose)
docker run --rm --network mainnet curlimages/curl:8.11.1 \
-v --max-time 5 -H 'Content-Type: application/json' \
-X POST http://infinite:8545 \
-d '{"jsonrpc":"2.0","method":"web3_clientVersion","params":[],"id":1}'

# Obtener altura del bloque
docker run --rm --network mainnet curlimages/curl:8.11.1 \
-s -H 'Content-Type: application/json' \
-X POST http://infinite:8545 \
-d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":2}'
```

Es correcto si se devuelve JSON como `{"result":"0x...","id":2,"jsonrpc":"2.0"}`.

> Ahora **el RPC no es accesible desde internet; solo Blockscout puede conectarse directamente a `infinite:8545` a través de la red.**


---

### Cambiar permisos del directorio blockscout

Cambia los permisos del directorio de base de datos de blockscout para evitar errores de permisos.

```bash
# Crear directorios para blockscout
sudo mkdir -p /home/ubuntu/drive-scan/drive/services/scan0-infinite/{db,stats-db,redis,logs,dets}

# Otorgar permiso de escritura
sudo chown -R ubuntu:ubuntu /home/ubuntu/drive-scan/drive/services/scan0-infinite/{db,stats-db,redis,logs,dets}

# Establecer propietario 2000:2000
sudo chown -R 2000:2000 ~/drive-scan//drive/services/scan0-infinite/db 
sudo chown -R 2000:2000 ~/drive-scan/drive/services/scan0-infinite/stats-db 
sudo chmod 700 ~/drive-scan/drive/services/scan0-infinite/db 
sudo chmod 700 ~/drive-scan/drive/services/scan0-infinite/stats-db
```

---

### Editar `docker-compose.override.yml` y `ports.env` del servicio scan

Edita las secciones frontend > environment y proxy > environment del archivo override.yml para incluir los dominios que uses realmente.

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
      # Configura el dominio que uses realmente
      APP_HOST: "xxx-scan.infinitedrive.xyz"
```


- Editar `ports.env`
```bash
nano ~/drive-scan/drive/services/scan0-infinite/ports.env
```

Sustituye el valor `APP_HOST` `xxxx-scan.infinitedrive.xyz` por el dominio real que quieras usar.
```
# Sustituye aquí por tu dominio real
APP_HOST=xxxx-scan.infinitedrive.xyz
```
</details>

<details>
<summary><strong>Instrucciones de configuración del escáner Testnet</strong></summary>

### **Crear una red compartida de Docker**

Esta sección explica el procedimiento para conectar nodos y Blockscout solo entre contenedores Docker (sin exponer el host).

> Los RPC no se exponen al host, por lo que no son accesibles desde el exterior. Solo Blockscout puede alcanzarlos mediante la red dedicada de Docker.

1. Crear una red Docker
2. Editar el `app.toml` creado tras inicializar cada nodo

```bash
docker network create testnet || true
```


---

### **Editar el `app.toml` del nodo**

Tras inicializar el nodo blockchain, edita la sección `[json-rpc]` y la configuración de pruning en `app.toml`.

- `~/drive-scan/drive/services/node1-infinite-testnet/persistent-data/config/app.toml`
```toml
### Base Configuration ###
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

Tras editar el archivo toml, reinicia el contenedor del servicio y el nodo blockchain.

**Reiniciar contenedor**
```bash
./drive.sh down

./drive.sh up -d

# ⚠️ Tras reiniciar el contenedor, reinicia el nodo desde la GUI.
./drive.sh node-ui
```


3️⃣ **Comprobación de funcionamiento (desde el lado de la red Docker)**


```bash
# Resolución de nombres + respuesta HTTP JSON-RPC (timeout 5 s, verbose)
docker run --rm --network testnet curlimages/curl:8.11.1 \
-v --max-time 5 -H 'Content-Type: application/json' \
-X POST http://infinite-testnet:8545 \
-d '{"jsonrpc":"2.0","method":"web3_clientVersion","params":[],"id":1}'

# Obtener altura del bloque
docker run --rm --network testnet curlimages/curl:8.11.1 \
-s -H 'Content-Type: application/json' \
-X POST http://infinite-testnet:8545 \
-d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":2}'
```

Es correcto si se devuelve JSON como `{"result":"0x...","id":2,"jsonrpc":"2.0"}`.

> Ahora **el RPC no es accesible desde internet; solo Blockscout puede conectarse directamente a `infinite-testnet:8545` a través de la red.**

---

### Cambiar permisos del directorio blockscout

Cambia los permisos del directorio de base de datos de blockscout para evitar errores de permisos.

```bash
# Crear directorios para blockscout
sudo mkdir -p /home/ubuntu/drive-scan/drive/services/scan1-infinite-testnet/{db,stats-db,redis,logs,dets}

# Otorgar permiso de escritura
sudo chown -R ubuntu:ubuntu /home/ubuntu/drive-scan/drive/services/scan1-infinite-testnet/{db,stats-db,redis,logs,dets}

# Establecer propietario 2000:2000
sudo chown -R 2000:2000 ~/drive-scan//drive/services/scan1-infinite-testnet/db 
sudo chown -R 2000:2000 ~/drive-scan/drive/services/scan1-infinite-testnet/stats-db 
sudo chmod 700 ~/drive-scan/drive/services/scan1-infinite-testnet/db 
sudo chmod 700 ~/drive-scan/drive/services/scan1-infinite-testnet/stats-db
```

---

### Editar `docker-compose.override.yml` y `ports.env` del servicio scan

Edita las secciones frontend > environment y proxy > environment del archivo override.yml para incluir los dominios que uses realmente.

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
      # Configura el dominio que uses realmente
      APP_HOST: "xxx-scan.infinitedrive.xyz"
```


- Editar `ports.env`
```bash
nano ~/drive-scan/drive/services/scan1-infinite-testnet/ports.env
```

Sustituye el valor `APP_HOST` `xxxx-scan.infinitedrive.xyz` por el dominio real que quieras usar.
```
# Sustituye aquí por tu dominio real
APP_HOST=xxxx-scan.infinitedrive.xyz
```
</details>

<details>
<summary><strong>Instrucciones de configuración del escáner Creative</strong></summary>


## **Crear una red compartida de Docker**

Esta sección explica el procedimiento para conectar nodos y Blockscout solo entre contenedores Docker (sin exponer el host).

> Los RPC no se exponen al host, por lo que no son accesibles desde el exterior. Solo Blockscout puede alcanzarlos mediante la red dedicada de Docker.

1. Crear una red Docker
2. Editar el `app.toml` creado tras inicializar cada nodo

```bash
docker network create creative || true
```

---

### **Editar el `app.toml` del nodo**

Tras inicializar el nodo blockchain, edita la sección `[json-rpc]` y la configuración de pruning en `app.toml`.

- `~/drive-scan/drive/services/node2-infinite-creative/persistent-data/config/app.toml`

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


Tras editar el archivo toml, reinicia el contenedor del servicio y el nodo blockchain.

**Reiniciar contenedor**
```bash
./drive.sh down

./drive.sh up -d

# ⚠️ Tras reiniciar el contenedor, reinicia el nodo desde la GUI.
./drive.sh node-ui
```


3️⃣ **Comprobación de funcionamiento (desde el lado de la red Docker)**

Comprueba si puedes acceder a la información de bloques desde la red Docker que acabas de configurar.

```bash
# Resolución de nombres + respuesta HTTP JSON-RPC (timeout 5 s, verbose)
docker run --rm --network creative curlimages/curl:8.11.1 \
-v --max-time 5 -H 'Content-Type: application/json' \
-X POST http://infinite-creative:8545 \
-d '{"jsonrpc":"2.0","method":"web3_clientVersion","params":[],"id":1}'

# Obtener altura del bloque
docker run --rm --network testnet curlimages/curl:8.11.1 \
-s -H 'Content-Type: application/json' \
-X POST http://infinite-creative:8545 \
-d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":2}'
```

Es correcto si se devuelve JSON como `{"result":"0x...","id":2,"jsonrpc":"2.0"}`.

> Ahora el RPC no es accesible desde internet; solo Blockscout puede conectarse directamente a `infinite-creative:8545` a través de la red.

---

## Cambiar permisos del directorio blockscout

Cambia los permisos del directorio de base de datos de blockscout para que funcione correctamente.

```bash
# Crear directorios para blockscout
sudo mkdir -p /home/ubuntu/drive-scan/drive/services/scan2-infinite-creative/{db,stats-db,redis,logs,dets}

# Otorgar permiso de escritura
sudo chown -R ubuntu:ubuntu /home/ubuntu/drive-scan/drive/services/scan2-infinite-creative/{db,stats-db,redis,logs,dets}

# Establecer propietario 2000:2000
sudo chown -R 2000:2000 ~/drive-scan//drive/services/scan2-infinite-creative/db 
sudo chown -R 2000:2000 ~/drive-scan/drive/services/scan2-infinite-creative/stats-db 
sudo chmod 700 ~/drive-scan/drive/services/scan2-infinite-creative/db 
sudo chmod 700 ~/drive-scan/drive/services/scan2-infinite-creative/stats-db
```

---

### Editar `docker-compose.override.yml` y `ports.env` del servicio scan

Edita las secciones frontend > environment y proxy > environment del archivo override.yml para incluir los dominios que uses realmente.

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
      # Configura el dominio que uses realmente
      APP_HOST: "xxx-scan.infinitedrive.xyz"
```


- Editar `ports.env`
```bash
nano ~/drive-scan/drive/services/scan2-infinite-creative/ports.env
```

Sustituye el valor `APP_HOST` `xxxx-scan.infinitedrive.xyz` por el dominio real que vayas a usar.
```
# Sustituye aquí por tu dominio real
APP_HOST=xxxx-scan.infinitedrive.xyz
```

</details>

<details>
<summary><strong>Nota: Cómo obtener un certificado CloudFlare</strong></summary>

### Emisión e implementación del certificado (p. ej. Cloudflare Origin Cert)

1️⃣ **Crear un certificado de origen Cloudflare (panel de Cloudflare)**

Cloudflare Dashboard → Tu dominio → **SSL/TLS** → **Origin Server** → **Create Certificate**

- Hostnames: `xxxx-scan.tudominio.ejemplo` (o `*.tudominio.ejemplo` si es necesario)

- Tipo de clave: RSA 2048

- Validez: Según prefieras (puede ser larga)


Guarda los dos elementos emitidos:

- **Certificado de origen (pem)**
    
- **Clave privada (pem)**  

</details>

## Paso 3: Colocar certificados y archivos vhost

1️⃣ **Instalar nginx**

```bash
sudo apt update
sudo apt install -y nginx
sudo systemctl enable --now nginx

# Comprobar que la instalación fue correcta
sudo systemctl status nginx --no-pager
```


2️⃣ **Crear directorio para los certificados y pegar el contenido**

Obtén el certificado desde Let's encrypt o el panel de Cloudflare.

```bash
# crear directorio si no existe
sudo mkdir -p /etc/nginx/{ssl,conf.d}
# copiar el directorio nginx
sudo cp -ri ~/drive-scan/nginx/* /etc/nginx/
# Pegar el contenido del certificado de origen emitido por Cloudflare.
sudo nano /etc/nginx/ssl/example.origin.crt
# Pegar el contenido de la clave privada emitida por Cloudflare.
sudo nano /etc/nginx/ssl/example.origin.key
# Otorgar permisos.
sudo chmod 600 /etc/nginx/ssl/example.origin.key
```


3️⃣ **Editar el archivo `.conf` e introducir el nombre de dominio real que quieras usar**

Sustituye el valor `server_name` en el archivo `.conf` por el dominio real (hay dos sitios).

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
> Elimina los archivos de escáneres que no vayas a alojar; los archivos innecesarios provocarán errores al ejecutar `nginx -t` en el siguiente paso.


```bash
# ej.) al eliminar creative-scan.conf
sudo rm /etc/nginx/conf.d/creative-scan.conf
```

Tras editar o eliminar el archivo anterior, prueba y recarga nginx:
```bash
sudo nginx -t
sudo systemctl reload nginx
```

Salida esperada:
```txt
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```


**4️⃣ Abrir puertos 80 y 443 en UFW de Ubuntu (o Firewall)**

**Comprobar el estado actual de UFW:**
```bash
sudo ufw status
```

Si los puertos 80 y 443 no están abiertos, haz lo siguiente:

**Permitir puertos 80 y 443 (requerido)**
```bash
sudo ufw allow 80/tcp 
sudo ufw allow 443/tcp

# Aplicar
sudo ufw reload
```

**Comprobar si el puerto 80 está libre:**
```bash
# Verificar que el puerto 80 está libre (solo la primera vez)
sudo ss -lntp | egrep ':(80)\b' || echo "OK: 80 está libre"

# O verificar que nginx está escuchando en 80 y 443.
sudo ss -lntp | egrep ':(80|443)\b' || true sudo systemctl status nginx --no-pager
```

---

## Paso 4: **Arrancar Blockscout**


```bash
# escáner mainnet
docker compose --env-file ~/drive-scan/drive/services/scan0-infinite/ports.env \
  -p scan0-infinite \
  -f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
  -f ~/drive-scan/drive/services/scan0-infinite/docker-compose.override.yml \
  up -d


# escáner testnet
docker compose --env-file ~/drive-scan/drive/services/scan1-infinite-testnet/ports.env \
  -p scan1-infinite-testnet \
  -f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
  -f ~/drive-scan/drive/services/scan1-infinite-testnet/docker-compose.override.yml \
  up -d


# escáner creative
docker compose --env-file ~/drive-scan/drive/services/scan2-infinite-creative/ports.env \
  -p scan2-infinite-creative \
  -f ~/drive-scan/Blockscout/docker-compose/docker-compose.yml \
  -f ~/drive-scan/drive/services/scan2-infinite-creative/docker-compose.override.yml \
  up -d  
```


> Ejecuta el comando de arranque indicando las rutas de `project name`, `docker-compose.yml`, `docker-compose.override.yml` y `ports.env`.
> La indexación comenzará en unos minutos o algo más, y la interfaz web se mostrará al acceder a `https://xxxx-scan.tudominio.ejemplo`.

Si la página no se muestra correctamente tras unos minutos o incluso decenas de minutos, usa los [comandos de comprobación de estado](../status-check-commands-for-scanners) siguientes para localizar el problema.
