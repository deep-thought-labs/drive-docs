---
title: "Scripts Internos del Contenedor"
weight: 408
---

El contenedor Drive incluye una colección de scripts shell que proporcionan toda la funcionalidad de gestión del nodo. Esta sección documenta cada script, su propósito, y cómo interactúan entre sí.

## Arquitectura de Scripts

### Carga de Configuración

Todos los scripts siguen el mismo patrón de carga:

```bash
#!/bin/bash

# Obtener directorio del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Cargar configuración centralizada
source "${SCRIPT_DIR}/node-config.sh"

# Cargar estilos (si es necesario)
source "${SCRIPT_DIR}/styles.sh"
```

**Ventajas:**
- Configuración centralizada
- Consistencia entre scripts
- Fácil mantenimiento

## Scripts de Configuración y Utilidad

### `node-config.sh`

**Propósito:** Configuración centralizada del sistema.

**Contenido:**
- Variables de entorno con valores por defecto
- Rutas fijas y derivadas
- Funciones de utilidad (`build_node_start_command`, `validate_node_config`)
- Patrones de detección de procesos

**Uso:**
- Cargado por todos los scripts
- No se ejecuta directamente
- Proporciona configuración compartida

**Ubicación:** `/usr/local/bin/node-config.sh`

### `styles.sh`

**Propósito:** Funciones de formato y estilos para salida de terminal.

**Contenido:**
- Colores y formato de texto
- Funciones de impresión (`print_header`, `print_success`, `print_error`, etc.)
- Funciones de utilidad (`is_interactive`, `print_code`, etc.)

**Uso:**
- Cargado por scripts que necesitan salida formateada
- Proporciona interfaz consistente para mensajes

**Ubicación:** `/usr/local/bin/styles.sh`

### `dialog-theme.sh`

**Propósito:** Configuración de tema para la interfaz gráfica `dialog`.

**Uso:**
- Cargado por `node-ui.sh`
- Define colores y estilo de la interfaz TUI

**Ubicación:** `/usr/local/bin/dialog-theme.sh`

### `container-info.sh`

**Propósito:** Información sobre el contenedor y el sistema.

**Uso:**
- Proporciona información del sistema
- Usado por scripts de diagnóstico

**Ubicación:** `/usr/local/bin/container-info.sh`

## Scripts Principales de Gestión

### `node-init`

**Propósito:** Inicializar el nodo blockchain.

**Funcionalidad:**
- Verifica si el nodo ya está inicializado
- Solicita o recibe moniker
- Soporta modo simple (claves aleatorias) y recuperación (con seed phrase)
- Descarga y valida genesis oficial
- Configura el nodo para uso

**Argumentos:**
- `[moniker]` - Nombre del nodo
- `--recover` o `-r` - Modo recuperación con seed phrase

**Uso:**
```bash
node-init my-node
node-init --recover my-node
```

**Ver también:** [Flujo de Inicialización Técnico]({{< relref "initialization-flow" >}})

### `node-start`

**Propósito:** Iniciar el nodo blockchain.

**Funcionalidad:**
- Valida configuración
- Verifica que el nodo esté inicializado
- Verifica que el nodo no esté ya corriendo
- Construye comando de inicio dinámicamente
- Inicia el nodo como daemon con `setsid`
- Crea flag de auto-start
- Inicia el supervisor
- Guarda PID del proceso

**Características:**
- Aislamiento completo del proceso
- Redirección de logs
- Reinicio automático en caso de caída

**Uso:**
```bash
node-start
```

**Ver también:** [Gestión de Procesos Interna]({{< relref "process-management" >}}), [Sistema de Supervisor y Auto-Start]({{< relref "supervisor-auto-start" >}})

### `node-stop`

**Propósito:** Detener el nodo blockchain de forma graceful.

**Funcionalidad:**
- Lee PID desde archivo o detecta proceso
- Elimina flag de auto-start (previene reinicio)
- Detiene supervisor primero
- Envía SIGTERM al proceso del nodo
- Espera hasta 30 segundos para terminación graceful
- Si no termina, envía SIGKILL
- Limpia archivos PID

**Características:**
- Detención graceful con fallback a forzada
- Previene race conditions
- Limpieza completa de archivos de control

**Uso:**
```bash
node-stop
```

**Ver también:** [Gestión de Procesos Interna]({{< relref "process-management" >}})

### `node-logs`

**Propósito:** Visualizar logs del nodo.

**Funcionalidad:**
- Verifica que el archivo de log exista
- Muestra últimas N líneas (por defecto 50)
- Soporta seguimiento en tiempo real con `-f` o `--follow`
- Usa `exec tail -f` para aislamiento de señales

**Argumentos:**
- `[número]` - Número de líneas a mostrar
- `-f` o `--follow` - Seguir logs en tiempo real

**Uso:**
```bash
node-logs          # Últimas 50 líneas
node-logs 100       # Últimas 100 líneas
node-logs -f        # Seguir en tiempo real
```

**Ver también:** [Sistema de Logs Interno]({{< relref "logging-system" >}})

### `node-keys`

**Propósito:** Gestión de claves criptográficas del nodo.

**Funcionalidad:**
- Crear nuevas claves
- Agregar claves desde seed phrase
- Listar claves existentes
- Mostrar información de una clave
- Eliminar claves
- Resetear contraseña del keyring

**Subcomandos:**
- `create` o `new` - Crear nueva clave
- `add` - Agregar clave desde seed phrase
- `list` - Listar todas las claves
- `show` - Mostrar información de una clave
- `delete` - Eliminar una clave
- `reset-password` - Resetear contraseña del keyring

**Uso:**
```bash
node-keys create my-key
node-keys add my-key
node-keys list
node-keys show my-key
node-keys delete my-key
node-keys reset-password
```

### `node-clean-data`

**Propósito:** Limpiar datos del nodo.

**Funcionalidad:**
- Verifica que el nodo esté detenido
- Soporta limpieza de: todo, solo blockchain, o solo keyring
- Crea backup del keyring antes de eliminar
- Solicita confirmación interactiva
- Elimina flag de auto-start si limpia todo

**Argumentos:**
- `all` - Eliminar todos los datos
- `blockchain` - Eliminar solo datos de blockchain
- `keyring` - Eliminar solo keyring

**Uso:**
```bash
node-clean-data all
node-clean-data blockchain
node-clean-data keyring
```

## Scripts del Sistema

### `node-supervisor`

**Propósito:** Monitorear y reiniciar automáticamente el nodo si se detiene.

**Funcionalidad:**
- Loop infinito con chequeos cada 10 segundos
- Verifica flag de auto-start
- Detecta si el proceso del nodo está corriendo
- Reinicia el nodo si se detiene y el flag existe
- Registra eventos en log del supervisor
- Se detiene si el flag es eliminado

**Características:**
- Ejecutado en background
- Prevención de race conditions
- Logging de eventos

**Uso:**
- Iniciado automáticamente por `node-start`
- No se ejecuta directamente por el usuario

**Ver también:** [Sistema de Supervisor y Auto-Start]({{< relref "supervisor-auto-start" >}})

### `node-auto-start`

**Propósito:** Iniciar automáticamente el nodo al iniciar el contenedor.

**Funcionalidad:**
- Verifica si el nodo está inicializado
- Verifica si existe flag de auto-start
- Limpia PIDs obsoletos de instancias anteriores
- Inicia el nodo si el flag existe

**Características:**
- Ejecutado por el `CMD` del Dockerfile
- Ejecuta solo una vez al iniciar el contenedor
- Silencioso (redirige salida a `/dev/null`)

**Uso:**
- Ejecutado automáticamente por Docker
- No se ejecuta directamente por el usuario

**Ver también:** [Sistema de Supervisor y Auto-Start]({{< relref "supervisor-auto-start" >}}), [Arquitectura del Contenedor]({{< relref "container-architecture" >}})

## Scripts de Monitoreo y Diagnóstico

### `node-process-status`

**Propósito:** Mostrar estado del proceso del nodo.

**Funcionalidad:**
- Verifica si el proceso está corriendo
- Muestra información del proceso (PID, tiempo de ejecución, etc.)
- Muestra uso de recursos (CPU, memoria)

**Uso:**
```bash
node-process-status
```

### `node-network-diagnosis`

**Propósito:** Diagnóstico de red y conectividad.

**Funcionalidad:**
- Verifica conectividad con peers
- Muestra información de red
- Diagnostica problemas de conexión

**Uso:**
```bash
node-network-diagnosis
```

## Scripts de Utilidad

### `node-update-genesis`

**Propósito:** Actualizar el archivo genesis del nodo.

**Funcionalidad:**
- Descarga el genesis oficial más reciente
- Valida el formato JSON
- Reemplaza el genesis actual
- Verifica que el nodo esté detenido

**Uso:**
```bash
node-update-genesis
```

### `node-validate-genesis`

**Propósito:** Validar el archivo genesis actual.

**Funcionalidad:**
- Verifica formato JSON
- Valida estructura del genesis
- Muestra información del genesis

**Uso:**
```bash
node-validate-genesis
```

### `node-help`

**Propósito:** Mostrar ayuda y documentación.

**Funcionalidad:**
- Lista todos los comandos disponibles
- Muestra uso y ejemplos
- Proporciona información de referencia rápida

**Uso:**
```bash
node-help
```

## Scripts de Interfaz de Usuario

### `node-ui`

**Propósito:** Interfaz gráfica de terminal (TUI) para gestión del nodo.

**Funcionalidad:**
- Menú principal con opciones
- Submenús para diferentes categorías:
  - Gestión de claves
  - Operaciones del nodo
  - Monitoreo
  - Ayuda
- Usa `dialog` para la interfaz
- Llama a los scripts correspondientes según la selección

**Características:**
- Interfaz interactiva y amigable
- Navegación por menús
- Integración con todos los scripts

**Uso:**
```bash
node-ui
```

**Requisitos:**
- Terminal interactivo
- `dialog` instalado

## Interacciones entre Scripts

### Flujo de Inicio

```
node-auto-start (al iniciar contenedor)
    ↓
node-start
    ↓
    ├─ Crea flag auto-start
    ├─ Inicia proceso infinited
    └─ Inicia node-supervisor
```

### Flujo de Detención

```
node-stop
    ↓
    ├─ Elimina flag auto-start
    ├─ Detiene node-supervisor
    └─ Detiene proceso infinited
```

### Flujo de Reinicio Automático

```
node-supervisor (cada 10 segundos)
    ↓
    ¿Flag auto-start existe?
    ├─ No → Detener supervisión
    └─ Sí → ¿Proceso corriendo?
        ├─ Sí → Continuar monitoreo
        └─ No → node-start (reiniciar)
```

### Flujo de Limpieza

```
node-clean-data
    ↓
    ¿Nodo corriendo?
    ├─ Sí → Error (debe estar detenido)
    └─ No → ¿Qué limpiar?
        ├─ Todo → Elimina flag auto-start
        ├─ Blockchain → Solo datos blockchain
        └─ Keyring → Solo keyring (con backup)
```

## Ubicación de Scripts

Todos los scripts se instalan en `/usr/local/bin/`:

```
/usr/local/bin/
├── node-init
├── node-start
├── node-stop
├── node-logs
├── node-keys
├── node-supervisor
├── node-auto-start
├── node-clean-data
├── node-process-status
├── node-network-diagnosis
├── node-update-genesis
├── node-validate-genesis
├── node-help
├── node-ui
├── node-config.sh
├── styles.sh
├── dialog-theme.sh
└── container-info.sh
```

**Nota:** La mayoría de los scripts tienen la extensión `.sh` removida para facilitar su uso.

## Permisos y Propiedad

Todos los scripts son:
- **Ejecutables:** `chmod +x`
- **Propietario:** `ubuntu:ubuntu` (UID 1000:GID 1000)
- **Permisos:** `755` (rwxr-xr-x)

## Modo Interactivo vs No Interactivo

La mayoría de los scripts soportan ambos modos:

### Modo Interactivo

- Solicita información al usuario cuando es necesario
- Muestra mensajes formateados
- Confirma acciones destructivas

### Modo No Interactivo

- Usa argumentos de línea de comando
- No solicita confirmación
- Adecuado para automatización

**Detección:**
```bash
is_interactive() {
    [ -t 0 ] && [ -t 1 ]
}
```

## Manejo de Errores

Todos los scripts implementan manejo de errores consistente:

1. **Validación temprana:** Verifican requisitos antes de ejecutar
2. **Mensajes claros:** Proporcionan mensajes de error descriptivos
3. **Códigos de salida:** Usan códigos de salida apropiados
4. **Limpieza:** Limpian recursos en caso de error

## Ver También

- [Sistema de Configuración Interna]({{< relref "configuration-system" >}}) - Cómo los scripts cargan configuración
- [Gestión de Procesos Interna]({{< relref "process-management" >}}) - Cómo los scripts gestionan procesos
- [Arquitectura del Contenedor]({{< relref "container-architecture" >}}) - Cómo se instalan los scripts

