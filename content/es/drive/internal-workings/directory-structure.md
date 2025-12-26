---
title: "Estructura Interna de Directorios"
weight: 403
---

El sistema Drive organiza sus archivos y directorios de manera estructurada para mantener separación de responsabilidades y facilitar la gestión. Esta sección documenta la estructura completa de directorios y el propósito de cada uno.

## Estructura Principal

```
/home/ubuntu/
├── .infinited/              # Directorio principal del nodo
│   ├── config/              # Archivos de configuración
│   │   ├── genesis.json     # Archivo genesis de la blockchain
│   │   ├── config.toml      # Configuración del nodo
│   │   └── ...              # Otros archivos de configuración
│   ├── data/                # Datos de la blockchain
│   │   ├── blocks/          # Bloques descargados
│   │   ├── state.db/        # Base de datos de estado
│   │   └── ...              # Otros datos de blockchain
│   └── keyring-file/        # Keyring (claves criptográficas)
│       └── ...              # Archivos de claves
│
├── .node/                   # Directorio de control del nodo
│   ├── node.pid             # PID del proceso del nodo
│   ├── supervisor.pid       # PID del proceso supervisor
│   └── auto-start           # Flag de auto-start
│
└── (otros archivos del usuario)

/var/log/node/               # Logs del sistema
├── node.log                 # Log principal del nodo
└── supervisor.log        # Log del supervisor

/usr/local/bin/              # Binarios y scripts del sistema
├── infinited                # Binario del nodo blockchain
├── node-init                # Script de inicialización
├── node-start               # Script de inicio
├── node-stop                # Script de detención
├── node-logs                # Script de visualización de logs
├── node-keys                # Script de gestión de claves
├── node-supervisor          # Script del supervisor
├── node-auto-start          # Script de auto-start
└── ...                      # Otros scripts
```

## Directorios Detallados

### 1. `/home/ubuntu/.infinited/` - Directorio Principal del Nodo

Este es el directorio home del nodo blockchain, donde se almacenan todos los datos y configuraciones del nodo.

**Propósito:**
- Contiene toda la configuración del nodo
- Almacena los datos de la blockchain
- Contiene el keyring con las claves criptográficas

**Subdirectorios:**

#### `config/`
Contiene todos los archivos de configuración del nodo.

**Archivos importantes:**
- `genesis.json` - Archivo genesis de la blockchain (define el estado inicial)
- `config.toml` - Configuración principal del nodo (puertos, peers, etc.)
- `app.toml` - Configuración de la aplicación
- `client.toml` - Configuración del cliente

**Variables relacionadas:**
- `NODE_HOME` = `/home/ubuntu/.infinited`
- `NODE_GENESIS_FILE` = `${NODE_HOME}/config/genesis.json`
- `NODE_CONFIG_FILE` = `${NODE_HOME}/config/config.toml`

#### `data/`
Contiene todos los datos de la blockchain que el nodo ha descargado y procesado.

**Contenido:**
- `blocks/` - Bloques de la blockchain
- `state.db/` - Base de datos de estado (estado actual de la blockchain)
- `application.db/` - Base de datos de la aplicación
- Otros archivos de datos generados por el nodo

**Nota:** Este directorio puede crecer significativamente a medida que el nodo sincroniza con la red.

#### `keyring-file/`
Contiene las claves criptográficas del nodo.

**Contenido:**
- Archivos de claves encriptadas
- Información del keyring
- Claves del validador (si aplica)

**Variable relacionada:**
- `NODE_KEYRING_BACKEND` = `file` (siempre usa keyring de archivo)

**Ubicación completa:**
```
/home/ubuntu/.infinited/keyring-file/
```

### 2. `/home/ubuntu/.node/` - Directorio de Control

Este directorio contiene archivos de control y estado del sistema de gestión del nodo.

**Propósito:**
- Almacenar PIDs de procesos
- Mantener flags de control
- Gestionar el estado del sistema

**Archivos:**

#### `node.pid`
Contiene el PID (Process ID) del proceso del nodo blockchain en ejecución.

**Formato:**
```
12345
```

**Uso:**
- Leído por `node-stop` para detener el nodo
- Actualizado por `node-start` cuando el nodo inicia
- Eliminado cuando el nodo se detiene

**Variable relacionada:**
- `NODE_PID_FILE` = `~/.node/node.pid`

#### `supervisor.pid`
Contiene el PID del proceso supervisor.

**Formato:**
```
12346
```

**Uso:**
- Leído por `node-stop` para detener el supervisor
- Actualizado por `node-start` cuando el supervisor inicia
- Eliminado cuando el supervisor se detiene

**Variable relacionada:**
- `NODE_SUPERVISOR_PID_FILE` = `~/.node/supervisor.pid`

#### `auto-start`
Archivo flag que indica que el nodo debe iniciarse automáticamente.

**Formato:**
- Archivo vacío (su existencia es lo importante)

**Uso:**
- Creado por `node-start` cuando el usuario inicia el nodo manualmente
- Eliminado por `node-stop` cuando el usuario detiene el nodo
- Verificado por `node-auto-start.sh` al iniciar el contenedor
- Verificado por `node-supervisor.sh` para decidir si reiniciar el nodo

**Variable relacionada:**
- `NODE_AUTO_START_FLAG` = `~/.node/auto-start`

**Variable relacionada:**
- `NODE_CONTROL_DIR` = `/home/ubuntu/.node`

### 3. `/var/log/node/` - Directorio de Logs

Este directorio contiene todos los logs del sistema del nodo.

**Propósito:**
- Almacenar logs del nodo blockchain
- Almacenar logs del supervisor
- Facilitar debugging y monitoreo

**Archivos:**

#### `node.log`
Log principal del nodo blockchain.

**Contenido:**
- Salida estándar y error del proceso `infinited`
- Mensajes de sincronización
- Errores y advertencias del nodo
- Información de conexión con peers

**Variable relacionada:**
- `NODE_LOG_FILE` = `/var/log/node/node.log`

**Uso:**
- Visualizado con `node-logs` o `node-logs -f` (seguimiento en tiempo real)
- Monitoreado por el supervisor para detectar problemas

#### `supervisor.log`
Log del proceso supervisor.

**Contenido:**
- Eventos de monitoreo
- Detección de nodo detenido
- Intentos de reinicio
- Detención de supervisión

**Variable relacionada:**
- `NODE_SUPERVISOR_LOG_FILE` = `/var/log/node/supervisor.log`

**Formato de entradas:**
```
[2024-01-15 10:30:45] Node not detected, attempting to restart...
[2024-01-15 10:30:50] Auto-start flag removed, stopping supervision...
```

### 4. `/usr/local/bin/` - Binarios y Scripts del Sistema

Este directorio contiene los binarios y scripts ejecutables del sistema.

**Propósito:**
- Almacenar el binario del nodo blockchain
- Contener todos los scripts de gestión del nodo
- Estar en el PATH del sistema para fácil acceso

**Archivos importantes:**

#### `infinited`
Binario principal del nodo blockchain.

**Ubicación:**
```
/usr/local/bin/infinited
```

**Variable relacionada:**
- `NODE_BINARY_PATH` = `/usr/local/bin/infinited`

**Uso:**
- Ejecutado directamente por los scripts de gestión
- Proceso principal del nodo blockchain

#### Scripts de Gestión

Todos los scripts tienen la extensión `.sh` removida y están en `/usr/local/bin/`:

- `node-init` - Inicialización del nodo
- `node-start` - Inicio del nodo
- `node-stop` - Detención del nodo
- `node-logs` - Visualización de logs
- `node-keys` - Gestión de claves
- `node-supervisor` - Supervisor del nodo
- `node-auto-start` - Auto-start al iniciar contenedor
- `node-clean-data` - Limpieza de datos
- `node-process-status` - Estado del proceso
- `node-network-diagnosis` - Diagnóstico de red
- `node-ui` - Interfaz gráfica de usuario
- Y otros scripts de utilidad

## Permisos y Propiedad

### Usuario y Grupo

Todos los archivos y directorios pertenecen al usuario `ubuntu` (UID 1000, GID 1000).

**Configuración:**
```bash
USER 1000:1000
```

**Aplicado a:**
- `/home/ubuntu/` y todo su contenido
- `/var/log/node/` y todo su contenido
- Scripts en `/usr/local/bin/node-*`

### Permisos de Directorios

Los directorios principales tienen permisos estándar:

- `/home/ubuntu/.infinited/` - `755` (rwxr-xr-x)
- `/home/ubuntu/.node/` - `755` (rwxr-xr-x)
- `/var/log/node/` - `755` (rwxr-xr-x)

### Permisos de Archivos

- Archivos de configuración - `644` (rw-r--r--)
- Scripts ejecutables - `755` (rwxr-xr-x)
- Archivos PID - `644` (rw-r--r--)
- Logs - `644` (rw-r--r--)

## Creación de Directorios

Los directorios se crean automáticamente cuando son necesarios:

**En el Dockerfile:**
```dockerfile
RUN mkdir -p /home/ubuntu/.infinited /var/log/node /home/ubuntu/.node && \
    chown -R 1000:1000 /home/ubuntu /var/log/node
```

**En los scripts:**
```bash
# Crear directorio de control si no existe
mkdir -p "$NODE_CONTROL_DIR"

# Crear directorio de logs si no existe
mkdir -p "$(dirname "$NODE_LOG_FILE")"
```

## Persistencia de Datos

### Datos Persistentes

Los siguientes directorios contienen datos que deben persistir:

1. **`~/.infinited/`** - Toda la configuración y datos del nodo
2. **`~/.node/`** - Estado de control (aunque se puede regenerar)

### Datos No Persistentes

Los siguientes archivos se regeneran automáticamente:

1. **`~/.node/node.pid`** - Se crea al iniciar, se elimina al detener
2. **`~/.node/supervisor.pid`** - Se crea al iniciar supervisor, se elimina al detener
3. **`/var/log/node/*.log`** - Se pueden regenerar (aunque contienen información valiosa)

## Mapeo con Docker Volumes

En un entorno Docker, estos directorios típicamente se mapean a volúmenes persistentes:

```yaml
volumes:
  - ./persistent-data/.infinited:/home/ubuntu/.infinited
  - ./persistent-data/.node:/home/ubuntu/.node
  - ./persistent-data/logs:/var/log/node
```

## Variables de Configuración Relacionadas

```bash
NODE_HOME="/home/ubuntu/.infinited"
NODE_CONTROL_DIR="/home/ubuntu/.node"
NODE_LOG_FILE="/var/log/node/node.log"
NODE_SUPERVISOR_LOG_FILE="/var/log/node/supervisor.log"
NODE_BINARY_PATH="/usr/local/bin/infinited"
NODE_GENESIS_FILE="${NODE_HOME}/config/genesis.json"
NODE_CONFIG_FILE="${NODE_HOME}/config/config.toml"
NODE_PID_FILE="${NODE_CONTROL_DIR}/node.pid"
NODE_SUPERVISOR_PID_FILE="${NODE_CONTROL_DIR}/supervisor.pid"
NODE_AUTO_START_FLAG="${NODE_CONTROL_DIR}/auto-start"
```

## Ver También

- [Sistema de Configuración Interna]({{< relref "configuration-system" >}}) - Variables y configuración
- [Sistema de Logs Interno]({{< relref "logging-system" >}}) - Detalles sobre el sistema de logs
- [Arquitectura del Contenedor]({{< relref "container-architecture" >}}) - Cómo se crean estos directorios en el build

