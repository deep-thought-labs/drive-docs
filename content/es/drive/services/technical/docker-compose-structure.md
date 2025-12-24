---
title: "Estructura de Docker Compose"
weight: 5361
---

> [!WARNING]
> **⚠️ Documentación en Construcción**
>
> Este documento está en construcción y contiene análisis técnico en desarrollo. Está siendo utilizado por los desarrolladores para identificar la mejor solución al problema de permisos entre el sistema host y los contenedores Docker.
>
> **No tomes este documento como una guía de uso aún.** Este es un análisis técnico que puede cambiar significativamente mientras se desarrolla la solución final.

Análisis técnico completo del archivo `docker-compose.yml` utilizado por los servicios de Drive.

## Ubicación del Archivo

Cada servicio tiene su propio archivo `docker-compose.yml` en su directorio:

```
services/
└── <service-name>/
    └── docker-compose.yml
```

## Estructura General

El archivo `docker-compose.yml` define un servicio Docker Compose con la siguiente estructura:

```yaml
services:
  <service-name>:
    # Configuración del contenedor
    image: <docker-image>
    container_name: <container-name>
    restart: unless-stopped
    
    # Configuración de red
    ports:
      - "<host-port>:<container-port>"
    
    # Configuración de volúmenes
    volumes:
      - ./persistent-data:/home/ubuntu/.infinited
    
    # Variables de entorno
    environment:
      VARIABLE_NAME: "value"
```

## Componentes Principales

### Configuración del Contenedor

#### `image`
- **Propósito:** Especifica la imagen Docker a utilizar
- **Ejemplo:** `deepthoughtlabs/infinite-drive:latest`
- **Nota:** La versión de la imagen está definida en la imagen misma

#### `container_name`
- **Propósito:** Define el nombre del contenedor
- **Ejemplo:** `infinite`
- **Nota:** Debe ser único en el sistema host

#### `restart`
- **Propósito:** Política de reinicio automático
- **Valor:** `unless-stopped`
- **Comportamiento:** El contenedor se reiniciará automáticamente a menos que se detenga manualmente

### Configuración de Usuario del Contenedor

**⚠️ Importante:** El archivo `docker-compose.yml` **no especifica explícitamente** el usuario que ejecuta el contenedor. Esto significa que:

- El contenedor utiliza el usuario por defecto definido en la imagen Docker
- Según el script `drive.sh`, el contenedor ejecuta como usuario `ubuntu` con **UID 1000**
- Esta configuración está definida en el Dockerfile de la imagen, no en `docker-compose.yml`

**Implicación:** Para cambiar el UID del contenedor, sería necesario modificar el Dockerfile de la imagen o agregar una configuración `user` en `docker-compose.yml`.

### Configuración de Puertos

```yaml
ports:
  - "<host-port>:<container-port>"
```

- **Formato:** `"HOST_PORT:CONTAINER_PORT"`
- **HOST_PORT:** Puerto en el sistema host (puede variar según el número de servicio)
- **CONTAINER_PORT:** Puerto dentro del contenedor (fijo, definido por la aplicación)
- **Ejemplo:** `"26656:26656"` - Puerto P2P mapeado del host al contenedor

Para más información sobre la estrategia de asignación de puertos, consulta [Estrategia de Puertos]({{< relref "../ports" >}}).

### Configuración de Volúmenes

```yaml
volumes:
  - ./persistent-data:/home/ubuntu/.infinited
```

- **Formato:** `"<host-path>:<container-path>"`
- **Tipo:** Bind mount (montaje directo del sistema de archivos del host)
- **HOST_PATH:** `./persistent-data` - Ruta relativa al directorio del servicio
- **CONTAINER_PATH:** `/home/ubuntu/.infinited` - Ruta dentro del contenedor

**Características importantes:**
- Los bind mounts preservan los UIDs/GIDs numéricos del sistema de archivos
- Docker no traduce nombres de usuario, solo usa UIDs numéricos
- Esto es crítico para la gestión de permisos (ver [Gestión de Permisos]({{< relref "permission-handling" >}}))

### Variables de Entorno

```yaml
environment:
  VARIABLE_NAME: "value"
```

- **Propósito:** Configurar el comportamiento del servicio
- **Alcance:** Disponibles dentro del contenedor durante la ejecución
- **Tipos comunes:**
  - Identificación de cadena (`NODE_CHAIN_ID`, `NODE_EVM_CHAIN_ID`)
  - Configuración de red (`NODE_P2P_SEEDS`, `NODE_PERSISTENT_PEERS`)
  - URLs de recursos (`NODE_GENESIS_URL`)

Para documentación completa de variables de entorno, consulta [Variables de Entorno]({{< relref "../environment" >}}).

## Análisis de Configuración Actual

### Usuario del Contenedor

El `docker-compose.yml` actual **no especifica** un usuario explícito, lo que significa:

1. **Usuario por defecto:** El contenedor ejecuta como el usuario definido en el Dockerfile
2. **UID esperado:** Según `drive.sh`, el contenedor ejecuta como UID 1000 (usuario `ubuntu`)
3. **Implicación:** Si el Dockerfile cambia el UID, habría que actualizar la lógica de permisos en `drive.sh`

### Gestión de Permisos

El `docker-compose.yml` **no gestiona permisos** directamente. La gestión de permisos se realiza en:

- **Script `drive.sh`:** Configura permisos de `persistent-data` antes de ejecutar Docker Compose
- **Docker bind mounts:** Preservan los permisos del sistema de archivos del host

Para detalles técnicos sobre cómo se manejan los permisos, consulta [Gestión de Permisos]({{< relref "permission-handling" >}}).

## Limitaciones y Consideraciones

### Limitaciones Actuales

1. **Usuario fijo:** El contenedor siempre ejecuta como UID 1000 (definido en Dockerfile)
2. **Sin configuración de usuario en Compose:** No hay forma de cambiar el UID desde `docker-compose.yml` sin modificar la imagen
3. **Permisos dependen del host:** Los permisos de `persistent-data` dependen del usuario del host y de la lógica en `drive.sh`

### Consideraciones para Mejoras Futuras

Si se necesita soportar diferentes UIDs:

1. **Opción 1:** Agregar configuración `user` en `docker-compose.yml`:
   ```yaml
   user: "${UID:-1000}:${GID:-1000}"
   ```
   Requeriría pasar variables de entorno UID/GID desde el host.

2. **Opción 2:** Modificar el Dockerfile para aceptar UID/GID como argumentos de construcción.

3. **Opción 3:** Usar un script de entrada (entrypoint) que ajuste el UID al iniciar el contenedor.

## Ver También

- [Análisis del Script drive.sh]({{< relref "drive-script-analysis" >}}) - Cómo el script gestiona los permisos
- [Gestión de Permisos]({{< relref "permission-handling" >}}) - Documentación técnica completa sobre permisos
- [Estructura del Servicio]({{< relref "../service-structure" >}}) - Visión general de la arquitectura

