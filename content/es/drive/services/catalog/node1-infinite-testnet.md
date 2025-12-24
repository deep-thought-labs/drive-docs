---
title: "Infinite Testnet (node1-infinite-testnet)"
---

**Número de Servicio:** 1  
**Directorio de Servicio:** `node1-infinite-testnet`  
**Nombre de Servicio/Contenedor:** `infinite-testnet`  
**Red:** Infinite Testnet  
**Tipo:** Blockchain Node

## Descripción

Testnet blockchain node for the Infinite network. All ports have a +10 offset from default ports. This is the test network for development and testing purposes.

---

## Tabla de Contenidos

- [Configuración de Puertos](#port-configuration)
- [Variables de Entorno](#environment-variables)
- [Comandos Esenciales](#essential-commands)
- [Configuración de Docker Compose](#docker-compose-configuration)
- [Configuración de Firewall](#firewall-configuration)
- [Datos Persistentes](#persistent-data)
- [Ver También](#see-also)

---

## Configuración de Puertos

### Referencia Rápida

**Número de Servicio:** 1  
**Desplazamiento de Puerto:** +10

| Tipo de Puerto | Puerto del Host | Puerto del Contenedor |
|-----------|-----------|---------------|
| P2P | 26666 | 26656 |
| RPC | 26667 | 26657 |
| gRPC | 9100 | 9090 |
| gRPC-Web | 9101 | 9091 |
| REST API | 1327 | 1317 |
| JSON-RPC HTTP | 8555 | 8545 |
| JSON-RPC WS | 8556 | 8546 |

### Cálculo de Puertos

{{< expand "Cálculo de Puertos Details" "↕" >}}
Este servicio usa **Número de Servicio 1**, por lo que todos los puertos tienen un desplazamiento de +10:

- **P2P**: 26656 + (1 × 10) = **26666**
- **RPC**: 26657 + (1 × 10) = **26667**
- **gRPC**: 9090 + (1 × 10) = **9100**
- **gRPC-Web**: 9091 + (1 × 10) = **9101**
- **REST API**: 1317 + (1 × 10) = **1327**
- **JSON-RPC HTTP**: 8545 + (1 × 10) = **8555**
- **JSON-RPC WebSocket**: 8546 + (1 × 10) = **8556**

Para descripciones detalladas de cada tipo de puerto, consulta [Referencia de Puertos: Nodos Blockchain]({{< relref "../ports/blockchain-nodes" >}}).
{{< /expand >}}

### Puertos Requeridos

{{< expand "Puertos Requeridos Details" "↕" >}}
Estos puertos deben estar configurados para que el servicio funcione:

| Tipo de Puerto | Puerto del Host | Puerto del Contenedor | Descripción |
|-----------|-----------|---------------|-------------|
| **P2P** | 26666 | 26656 | Comunicación de red peer-to-peer |
| **RPC** | 26667 | 26657 | API RPC de Tendermint |
{{< /expand >}}

### Puertos Opcionales

{{< expand "Puertos Opcionales Details" "↕" >}}
Estos puertos pueden habilitarse si se necesitan para casos de uso específicos:

| Tipo de Puerto | Puerto del Host | Puerto del Contenedor | Descripción | Cuándo Habilitar |
|-----------|-----------|---------------|-------------|----------------|
| **gRPC** | 9100 | 9090 | Consultas gRPC del Cosmos SDK | Endpoint de API pública, conexiones de billetera |
| **gRPC-Web** | 9101 | 9091 | gRPC-Web (navegador) | Aplicaciones web, billeteras de navegador |
| **REST API** | 1327 | 1317 | API REST del Cosmos SDK | Compatibilidad con aplicaciones legacy |
| **JSON-RPC HTTP** | 8555 | 8545 | Ethereum JSON-RPC (HTTP) | MetaMask, herramientas Ethereum, dApps |
| **JSON-RPC WebSocket** | 8556 | 8546 | Ethereum JSON-RPC (WebSocket) | Eventos de blockchain en tiempo real |
| **Prometheus** | 26670 | 26660 | Métricas de Prometheus | Monitoreo de nodos |
| **EVM Metrics** | 6075 | 6065 | Métricas Prometheus de EVM | Monitoreo de rendimiento EVM |
| **Geth Metrics** | 8110 | 8100 | Métricas compatibles con Geth | Herramientas de monitoreo Geth |
{{< /expand >}}

---

## Variables de Entorno

Este servicio usa las siguientes variables de entorno con los valores mostrados a continuación. Para documentación completa de todas las variables de entorno disponibles, consulta [Variables de Entorno: Nodos Blockchain]({{< relref "../environment/blockchain-nodes" >}}).

### Configuración del Binario

Este servicio usa el **binario Infinite predeterminado** (no un binario alternativo). El binario se descarga automáticamente desde las releases de GitHub.

**Nota:** Para servicios que usan binarios alternativos (como QOM), consulta la documentación del servicio respectivo.

### Identificación de Cadena

{{< expand "Variables de Identificación de Cadena" "↕" >}}
Este servicio está configurado con las siguientes variables de identificación de cadena:

**NODE_CHAIN_ID**  
The chain ID for the Infinite testnet network. This uniquely identifies the blockchain network.

```yaml
NODE_CHAIN_ID: "infinite_421018001-1"
```

**NODE_EVM_CHAIN_ID**  
El ID de cadena EVM para protección contra replay compatible con EIP-155.

Esto es independiente del ID de cadena de Cosmos y se usa para transacciones compatibles con Ethereum.

```yaml
NODE_EVM_CHAIN_ID: "421018001"
```

**NODE_GENESIS_URL**  
URL para descargar el archivo genesis oficial durante la inicialización del nodo.

El archivo genesis contiene el estado inicial de la blockchain.

```yaml
NODE_GENESIS_URL: "https://raw.githubusercontent.com/deep-thought-labs/drive/refs/heads/main/services/node1-infinite-testnet/genesis.json"
```
{{< /expand >}}

### Configuración de Red P2P

{{< expand "Variables de Configuración de Red P2P" "↕" >}}
Este servicio usa las siguientes variables de configuración de red P2P:

**NODE_P2P_SEEDS**  
Nodos semilla para descubrimiento P2P. Estos nodos ayudan a tu nodo a descubrir otros pares en la red durante la conexión inicial.

Los nodos semilla se usan para el descubrimiento de red pero no son conexiones persistentes.

```yaml
NODE_P2P_SEEDS: "88ec87026e7b61eceeca0d74cf47a24cea36642b@66.70.178.128:26666"
```

**NODE_PERSISTENT_PEERS**  
Los nodos pares persistentes mantienen conexiones continuas, a diferencia de los nodos semilla que solo se usan para descubrimiento.

Este servicio no tiene un valor preconfigurado para esta variable.

```yaml
# NODE_PERSISTENT_PEERS: ""  # Sin valor preconfigurado para este servicio
```

**NODE_P2P_EXTERNAL_ADDRESS**  
Dirección externa para anunciar a los pares para que se conecten. Se usa cuando el nodo está detrás de NAT o firewall.

Este servicio no tiene un valor preconfigurado para esta variable. Si es necesario, configúralo con la dirección IP pública o el nombre de dominio de tu nodo.

```yaml
# NODE_P2P_EXTERNAL_ADDRESS: ""  # Sin valor preconfigurado para este servicio
```
{{< /expand >}}

---

## Comandos Esenciales

Este servicio es un nodo blockchain, que requiere comandos especializados para la inicialización, inicio, detención y gestión del nodo.

Comandos generales de gestión de contenedores (iniciar, detener, reiniciar, etc.) se describen en la [Gestión de Contenedores]({{< relref "../../guides/general/container-management" >}}) sección.

Para información detallada sobre comandos específicos de nodos blockchain, incluyendo:
- Cómo inicializar un nodo blockchain
- Cómo iniciar y detener nodos
- Operaciones de gestión de claves
- Acceder a la interfaz gráfica

Consulta las [Guías de Nodos Blockchain]({{< relref "../../guides/blockchain-nodes" >}}) sección en la documentación.

---

## Configuración de Docker Compose

{{< expand "Configuración Mínima (Solo Puertos Requeridos)" "↕" >}}
```yaml
services:
  infinite-testnet:
    image: deepthoughtlabs/infinite-drive:dev
    container_name: infinite-testnet
    restart: unless-stopped

    ports:
      - "26666:26656"  # P2P (required)
      - "26667:26657"  # RPC (required)
    
    volumes:
      - ./persistent-data:/home/ubuntu/.infinited

    environment:
      NODE_CHAIN_ID: "infinite_421018001-1"
      NODE_EVM_CHAIN_ID: "421018001"
      NODE_GENESIS_URL: "https://raw.githubusercontent.com/deep-thought-labs/drive/refs/heads/main/services/node1-infinite-testnet/genesis.json"
      NODE_P2P_SEEDS: "88ec87026e7b61eceeca0d74cf47a24cea36642b@66.70.178.128:26666"
```
{{< /expand >}}

{{< expand "Configuración Completa (Todos los Puertos)" "↕" >}}
```yaml
services:
  infinite-testnet:
    image: deepthoughtlabs/infinite-drive:dev
    container_name: infinite-testnet
    restart: unless-stopped

    ports:
      # Puertos requeridos
      - "26666:26656"  # P2P
      - "26667:26657"  # RPC
      
      # Puertos opcionales (descomenta si es necesario)
      - "9100:9090"    # gRPC
      - "9101:9091"    # gRPC-Web
      - "1327:1317"    # REST API
      - "8555:8545"    # JSON-RPC HTTP
      - "8556:8546"    # JSON-RPC WebSocket
      - "26670:26660"  # Prometheus
      - "6075:6065"    # EVM Metrics
      - "8110:8100"    # Geth Metrics
    
    volumes:
      - ./persistent-data:/home/ubuntu/.infinited

    environment:
      NODE_CHAIN_ID: "infinite_421018001-1"
      NODE_EVM_CHAIN_ID: "421018001"
      NODE_GENESIS_URL: "https://raw.githubusercontent.com/deep-thought-labs/drive/refs/heads/main/services/node1-infinite-testnet/genesis.json"
      NODE_P2P_SEEDS: "88ec87026e7b61eceeca0d74cf47a24cea36642b@66.70.178.128:26666"
      # NODE_PERSISTENT_PEERS: ""
      # NODE_P2P_EXTERNAL_ADDRESS: ""
```
{{< /expand >}}

---

## Configuración de Firewall

**⚠️ Crítico:** Antes de configurar cualquier regla de firewall para este servicio, debes permitir primero SSH (puerto 22) en tu sistema. Si te estás conectando a un servidor remoto vía SSH y habilitas el firewall sin permitir SSH primero, perderás el acceso a tu servidor.

El proceso completo de configuración de firewall, incluyendo cómo verificar y permitir SSH (puerto 22), se describe en detalle en la [Configuración de Firewall Guide]({{< relref "../ports/firewall-configuration" >}}). Los comandos mostrados a continuación are specific to this service with the correct port numbers for Infinite Testnet, but please review the guide for the complete setup process.

### Puertos Requeridos

{{< tabs "firewall-required" >}}
{{< tab "Ubuntu/Linux" >}}
```bash
# Puerto P2P (requerido para validadores y conexiones peer)
sudo ufw allow 26666/tcp

# Puerto RPC (opcional, solo si expones la API RPC)
sudo ufw allow 26667/tcp
```
{{< /tab >}}
{{< tab "macOS" >}}
**Recommended:** macOS typically allows incoming connections by default, so you may not need to configure anything. However, we recommend verifying your firewall settings.

**First Option - System Preferences (Recommended):**
Use the built-in graphical interface to configure firewall rules:
1. Open **System Preferences** (or **System Settings** on newer macOS versions)
2. Go to **Security & Privacy** > **Firewall**
3. Click the lock icon and enter your password to make changes
4. Click **Firewall Options...**
5. Add rules to permitir conexiones entrantes for the required ports (26666, 26667)

**Second Option - Command Line (Advanced):**
If you prefer command-line configuration, you can modify `/etc/pf.conf`:

```bash
# Edit /etc/pf.conf and add rules:
# pass in proto tcp from any to any port 26666  # P2P port
# pass in proto tcp from any to any port 26667  # RPC port

# Then reload the firewall:
sudo pfctl -f /etc/pf.conf
```
{{< /tab >}}
{{< tab "Windows" >}}
```powershell
# Puerto P2P (requerido para validadores y conexiones peer)
New-NetFirewallRule -DisplayName "Drive P2P" -Direction Inbound -LocalPort 26666 -Protocol TCP -Action Allow

# Puerto RPC (opcional, solo si expones la API RPC)
New-NetFirewallRule -DisplayName "Drive RPC" -Direction Inbound -LocalPort 26667 -Protocol TCP -Action Allow
```
{{< /tab >}}
{{< /tabs >}}

### Puertos Opcionales

{{< tabs "firewall-optional" >}}
{{< tab "Ubuntu/Linux" >}}
```bash
# gRPC (if exposing gRPC API)
sudo ufw allow 9100/tcp

# gRPC-Web (if exposing gRPC-Web API)
sudo ufw allow 9101/tcp

# REST API (if exposing REST API)
sudo ufw allow 1327/tcp

# JSON-RPC HTTP (if exposing Ethereum-compatible API)
sudo ufw allow 8555/tcp

# JSON-RPC WebSocket (if exposing WebSocket API)
sudo ufw allow 8556/tcp

# Prometheus (if exposing metrics)
sudo ufw allow 26670/tcp

# EVM Metrics (if exposing EVM metrics)
sudo ufw allow 6075/tcp

# Geth Metrics (if exposing Geth metrics)
sudo ufw allow 8110/tcp
```

**Note:** The `/tcp` protocol specification is optional in UFW. You can use either `sudo ufw allow 26666/tcp` or `sudo ufw allow 26666` - both work the same way.
{{< /tab >}}
{{< tab "macOS" >}}
**Recommended:** macOS typically allows incoming connections by default, so you may not need to configure anything. However, we recommend verifying your firewall settings.

**First Option - System Preferences (Recommended):**
Use the built-in graphical interface to configure firewall rules:
1. Open **System Preferences** (or **System Settings** on newer macOS versions)
2. Go to **Security & Privacy** > **Firewall**
3. Click the lock icon and enter your password to make changes
4. Click **Firewall Options...**
5. Add rules to permitir conexiones entrantes for the optional ports you want to expose (9100, 9101, 1327, 8555, 8556, 26670, 6075, 8110)

**Second Option - Command Line (Advanced):**
If you prefer command-line configuration, you can modify `/etc/pf.conf`:

```bash
# Edit /etc/pf.conf and add rules for each port you want to expose:
# pass in proto tcp from any to any port 9100  # gRPC
# pass in proto tcp from any to any port 9101  # gRPC-Web
# pass in proto tcp from any to any port 1327  # REST API
# pass in proto tcp from any to any port 8555  # JSON-RPC HTTP
# pass in proto tcp from any to any port 8556  # JSON-RPC WebSocket
# pass in proto tcp from any to any port 26670 # Prometheus
# pass in proto tcp from any to any port 6075  # EVM Metrics
# pass in proto tcp from any to any port 8110  # Geth Metrics

# Then reload the firewall:
sudo pfctl -f /etc/pf.conf
```
{{< /tab >}}
{{< tab "Windows" >}}
```powershell
# gRPC (if exposing gRPC API)
New-NetFirewallRule -DisplayName "Drive gRPC" -Direction Inbound -LocalPort 9100 -Protocol TCP -Action Allow

# gRPC-Web (if exposing gRPC-Web API)
New-NetFirewallRule -DisplayName "Drive gRPC-Web" -Direction Inbound -LocalPort 9101 -Protocol TCP -Action Allow

# REST API (if exposing REST API)
New-NetFirewallRule -DisplayName "Drive REST API" -Direction Inbound -LocalPort 1327 -Protocol TCP -Action Allow

# JSON-RPC HTTP (if exposing Ethereum-compatible API)
New-NetFirewallRule -DisplayName "Drive JSON-RPC HTTP" -Direction Inbound -LocalPort 8555 -Protocol TCP -Action Allow

# JSON-RPC WebSocket (if exposing WebSocket API)
New-NetFirewallRule -DisplayName "Drive JSON-RPC WS" -Direction Inbound -LocalPort 8556 -Protocol TCP -Action Allow

# Prometheus (if exposing metrics)
New-NetFirewallRule -DisplayName "Drive Prometheus" -Direction Inbound -LocalPort 26670 -Protocol TCP -Action Allow

# EVM Metrics (if exposing EVM metrics)
New-NetFirewallRule -DisplayName "Drive EVM Metrics" -Direction Inbound -LocalPort 6075 -Protocol TCP -Action Allow

# Geth Metrics (if exposing Geth metrics)
New-NetFirewallRule -DisplayName "Drive Geth Metrics" -Direction Inbound -LocalPort 8110 -Protocol TCP -Action Allow
```
{{< /tab >}}
{{< /tabs >}}

---

## Datos Persistentes

### Volume Mapping

- **Host Path:** `./persistent-data`
- **Container Path:** `/home/ubuntu/.infinited`

### Data Stored

The persistent data directory contains:
- **Chain data** - Blockchain state and history
- **Keys** - Validator and account keys (if configured)
- **Configuración files** - Archivos de configuración del nodo (`config.toml`, `app.toml`)
- **Genesis file** - Downloaded genesis file

**Importante:** This data is stored locally on your system and is never shared or synced. It is exclusively yours.

---

## Ver También

- [Estrategia de Puertos]({{< relref "../ports" >}}) - Estrategia de asignación de puertos e información general
- [Referencia de Puertos: Nodos Blockchain]({{< relref "../ports/blockchain-nodes" >}}) - Detailed descriptions of all port types
- [Variables de Entorno: Nodos Blockchain]({{< relref "../environment/blockchain-nodes" >}}) - Complete environment variable reference
- [Estructura del Servicio]({{< relref "../service-structure" >}}) - Arquitectura técnica and service structure
