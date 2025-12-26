---
title: "Sistema de Configuración Interna"
weight: 404
---

El sistema Drive utiliza un sistema de configuración centralizado basado en variables de entorno y un archivo de configuración compartido (`node-config.sh`). Esta sección documenta cómo funciona este sistema de configuración.

## Arquitectura del Sistema de Configuración

### Archivo Central: `node-config.sh`

Todos los scripts del sistema cargan la configuración desde un archivo centralizado:

```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/node-config.sh"
```

**Ubicación en el contenedor:**
```
/usr/local/bin/node-config.sh
```

**Propósito:**
- Definir valores por defecto para todas las variables
- Cargar variables de entorno del contenedor
- Proporcionar funciones de utilidad para configuración
- Validar la configuración antes de usar

## Variables de Configuración

### Configuración Core

#### Identificación del Nodo

```bash
NODE_CHAIN_ID="${NODE_CHAIN_ID:-infinite_421018-1}"
NODE_EVM_CHAIN_ID="${NODE_EVM_CHAIN_ID:-421018}"
```

**Propósito:**
- `NODE_CHAIN_ID`: Identificador de la cadena blockchain
- `NODE_EVM_CHAIN_ID`: Identificador de la cadena para compatibilidad EVM

**Valores por defecto:**
- Chain ID: `infinite_421018-1`
- EVM Chain ID: `421018`

**Uso:**
- Pasados como argumentos al binario `infinited`
- Usados para construir el patrón de detección de procesos
- Identifican la red blockchain específica

#### Rutas Fijas

```bash
NODE_HOME="/home/ubuntu/.infinited"
NODE_BINARY_PATH="/usr/local/bin/infinited"
NODE_LOG_FILE="/var/log/node/node.log"
NODE_CONTROL_DIR="/home/ubuntu/.node"
```

**Propósito:**
- `NODE_HOME`: Directorio principal del nodo (configuración y datos)
- `NODE_BINARY_PATH`: Ruta al binario ejecutable del nodo
- `NODE_LOG_FILE`: Archivo donde se escriben los logs del nodo
- `NODE_CONTROL_DIR`: Directorio para archivos de control (PIDs, flags)

**Nota:** Estas rutas son fijas y no se pueden cambiar mediante variables de entorno.

#### Configuración de Genesis

```bash
NODE_GENESIS_URL="${NODE_GENESIS_URL:-https://raw.githubusercontent.com/deep-thought-labs/infinite/migration/config/genesis/assets/pre-mainet-genesis.json}"
```

**Propósito:**
- URL desde donde descargar el archivo genesis oficial
- Usado durante la inicialización del nodo

**Valor por defecto:**
- URL del repositorio oficial de Infinite

#### Configuración de Red P2P

```bash
NODE_P2P_SEEDS="${NODE_P2P_SEEDS:-}"
NODE_PERSISTENT_PEERS="${NODE_PERSISTENT_PEERS:-}"
NODE_P2P_EXTERNAL_ADDRESS="${NODE_P2P_EXTERNAL_ADDRESS:-}"
```

**Propósito:**
- `NODE_P2P_SEEDS`: Nodos seed para descubrimiento inicial de peers
- `NODE_PERSISTENT_PEERS`: Peers persistentes para conexión directa
- `NODE_P2P_EXTERNAL_ADDRESS`: Dirección externa del nodo (formato: `IP:puerto`)

**Formato:**
- Seeds y peers: Lista separada por comas de direcciones `ID@IP:puerto`
- External address: `IP:puerto` o `dominio:puerto`

**Ejemplo:**
```bash
NODE_P2P_SEEDS="abc123@1.2.3.4:26656,def456@5.6.7.8:26656"
NODE_PERSISTENT_PEERS="abc123@1.2.3.4:26656"
NODE_P2P_EXTERNAL_ADDRESS="example.com:26656"
```

#### Configuración de Keyring

```bash
NODE_KEYRING_BACKEND="file"
```

**Propósito:**
- Define el backend del keyring (siempre `file` en este sistema)
- No se puede cambiar, es fijo

### Rutas Derivadas

Estas rutas se construyen a partir de las rutas base:

```bash
NODE_GENESIS_FILE="${NODE_HOME}/config/genesis.json"
NODE_CONFIG_FILE="${NODE_HOME}/config/config.toml"
NODE_PID_FILE="${NODE_CONTROL_DIR}/node.pid"
NODE_SUPERVISOR_PID_FILE="${NODE_CONTROL_DIR}/supervisor.pid"
NODE_AUTO_START_FLAG="${NODE_CONTROL_DIR}/auto-start"
NODE_SUPERVISOR_LOG_FILE="${NODE_SUPERVISOR_LOG_FILE:-/var/log/node/supervisor.log}"
```

**Propósito:**
- Simplificar referencias a archivos importantes
- Centralizar la lógica de construcción de rutas
- Facilitar cambios futuros en la estructura

### Patrón de Detección de Proceso

```bash
NODE_PROCESS_PATTERN="${NODE_BINARY_PATH} start.*--chain-id ${NODE_CHAIN_ID}"
```

**Propósito:**
- Patrón usado por `pgrep` para identificar el proceso del nodo
- Permite múltiples nodos en el mismo host (diferentes chain-id)
- Evita falsos positivos con otros procesos

**Ejemplo de patrón:**
```
/usr/local/bin/infinited start.*--chain-id infinite_421018-1
```

## Funciones de Utilidad

### `build_node_start_command()`

Construye el comando completo para iniciar el nodo con todos los argumentos necesarios.

**Implementación:**
```bash
build_node_start_command() {
    local cmd="${NODE_BINARY_PATH} start"
    
    # Argumentos requeridos
    cmd="${cmd} --home ${NODE_HOME}"
    cmd="${cmd} --chain-id ${NODE_CHAIN_ID}"
    cmd="${cmd} --evm.evm-chain-id ${NODE_EVM_CHAIN_ID}"
    
    # Argumentos opcionales (solo si están definidos)
    if [ -n "${NODE_P2P_SEEDS}" ]; then
        cmd="${cmd} --p2p.seeds \"${NODE_P2P_SEEDS}\""
    fi
    
    if [ -n "${NODE_PERSISTENT_PEERS}" ]; then
        cmd="${cmd} --p2p.persistent_peers \"${NODE_PERSISTENT_PEERS}\""
    fi
    
    if [ -n "${NODE_P2P_EXTERNAL_ADDRESS}" ]; then
        cmd="${cmd} --p2p.external_address \"${NODE_P2P_EXTERNAL_ADDRESS}\""
    fi
        
    echo "$cmd"
}
```

**Características:**
- Construye el comando dinámicamente basado en la configuración
- Maneja correctamente argumentos con comas y caracteres especiales usando comillas
- Solo incluye argumentos opcionales si están definidos

**Uso:**
```bash
START_CMD=$(build_node_start_command)
eval ${START_CMD} > ${NODE_LOG_FILE} 2>&1
```

### `validate_node_config()`

Valida que la configuración requerida esté presente y sea válida.

**Implementación:**
```bash
validate_node_config() {
    local errors=0
    
    if [ ! -f "${NODE_BINARY_PATH}" ]; then
        echo "Error: Binary not found at ${NODE_BINARY_PATH}" >&2
        errors=$((errors + 1))
    fi
    
    if [ -z "${NODE_CHAIN_ID}" ]; then
        echo "Error: NODE_CHAIN_ID is not set" >&2
        errors=$((errors + 1))
    fi
    
    if [ -z "${NODE_EVM_CHAIN_ID}" ]; then
        echo "Error: NODE_EVM_CHAIN_ID is not set" >&2
        errors=$((errors + 1))
    fi
    
    return $errors
}
```

**Validaciones:**
1. Verifica que el binario existe en la ruta especificada
2. Verifica que `NODE_CHAIN_ID` está definido
3. Verifica que `NODE_EVM_CHAIN_ID` está definido

**Uso:**
```bash
if ! validate_node_config; then
    print_error "Invalid node configuration"
    exit 1
fi
```

## Carga de Variables de Entorno

### Orden de Precedencia

1. **Variables de entorno del contenedor** (más alta prioridad)
2. **Valores por defecto en `node-config.sh`** (si la variable no está definida)

**Sintaxis:**
```bash
VARIABLE="${VARIABLE:-valor_por_defecto}"
```

**Ejemplo:**
```bash
NODE_CHAIN_ID="${NODE_CHAIN_ID:-infinite_421018-1}"
```

Si `NODE_CHAIN_ID` está definido en el entorno, se usa ese valor. Si no, se usa `infinite_421018-1`.

### Variables de Entorno en Docker

Las variables de entorno se pueden definir en:

1. **`docker-compose.yml`:**
   ```yaml
   environment:
     - NODE_CHAIN_ID=infinite_421018-1
     - NODE_P2P_SEEDS=abc123@1.2.3.4:26656
   ```

2. **Archivo `.env`:**
   ```
   NODE_CHAIN_ID=infinite_421018-1
   NODE_P2P_SEEDS=abc123@1.2.3.4:26656
   ```

3. **Línea de comando:**
   ```bash
   docker compose run -e NODE_CHAIN_ID=test-chain infinite-drive node-start
   ```

## Exportación de Variables

Todas las variables se exportan para que estén disponibles en los scripts hijos:

```bash
export NODE_CHAIN_ID="${NODE_CHAIN_ID:-infinite_421018-1}"
export NODE_HOME="/home/ubuntu/.infinited"
# ... etc
```

**Propósito:**
- Hacer las variables disponibles para scripts que se ejecutan desde otros scripts
- Permitir que funciones accedan a las variables

## Uso en Scripts

### Carga Estándar

Todos los scripts cargan la configuración de la misma manera:

```bash
#!/bin/bash

# Obtener directorio del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Cargar configuración centralizada
source "${SCRIPT_DIR}/node-config.sh"

# Cargar estilos (si es necesario)
source "${SCRIPT_DIR}/styles.sh"
```

**Nota:** `node-config.sh` debe estar en el mismo directorio que los scripts, o en `/usr/local/bin/` donde se instalan.

## Configuración por Servicio

Cada servicio de nodo blockchain puede tener su propia configuración mediante variables de entorno en `docker-compose.yml`:

```yaml
services:
  node0-infinite:
    environment:
      - NODE_CHAIN_ID=infinite_421018-1
      - NODE_EVM_CHAIN_ID=421018
      - NODE_P2P_SEEDS=abc123@1.2.3.4:26656
      - NODE_GENESIS_URL=https://...
```

Esto permite que múltiples nodos con diferentes configuraciones coexistan en el mismo sistema.

## Validación en Tiempo de Ejecución

Los scripts validan la configuración antes de realizar operaciones críticas:

```bash
# En node-start.sh
if ! validate_node_config; then
    print_error "Invalid node configuration. Please check environment variables."
    exit 1
fi
```

**Ventajas:**
- Detecta problemas de configuración temprano
- Proporciona mensajes de error claros
- Previene ejecución con configuración inválida

## Resumen de Variables

### Variables Requeridas (con valores por defecto)
- `NODE_CHAIN_ID` - ID de la cadena
- `NODE_EVM_CHAIN_ID` - ID de la cadena EVM

### Variables Opcionales
- `NODE_P2P_SEEDS` - Nodos seed
- `NODE_PERSISTENT_PEERS` - Peers persistentes
- `NODE_P2P_EXTERNAL_ADDRESS` - Dirección externa
- `NODE_GENESIS_URL` - URL del genesis
- `NODE_SUPERVISOR_LOG_FILE` - Ruta del log del supervisor

### Variables Fijas (no configurables)
- `NODE_HOME` - Directorio home del nodo
- `NODE_BINARY_PATH` - Ruta al binario
- `NODE_LOG_FILE` - Archivo de log
- `NODE_CONTROL_DIR` - Directorio de control
- `NODE_KEYRING_BACKEND` - Backend del keyring

## Ver También

- [Estructura Interna de Directorios]({{< relref "directory-structure" >}}) - Dónde se almacenan los archivos de configuración
- [Arquitectura del Contenedor]({{< relref "container-architecture" >}}) - Cómo se instala `node-config.sh`
- [Scripts Internos del Contenedor]({{< relref "internal-scripts" >}}) - Cómo los scripts usan la configuración

