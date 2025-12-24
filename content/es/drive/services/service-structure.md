---
title: "Estructura del Servicio"
weight: 530
---

## Arquitectura Overview

Los servicios de Drive son contenedores Docker definidos usando Docker Compose. Cada servicio tiene:
- `docker-compose.yml` - Service definition and configuration
- `drive.sh` - Management wrapper script
- `persistent-data/` - Service-specific data (user-owned, not in repository)

## Service Directory Structure

```
services/
├── <service-name>/
│   ├── docker-compose.yml    # Container definition
│   ├── drive.sh              # Management script
│   └── persistent-data/       # User data (git-ignored)
```

## Configuración de Docker Compose

Los servicios se definen en `docker-compose.yml`, que contiene todas las configuraciones específicas del servicio:

- **Imagen y versión del contenedor** - La imagen Docker utilizada para el servicio
- **Variables de entorno** - Configuración del servicio a través de variables de entorno (ver [Variables de Entorno]({{< relref "environment" >}}))
- **Montajes de volúmenes** - Directorios de datos persistentes mapeados al contenedor
- **Mapeo de puertos** - Puertos de red expuestos por el servicio (ver [Estrategia de Puertos]({{< relref "ports" >}}))
- **Configuración de red** - Configuración de red del contenedor

El archivo `docker-compose.yml` es el punto central de configuración para cada servicio, definiendo cómo se ejecuta el contenedor, qué recursos usa y cómo se conecta a tu sistema.

Para un análisis técnico detallado del archivo `docker-compose.yml`, consulta [Estructura de Docker Compose]({{< relref "technical/docker-compose-structure" >}}).

## drive.sh Script

El script `drive.sh` proporciona gestión consistente en todos los servicios:

### Comandos Básicos

Para ver todos los comandos disponibles y su uso detallado, consulta [Gestión de Contenedores]({{< relref "../guides/general/container-management" >}}) en las Guías.

### Características del Script

- **Manejo automático de permisos** - Funciona con o sin `sudo`
- **Interfaz consistente** - Los mismos comandos funcionan en todos los servicios
- **Gestión simplificada** - Abstrae la complejidad de Docker Compose

Para un análisis técnico detallado del script `drive.sh`, incluyendo cómo gestiona los permisos, consulta [Análisis del Script drive.sh]({{< relref "technical/drive-script-analysis" >}}).

## Datos Persistentes

Cada directorio `persistent-data/` del servicio:
- Se almacena localmente en tu sistema
- Nunca se comparte ni sincroniza
- Contiene datos específicos del servicio:
  - Nodos blockchain: datos de cadena, claves, configuración

**Importante:** Los permisos de `persistent-data/` son gestionados automáticamente por el script `drive.sh`. Para documentación técnica completa sobre cómo Drive maneja los permisos, consulta [Gestión de Permisos]({{< relref "technical/permission-handling" >}}).

## Tipos de Servicios

### Nodos Blockchain

All blockchain nodes share the same Docker image but differ in:
- Network/chain configuration
- Binary download URLs
- Genesis files
- Port assignments

See [Catálogo de Servicios]({{< relref "catalog" >}}) for the complete list of all blockchain node services and their configurations.
