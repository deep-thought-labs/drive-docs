---
title: "Sistema de Supervisor y Auto-Start"
weight: 401
---

El sistema de supervisor y auto-start es un mecanismo interno que garantiza que el nodo se mantenga en ejecución y se reinicie automáticamente cuando sea necesario. Este sistema consta de dos componentes principales: el **supervisor** y el **auto-start**.

## Componentes del Sistema

### 1. Auto-Start Flag

El sistema utiliza un archivo flag (`NODE_AUTO_START_FLAG`) ubicado en `~/.node/auto-start` para indicar que el nodo debe iniciarse automáticamente.

**Ubicación:**
```
/home/ubuntu/.node/auto-start
```

**Propósito:**
- Indica que el nodo fue iniciado manualmente por el usuario
- Permite que el nodo se reinicie automáticamente al reiniciar el contenedor
- Controla si el supervisor debe monitorear y reiniciar el nodo

**Gestión:**
- Se crea cuando el usuario ejecuta `node-start`
- Se elimina cuando el usuario ejecuta `node-stop`
- Se verifica al iniciar el contenedor (`node-auto-start.sh`)
- Se verifica continuamente por el supervisor (`node-supervisor.sh`)

### 2. Script de Auto-Start (`node-auto-start.sh`)

Este script se ejecuta automáticamente cuando el contenedor inicia (definido en el `CMD` del Dockerfile).

**Flujo de Ejecución:**

1. **Verificación de Inicialización:**
   ```bash
   if [ ! -f "$NODE_GENESIS_FILE" ]; then
       exit 0  # Nodo no inicializado, no hacer nada
   fi
   ```

2. **Verificación del Flag:**
   ```bash
   if [ -f "$NODE_AUTO_START_FLAG" ]; then
       # Limpiar PIDs obsoletos de instancias anteriores
       rm -f "$NODE_PID_FILE"
       rm -f "$NODE_SUPERVISOR_PID_FILE"
       
       # Iniciar el nodo
       /usr/local/bin/node-start
   fi
   ```

**Características:**
- Se ejecuta solo una vez al iniciar el contenedor
- Limpia archivos PID obsoletos de instancias anteriores del contenedor
- Solo inicia el nodo si existe el flag de auto-start
- Ejecuta `node-start` de forma silenciosa (redirige salida a `/dev/null`)

### 3. Supervisor del Nodo (`node-supervisor.sh`)

El supervisor es un proceso en segundo plano que monitorea continuamente el estado del nodo y lo reinicia si detecta que se ha detenido inesperadamente.

**Flujo de Monitoreo:**

```bash
while true; do
    # 1. Verificar si el flag de auto-start existe
    if [ ! -f "$NODE_AUTO_START_FLAG" ]; then
        # Flag eliminado, usuario detuvo el nodo explícitamente
        exit 0  # Detener supervisión
    fi
    
    # 2. Verificar si el proceso del nodo está corriendo
    if ! pgrep -f "$NODE_PROCESS_PATTERN" > /dev/null; then
        # 3. Doble verificación del flag (prevenir race condition)
        if [ -f "$NODE_AUTO_START_FLAG" ]; then
            # 4. Verificar que el nodo esté inicializado
            if [ -f "$NODE_GENESIS_FILE" ]; then
                # 5. Reiniciar el nodo
                /usr/local/bin/node-start
            fi
        fi
    fi
    
    sleep 10  # Esperar 10 segundos antes del siguiente chequeo
done
```

**Características:**
- Ejecuta un loop infinito con chequeos cada 10 segundos
- Verifica el flag de auto-start antes de cada acción
- Detecta si el proceso del nodo se ha detenido usando `pgrep`
- Previene race conditions con doble verificación del flag
- Solo reinicia si el nodo está inicializado
- Registra eventos en el log del supervisor (`/var/log/node/supervisor.log`)

**Inicio del Supervisor:**

El supervisor se inicia automáticamente cuando el usuario ejecuta `node-start`:

```bash
# En node-start.sh
if ! pgrep -f "node-supervisor" > /dev/null; then
    nohup /usr/local/bin/node-supervisor > /dev/null 2>&1 &
    SUPERVISOR_PID=$!
    echo "$SUPERVISOR_PID" > "$NODE_SUPERVISOR_PID_FILE"
fi
```

**Detención del Supervisor:**

El supervisor se detiene cuando el usuario ejecuta `node-stop`:

```bash
# En node-stop.sh
# CRITICAL: Remover flag PRIMERO para prevenir que supervisor reinicie
rm -f "$NODE_AUTO_START_FLAG"

# Detener supervisor ANTES de detener el nodo
if [ -f "$NODE_SUPERVISOR_PID_FILE" ]; then
    SUPERVISOR_PID=$(cat "$NODE_SUPERVISOR_PID_FILE")
    kill "$SUPERVISOR_PID" 2>/dev/null || true
    rm -f "$NODE_SUPERVISOR_PID_FILE"
fi

# También eliminar cualquier proceso supervisor restante
pkill -f "node-supervisor" 2>/dev/null || true
```

## Flujo Completo del Sistema

### Escenario 1: Inicio Manual del Nodo

1. Usuario ejecuta `node-start`
2. `node-start.sh` inicia el proceso del nodo
3. `node-start.sh` crea el flag `NODE_AUTO_START_FLAG`
4. `node-start.sh` inicia el supervisor
5. Supervisor comienza a monitorear el nodo

### Escenario 2: Reinicio del Contenedor

1. Contenedor se reinicia (por cualquier razón)
2. Docker ejecuta el `CMD` del Dockerfile: `node-auto-start.sh`
3. `node-auto-start.sh` verifica si existe `NODE_AUTO_START_FLAG`
4. Si existe, ejecuta `node-start` para reiniciar el nodo
5. `node-start` crea nuevamente el flag y inicia el supervisor

### Escenario 3: Caída Inesperada del Nodo

1. El proceso del nodo se detiene inesperadamente (crash, error, etc.)
2. Supervisor detecta que el proceso no está corriendo (en el siguiente chequeo, máximo 10 segundos)
3. Supervisor verifica que el flag de auto-start existe
4. Supervisor ejecuta `node-start` para reiniciar el nodo
5. El nodo se reinicia automáticamente

### Escenario 4: Detención Manual del Nodo

1. Usuario ejecuta `node-stop`
2. `node-stop.sh` elimina el flag `NODE_AUTO_START_FLAG` **PRIMERO**
3. `node-stop.sh` detiene el supervisor
4. `node-stop.sh` detiene el proceso del nodo
5. Supervisor detecta que el flag no existe y se detiene
6. El nodo no se reiniciará automáticamente

## Archivos y Variables Relacionados

**Archivos:**
- `~/.node/auto-start` - Flag de auto-start
- `~/.node/supervisor.pid` - PID del proceso supervisor
- `/var/log/node/supervisor.log` - Log del supervisor

**Variables de Configuración:**
- `NODE_AUTO_START_FLAG` - Ruta al archivo flag
- `NODE_SUPERVISOR_PID_FILE` - Ruta al archivo PID del supervisor
- `NODE_SUPERVISOR_LOG_FILE` - Ruta al log del supervisor
- `NODE_PROCESS_PATTERN` - Patrón para detectar el proceso del nodo

## Consideraciones de Diseño

### Prevención de Race Conditions

El sistema implementa varias medidas para prevenir race conditions:

1. **Doble verificación del flag:** El supervisor verifica el flag dos veces antes de reiniciar
2. **Orden de operaciones en node-stop:** El flag se elimina ANTES de detener el proceso
3. **Verificación atómica:** Uso de archivos de flag para comunicación entre procesos

### Aislamiento de Procesos

- El supervisor se ejecuta con `nohup` para aislarlo del terminal
- El nodo se ejecuta con `setsid` para crear una sesión completamente aislada
- Los procesos no se afectan mutuamente por señales del terminal

### Logging

El supervisor registra eventos importantes en su log:
- Inicio de supervisión
- Detección de nodo detenido
- Intentos de reinicio
- Detención de supervisión

## Ver También

- [Gestión de Procesos Interna]({{< relref "process-management" >}}) - Detalles sobre daemonización y tracking de procesos
- [Sistema de Configuración Interna]({{< relref "configuration-system" >}}) - Variables y configuración del sistema
- [Scripts Internos del Contenedor]({{< relref "internal-scripts" >}}) - Descripción completa de los scripts

