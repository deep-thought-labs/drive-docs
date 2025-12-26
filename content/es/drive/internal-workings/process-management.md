---
title: "Gestión de Procesos Interna"
weight: 402
---

El sistema Drive utiliza técnicas avanzadas de gestión de procesos para garantizar que el nodo blockchain se ejecute de forma estable y aislada. Esta sección documenta cómo funciona la daemonización, el tracking de PIDs, y el manejo de señales.

## Daemonización del Nodo

### Método Principal: `setsid`

El nodo se inicia como un proceso daemon usando `setsid`, que crea una nueva sesión completamente aislada del terminal:

```bash
setsid bash -c "eval ${START_CMD} > ${NODE_LOG_FILE} 2>&1" < /dev/null &
```

**Características de `setsid`:**

1. **Nueva Sesión:** Crea una nueva sesión de proceso, separada del terminal
2. **Aislamiento de Señales:** Las señales del terminal (SIGINT, SIGHUP, etc.) no afectan al proceso
3. **Proceso Líder:** El proceso se convierte en líder de su propia sesión
4. **Redirección de I/O:** Redirige stdin desde `/dev/null` para evitar bloqueos

**Ventajas:**
- El nodo continúa ejecutándose incluso si el terminal se cierra
- Las señales del terminal no afectan al proceso del nodo
- El proceso está completamente aislado del shell que lo inició

### Método Alternativo: `nohup`

Si `setsid` no está disponible, el sistema usa `nohup` como fallback:

```bash
eval "nohup ${START_CMD} > ${NODE_LOG_FILE} 2>&1 &"
NODE_PID=$!
disown $NODE_PID 2>/dev/null || true
```

**Características de `nohup`:**
- Previene que el proceso reciba SIGHUP cuando el terminal se cierra
- Redirige la salida a un archivo de log
- `disown` remueve el proceso de la tabla de trabajos del shell

## Tracking de PIDs

### Archivos de PID

El sistema mantiene archivos PID para rastrear procesos importantes:

**Archivos:**
- `~/.node/node.pid` - PID del proceso del nodo blockchain
- `~/.node/supervisor.pid` - PID del proceso supervisor

**Ubicación:**
```
/home/ubuntu/.node/node.pid
/home/ubuntu/.node/supervisor.pid
```

### Obtención del PID

El sistema utiliza múltiples métodos para obtener el PID del nodo:

1. **Desde archivo PID:**
   ```bash
   PID=$(cat "$NODE_PID_FILE")
   ```

2. **Desde proceso en ejecución (usando `pgrep`):**
   ```bash
   PID=$(pgrep -f "$NODE_PROCESS_PATTERN" | head -1)
   ```

3. **Verificación de existencia:**
   ```bash
   if ps -p $PID > /dev/null; then
       # Proceso existe
   fi
   ```

### Patrón de Detección de Proceso

El sistema usa un patrón específico para identificar el proceso del nodo:

```bash
NODE_PROCESS_PATTERN="${NODE_BINARY_PATH} start.*--chain-id ${NODE_CHAIN_ID}"
```

**Ejemplo:**
```
/usr/local/bin/infinited start.*--chain-id infinite_421018-1
```

**Ventajas:**
- Permite múltiples nodos en el mismo host (diferentes chain-id)
- Identifica específicamente el proceso del nodo, no otros procesos
- Evita falsos positivos con otros procesos que usen el binario

## Manejo de Señales

### Detención Graceful (SIGTERM)

Cuando el usuario ejecuta `node-stop`, el sistema primero intenta detener el nodo de forma graceful:

```bash
kill -TERM $PID
```

**Proceso:**
1. Se envía SIGTERM al proceso
2. El proceso tiene hasta 30 segundos para terminar gracefully
3. El sistema verifica cada segundo si el proceso aún existe
4. Si el proceso termina dentro del tiempo, se considera exitoso

**Código:**
```bash
kill -TERM $PID

# Esperar hasta que termine (máximo 30 segundos)
for i in {1..30}; do
    if ! ps -p $PID > /dev/null; then
        print_success "Node stopped successfully"
        rm -f "$NODE_PID_FILE"
        exit 0
    fi
    sleep 1
done
```

### Detención Forzada (SIGKILL)

Si el proceso no responde a SIGTERM dentro de 30 segundos, se fuerza la terminación:

```bash
if ps -p $PID > /dev/null; then
    print_warning "Forcing termination..."
    kill -KILL $PID
    rm -f "$NODE_PID_FILE"
    print_success "Node stopped (forced)"
fi
```

**Consideraciones:**
- SIGKILL no puede ser ignorado por el proceso
- Puede resultar en pérdida de datos si el nodo estaba escribiendo
- Solo se usa como último recurso

## Verificación de Estado del Proceso

### Verificación de Proceso en Ejecución

Antes de iniciar el nodo, el sistema verifica si ya está corriendo:

```bash
if pgrep -f "$NODE_PROCESS_PATTERN" > /dev/null; then
    local_pid=$(pgrep -f "$NODE_PROCESS_PATTERN" | head -1)
    print_warning "The node is already running (PID: $local_pid)"
    exit 1
fi
```

### Verificación Post-Inicio

Después de iniciar el nodo, el sistema verifica que realmente se inició:

```bash
# Esperar un momento para que el proceso inicie
sleep 2

# Verificar que el proceso existe
if [ -n "$NODE_PID" ] && ps -p $NODE_PID > /dev/null; then
    print_success "Node started successfully (PID: $NODE_PID)"
    # Guardar PID en archivo
    echo "$NODE_PID" > "$NODE_PID_FILE"
else
    print_error "The node could not start"
    exit 1
fi
```

## Aislamiento de Procesos

### Aislamiento del Nodo

El proceso del nodo está completamente aislado:

1. **Sesión Aislada:** `setsid` crea una nueva sesión
2. **I/O Redirigido:** stdin, stdout, stderr redirigidos a archivos/logs
3. **Sin Control del Terminal:** No responde a señales del terminal
4. **Proceso en Background:** Ejecutado como proceso en segundo plano

### Aislamiento del Supervisor

El supervisor también está aislado:

```bash
nohup /usr/local/bin/node-supervisor > /dev/null 2>&1 &
SUPERVISOR_PID=$!
echo "$SUPERVISOR_PID" > "$NODE_SUPERVISOR_PID_FILE"
```

**Características:**
- Ejecutado con `nohup` para evitar SIGHUP
- Redirección de salida a `/dev/null` (logs se escriben directamente al archivo)
- PID guardado en archivo para referencia futura

## Limpieza de PIDs Obsoletos

Al reiniciar el contenedor, el sistema limpia archivos PID obsoletos:

```bash
# En node-auto-start.sh
rm -f "$NODE_PID_FILE"
rm -f "$NODE_SUPERVISOR_PID_FILE"
```

**Razón:**
- Los PIDs de instancias anteriores del contenedor ya no son válidos
- Los procesos anteriores fueron terminados cuando el contenedor se detuvo
- Los nuevos procesos tendrán nuevos PIDs

## Flujo Completo de Gestión de Procesos

### Inicio del Nodo

1. Verificar que el nodo no esté ya corriendo
2. Construir comando de inicio con argumentos dinámicos
3. Iniciar proceso con `setsid` (o `nohup` como fallback)
4. Esperar 2 segundos para que el proceso inicie
5. Verificar que el proceso existe usando `pgrep`
6. Guardar PID en archivo `~/.node/node.pid`
7. Iniciar supervisor si no está corriendo

### Detención del Nodo

1. Leer PID desde archivo o detectar con `pgrep`
2. Verificar que el proceso existe
3. Eliminar flag de auto-start (previene reinicio)
4. Detener supervisor primero (previene race condition)
5. Enviar SIGTERM al proceso del nodo
6. Esperar hasta 30 segundos para terminación graceful
7. Si no termina, enviar SIGKILL
8. Eliminar archivo PID

### Monitoreo del Nodo

1. Supervisor verifica cada 10 segundos
2. Usa `pgrep` con patrón para detectar proceso
3. Si proceso no existe y flag existe, reinicia
4. Registra eventos en log del supervisor

## Variables y Archivos Relacionados

**Variables:**
- `NODE_PID_FILE` - Ruta al archivo PID del nodo
- `NODE_SUPERVISOR_PID_FILE` - Ruta al archivo PID del supervisor
- `NODE_PROCESS_PATTERN` - Patrón para detectar el proceso
- `NODE_BINARY_PATH` - Ruta al binario del nodo

**Archivos:**
- `~/.node/node.pid` - PID del nodo
- `~/.node/supervisor.pid` - PID del supervisor

## Ver También

- [Sistema de Supervisor y Auto-Start]({{< relref "supervisor-auto-start" >}}) - Cómo funciona el sistema de monitoreo
- [Sistema de Configuración Interna]({{< relref "configuration-system" >}}) - Variables de configuración relacionadas
- [Scripts Internos del Contenedor]({{< relref "internal-scripts" >}}) - Scripts que implementan esta funcionalidad

