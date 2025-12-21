---
title: "QOM Network (node3-qom)"
---

**Número de Servicio:** 3  
**Directorio de Servicio:** `node3-qom`  
**Nombre de Servicio/Contenedor:** `qom`  
**Red:** QOM Network  
**Tipo:** Blockchain Node

## Descripción

QOM Network blockchain node. Uses alternative binary configuration (qomd). All ports have a +30 offset from default ports. This is a different blockchain project that uses the same Drive infrastructure.

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

**Número de Servicio:** 3  
**Desplazamiento de Puerto:** +30

| Tipo de Puerto | Puerto del Host | Puerto del Contenedor |
|-----------|-----------|---------------|
| P2P | 26686 | 26656 |
| RPC | 26687 | 26657 |
| gRPC | 9120 | 9090 |
| gRPC-Web | 9121 | 9091 |
| REST API | 1347 | 1317 |
| JSON-RPC HTTP | 8575 | 8545 |
| JSON-RPC WS | 8576 | 8546 |

### Cálculo de Puertos

{{< expand "Cálculo de Puertos Details" "↕" >}}
Este servicio usa **Número de Servicio 3**, por lo que todos los puertos tienen un desplazamiento de +30:

- **P2P**: 26656 + (3 × 10) = **26686**
- **RPC**: 26657 + (3 × 10) = **26687**
- **gRPC**: 9090 + (3 × 10) = **9120**
- **gRPC-Web**: 9091 + (3 × 10) = **9121**
- **REST API**: 1317 + (3 × 10) = **1347**
- **JSON-RPC HTTP**: 8545 + (3 × 10) = **8575**
- **JSON-RPC WebSocket**: 8546 + (3 × 10) = **8576**

Para descripciones detalladas de cada tipo de puerto, consulta [Referencia de Puertos: Nodos Blockchain]({{< relref "../ports/blockchain-nodes" >}}).
{{< /expand >}}

### Puertos Requeridos

{{< expand "Puertos Requeridos Details" "↕" >}}
Estos puertos deben estar configurados para que el servicio funcione:

| Tipo de Puerto | Puerto del Host | Puerto del Contenedor | Descripción |
|-----------|-----------|---------------|-------------|
| **P2P** | 26686 | 26656 | Comunicación de red peer-to-peer |
| **RPC** | 26687 | 26657 | API RPC de Tendermint |
{{< /expand >}}

### Puertos Opcionales

{{< expand "Puertos Opcionales Details" "↕" >}}
Estos puertos pueden habilitarse si se necesitan para casos de uso específicos:

| Tipo de Puerto | Puerto del Host | Puerto del Contenedor | Descripción | Cuándo Habilitar |
|-----------|-----------|---------------|-------------|----------------|
| **gRPC** | 9120 | 9090 | Consultas gRPC del Cosmos SDK | Endpoint de API pública, conexiones de billetera |
| **gRPC-Web** | 9121 | 9091 | gRPC-Web (navegador) | Aplicaciones web, billeteras de navegador |
| **REST API** | 1347 | 1317 | API REST del Cosmos SDK | Compatibilidad con aplicaciones legacy |
| **JSON-RPC HTTP** | 8575 | 8545 | Ethereum JSON-RPC (HTTP) | MetaMask, herramientas Ethereum, dApps |
| **JSON-RPC WebSocket** | 8576 | 8546 | Ethereum JSON-RPC (WebSocket) | Eventos de blockchain en tiempo real |
| **Prometheus** | 26690 | 26660 | Métricas de Prometheus | Monitoreo de nodos |
| **EVM Metrics** | 6095 | 6065 | Métricas Prometheus de EVM | Monitoreo de rendimiento EVM |
| **Geth Metrics** | 8130 | 8100 | Métricas compatibles con Geth | Herramientas de monitoreo Geth |
{{< /expand >}}

---

## Variables de Entorno

Este servicio usa las siguientes variables de entorno con los valores mostrados a continuación. Para documentación completa de todas las variables de entorno disponibles, consulta [Variables de Entorno: Nodos Blockchain]({{< relref "../environment/blockchain-nodes" >}}).

### Configuración del Binario

This service uses an **alternative binary** (`qomd`) instead of the default Infinite binary. The binary is downloaded from the specified URL at container startup.

**Alternative Configuración del Binario:**
- **Binary Name:** `qomd`
- **Binary URL (AMD64):** `https://github.com/WizardLatino/test-qom-node/releases/download/v1.0.1/qomd-linux-amd64`
- **Home Directory:** `/home/ubuntu/.qomd`

### Identificación de Cadena

{{< expand "Variables de Identificación de Cadena" "↕" >}}
Este servicio está configurado con las siguientes variables de identificación de cadena:

**NODE_CHAIN_ID**  
The chain ID for the QOM Network. This uniquely identifies the blockchain network.

```yaml
NODE_CHAIN_ID: "qom_766-1"
```

**NODE_EVM_CHAIN_ID**  
El ID de cadena EVM para protección contra replay compatible con EIP-155.

Esto es independiente del ID de cadena de Cosmos y se usa para transacciones compatibles con Ethereum.

```yaml
NODE_EVM_CHAIN_ID: "766"
```

**NODE_GENESIS_URL**  
URL para descargar el archivo genesis oficial durante la inicialización del nodo.

El archivo genesis contiene el estado inicial de la blockchain.

```yaml
NODE_GENESIS_URL: "https://raw.githubusercontent.com/deep-thought-labs/babelfish-vm/main/resources/genesis.json"
```
{{< /expand >}}

### Configuración de Red P2P

{{< expand "Variables de Configuración de Red P2P" "↕" >}}
Este servicio usa las siguientes variables de configuración de red P2P:

**NODE_P2P_SEEDS**  
Nodos semilla para descubrimiento P2P. Estos nodos ayudan a tu nodo a descubrir otros pares en la red durante la conexión inicial.

Los nodos semilla se usan para el descubrimiento de red pero no son conexiones persistentes.

```yaml
NODE_P2P_SEEDS: "7768864af4003165c10b77802a673006f98d54c6@p2p.foxxone.one:26656"
```

**NODE_PERSISTENT_PEERS**  
Los nodos pares persistentes mantienen conexiones continuas, a diferencia de los nodos semilla que solo se usan para descubrimiento.

```yaml
NODE_PERSISTENT_PEERS: "7768864af4003165c10b77802a673006f98d54c6@p2p.foxxone.one:26656"
```

**NODE_P2P_EXTERNAL_ADDRESS**  
Dirección externa para anunciar a los pares para que se conecten. Se usa cuando el nodo está detrás de NAT o firewall.

Este servicio no tiene un valor preconfigurado para esta variable. Si es necesario, configúralo con la dirección IP pública o el nombre de dominio de tu nodo.

```yaml
# NODE_P2P_EXTERNAL_ADDRESS: ""  # Sin valor preconfigurado para este servicio
```
{{< /expand >}}

### Alternative Configuración del Binario

{{< expand "Alternative Configuración del Binario Variables" "↕" >}}
This service uses an alternative binary instead of the default Infinite binary. The following variables configure the alternative binary:

**NODE_ALT_BINARY_URL_AMD64**  
URL to download the alternative binary for AMD64/x86_64 architecture.

The binary will be downloaded at container startup.

```yaml
NODE_ALT_BINARY_URL_AMD64: "https://github.com/WizardLatino/test-qom-node/releases/download/v1.0.1/qomd-linux-amd64"
```

**NODE_ALT_BINARY_NAME**  
Name of the alternative binary executable.

This is the name of the binary file (without path). It will be installed in `/home/ubuntu/bin/`.

```yaml
NODE_ALT_BINARY_NAME: "qomd"
```

**NODE_ALT_HOME**  
Custom home directory for the alternative blockchain node.

This is where the blockchain node stores its data and configuration files.

```yaml
NODE_ALT_HOME: "/home/ubuntu/.qomd"
```
{{< /expand >}}

---

## Comandos Esenciales

Este servicio es un nodo blockchain, que requiere comandos especializados para la inicialización, inicio, detención y gestión del nodo.

Comandos generales de gestión de contenedores (iniciar, detener, reiniciar, etc.) se describen en la [Managing Servicios]({{< relref "../../quick-start/managing-services" >}}) sección.

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
  qom:
    image: deepthoughtlabs/infinite-drive:dev
    container_name: qom
    restart: unless-stopped

    ports:
      - "26686:26656"  # P2P (required)
      - "26687:26657"  # RPC (required)
    
    volumes:
      - ./persistent-data:/home/ubuntu/.qomd

    environment:
      NODE_CHAIN_ID: "qom_766-1"
      NODE_EVM_CHAIN_ID: "766"
      NODE_GENESIS_URL: "https://raw.githubusercontent.com/deep-thought-labs/babelfish-vm/main/resources/genesis.json"
      NODE_P2P_SEEDS: "7768864af4003165c10b77802a673006f98d54c6@p2p.foxxone.one:26656"
      NODE_PERSISTENT_PEERS: "7768864af4003165c10b77802a673006f98d54c6@p2p.foxxone.one:26656"
      NODE_ALT_BINARY_URL_AMD64: "https://github.com/WizardLatino/test-qom-node/releases/download/v1.0.1/qomd-linux-amd64"
      NODE_ALT_BINARY_NAME: "qomd"
      NODE_ALT_HOME: "/home/ubuntu/.qomd"
```
{{< /expand >}}

{{< expand "Configuración Completa (Todos los Puertos)" "↕" >}}
```yaml
services:
  qom:
    image: deepthoughtlabs/infinite-drive:dev
    container_name: qom
    restart: unless-stopped

    ports:
      # Puertos requeridos
      - "26686:26656"  # P2P
      - "26687:26657"  # RPC
      
      # Puertos opcionales (descomenta si es necesario)
      - "9120:9090"    # gRPC
      - "9121:9091"    # gRPC-Web
      - "1347:1317"    # REST API
      - "8575:8545"    # JSON-RPC HTTP
      - "8576:8546"    # JSON-RPC WebSocket
      - "26690:26660"  # Prometheus
      - "6095:6065"    # EVM Metrics
      - "8130:8100"    # Geth Metrics
    
    volumes:
      - ./persistent-data:/home/ubuntu/.qomd

    environment:
      NODE_CHAIN_ID: "qom_766-1"
      NODE_EVM_CHAIN_ID: "766"
      NODE_GENESIS_URL: "https://raw.githubusercontent.com/deep-thought-labs/babelfish-vm/main/resources/genesis.json"
      NODE_P2P_SEEDS: "7768864af4003165c10b77802a673006f98d54c6@p2p.foxxone.one:26656"
      NODE_PERSISTENT_PEERS: "7768864af4003165c10b77802a673006f98d54c6@p2p.foxxone.one:26656"
      NODE_ALT_BINARY_URL_AMD64: "https://github.com/WizardLatino/test-qom-node/releases/download/v1.0.1/qomd-linux-amd64"
      NODE_ALT_BINARY_NAME: "qomd"
      NODE_ALT_HOME: "/home/ubuntu/.qomd"
      # NODE_P2P_EXTERNAL_ADDRESS: ""
```
{{< /expand >}}

---

## Configuración de Firewall

**⚠️ Crítico:** Antes de configurar cualquier regla de firewall para este servicio, debes permitir primero SSH (puerto 22) en tu sistema. Si te estás conectando a un servidor remoto vía SSH y habilitas el firewall sin permitir SSH primero, perderás el acceso a tu servidor.

El proceso completo de configuración de firewall, incluyendo cómo verificar y permitir SSH (puerto 22), se describe en detalle en la [Configuración de Firewall Guide]({{< relref "../ports/firewall-configuration" >}}). Los comandos mostrados a continuación are specific to this service with the correct port numbers for QOM Network, but please review the guide for the complete setup process.

### Puertos Requeridos

{{< tabs "firewall-required" >}}
{{< tab "Ubuntu/Linux" >}}
```bash
# Puerto P2P (requerido para validadores y conexiones peer)
sudo ufw allow 26686/tcp

# Puerto RPC (opcional, solo si expones la API RPC)
sudo ufw allow 26687/tcp
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
5. Add rules to permitir conexiones entrantes for the required ports (26686, 26687)

**Second Option - Command Line (Advanced):**
If you prefer command-line configuration, you can modify `/etc/pf.conf`:

```bash
# Edit /etc/pf.conf and add rules:
# pass in proto tcp from any to any port 26686  # P2P port
# pass in proto tcp from any to any port 26687  # RPC port

# Then reload the firewall:
sudo pfctl -f /etc/pf.conf
```
{{< /tab >}}
{{< tab "Windows" >}}
```powershell
# Puerto P2P (requerido para validadores y conexiones peer)
New-NetFirewallRule -DisplayName "Drive P2P" -Direction Inbound -LocalPort 26686 -Protocol TCP -Action Allow

# Puerto RPC (opcional, solo si expones la API RPC)
New-NetFirewallRule -DisplayName "Drive RPC" -Direction Inbound -LocalPort 26687 -Protocol TCP -Action Allow
```
{{< /tab >}}
{{< /tabs >}}

### Puertos Opcionales

{{< tabs "firewall-optional" >}}
{{< tab "Ubuntu/Linux" >}}
```bash
# gRPC (if exposing gRPC API)
sudo ufw allow 9120/tcp

# gRPC-Web (if exposing gRPC-Web API)
sudo ufw allow 9121/tcp

# REST API (if exposing REST API)
sudo ufw allow 1347/tcp

# JSON-RPC HTTP (if exposing Ethereum-compatible API)
sudo ufw allow 8575/tcp

# JSON-RPC WebSocket (if exposing WebSocket API)
sudo ufw allow 8576/tcp

# Prometheus (if exposing metrics)
sudo ufw allow 26690/tcp

# EVM Metrics (if exposing EVM metrics)
sudo ufw allow 6095/tcp

# Geth Metrics (if exposing Geth metrics)
sudo ufw allow 8130/tcp
```

**Note:** The `/tcp` protocol specification is optional in UFW. You can use either `sudo ufw allow 26686/tcp` or `sudo ufw allow 26686` - both work the same way.
{{< /tab >}}
{{< tab "macOS" >}}
**Recommended:** macOS typically allows incoming connections by default, so you may not need to configure anything. However, we recommend verifying your firewall settings.

**First Option - System Preferences (Recommended):**
Use the built-in graphical interface to configure firewall rules:
1. Open **System Preferences** (or **System Settings** on newer macOS versions)
2. Go to **Security & Privacy** > **Firewall**
3. Click the lock icon and enter your password to make changes
4. Click **Firewall Options...**
5. Add rules to permitir conexiones entrantes for the optional ports you want to expose (9120, 9121, 1347, 8575, 8576, 26690, 6095, 8130)

**Second Option - Command Line (Advanced):**
If you prefer command-line configuration, you can modify `/etc/pf.conf`:

```bash
# Edit /etc/pf.conf and add rules for each port you want to expose:
# pass in proto tcp from any to any port 9120  # gRPC
# pass in proto tcp from any to any port 9121  # gRPC-Web
# pass in proto tcp from any to any port 1347  # REST API
# pass in proto tcp from any to any port 8575  # JSON-RPC HTTP
# pass in proto tcp from any to any port 8576  # JSON-RPC WebSocket
# pass in proto tcp from any to any port 26690 # Prometheus
# pass in proto tcp from any to any port 6095  # EVM Metrics
# pass in proto tcp from any to any port 8130  # Geth Metrics

# Then reload the firewall:
sudo pfctl -f /etc/pf.conf
```
{{< /tab >}}
{{< tab "Windows" >}}
```powershell
# gRPC (if exposing gRPC API)
New-NetFirewallRule -DisplayName "Drive gRPC" -Direction Inbound -LocalPort 9120 -Protocol TCP -Action Allow

# gRPC-Web (if exposing gRPC-Web API)
New-NetFirewallRule -DisplayName "Drive gRPC-Web" -Direction Inbound -LocalPort 9121 -Protocol TCP -Action Allow

# REST API (if exposing REST API)
New-NetFirewallRule -DisplayName "Drive REST API" -Direction Inbound -LocalPort 1347 -Protocol TCP -Action Allow

# JSON-RPC HTTP (if exposing Ethereum-compatible API)
New-NetFirewallRule -DisplayName "Drive JSON-RPC HTTP" -Direction Inbound -LocalPort 8575 -Protocol TCP -Action Allow

# JSON-RPC WebSocket (if exposing WebSocket API)
New-NetFirewallRule -DisplayName "Drive JSON-RPC WS" -Direction Inbound -LocalPort 8576 -Protocol TCP -Action Allow

# Prometheus (if exposing metrics)
New-NetFirewallRule -DisplayName "Drive Prometheus" -Direction Inbound -LocalPort 26690 -Protocol TCP -Action Allow

# EVM Metrics (if exposing EVM metrics)
New-NetFirewallRule -DisplayName "Drive EVM Metrics" -Direction Inbound -LocalPort 6095 -Protocol TCP -Action Allow

# Geth Metrics (if exposing Geth metrics)
New-NetFirewallRule -DisplayName "Drive Geth Metrics" -Direction Inbound -LocalPort 8130 -Protocol TCP -Action Allow
```
{{< /tab >}}
{{< /tabs >}}

---

## Datos Persistentes

### Volume Mapping

- **Host Path:** `./persistent-data`
- **Container Path:** `/home/ubuntu/.qomd`

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
