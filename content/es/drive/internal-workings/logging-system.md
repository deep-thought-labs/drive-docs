---
title: "Sistema de Logs Interno"
weight: 405
---

El sistema Drive implementa un sistema de logs estructurado para facilitar el monitoreo, debugging y diagnóstico de problemas. Esta sección documenta cómo funciona el sistema de logs internamente.

## Arquitectura del Sistema de Logs

### Tipos de Logs

El sistema mantiene dos tipos principales de logs:

1. **Logs del Nodo** - Salida del proceso blockchain
2. **Logs del Supervisor** - Eventos del sistema de monitoreo

### Ubicación de Logs

Todos los logs se almacenan en `/var/log/node/`:

```
/var/log/node/
├── node.log          # Log principal del nodo blockchain
└── supervisor.log    # Log del supervisor
```

## Log del Nodo (`node.log`)

### Ubicación y Configuración

**Ruta:**
```
/var/log/node/node.log
```

**Variable:**
```bash
NODE_LOG_FILE="/var/log/node/node.log"
```

### Contenido

El log del nodo contiene toda la salida del proceso `infinited`:

- **Salida estándar (stdout):** Mensajes informativos del nodo
- **Salida de error (stderr):** Errores y advertencias

### Redirección

El log se crea mediante redirección de I/O cuando se inicia el nodo:

```bash
# En node-start.sh
setsid bash -c "eval ${START_CMD} > ${NODE_LOG_FILE} 2>&1" < /dev/null &
```

**Explicación:**
- `> ${NODE_LOG_FILE}` - Redirige stdout al archivo de log
- `2>&1` - Redirige stderr a stdout (ambos van al mismo archivo)
- `< /dev/null` - Redirige stdin desde /dev/null (evita bloqueos)

### Características

1. **Append Mode:** Los logs se agregan al archivo (no se sobrescriben)
2. **Formato de Texto:** Logs en formato de texto plano
3. **Tamaño:** El archivo crece continuamente mientras el nodo está en ejecución
4. **Rotación:** No hay rotación automática implementada (se puede agregar externamente)

### Visualización

#### Ver Últimas N Líneas

```bash
node-logs [número]
```

**Ejemplo:**
```bash
node-logs 100    # Últimas 100 líneas
node-logs        # Últimas 50 líneas (por defecto)
```

**Implementación:**
```bash
if [ -n "$1" ]; then
    tail -n "$1" "$NODE_LOG_FILE"
else
    tail -n 50 "$NODE_LOG_FILE"
fi
```

#### Seguimiento en Tiempo Real

```bash
node-logs -f
# o
node-logs --follow
```

**Implementación:**
```bash
if [ "$1" = "-f" ] || [ "$1" = "--follow" ]; then
    # Usar exec para reemplazar el proceso del script con tail
    exec tail -f "$NODE_LOG_FILE"
fi
```

**Características:**
- Usa `exec tail -f` para reemplazar el proceso del script
- Permite que Ctrl+C solo afecte a `tail`, no el nodo
- Muestra logs en tiempo real mientras se generan

### Aislamiento de Señales

El sistema está diseñado para que las señales del terminal no afecten al proceso del nodo:

```bash
# El nodo se ejecuta con setsid, en una sesión aislada
setsid bash -c "eval ${START_CMD} > ${NODE_LOG_FILE} 2>&1" < /dev/null &

# tail también se ejecuta con exec para aislar señales
exec tail -f "$NODE_LOG_FILE"
```

**Ventajas:**
- Ctrl+C en `node-logs -f` solo detiene `tail`, no el nodo
- El nodo continúa ejecutándose independientemente
- No hay interferencia entre visualización y ejecución

## Log del Supervisor (`supervisor.log`)

### Ubicación y Configuración

**Ruta:**
```
/var/log/node/supervisor.log
```

**Variable:**
```bash
NODE_SUPERVISOR_LOG_FILE="${NODE_SUPERVISOR_LOG_FILE:-/var/log/node/supervisor.log}"
```

### Contenido

El log del supervisor contiene eventos del sistema de monitoreo:

- Inicio de supervisión
- Detección de nodo detenido
- Intentos de reinicio
- Detención de supervisión
- Errores o problemas detectados

### Formato de Entradas

Cada entrada incluye una marca de tiempo:

```
[2024-01-15 10:30:45] Node not detected, attempting to restart...
[2024-01-15 10:30:50] Auto-start flag removed, stopping supervision...
```

**Formato:**
```bash
echo "[$(date +"%Y-%m-%d %H:%M:%S")] Mensaje..." >> "$NODE_SUPERVISOR_LOG_FILE"
```

### Escritura

El supervisor escribe directamente al archivo usando append (`>>`):

```bash
# En node-supervisor.sh
echo "[$(date +"%Y-%m-%d %H:%M:%S")] Node not detected, attempting to restart..." >> "$NODE_SUPERVISOR_LOG_FILE"
```

**Características:**
- Append mode (no sobrescribe)
- Formato consistente con timestamps
- Solo escribe cuando hay eventos importantes

### Creación del Directorio

El directorio de logs se crea automáticamente si no existe:

```bash
# En node-supervisor.sh
mkdir -p "$(dirname "$NODE_SUPERVISOR_LOG_FILE")"
```

## Diferencia entre Logs del Nodo y Logs del Contenedor

### Logs del Nodo

- **Origen:** Proceso `infinited` dentro del contenedor
- **Ubicación:** `/var/log/node/node.log` (dentro del contenedor)
- **Contenido:** Salida específica del nodo blockchain
- **Acceso:** `node-logs` o `docker compose exec infinite-drive node-logs`

### Logs del Contenedor

- **Origen:** Salida de todos los procesos del contenedor
- **Ubicación:** Gestión de Docker (no en el sistema de archivos del contenedor)
- **Contenido:** Salida de `node-auto-start.sh`, errores de inicio, etc.
- **Acceso:** `docker compose logs infinite-drive`

**Nota:** Los logs del contenedor pueden incluir la salida inicial de `node-auto-start.sh`, pero una vez que el nodo está corriendo, los logs del nodo son más relevantes.

## Gestión de Logs

### Creación de Directorios

Los directorios de logs se crean automáticamente:

**En el Dockerfile:**
```dockerfile
RUN mkdir -p /home/ubuntu/.infinited /var/log/node /home/ubuntu/.node && \
    chown -R 1000:1000 /home/ubuntu /var/log/node
```

**En los scripts:**
```bash
# Crear directorio si no existe
mkdir -p "$(dirname "$NODE_LOG_FILE")"
mkdir -p "$(dirname "$NODE_SUPERVISOR_LOG_FILE")"
```

### Permisos

Los logs tienen permisos estándar:

- **Propietario:** `ubuntu` (UID 1000)
- **Grupo:** `ubuntu` (GID 1000)
- **Permisos:** `644` (rw-r--r--)

### Persistencia

Los logs se almacenan en volúmenes persistentes en Docker:

```yaml
volumes:
  - ./persistent-data/logs:/var/log/node
```

**Ventajas:**
- Los logs persisten entre reinicios del contenedor
- Accesibles desde el host
- No se pierden al recrear el contenedor

## Rotación de Logs

### Estado Actual

El sistema **no implementa rotación automática de logs** internamente.

### Consideraciones

1. **Crecimiento Continuo:** Los logs crecen indefinidamente
2. **Espacio en Disco:** Puede consumir espacio significativo con el tiempo
3. **Rendimiento:** Archivos muy grandes pueden afectar el rendimiento

### Soluciones Externas

Se pueden implementar soluciones externas:

1. **logrotate:** Configurar logrotate en el host
2. **Scripts personalizados:** Crear scripts que roten logs periódicamente
3. **Gestión manual:** Limpiar logs manualmente cuando sea necesario

**Ejemplo con logrotate:**
```
/var/log/node/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    missingok
}
```

## Verificación de Logs

### Verificar si el Log Existe

```bash
if [ ! -f "$NODE_LOG_FILE" ]; then
    print_error "Log file not found: $NODE_LOG_FILE"
    echo "   The node may not have been started yet."
    exit 1
fi
```

### Verificar si el Nodo Está Corriendo

Antes de seguir logs, se puede verificar el estado:

```bash
if ! pgrep -f "$NODE_PROCESS_PATTERN" > /dev/null; then
    print_warning "Node is not currently running, but showing logs..."
fi
```

## Interpretación de Logs

### Logs del Nodo

Los logs del nodo contienen información sobre:

- **Sincronización:** Progreso de sincronización con la red
- **Conexiones:** Conexión y desconexión de peers
- **Bloques:** Descarga y procesamiento de bloques
- **Errores:** Errores de conexión, validación, etc.
- **Estado:** Estado general del nodo

### Logs del Supervisor

Los logs del supervisor contienen información sobre:

- **Monitoreo:** Eventos de monitoreo del nodo
- **Reinicios:** Intentos de reinicio automático
- **Detención:** Detención de supervisión
- **Problemas:** Problemas detectados por el supervisor

## Variables Relacionadas

```bash
NODE_LOG_FILE="/var/log/node/node.log"
NODE_SUPERVISOR_LOG_FILE="/var/log/node/supervisor.log"
```

## Ver También

- [Estructura Interna de Directorios]({{< relref "directory-structure" >}}) - Ubicación de los archivos de log
- [Gestión de Procesos Interna]({{< relref "process-management" >}}) - Cómo se redirigen los logs
- [Guía de Monitoreo del Nodo]({{< relref "../guides/blockchain-nodes/node-monitoring" >}}) - Cómo usar los logs desde la perspectiva del usuario

