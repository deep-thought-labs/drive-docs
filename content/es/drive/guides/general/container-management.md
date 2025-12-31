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
- ✅ **Sintaxis simplificada** - Para comandos `node-*`, no necesitas especificar `exec` ni el nombre del servicio
- ✅ **Detección automática de modo interactivo** - Agrega automáticamente `-it` cuando es necesario

{{< callout type="info" >}}
**Disponibilidad de la Sintaxis Simplificada**

La sintaxis simplificada para comandos `node-*` (que no requiere especificar `exec` ni el nombre del servicio) estará disponible a partir de la versión **Drive v0.1.12** en **enero de 2026**.

Si estás usando una versión anterior, deberás usar la sintaxis completa con `exec` y el nombre del servicio.
{{< /callout >}}

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

Los logs del contenedor muestran información sobre el contenedor Docker mismo, incluyendo mensajes de inicio, errores de Docker y cualquier salida del entrypoint o CMD del contenedor.

> [!NOTE]
> **Diferencia entre Logs del Contenedor y Logs del Nodo**
>
> Es importante entender la diferencia:
> - **Logs del contenedor:** Logs de Docker (inicio del contenedor, errores de Docker, configuración del contenedor)
> - **Logs del nodo:** Logs del proceso blockchain (sincronización, bloques, actividad del nodo)
>
> Para ver los logs del nodo blockchain, consulta [Monitoreo del Nodo]({{< relref "../blockchain-nodes/node-monitoring" >}}).

#### Ver Todos los Logs

```bash
cd services/node0-infinite  # O cualquier otro servicio
./drive.sh logs
```

Muestra todos los logs del contenedor desde su inicio.

#### Seguir Logs en Tiempo Real

```bash
cd services/node0-infinite
./drive.sh logs -f
```

Muestra los logs del contenedor en tiempo real, actualizándose automáticamente. Presiona `Ctrl+C` para detener.

#### Ver Últimas N Líneas

```bash
cd services/node0-infinite
./drive.sh logs --tail=100
```

Muestra solo las últimas 100 líneas de logs. Puedes cambiar el número según necesites.

#### Ver Últimas N Líneas y Seguir

```bash
cd services/node0-infinite
./drive.sh logs --tail=100 -f
```

Muestra las últimas 100 líneas y luego continúa mostrando logs nuevos en tiempo real.

#### Filtrar Logs por Tiempo

```bash
cd services/node0-infinite
# Logs de la última hora
./drive.sh logs --since=1h

# Logs hasta hace 1 hora
./drive.sh logs --until=1h
```

**Opciones disponibles:**
- `-f` o `--follow`: Transmitir logs en tiempo real
- `--tail=N`: Mostrar solo las últimas N líneas
- `--since=1h`: Mostrar logs desde hace 1 hora (puedes usar `1m`, `1h`, `1d`, etc.)
- `--until=1h`: Mostrar logs hasta hace 1 hora

**Cuándo usar logs del contenedor:**
- Depurar problemas de inicio del contenedor
- Ver errores a nivel de Docker
- Verificar configuración del contenedor
- Problemas de permisos o montaje de volúmenes

**Cuándo usar logs del nodo:**
- Monitorear actividad del nodo blockchain
- Ver progreso de sincronización
- Depurar problemas de la blockchain
- Ver procesamiento de bloques

Para más información sobre logs del nodo, consulta [Monitoreo del Nodo]({{< relref "../blockchain-nodes/node-monitoring" >}}).

## Ejecutar Comandos Dentro del Contenedor

Para ejecutar comandos dentro del contenedor, `drive.sh` ofrece dos formas de hacerlo:

### ✨ Sintaxis Simplificada (Recomendada)

{{< callout type="info" >}}
**Disponible desde Drive v0.1.12 (enero 2026)**

La sintaxis simplificada estará disponible a partir de la versión **Drive v0.1.12** en **enero de 2026**. Si estás usando una versión anterior, usa la sintaxis completa con `exec` y el nombre del servicio.
{{< /callout >}}

Para comandos que empiezan con `node-*` (como `node-init`, `node-ui`, `node-keys`, etc.), puedes usar la sintaxis simplificada:

```bash
./drive.sh <comando-node-*>
```

El script automáticamente:
- Detecta que es un comando `node-*`
- Obtiene el nombre del servicio del `docker-compose.yml` del directorio actual
- Agrega `exec` y el nombre del servicio automáticamente
- Agrega `-it` si el comando requiere modo interactivo

**Ejemplos:**
```bash
# Sintaxis simplificada - El script completa automáticamente
./drive.sh node-ui              # Abrir interfaz gráfica
./drive.sh node-init            # Inicializar nodo
./drive.sh node-init --recover  # Inicializar con recovery
./drive.sh node-keys list       # Listar claves
./drive.sh node-keys create     # Crear nueva clave
./drive.sh node-start           # Iniciar nodo
./drive.sh node-logs -f         # Ver logs en tiempo real
```

> [!TIP]
> **Ventaja de la Sintaxis Simplificada**
>
> No necesitas recordar el nombre del servicio ni especificar `exec` o `-it`. El script lo hace automáticamente por ti.

### Sintaxis Completa (Alternativa)

Si prefieres especificar explícitamente el nombre del servicio, puedes usar la sintaxis completa:

```bash
./drive.sh exec <nombre-contenedor> <comando>
```

**Ejemplos:**
```bash
# Sintaxis completa - Especificas todo manualmente
./drive.sh exec infinite node-ui
./drive.sh exec infinite node-init --recover
./drive.sh exec infinite node-keys list
```

**Cuándo usar la sintaxis completa:**
- Si quieres especificar un servicio diferente al del directorio actual
- Si prefieres ser explícito sobre qué servicio estás usando
- Para comandos que no son `node-*` (como `bash`, `sh`, etc.)

**Equivalente a:**
```bash
docker compose exec <nombre-contenedor> <comando>
```

### 💻 Acceder a la Shell del Contenedor

Para acceder a la shell del contenedor, debes usar la sintaxis completa (ya que `bash` no es un comando `node-*`):

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
> **Comandos que Requieren Sintaxis Completa**
>
> Algunos comandos siempre requieren la sintaxis completa porque no son comandos `node-*`:
> - `bash` o `sh` - Acceder a shell
> - Comandos del sistema como `ls`, `cat`, `grep`, etc.
> - Comandos personalizados que no siguen el patrón `node-*`
>
> Para comandos `node-*`, puedes usar la sintaxis simplificada. Para otros comandos, usa la sintaxis completa con el nombre del contenedor.

## Nombres de Contenedores por Servicio

> [!IMPORTANT]
> **Sintaxis Simplificada para Comandos `node-*`**
>
> {{< callout type="info" >}}
> **Disponible desde Drive v0.1.12 (enero 2026)**
>
> Esta funcionalidad estará disponible a partir de la versión **Drive v0.1.12** en **enero de 2026**. Si estás usando una versión anterior, deberás usar la sintaxis completa especificando el nombre del contenedor.
> {{< /callout >}}
>
> Para comandos que empiezan con `node-*`, **NO necesitas** especificar el nombre del contenedor. El script lo detecta automáticamente del `docker-compose.yml` del directorio actual.
>
> **Ejemplo simplificado:**
> ```bash
> cd services/node0-infinite
> ./drive.sh node-ui          # ✅ Funciona sin especificar nombre
> ./drive.sh node-init         # ✅ Funciona sin especificar nombre
> ```
>
> **Solo necesitas especificar el nombre del contenedor para:**
> - Comandos que NO son `node-*` (como `bash`, `sh`, `ls`, etc.)
> - Cuando quieres usar la sintaxis completa explícitamente

### Tabla de Referencia de Nombres de Contenedores

Si necesitas usar la sintaxis completa o acceder a comandos que no son `node-*`, aquí están los nombres de contenedores por servicio:

| Servicio | Nombre del Contenedor | Ejemplo con Sintaxis Simplificada | Ejemplo con Sintaxis Completa |
|----------|----------------------|-----------------------------------|-------------------------------|
| `node0-infinite` | `infinite` | `./drive.sh node-ui` | `./drive.sh exec infinite bash` |
| `node1-infinite-testnet` | `infinite-testnet` | `./drive.sh node-ui` | `./drive.sh exec infinite-testnet bash` |
| `node2-infinite-creative` | `infinite-creative` | `./drive.sh node-ui` | `./drive.sh exec infinite-creative bash` |
| `node3-qom` | `qom` | `./drive.sh node-ui` | `./drive.sh exec qom bash` |

### Ejemplos de Uso

Aquí tienes ejemplos prácticos usando ambas sintaxis:

```bash
# Infinite Mainnet (node0-infinite)
cd services/node0-infinite

# Sintaxis simplificada (recomendada para comandos node-*)
./drive.sh node-ui              # ✅ Abrir interfaz gráfica
./drive.sh node-init            # ✅ Inicializar nodo
./drive.sh node-keys list       # ✅ Listar claves

# Sintaxis completa (necesaria para comandos no node-*)
./drive.sh exec infinite bash   # Acceder a shell del contenedor

# Infinite Testnet (node1-infinite-testnet)
cd services/node1-infinite-testnet
./drive.sh node-ui              # ✅ Sintaxis simplificada
./drive.sh exec infinite-testnet bash  # Sintaxis completa para bash

# Infinite Creative (node2-infinite-creative)
cd services/node2-infinite-creative
./drive.sh node-ui              # ✅ Sintaxis simplificada
./drive.sh exec infinite-creative bash  # Sintaxis completa

# QOM Network (node3-qom)
cd services/node3-qom
./drive.sh node-ui              # ✅ Sintaxis simplificada
./drive.sh exec qom bash         # Sintaxis completa
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
- **Para comandos `node-*`**: No necesitas especificar el nombre del contenedor - usa la sintaxis simplificada
- **Para otros comandos**: Debes usar la sintaxis completa con el nombre del contenedor
- La mayoría de comandos de gestión (up, down, stop, start, ps, logs) **NO requieren** especificar el nombre del contenedor
- El script detecta automáticamente el modo interactivo y agrega `-it` cuando es necesario para comandos `node-*`
