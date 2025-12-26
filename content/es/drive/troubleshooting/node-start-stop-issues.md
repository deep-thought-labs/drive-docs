---
title: "Problemas de Inicio y Detención del Nodo"
weight: 542
---

Soluciones a problemas comunes relacionados con iniciar y detener el nodo blockchain.

## El Nodo No Inicia

Si el nodo no inicia, sigue estos pasos para diagnosticar y resolver el problema:

### 1. Verificar que el Nodo Esté Inicializado

El nodo debe estar inicializado antes de poder iniciarlo. Verifica que el archivo genesis exista:

```bash
./drive.sh exec infinite ls -la /home/ubuntu/.infinited/config/genesis.json
```

**Si el archivo no existe:**
- El nodo no ha sido inicializado
- Necesitas ejecutar `node-init` primero
- Consulta la guía de [Inicialización de Nodo]({{< relref "../guides/blockchain-nodes/initialization" >}})

**Si el archivo existe:**
- El nodo está inicializado correctamente
- Continúa con el siguiente paso

### 2. Verificar que No Haya Otra Instancia Ejecutándose

El sistema no permite múltiples instancias del mismo nodo. Verifica el estado:

```bash
./drive.sh exec infinite node-process-status
```

**Si hay una instancia ejecutándose:**
- Verás el PID del proceso en ejecución
- Detén la instancia anterior primero con `node-stop`
- Luego intenta iniciar nuevamente

**Si no hay instancia ejecutándose:**
- Continúa con el siguiente paso

### 3. Revisar los Logs del Contenedor

Los logs del contenedor pueden mostrar errores de inicio:

```bash
./drive.sh logs infinite-drive
```

**Qué buscar:**
- Errores de configuración
- Problemas de permisos
- Errores de red
- Problemas con el binario

### 4. Revisar los Logs del Nodo

Si el nodo intentó iniciar pero falló, revisa los logs del nodo:

```bash
./drive.sh exec infinite node-logs 50
```

**Qué buscar:**
- Mensajes de error específicos
- Problemas de sincronización
- Errores de conexión con peers

### 5. Verificar Configuración

Verifica que las variables de entorno estén configuradas correctamente:

```bash
./drive.sh exec infinite env | grep NODE_
```

**Variables importantes:**
- `NODE_CHAIN_ID` - Debe estar definido
- `NODE_EVM_CHAIN_ID` - Debe estar definido
- `NODE_HOME` - Debe apuntar al directorio correcto

### 6. Verificar Permisos

Si hay problemas de permisos, consulta [Problemas de Permisos]({{< relref "permission-issues" >}}).

## El Nodo No Se Detiene

Si el nodo no se detiene correctamente:

### 1. Esperar el Cierre Controlado

El cierre controlado puede tomar hasta 30 segundos. Espera unos momentos antes de tomar acciones adicionales.

### 2. Verificar el Estado

Verifica si el proceso aún está ejecutándose:

```bash
./drive.sh exec infinite node-process-status
```

**Si el proceso ya no está ejecutándose:**
- El nodo se detuvo correctamente
- Puede haber un retraso en la actualización del estado

**Si el proceso aún está ejecutándose:**
- Continúa con el siguiente paso

### 3. Verificar Logs del Supervisor

El supervisor puede estar reiniciando el nodo. Verifica los logs:

```bash
./drive.sh exec infinite cat /var/log/node/supervisor.log
```

**Si el supervisor está reiniciando el nodo:**
- El flag de auto-start aún existe
- El supervisor detecta que el nodo se detuvo y lo reinicia
- Detén el supervisor primero o elimina el flag de auto-start

### 4. Forzar el Cierre (Último Recurso)

> [!WARNING]
> **⚠️ Advertencia: Forzar el Cierre**
>
> Forzar el cierre del nodo puede causar:
> - Pérdida de datos no guardados
> - Problemas de sincronización
> - Slashing para validadores (en casos extremos)
>
> Solo úsalo como último recurso después de intentar todos los métodos anteriores.

Si es absolutamente necesario forzar el cierre:

```bash
# 1. Encontrar el PID del proceso
./drive.sh exec infinite node-process-status

# 2. Eliminar el flag de auto-start para prevenir reinicio
./drive.sh exec infinite rm -f /home/ubuntu/.node/auto-start

# 3. Detener el supervisor
./drive.sh exec infinite pkill -f node-supervisor

# 4. Enviar señal de terminación forzada (último recurso)
./drive.sh exec infinite kill -KILL <PID>
```

**Después de forzar el cierre:**
- Verifica que el proceso se haya detenido
- Revisa los logs para identificar la causa del problema
- Considera reinicializar el nodo si hay corrupción de datos

## El Nodo Se Reinicia Automáticamente

Si el nodo se reinicia automáticamente después de detenerlo:

### Causa: Flag de Auto-Start Activo

El nodo tiene un flag de auto-start que indica que debe reiniciarse automáticamente. Esto es normal si iniciaste el nodo manualmente, pero puede ser problemático si quieres mantenerlo detenido.

### Solución

1. **Detener el nodo correctamente:**
   ```bash
   ./drive.sh exec infinite node-stop
   ```
   
   El comando `node-stop` elimina automáticamente el flag de auto-start.

2. **Verificar que el flag fue eliminado:**
   ```bash
   ./drive.sh exec infinite ls -la /home/ubuntu/.node/auto-start
   ```
   
   Si el archivo no existe, el flag fue eliminado correctamente.

3. **Si el nodo aún se reinicia:**
   - Verifica que el supervisor esté detenido
   - Verifica que no haya múltiples instancias del supervisor
   - Revisa los logs del supervisor

## El Nodo No Se Inicia Después de Reiniciar el Contenedor

Si el nodo no se inicia automáticamente después de reiniciar el contenedor:

### Verificar Flag de Auto-Start

El nodo solo se inicia automáticamente si el flag de auto-start existe:

```bash
./drive.sh exec infinite ls -la /home/ubuntu/.node/auto-start
```

**Si el flag no existe:**
- El nodo no se iniciará automáticamente
- Esto es normal si detuviste el nodo manualmente antes de reiniciar el contenedor
- Inicia el nodo manualmente con `node-start`

**Si el flag existe pero el nodo no inicia:**
- Revisa los logs del contenedor: `./drive.sh logs infinite-drive`
- Verifica que el nodo esté inicializado
- Revisa los logs del auto-start si están disponibles

## Problemas de Sincronización Después de Reinicio

Si el nodo tiene problemas de sincronización después de reiniciarlo:

### Verificar Estado de Sincronización

```bash
./drive.sh exec infinite node-process-status
```

### Revisar Logs

```bash
./drive.sh exec infinite node-logs -f
```

**Qué buscar:**
- Errores de conexión con peers
- Problemas de red
- Errores de validación de bloques

### Soluciones Comunes

1. **Esperar a que sincronice** - La sincronización puede tomar tiempo
2. **Verificar conectividad de red** - Consulta [Diagnóstico de Red]({{< relref "network-diagnosis" >}})
3. **Reiniciar el nodo** - A veces un reinicio resuelve problemas temporales
4. **Limpiar datos y resincronizar** - Como último recurso, consulta [Borrar Data del Nodo]({{< relref "../guides/blockchain-nodes/delete-node-data" >}})

## Ver También

- [Iniciar/Detener Nodo]({{< relref "../guides/blockchain-nodes/start-stop-node" >}}) - Guía completa sobre cómo iniciar y detener el nodo
- [Monitoreo del Nodo]({{< relref "../guides/blockchain-nodes/node-monitoring" >}}) - Cómo monitorear el estado del nodo
- [Problemas Comunes]({{< relref "common-issues" >}}) - Otros problemas comunes
- [Diagnóstico de Red]({{< relref "network-diagnosis" >}}) - Herramientas de diagnóstico de red

