---
title: "Data del Nodo"
weight: 5
---

La **data del nodo** es toda la información que un nodo blockchain almacena para su funcionamiento, incluyendo archivos de configuración, claves criptográficas, datos de la blockchain y estado de sincronización.

## ¿Qué es la Data del Nodo?

La data del nodo comprende todos los archivos y directorios que el nodo necesita para operar:

- **Archivos de configuración** - Parámetros de operación del nodo
- **Claves criptográficas** - Identidades del nodo y validador
- **Archivo génesis** - Estado inicial de la blockchain
- **Base de datos de la blockchain** - Historial de bloques y transacciones
- **Estado de la aplicación** - Estado actual de la blockchain
- **Logs y datos temporales** - Información de depuración y operación

## Ubicación de la Data del Nodo

En Drive, la data del nodo se almacena en el directorio `persistent-data`:

- **Ruta en el host:** `./persistent-data/` (relativa al directorio del servicio)
- **Ruta en el contenedor:** `/home/ubuntu/.infinited/`

### Estructura de Directorios

```
persistent-data/
├── config/              # Archivos de configuración
│   ├── config.toml      # Configuración general del nodo
│   ├── app.toml         # Configuración de la aplicación
│   ├── client.toml      # Configuración del cliente
│   ├── genesis.json     # Archivo génesis de la red
│   └── priv_validator_key.json  # Clave del validador
├── data/                # Base de datos de la blockchain
│   ├── blocks/          # Bloques descargados
│   ├── state.db/        # Base de datos de estado
│   └── application.db   # Base de datos de la aplicación
└── keyring-file/        # Keyring (claves criptográficas de cuenta)
    └── ...              # Archivos de claves encriptadas
```

**Nota:** Los logs del nodo se almacenan en un directorio separado:
- **Ruta en el contenedor:** `/var/log/node/`
- **Ruta en el host:** `./persistent-data/logs/` (si está mapeado como volumen)

## Componentes de la Data del Nodo

### Archivos de Configuración

Los archivos de configuración se crean durante la [inicialización del nodo]({{< relref "node-initialization" >}}) y definen cómo opera el nodo:

- **`config.toml`** - Configuración de red, consenso y P2P
- **`app.toml`** - Configuración de la aplicación blockchain
- **`client.toml`** - Configuración del cliente para interacciones

### Claves Criptográficas

Las claves se generan durante la inicialización y son críticas para la identidad del nodo:

- **[Private Validator Key]({{< relref "private-validator-key" >}})** (`priv_validator_key.json`) - Identifica al validador, ubicada en `config/`
- **Node Key** - Identifica al nodo en la red P2P, generada automáticamente
- **Consensus Key** - Clave para el consenso, generada automáticamente

**Nota:** Las claves de cuenta (account keys) se almacenan en el [keyring]({{< relref "keyring" >}}) en `keyring-file/`, no en `config/`.

### Archivo Génesis

El [archivo génesis]({{< relref "genesis-file" >}}) define el estado inicial de la blockchain y se descarga durante la inicialización.

### Base de Datos de la Blockchain

La base de datos almacena:

- **Historial de bloques** - Todos los bloques sincronizados
- **Transacciones** - Historial de transacciones
- **Estado de la aplicación** - Estado actual de la blockchain
- **Índices** - Para búsquedas rápidas

## Persistencia de la Data

La data del nodo se almacena en el directorio `persistent-data` que está montado como un volumen persistente en Docker. Esto significa que:

- **La data persiste** entre reinicios del contenedor
- **La data se comparte** entre el host y el contenedor
- **La data se respalda** automáticamente si respaldas el directorio `persistent-data`

## Importancia de la Data del Nodo

La data del nodo es crítica porque:

- **Contiene la identidad del nodo** - Las claves definen quién es el nodo
- **Permite la sincronización** - La base de datos almacena el estado de la blockchain
- **Habilita la validación** - El validador necesita su Private Validator Key para firmar bloques
- **Permite la recuperación** - Con la data correcta, puedes restaurar el nodo

## Limpiar la Data del Nodo

En algunos casos, necesitas limpiar la data del nodo:

- **Reinicializar el nodo** - Para cambiar el modo de inicialización
- **Resolver problemas de sincronización** - Para empezar desde cero
- **Cambiar de red** - Para conectarte a una red diferente

> [!WARNING]
> **⚠️ Advertencia: Limpiar la Data**
>
> Limpiar la data del nodo elimina:
> - Todos los bloques sincronizados
> - El estado de la aplicación
> - Las claves (si no están respaldadas)
>
> **Asegúrate de tener respaldos** antes de limpiar la data, especialmente si eres validador.

Para más información sobre cómo eliminar la data del nodo, consulta [Borrar Data del Nodo]({{< relref "../drive/guides/blockchain-nodes/delete-node-data" >}}).

## Respaldo de la Data del Nodo

Para validadores, es crítico respaldar:

- **Private Validator Key** - `priv_validator_key.json` (o la frase semilla si usaste recovery)
- **Archivos de configuración** - Para restaurar la configuración personalizada

Para full nodes, generalmente no es necesario respaldar la data, ya que puede ser regenerada sincronizando con la red.

## Ver También

- [Inicialización de Nodo]({{< relref "node-initialization" >}}) - Qué es la inicialización y qué componentes crea
- [Archivo Génesis]({{< relref "genesis-file" >}}) - Qué es el archivo génesis y su propósito
- [Private Validator Key]({{< relref "private-validator-key" >}}) - Qué es el Private Validator Key
- [Inicialización de Nodo]({{< relref "../drive/guides/blockchain-nodes/initialization" >}}) - Guía práctica para inicializar un nodo
- [Iniciar/Detener Nodo]({{< relref "../drive/guides/blockchain-nodes/start-stop-node" >}}) - Cómo gestionar el nodo

