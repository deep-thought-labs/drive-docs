---
title: "Iniciar/Detener Nodo"
weight: 5224
---

Guía completa para iniciar, detener y gestionar el ciclo de vida de tu nodo blockchain. Esta guía cubre tanto la **interfaz gráfica (recomendada)** como las **operaciones de línea de comandos (para usuarios avanzados)**.

## Iniciar Nodo

Después de inicializar tu nodo, necesitas iniciarlo para que comience a sincronizar con la red blockchain.

### Usando Interfaz Gráfica (Recomendado)

1. Abre la interfaz gráfica:

   ```bash
   cd services/node0-infinite  # O cualquier otro servicio
   ./drive.sh up -d            # Asegúrate de que el contenedor esté ejecutándose
   ./drive.sh exec infinite node-ui
   ```

2. En el menú principal, selecciona **"Node Operations"**

   ![Menú Principal - Node Operations seleccionada](/images/node-ui-op2-operations.png)

3. Selecciona **"Start Node"**

   ![Node Operations - Start Node seleccionada](/images/node-ui-operations-op1-start.png)

4. La interfaz mostrará el proceso de inicio y confirmará cuando el nodo esté ejecutándose

### Usando Línea de Comandos

```bash
cd services/node0-infinite  # O cualquier otro servicio
./drive.sh up -d            # Asegúrate de que el contenedor esté ejecutándose
./drive.sh exec infinite node-start
```

**Qué hace:** Inicia el nodo blockchain como un proceso daemon en segundo plano. El nodo se ejecuta continuamente hasta que lo detengas manualmente.

**Cuándo usar:** Después de inicializar el nodo, o cuando necesites iniciar el nodo después de haberlo detenido.

**Salida esperada:**
- Muestra detalles de configuración: Chain ID, EVM Chain ID, directorio home, ubicación de logs
- Mensaje de éxito: `✅ Node started successfully (PID: 123)`
- Instrucciones para ver logs y detener el nodo

**Qué sucede internamente:**
1. Verifica que el nodo esté inicializado (comprueba la existencia de `genesis.json`)
2. Verifica que no haya otra instancia ejecutándose
3. Inicia el proceso del nodo en segundo plano usando `setsid` para aislamiento
4. Redirige toda la salida a `/var/log/node/node.log`
5. Guarda el ID del proceso (PID) para seguimiento
6. Crea el flag de auto-start para reinicio automático
7. Inicia el supervisor para monitoreo y reinicio automático

**Si el nodo ya está ejecutándose:** El comando mostrará una advertencia con el PID existente y saldrá sin iniciar una instancia duplicada.

## Detener Nodo

Detener el nodo de forma controlada es importante para mantener la integridad de los datos, especialmente para validadores.

### Usando Interfaz Gráfica (Recomendado)

1. Abre la interfaz gráfica:

   ```bash
   cd services/node0-infinite  # O cualquier otro servicio
   ./drive.sh exec infinite node-ui
   ```

2. En el menú principal, selecciona **"Node Operations"**

   ![Menú Principal - Node Operations seleccionada](/images/node-ui-op2-operations.png)

3. Selecciona **"Stop Node"**

   ![Node Operations - Stop Node seleccionada](/images/node-ui-operations-op2-stop.png)

4. Confirma la operación

### Usando Línea de Comandos

```bash
cd services/node0-infinite  # O cualquier otro servicio
./drive.sh exec infinite node-stop
```

**Qué hace:** Detiene el proceso del nodo de forma controlada. Envía una señal de terminación (SIGTERM) y espera a que el proceso se cierre correctamente.

**Cuándo usar:** Antes de hacer cambios de configuración, actualizar el nodo, o cuando necesites detener el nodo temporalmente.

**Salida esperada:**
- Encabezado: `Stopping Infinite Drive Blockchain Node`
- Mensaje: `Stopping node process (PID: 123)...`
- Éxito: `✅ Node stopped successfully`

**Cierre controlado:** El nodo guarda su estado antes de detenerse, asegurando la integridad de los datos. Esto es importante para validadores para evitar slashing (penalizaciones).

> [!WARNING]
> **⚠️ Advertencia para Validadores**
>
> Siempre detén el nodo de forma controlada antes de:
> - Apagar el servidor
> - Reiniciar el contenedor
> - Hacer cambios de configuración
>
> Un cierre abrupto puede causar problemas de sincronización y, en casos extremos, puede resultar en slashing para validadores.

## Verificar Estado y Sincronización

Para verificar el estado del nodo y su sincronización, consulta la guía completa de [Monitoreo del Nodo]({{< relref "node-monitoring" >}}), que incluye:

- Verificar estado del proceso del nodo
- Ver logs del nodo (últimas líneas y tiempo real)
- Verificar sincronización de la blockchain
- Diagnóstico de red e información del sistema

## Reiniciar Nodo

Para reiniciar el nodo (detener y volver a iniciar), consulta la guía completa:

- **[Reiniciar Nodo]({{< relref "restart-node" >}})** - Guía completa sobre cómo reiniciar el nodo

## Solución de Problemas

Si encuentras problemas al iniciar o detener el nodo, consulta la guía centralizada de troubleshooting:

- **[Problemas de Inicio y Detención del Nodo]({{< relref "../../troubleshooting/node-start-stop-issues" >}})** - Soluciones a problemas comunes relacionados con iniciar y detener el nodo


## Próximos Pasos

Después de iniciar tu nodo:

1. **[Monitoreo del Nodo]({{< relref "node-monitoring" >}})** - Monitorea el estado, logs y sincronización de tu nodo
2. **[Interfaz Gráfica]({{< relref "graphical-interface" >}})** - Usa la interfaz gráfica para gestionar tu nodo
3. **[Gestión de Claves]({{< relref "keys" >}})** - Si eres validador, gestiona tus claves criptográficas

## Ver También

- [Monitoreo del Nodo]({{< relref "node-monitoring" >}}) - Guía completa para monitorear estado, logs y sincronización
- [Inicialización de Nodo]({{< relref "initialization" >}}) - Cómo inicializar un nodo antes de iniciarlo
- [Borrar Data del Nodo]({{< relref "delete-node-data" >}}) - Cómo eliminar la data del nodo para reinicializar
- [Interfaz Gráfica]({{< relref "graphical-interface" >}}) - Usa la interfaz gráfica para gestionar tu nodo
- [Gestión de Contenedores]({{< relref "../general/container-management" >}}) - Cómo gestionar el contenedor Docker
- [Data del Nodo]({{< relref "../../../../concepts/node-data" >}}) - Entender qué es la data del nodo y su importancia
- [Problemas de Permisos]({{< relref "../../troubleshooting/permission-issues" >}}) - Solución de problemas de permisos
