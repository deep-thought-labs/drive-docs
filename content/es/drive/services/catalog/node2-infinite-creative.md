---
title: "Infinite Creative Network (node2-infinite-creative)"
---

**Número de Servicio:** 2  
**Directorio de Servicio:** `node2-infinite-creative`  
**Nombre de Servicio/Contenedor:** `infinite-creative`  
**Red:** Infinite Creative Network  
**Tipo:** Blockchain Node

## Descripción

Creative Network blockchain node. All ports have a +20 offset from default ports. This network is designed for creative and experimental use cases.

---

{{< callout type="info" >}}
**Estado de la Red: Fase Beta**

Esta red se encuentra actualmente en una fase beta. Los valores configurados en este documento para las semillas P2P (`NODE_P2P_SEEDS`), los pares persistentes (`NODE_PERSISTENT_PEERS`) y la URL del archivo genesis (`NODE_GENESIS_URL`) corresponden a la fase de pruebas de esta cadena.

**Importante:** Estos valores pueden cambiar en el futuro cuando la fase de pruebas termine y la red entre en producción. Se recomienda verificar periódicamente la documentación oficial para asegurar que estás utilizando los valores más actualizados.
{{< /callout >}}

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

**Número de Servicio:** 2  
**Desplazamiento de Puerto:** +20

| Tipo de Puerto | Puerto del Host | Puerto del Contenedor |
|-----------|-----------|---------------|
| P2P | 26676 | 26656 |
| RPC | 26677 | 26657 |
| gRPC | 9110 | 9090 |
| gRPC-Web | 9111 | 9091 |
| REST API | 1337 | 1317 |
| JSON-RPC HTTP | 8565 | 8545 |
| JSON-RPC WS | 8566 | 8546 |

### Cálculo de Puertos

{{< expand "Cálculo de Puertos Details" "↕" >}}
Este servicio usa **Número de Servicio 2**, por lo que todos los puertos tienen un desplazamiento de +20:

- **P2P**: 26656 + (2 × 10) = **26676**
- **RPC**: 26657 + (2 × 10) = **26677**
- **gRPC**: 9090 + (2 × 10) = **9110**
- **gRPC-Web**: 9091 + (2 × 10) = **9111**
- **REST API**: 1317 + (2 × 10) = **1337**
- **JSON-RPC HTTP**: 8545 + (2 × 10) = **8565**
- **JSON-RPC WebSocket**: 8546 + (2 × 10) = **8566**

Para descripciones detalladas de cada tipo de puerto, consulta [Referencia de Puertos: Nodos Blockchain]({{< relref "../ports/blockchain-nodes" >}}).
{{< /expand >}}

### Puertos Requeridos

{{< expand "Puertos Requeridos Details" "↕" >}}
Estos puertos deben estar configurados para que el servicio funcione:

| Tipo de Puerto | Puerto del Host | Puerto del Contenedor | Descripción |
|-----------|-----------|---------------|-------------|
| **P2P** | 26676 | 26656 | Comunicación de red peer-to-peer |
| **RPC** | 26677 | 26657 | API RPC de Tendermint |
{{< /expand >}}

### Puertos Opcionales

{{< expand "Puertos Opcionales Details" "↕" >}}
Estos puertos pueden habilitarse si se necesitan para casos de uso específicos:

| Tipo de Puerto | Puerto del Host | Puerto del Contenedor | Descripción | Cuándo Habilitar |
|-----------|-----------|---------------|-------------|----------------|
| **gRPC** | 9110 | 9090 | Consultas gRPC del Cosmos SDK | Endpoint de API pública, conexiones de billetera |
| **gRPC-Web** | 9111 | 9091 | gRPC-Web (navegador) | Aplicaciones web, billeteras de navegador |
| **REST API** | 1337 | 1317 | API REST del Cosmos SDK | Compatibilidad con aplicaciones legacy |
| **JSON-RPC HTTP** | 8565 | 8545 | Ethereum JSON-RPC (HTTP) | MetaMask, herramientas Ethereum, dApps |
| **JSON-RPC WebSocket** | 8566 | 8546 | Ethereum JSON-RPC (WebSocket) | Eventos de blockchain en tiempo real |
| **Prometheus** | 26680 | 26660 | Métricas de Prometheus | Monitoreo de nodos |
| **EVM Metrics** | 6085 | 6065 | Métricas Prometheus de EVM | Monitoreo de rendimiento EVM |
| **Geth Metrics** | 8120 | 8100 | Métricas compatibles con Geth | Herramientas de monitoreo Geth |
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
The chain ID for the Infinite Creative Network. This uniquely identifies the blockchain network.

```yaml
NODE_CHAIN_ID: "infinite_421018002-1"
```

**NODE_EVM_CHAIN_ID**  
El ID de cadena EVM para protección contra replay compatible con EIP-155.

Esto es independiente del ID de cadena de Cosmos y se usa para transacciones compatibles con Ethereum.

```yaml
NODE_EVM_CHAIN_ID: "421018002"
```

**NODE_GENESIS_URL**  
URL para descargar el archivo genesis oficial durante la inicialización del nodo.

El archivo genesis contiene el estado inicial de la blockchain.

```yaml
NODE_GENESIS_URL: "https://assets.infinitedrive.xyz/tests-round1/genesis-final.json"
```
{{< /expand >}}

### Configuración de Red P2P

{{< expand "Variables de Configuración de Red P2P" "↕" >}}
Este servicio usa las siguientes variables de configuración de red P2P:

**Detalles de Nodos Confiables:**

| # | Node ID | Dirección | Puerto | Persistente | Semilla Completa |
|---|---------|-----------|--------|-------------|------------------|
| 1 | `dd5689375610aaa35b69ed311d69e51ea5557474` | `server-red.infinitedrive.xyz` | `26676` | Sí | `dd5689375610aaa35b69ed311d69e51ea5557474@server-red.infinitedrive.xyz:26676` |
| 2 | `e5c1b7423d098c660bb82b7f44f86e333cb6af9e` | `server-farmer.infinitedrive.xyz` | `26676` | Sí | `e5c1b7423d098c660bb82b7f44f86e333cb6af9e@server-farmer.infinitedrive.xyz:26676` |
| 3 | `c55506b50d0442628308f2bfbc986b7d4b571784` | `server-pauline.infinitedrive.xyz` | `26676` | Sí | `c55506b50d0442628308f2bfbc986b7d4b571784@server-pauline.infinitedrive.xyz:26676` |
| 4 | `9671910fe6fa13fc40c6fa53f8f6ebac2a5ece9e` | `server-gammaray.infinitedrive.xyz` | `26676` | Sí | `9671910fe6fa13fc40c6fa53f8f6ebac2a5ece9e@server-gammaray.infinitedrive.xyz:26676` |
| 5 | `e40ed2462c8471b2e71b8d32f26fa962d376e2cb` | `server-phoenix.infinitedrive.xyz` | `26676` | Sí | `e40ed2462c8471b2e71b8d32f26fa962d376e2cb@server-phoenix.infinitedrive.xyz:26676` |
| 6 | `02df0ae579b235f905b04f65217d112204bd2148` | `server-xenia.infinitedrive.xyz` | `26676` | Sí | `02df0ae579b235f905b04f65217d112204bd2148@server-xenia.infinitedrive.xyz:26676` |
| 7 | `0ca29b243a2ae5baee08d993c9457d01ace8e0c3` | `server-panda.infinitedrive.xyz` | `26676` | Sí | `0ca29b243a2ae5baee08d993c9457d01ace8e0c3@server-panda.infinitedrive.xyz:26676` |
| 8 | `93a42038e6adb8e7c2c6bc48d1cfaf5d7a2c26a0` | `server-mt.infinitedrive.xyz` | `26676` | Sí | `93a42038e6adb8e7c2c6bc48d1cfaf5d7a2c26a0@server-mt.infinitedrive.xyz:26676` |
| 9 | `9e003452950262e5585b7bfcac04072db7e5ef7f` | `server-justdude.infinitedrive.xyz` | `26676` | Sí | `9e003452950262e5585b7bfcac04072db7e5ef7f@server-justdude.infinitedrive.xyz:26676` |
| 10 | `e77165e145fce561add786a17316b6b686a5d864` | `server-luke.infinitedrive.xyz` | `26676` | Sí | `e77165e145fce561add786a17316b6b686a5d864@server-luke.infinitedrive.xyz:26676` |
| 11 | `8a03cbe28a39da940df7247079a15ae1aa8e7680` | `server-viethawk.infinitedrive.xyz` | `26676` | Sí | `8a03cbe28a39da940df7247079a15ae1aa8e7680@server-viethawk.infinitedrive.xyz:26676` |
| 12 | `e124f7b16b876abef4aa4837cf03123db622b61d` | `server-ayc.infinitedrive.xyz` | `26676` | Sí | `e124f7b16b876abef4aa4837cf03123db622b61d@server-ayc.infinitedrive.xyz:26676` |
| 13 | `7460b57c1cc977d036e0f40c9c5f5ac946e26c04` | `server-kim.infinitedrive.xyz` | `26676` | Sí | `7460b57c1cc977d036e0f40c9c5f5ac946e26c04@server-kim.infinitedrive.xyz:26676` |

**NODE_P2P_SEEDS**  
Nodos semilla para descubrimiento P2P. Estos nodos ayudan a tu nodo a descubrir otros pares en la red durante la conexión inicial.

Los nodos semilla se usan para el descubrimiento de red pero no son conexiones persistentes.

Las semillas se especifican en formato `node-id@ip:port`, separadas por comas si hay múltiples semillas.

Ver la tabla de detalles de nodos confiables arriba para la lista completa de nodos.

```yaml
NODE_P2P_SEEDS: "dd5689375610aaa35b69ed311d69e51ea5557474@server-red.infinitedrive.xyz:26676,e5c1b7423d098c660bb82b7f44f86e333cb6af9e@server-farmer.infinitedrive.xyz:26676,c55506b50d0442628308f2bfbc986b7d4b571784@server-pauline.infinitedrive.xyz:26676,9671910fe6fa13fc40c6fa53f8f6ebac2a5ece9e@server-gammaray.infinitedrive.xyz:26676,e40ed2462c8471b2e71b8d32f26fa962d376e2cb@server-phoenix.infinitedrive.xyz:26676,02df0ae579b235f905b04f65217d112204bd2148@server-xenia.infinitedrive.xyz:26676,0ca29b243a2ae5baee08d993c9457d01ace8e0c3@server-panda.infinitedrive.xyz:26676,93a42038e6adb8e7c2c6bc48d1cfaf5d7a2c26a0@server-mt.infinitedrive.xyz:26676,9e003452950262e5585b7bfcac04072db7e5ef7f@server-justdude.infinitedrive.xyz:26676,e77165e145fce561add786a17316b6b686a5d864@server-luke.infinitedrive.xyz:26676,8a03cbe28a39da940df7247079a15ae1aa8e7680@server-viethawk.infinitedrive.xyz:26676,e124f7b16b876abef4aa4837cf03123db622b61d@server-ayc.infinitedrive.xyz:26676,7460b57c1cc977d036e0f40c9c5f5ac946e26c04@server-kim.infinitedrive.xyz:26676"
```

**NODE_PERSISTENT_PEERS**  
Los nodos pares persistentes mantienen conexiones continuas, a diferencia de los nodos semilla que solo se usan para descubrimiento.

En este servicio, todos los nodos configurados son persistentes, por lo que esta variable contiene el mismo valor que `NODE_P2P_SEEDS`.

Ver la tabla de detalles de nodos confiables arriba para la lista completa de nodos.

```yaml
NODE_PERSISTENT_PEERS: "dd5689375610aaa35b69ed311d69e51ea5557474@server-red.infinitedrive.xyz:26676,e5c1b7423d098c660bb82b7f44f86e333cb6af9e@server-farmer.infinitedrive.xyz:26676,c55506b50d0442628308f2bfbc986b7d4b571784@server-pauline.infinitedrive.xyz:26676,9671910fe6fa13fc40c6fa53f8f6ebac2a5ece9e@server-gammaray.infinitedrive.xyz:26676,e40ed2462c8471b2e71b8d32f26fa962d376e2cb@server-phoenix.infinitedrive.xyz:26676,02df0ae579b235f905b04f65217d112204bd2148@server-xenia.infinitedrive.xyz:26676,0ca29b243a2ae5baee08d993c9457d01ace8e0c3@server-panda.infinitedrive.xyz:26676,93a42038e6adb8e7c2c6bc48d1cfaf5d7a2c26a0@server-mt.infinitedrive.xyz:26676,9e003452950262e5585b7bfcac04072db7e5ef7f@server-justdude.infinitedrive.xyz:26676,e77165e145fce561add786a17316b6b686a5d864@server-luke.infinitedrive.xyz:26676,8a03cbe28a39da940df7247079a15ae1aa8e7680@server-viethawk.infinitedrive.xyz:26676,e124f7b16b876abef4aa4837cf03123db622b61d@server-ayc.infinitedrive.xyz:26676,7460b57c1cc977d036e0f40c9c5f5ac946e26c04@server-kim.infinitedrive.xyz:26676"
```

**NODE_P2P_EXTERNAL_ADDRESS**  
Dirección externa para anunciar a los pares para que se conecten. Se usa cuando el nodo está detrás de NAT o firewall.

Esta variable especifica la dirección que otros nodos deben usar para conectarse a tu nodo. El formato es `host:puerto`, donde:
- **host**: Puede ser una dirección IP (IPv4) o un nombre de dominio
- **puerto**: El puerto P2P del host (en este servicio, `26676`)

**Nota:** Esta variable contiene únicamente el host y el puerto, sin incluir el Node ID. Esencialmente, corresponde a la parte `host:puerto` de una semilla P2P completa (que tiene el formato `node-id@host:puerto`), pero sin el identificador del nodo.

Este servicio no tiene un valor preconfigurado para esta variable. Si es necesario, configúralo con la dirección IP pública o el nombre de dominio de tu nodo.

**Ejemplos de valores:**

```yaml
# Ejemplo con dirección IP IPv4
NODE_P2P_EXTERNAL_ADDRESS: "192.168.1.100:26676"

# Ejemplo con nombre de dominio
NODE_P2P_EXTERNAL_ADDRESS: "mi-nodo.ejemplo.com:26676"
```

**Configuración sin valor preconfigurado:**

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
  infinite-creative:
    image: deepthoughtlabs/infinite-drive:dev
    container_name: infinite-creative
    restart: unless-stopped

    ports:
      - "26676:26656"  # P2P (required)
      - "26677:26657"  # RPC (required)
    
    volumes:
      - ./persistent-data:/home/ubuntu/.infinited

    environment:
      NODE_CHAIN_ID: "infinite_421018002-1"
      NODE_EVM_CHAIN_ID: "421018002"
      NODE_GENESIS_URL: "https://assets.infinitedrive.xyz/tests-round1/genesis-final.json"
      NODE_P2P_SEEDS: "dd5689375610aaa35b69ed311d69e51ea5557474@server-red.infinitedrive.xyz:26676,e5c1b7423d098c660bb82b7f44f86e333cb6af9e@server-farmer.infinitedrive.xyz:26676,c55506b50d0442628308f2bfbc986b7d4b571784@server-pauline.infinitedrive.xyz:26676,9671910fe6fa13fc40c6fa53f8f6ebac2a5ece9e@server-gammaray.infinitedrive.xyz:26676,e40ed2462c8471b2e71b8d32f26fa962d376e2cb@server-phoenix.infinitedrive.xyz:26676,02df0ae579b235f905b04f65217d112204bd2148@server-xenia.infinitedrive.xyz:26676,0ca29b243a2ae5baee08d993c9457d01ace8e0c3@server-panda.infinitedrive.xyz:26676,93a42038e6adb8e7c2c6bc48d1cfaf5d7a2c26a0@server-mt.infinitedrive.xyz:26676,9e003452950262e5585b7bfcac04072db7e5ef7f@server-justdude.infinitedrive.xyz:26676,e77165e145fce561add786a17316b6b686a5d864@server-luke.infinitedrive.xyz:26676,8a03cbe28a39da940df7247079a15ae1aa8e7680@server-viethawk.infinitedrive.xyz:26676,e124f7b16b876abef4aa4837cf03123db622b61d@server-ayc.infinitedrive.xyz:26676,7460b57c1cc977d036e0f40c9c5f5ac946e26c04@server-kim.infinitedrive.xyz:26676"
      NODE_PERSISTENT_PEERS: "dd5689375610aaa35b69ed311d69e51ea5557474@server-red.infinitedrive.xyz:26676,e5c1b7423d098c660bb82b7f44f86e333cb6af9e@server-farmer.infinitedrive.xyz:26676,c55506b50d0442628308f2bfbc986b7d4b571784@server-pauline.infinitedrive.xyz:26676,9671910fe6fa13fc40c6fa53f8f6ebac2a5ece9e@server-gammaray.infinitedrive.xyz:26676,e40ed2462c8471b2e71b8d32f26fa962d376e2cb@server-phoenix.infinitedrive.xyz:26676,02df0ae579b235f905b04f65217d112204bd2148@server-xenia.infinitedrive.xyz:26676,0ca29b243a2ae5baee08d993c9457d01ace8e0c3@server-panda.infinitedrive.xyz:26676,93a42038e6adb8e7c2c6bc48d1cfaf5d7a2c26a0@server-mt.infinitedrive.xyz:26676,9e003452950262e5585b7bfcac04072db7e5ef7f@server-justdude.infinitedrive.xyz:26676,e77165e145fce561add786a17316b6b686a5d864@server-luke.infinitedrive.xyz:26676,8a03cbe28a39da940df7247079a15ae1aa8e7680@server-viethawk.infinitedrive.xyz:26676,e124f7b16b876abef4aa4837cf03123db622b61d@server-ayc.infinitedrive.xyz:26676,7460b57c1cc977d036e0f40c9c5f5ac946e26c04@server-kim.infinitedrive.xyz:26676"
```
{{< /expand >}}

{{< expand "Configuración Completa (Todos los Puertos)" "↕" >}}
```yaml
services:
  infinite-creative:
    image: deepthoughtlabs/infinite-drive:dev
    container_name: infinite-creative
    restart: unless-stopped

    ports:
      # Puertos requeridos
      - "26676:26656"  # P2P
      - "26677:26657"  # RPC
      
      # Puertos opcionales (descomenta si es necesario)
      - "9110:9090"    # gRPC
      - "9111:9091"    # gRPC-Web
      - "1337:1317"    # REST API
      - "8565:8545"    # JSON-RPC HTTP
      - "8566:8546"    # JSON-RPC WebSocket
      - "26680:26660"  # Prometheus
      - "6085:6065"    # EVM Metrics
      - "8120:8100"    # Geth Metrics
    
    volumes:
      - ./persistent-data:/home/ubuntu/.infinited

    environment:
      NODE_CHAIN_ID: "infinite_421018002-1"
      NODE_EVM_CHAIN_ID: "421018002"
      NODE_GENESIS_URL: "https://assets.infinitedrive.xyz/tests-round1/genesis-final.json"
      NODE_P2P_SEEDS: "dd5689375610aaa35b69ed311d69e51ea5557474@server-red.infinitedrive.xyz:26676,e5c1b7423d098c660bb82b7f44f86e333cb6af9e@server-farmer.infinitedrive.xyz:26676,c55506b50d0442628308f2bfbc986b7d4b571784@server-pauline.infinitedrive.xyz:26676,9671910fe6fa13fc40c6fa53f8f6ebac2a5ece9e@server-gammaray.infinitedrive.xyz:26676,e40ed2462c8471b2e71b8d32f26fa962d376e2cb@server-phoenix.infinitedrive.xyz:26676,02df0ae579b235f905b04f65217d112204bd2148@server-xenia.infinitedrive.xyz:26676,0ca29b243a2ae5baee08d993c9457d01ace8e0c3@server-panda.infinitedrive.xyz:26676,93a42038e6adb8e7c2c6bc48d1cfaf5d7a2c26a0@server-mt.infinitedrive.xyz:26676,9e003452950262e5585b7bfcac04072db7e5ef7f@server-justdude.infinitedrive.xyz:26676,e77165e145fce561add786a17316b6b686a5d864@server-luke.infinitedrive.xyz:26676,8a03cbe28a39da940df7247079a15ae1aa8e7680@server-viethawk.infinitedrive.xyz:26676,e124f7b16b876abef4aa4837cf03123db622b61d@server-ayc.infinitedrive.xyz:26676,7460b57c1cc977d036e0f40c9c5f5ac946e26c04@server-kim.infinitedrive.xyz:26676"
      NODE_PERSISTENT_PEERS: "dd5689375610aaa35b69ed311d69e51ea5557474@server-red.infinitedrive.xyz:26676,e5c1b7423d098c660bb82b7f44f86e333cb6af9e@server-farmer.infinitedrive.xyz:26676,c55506b50d0442628308f2bfbc986b7d4b571784@server-pauline.infinitedrive.xyz:26676,9671910fe6fa13fc40c6fa53f8f6ebac2a5ece9e@server-gammaray.infinitedrive.xyz:26676,e40ed2462c8471b2e71b8d32f26fa962d376e2cb@server-phoenix.infinitedrive.xyz:26676,02df0ae579b235f905b04f65217d112204bd2148@server-xenia.infinitedrive.xyz:26676,0ca29b243a2ae5baee08d993c9457d01ace8e0c3@server-panda.infinitedrive.xyz:26676,93a42038e6adb8e7c2c6bc48d1cfaf5d7a2c26a0@server-mt.infinitedrive.xyz:26676,9e003452950262e5585b7bfcac04072db7e5ef7f@server-justdude.infinitedrive.xyz:26676,e77165e145fce561add786a17316b6b686a5d864@server-luke.infinitedrive.xyz:26676,8a03cbe28a39da940df7247079a15ae1aa8e7680@server-viethawk.infinitedrive.xyz:26676,e124f7b16b876abef4aa4837cf03123db622b61d@server-ayc.infinitedrive.xyz:26676,7460b57c1cc977d036e0f40c9c5f5ac946e26c04@server-kim.infinitedrive.xyz:26676"
      # NODE_P2P_EXTERNAL_ADDRESS: ""
```
{{< /expand >}}

---

## Configuración de Firewall

**⚠️ Crítico:** Antes de configurar cualquier regla de firewall para este servicio, debes permitir primero SSH (puerto 22) en tu sistema. Si te estás conectando a un servidor remoto vía SSH y habilitas el firewall sin permitir SSH primero, perderás el acceso a tu servidor.

El proceso completo de configuración de firewall, incluyendo cómo verificar y permitir SSH (puerto 22), se describe en detalle en la [Configuración de Firewall Guide]({{< relref "../ports/firewall-configuration" >}}). Los comandos mostrados a continuación are specific to this service with the correct port numbers for Infinite Creative Network, but please review the guide for the complete setup process.

### Puertos Requeridos

{{< tabs "firewall-required" >}}
{{< tab "Ubuntu/Linux" >}}
```bash
# Puerto P2P (requerido para validadores y conexiones peer)
sudo ufw allow 26676/tcp

# Puerto RPC (opcional, solo si expones la API RPC)
sudo ufw allow 26677/tcp
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
5. Add rules to permitir conexiones entrantes for the required ports (26676, 26677)

**Second Option - Command Line (Advanced):**
If you prefer command-line configuration, you can modify `/etc/pf.conf`:

```bash
# Edit /etc/pf.conf and add rules:
# pass in proto tcp from any to any port 26676  # P2P port
# pass in proto tcp from any to any port 26677  # RPC port

# Then reload the firewall:
sudo pfctl -f /etc/pf.conf
```
{{< /tab >}}
{{< tab "Windows" >}}
```powershell
# Puerto P2P (requerido para validadores y conexiones peer)
New-NetFirewallRule -DisplayName "Drive P2P" -Direction Inbound -LocalPort 26676 -Protocol TCP -Action Allow

# Puerto RPC (opcional, solo si expones la API RPC)
New-NetFirewallRule -DisplayName "Drive RPC" -Direction Inbound -LocalPort 26677 -Protocol TCP -Action Allow
```
{{< /tab >}}
{{< /tabs >}}

### Puertos Opcionales

{{< tabs "firewall-optional" >}}
{{< tab "Ubuntu/Linux" >}}
```bash
# gRPC (if exposing gRPC API)
sudo ufw allow 9110/tcp

# gRPC-Web (if exposing gRPC-Web API)
sudo ufw allow 9111/tcp

# REST API (if exposing REST API)
sudo ufw allow 1337/tcp

# JSON-RPC HTTP (if exposing Ethereum-compatible API)
sudo ufw allow 8565/tcp

# JSON-RPC WebSocket (if exposing WebSocket API)
sudo ufw allow 8566/tcp

# Prometheus (if exposing metrics)
sudo ufw allow 26680/tcp

# EVM Metrics (if exposing EVM metrics)
sudo ufw allow 6085/tcp

# Geth Metrics (if exposing Geth metrics)
sudo ufw allow 8120/tcp
```

**Note:** The `/tcp` protocol specification is optional in UFW. You can use either `sudo ufw allow 26676/tcp` or `sudo ufw allow 26676` - both work the same way.
{{< /tab >}}
{{< tab "macOS" >}}
**Recommended:** macOS typically allows incoming connections by default, so you may not need to configure anything. However, we recommend verifying your firewall settings.

**First Option - System Preferences (Recommended):**
Use the built-in graphical interface to configure firewall rules:
1. Open **System Preferences** (or **System Settings** on newer macOS versions)
2. Go to **Security & Privacy** > **Firewall**
3. Click the lock icon and enter your password to make changes
4. Click **Firewall Options...**
5. Add rules to permitir conexiones entrantes for the optional ports you want to expose (9110, 9111, 1337, 8565, 8566, 26680, 6085, 8120)

**Second Option - Command Line (Advanced):**
If you prefer command-line configuration, you can modify `/etc/pf.conf`:

```bash
# Edit /etc/pf.conf and add rules for each port you want to expose:
# pass in proto tcp from any to any port 9110  # gRPC
# pass in proto tcp from any to any port 9111  # gRPC-Web
# pass in proto tcp from any to any port 1337  # REST API
# pass in proto tcp from any to any port 8565  # JSON-RPC HTTP
# pass in proto tcp from any to any port 8566  # JSON-RPC WebSocket
# pass in proto tcp from any to any port 26680 # Prometheus
# pass in proto tcp from any to any port 6085  # EVM Metrics
# pass in proto tcp from any to any port 8120  # Geth Metrics

# Then reload the firewall:
sudo pfctl -f /etc/pf.conf
```
{{< /tab >}}
{{< tab "Windows" >}}
```powershell
# gRPC (if exposing gRPC API)
New-NetFirewallRule -DisplayName "Drive gRPC" -Direction Inbound -LocalPort 9110 -Protocol TCP -Action Allow

# gRPC-Web (if exposing gRPC-Web API)
New-NetFirewallRule -DisplayName "Drive gRPC-Web" -Direction Inbound -LocalPort 9111 -Protocol TCP -Action Allow

# REST API (if exposing REST API)
New-NetFirewallRule -DisplayName "Drive REST API" -Direction Inbound -LocalPort 1337 -Protocol TCP -Action Allow

# JSON-RPC HTTP (if exposing Ethereum-compatible API)
New-NetFirewallRule -DisplayName "Drive JSON-RPC HTTP" -Direction Inbound -LocalPort 8565 -Protocol TCP -Action Allow

# JSON-RPC WebSocket (if exposing WebSocket API)
New-NetFirewallRule -DisplayName "Drive JSON-RPC WS" -Direction Inbound -LocalPort 8566 -Protocol TCP -Action Allow

# Prometheus (if exposing metrics)
New-NetFirewallRule -DisplayName "Drive Prometheus" -Direction Inbound -LocalPort 26680 -Protocol TCP -Action Allow

# EVM Metrics (if exposing EVM metrics)
New-NetFirewallRule -DisplayName "Drive EVM Metrics" -Direction Inbound -LocalPort 6085 -Protocol TCP -Action Allow

# Geth Metrics (if exposing Geth metrics)
New-NetFirewallRule -DisplayName "Drive Geth Metrics" -Direction Inbound -LocalPort 8120 -Protocol TCP -Action Allow
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
