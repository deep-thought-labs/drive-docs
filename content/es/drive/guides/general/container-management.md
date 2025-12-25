---
title: "Gestión de Contenedores"
weight: 5211
---

Aprende a gestionar contenedores de Drive usando el script `drive.sh`. Todos los servicios de Drive usan este script para operaciones de gestión.

## ¿Qué es drive.sh?

El script `drive.sh` es un **wrapper alrededor de `docker compose`**. Esto significa que funciona como una capa de abstracción que simplifica y mejora el uso de Docker Compose, pero mantiene la misma sintaxis básica.

### Ventajas de usar drive.sh

- ✅ **Manejo automático de permisos** - Configura automáticamente los permisos de `persistent-data`
- ✅ **Funciona con o sin `sudo`** - Detecta y maneja ambos casos automáticamente
- ✅ **Interfaz consistente** - Los mismos comandos funcionan en todos los servicios
- ✅ **Gestión simplificada** - Abstrae la complejidad de Docker Compose

## Ubicación del Script

Cada servicio tiene su propio script `drive.sh` en su directorio:

```bash
cd services/<service-name>
./drive.sh <comando>
```

**Importante:** Siempre navega al directorio del servicio antes de ejecutar comandos con `drive.sh`.

## Comandos Disponibles

### 🚀 Iniciar Servicio

Inicia el servicio en modo daemon (en segundo plano):

```bash
./drive.sh up -d
```

Este comando crea e inicia el contenedor Docker del servicio.

### 📊 Mostrar Estado del Contenedor

Verifica el estado actual del contenedor:

```bash
./drive.sh ps
```

Muestra información sobre el contenedor: si está ejecutándose, cuándo se inició, etc.

### ⏹️ Detener Servicio

Detiene el servicio de forma controlada:

```bash
./drive.sh stop
```

El contenedor se detiene pero no se elimina, por lo que puedes reiniciarlo más tarde.

### 🗑️ Detener y Eliminar Contenedor

Detiene el servicio y elimina el contenedor:

```bash
./drive.sh down
```

**Nota:** Esto elimina el contenedor pero **no** elimina los datos persistentes almacenados en `persistent-data/`.

### ▶️ Iniciar Servicio (si está detenido)

Si el servicio está detenido pero el contenedor aún existe, puedes iniciarlo:

```bash
./drive.sh start
```

### 🔄 Reiniciar Servicio

Reinicia un servicio que ya está ejecutándose:

```bash
./drive.sh restart
```

Útil cuando necesitas aplicar cambios de configuración o resolver problemas temporales.

### 📋 Ver Registros del Contenedor

Visualiza los logs del contenedor en tiempo real:

```bash
./drive.sh logs
```

Para ver los últimos logs y salir, presiona `Ctrl+C`.

## Comandos que Requieren Nombre de Contenedor

Algunos comandos necesitan que especifiques el nombre del contenedor. Estos son comandos que ejecutan acciones **dentro** del contenedor:

### Ejecutar Comandos Dentro del Contenedor

Para ejecutar comandos dentro del contenedor, usa `exec`:

```bash
./drive.sh exec <nombre-contenedor> <comando>
```

**Ejemplos:**
```bash
# Abrir la interfaz gráfica
./drive.sh exec infinite node-ui

# Ejecutar cualquier comando dentro del contenedor
./drive.sh exec infinite node-keys list
./drive.sh exec infinite node-start
```

**Equivalente a:**
```bash
docker compose exec <nombre-contenedor> <comando>
```

### 💻 Acceder a la Shell del Contenedor

Abre una sesión de shell dentro del contenedor:

```bash
./drive.sh exec <nombre-contenedor> bash
```

**Ejemplo:**
```bash
cd services/node0-infinite
./drive.sh exec infinite bash
```

Útil para depuración, inspección de archivos dentro del contenedor, o ejecutar comandos manuales.

> [!NOTE]
> **Nombres de Contenedores**
>
> Estos comandos requieren especificar el nombre del contenedor. Para conocer los nombres correctos de contenedores para cada servicio, consulta la sección [Nombres de Contenedores por Servicio](#nombres-de-contenedores-por-servicio) más abajo en este documento.

## Nombres de Contenedores por Servicio

Algunos comandos (como `exec` y `bash`) requieren que especifiques el **nombre del contenedor**. Cada servicio tiene un nombre de contenedor único definido en su archivo `docker-compose.yml` bajo `container_name`.

### Tabla de Referencia

| Servicio | Nombre del Contenedor | Ejemplo de Comando |
|----------|----------------------|-------------------|
| `node0-infinite` | `infinite` | `./drive.sh exec infinite node-ui` |
| `node1-infinite-testnet` | `infinite-testnet` | `./drive.sh exec infinite-testnet node-ui` |
| `node2-infinite-creative` | `infinite-creative` | `./drive.sh exec infinite-creative node-ui` |
| `node3-qom` | `qom` | `./drive.sh exec qom node-ui` |

### Ejemplos de Uso

Aquí tienes algunos ejemplos prácticos de cómo usar los nombres de contenedores con diferentes servicios:

```bash
# Infinite Mainnet (node0-infinite)
cd services/node0-infinite
./drive.sh exec infinite node-ui          # Abrir interfaz gráfica
./drive.sh exec infinite bash            # Acceder a shell del contenedor
./drive.sh exec infinite node-keys list   # Listar claves

# Infinite Testnet (node1-infinite-testnet)
cd services/node1-infinite-testnet
./drive.sh exec infinite-testnet node-ui
./drive.sh exec infinite-testnet bash

# Infinite Creative (node2-infinite-creative)
cd services/node2-infinite-creative
./drive.sh exec infinite-creative node-ui
./drive.sh exec infinite-creative bash

# QOM Network (node3-qom)
cd services/node3-qom
./drive.sh exec qom node-ui
./drive.sh exec qom bash
```

> [!NOTE]
> **Documentación Específica de Comandos**
>
> Para comandos específicos como los comandos de blockchain (por ejemplo, `node-keys`, `node-start`, `node-init`, etc.) y otros comandos especializados, consulta la documentación específica correspondiente:
>
> - **Comandos de Blockchain Nodes**: Consulta las guías en [Nodos Blockchain]({{< relref "../../guides/blockchain-nodes" >}}) para comandos específicos de nodos blockchain
> - **Otros comandos especializados**: Cada tipo de servicio puede tener comandos específicos documentados en su sección correspondiente

### Cómo Verificar el Nombre del Contenedor

Si no estás seguro del nombre del contenedor para tu servicio:

1. **Usar `./drive.sh ps`**: Muestra el nombre del contenedor en la lista
   ```bash
   cd services/node0-infinite
   ./drive.sh ps
   ```

2. **Revisar `docker-compose.yml`**: El nombre está definido bajo `container_name`
   ```bash
   cat docker-compose.yml | grep container_name
   ```

**Importante:** 
- El nombre del contenedor está definido en el archivo `docker-compose.yml` de cada servicio
- Siempre usa el nombre correcto del contenedor según el servicio en el que estés trabajando
- La mayoría de comandos de gestión (up, down, stop, start, ps, logs) **NO requieren** especificar el nombre del contenedor
- Solo los comandos que ejecutan acciones dentro del contenedor (`exec`, `bash`) requieren el nombre
