---
title: "Reiniciar Nodo"
weight: 5225
---

Guía para reiniciar el nodo blockchain (detener y volver a iniciar). Esta guía cubre tanto la **interfaz gráfica (recomendada)** como las **operaciones de línea de comandos (para usuarios avanzados)**.

## ¿Cuándo Reiniciar el Nodo?

Puedes necesitar reiniciar el nodo en las siguientes situaciones:

- **Después de cambios de configuración** - Algunos cambios requieren reiniciar el nodo
- **Problemas de sincronización** - Un reinicio puede resolver problemas temporales
- **Actualizaciones** - Después de actualizar el nodo o el contenedor
- **Problemas de rendimiento** - Si el nodo está funcionando lentamente
- **Mantenimiento programado** - Para realizar tareas de mantenimiento

## Reiniciar Nodo

Para reiniciar el nodo (detener y volver a iniciar):

### Usando Interfaz Gráfica (Recomendado)

1. Abre la interfaz gráfica:

   ```bash
   cd services/node0-infinite  # O cualquier otro servicio
   ./drive.sh exec infinite node-ui
   ```

2. En el menú principal, selecciona **"Node Operations"**

   ![Menú Principal - Node Operations seleccionada](/images/node-ui-op2-operations.png)

3. Selecciona **"Restart Node"**

   ![Node Operations - Restart Node seleccionada](/images/node-ui-operations-op3-restart.png)

4. La interfaz detendrá y reiniciará el nodo automáticamente

### Usando Línea de Comandos

1. **Detén el nodo** usando `node-stop`:

   ```bash
   cd services/node0-infinite  # O cualquier otro servicio
   ./drive.sh exec infinite node-stop
   ```

2. **Espera unos segundos** para que el proceso se cierre completamente

   El cierre controlado puede tomar hasta 30 segundos. Es importante esperar para asegurar que el nodo se detenga correctamente.

3. **Inicia el nodo** nuevamente usando `node-start`:

   ```bash
   ./drive.sh exec infinite node-start
   ```

**Ejemplo completo:**

```bash
cd services/node0-infinite
./drive.sh exec infinite node-stop
sleep 5  # Esperar 5 segundos para que el proceso se cierre
./drive.sh exec infinite node-start
```

## Qué Sucede Durante el Reinicio

Durante el reinicio, el sistema realiza las siguientes operaciones:

1. **Detención controlada:**
   - Envía señal SIGTERM al proceso del nodo
   - Espera hasta 30 segundos para cierre graceful
   - El nodo guarda su estado antes de detenerse

2. **Limpieza de recursos:**
   - Elimina el flag de auto-start (temporalmente)
   - Detiene el supervisor
   - Limpia archivos PID

3. **Reinicio:**
   - Inicia el proceso del nodo nuevamente
   - Crea nuevo flag de auto-start
   - Inicia el supervisor nuevamente
   - El nodo comienza a sincronizar con la red

## Consideraciones Importantes

### Para Validadores

> [!WARNING]
> **⚠️ Advertencia para Validadores**
>
> Al reiniciar un nodo validador:
> - Asegúrate de que el reinicio sea controlado (no fuerces el cierre)
> - El nodo puede perder algunos bloques durante el reinicio
> - En casos extremos, un reinicio mal ejecutado puede resultar en slashing
> - Siempre usa `node-stop` antes de reiniciar, nunca fuerces el cierre

### Tiempo de Reinicio

El tiempo de reinicio depende de:

- **Tiempo de detención:** Hasta 30 segundos para cierre graceful
- **Tiempo de inicio:** Generalmente unos segundos
- **Tiempo de sincronización:** Puede tomar tiempo si el nodo se desincronizó

### Estado de Sincronización

Después de reiniciar:

- El nodo comenzará a sincronizar automáticamente
- Puede tomar tiempo dependiendo de cuánto tiempo estuvo detenido
- Usa `node-process-status` para verificar el estado de sincronización

## Verificar el Reinicio

Después de reiniciar, verifica que el nodo esté funcionando correctamente:

### 1. Verificar Estado del Proceso

```bash
./drive.sh exec infinite node-process-status
```

**Qué buscar:**
- El proceso está ejecutándose
- El PID es diferente al anterior (confirmación de reinicio)
- El nodo está sincronizando

### 2. Verificar Logs

```bash
./drive.sh exec infinite node-logs -f
```

**Qué buscar:**
- Mensajes de inicio exitoso
- Conexión con peers
- Proceso de sincronización

### 3. Verificar Sincronización

Consulta la guía de [Monitoreo del Nodo]({{< relref "node-monitoring" >}}) para verificar el estado de sincronización.

## Solución de Problemas

Si encuentras problemas al reiniciar el nodo:

- **[Problemas de Inicio y Detención]({{< relref "../../troubleshooting/node-start-stop-issues" >}})** - Soluciones a problemas comunes
- **[Problemas Comunes]({{< relref "../../troubleshooting/common-issues" >}})** - Otros problemas comunes

## Próximos Pasos

Después de reiniciar tu nodo:

1. **[Monitoreo del Nodo]({{< relref "node-monitoring" >}})** - Monitorea el estado y sincronización
2. **[Interfaz Gráfica]({{< relref "graphical-interface" >}})** - Usa la interfaz gráfica para gestionar tu nodo
3. **[Gestión de Claves]({{< relref "keys" >}})** - Si eres validador, gestiona tus claves criptográficas

## Ver También

- [Iniciar/Detener Nodo]({{< relref "start-stop-node" >}}) - Cómo iniciar y detener el nodo individualmente
- [Monitoreo del Nodo]({{< relref "node-monitoring" >}}) - Guía completa para monitorear estado, logs y sincronización
- [Interfaz Gráfica]({{< relref "graphical-interface" >}}) - Usa la interfaz gráfica para todas las operaciones
- [Problemas de Inicio y Detención]({{< relref "../../troubleshooting/node-start-stop-issues" >}}) - Solución de problemas relacionados

