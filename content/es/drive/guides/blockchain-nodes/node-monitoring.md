---
title: "Monitoreo del Nodo"
weight: 5226
---

Guía completa para monitorear el estado y actividad de tu nodo blockchain. Esta guía cubre todas las opciones de monitoreo disponibles, incluyendo logs, estado del proceso, sincronización y diagnóstico de red.

## Acceder al Monitoreo

Todas las opciones de monitoreo están disponibles a través de la interfaz gráfica en el submenú **"Node Monitoring"**.

### Usando Interfaz Gráfica (Recomendado)

1. Abre la interfaz gráfica (ver [Interfaz Gráfica]({{< relref "graphical-interface" >}}))

2. Navega: Menú Principal → **"Node Monitoring"**

   ![Submenú Node Monitoring](/images/node-ui-monitoring.png)

Este submenú contiene todas las opciones para monitorear el estado y los logs del nodo.

## Opciones de Monitoreo Disponibles

El submenú **"Node Monitoring"** incluye las siguientes opciones:

1. **Node Status** - Verificar el estado del proceso del nodo
2. **View Logs** - Ver las últimas N líneas de logs
3. **Follow Logs** - Seguir logs en tiempo real
4. **Network Diagnosis** - Diagnóstico de red y información del sistema

## Verificar Estado del Proceso del Nodo

Verifica si el proceso del nodo está ejecutándose y obtén información sobre el proceso.

### Usando Interfaz Gráfica (Recomendado)

1. En el submenú **"Node Monitoring"**, selecciona **"Node Status"** o **"Node Process Status"**

2. La interfaz mostrará información sobre el estado del proceso:
   - Si está ejecutándose: PID, usuario, tiempo de CPU y comando completo
   - Si no está ejecutándose: Mensaje indicando que el nodo no está activo

### Usando Línea de Comandos

```bash
./drive.sh exec infinite node-process-status
```

**Qué hace:** Verifica si el proceso del nodo está actualmente ejecutándose y muestra información del proceso.

**Salida esperada:**
- **Si está ejecutándose:** Muestra PID, usuario, tiempo de CPU y comando completo
- **Si no está ejecutándose:** Muestra mensaje de error con instrucciones para iniciar el nodo

**Cuándo usar:** Verificación rápida de que el proceso del nodo está activo, especialmente útil para troubleshooting o scripts de monitoreo.

> [!NOTE]
> **Nota sobre el Estado**
>
> Este comando verifica el estado del proceso, no el estado de sincronización de la blockchain. Para verificar la sincronización de la blockchain, consulta la sección "Verificar Sincronización" más abajo.

## Ver Logs del Nodo

Los logs del nodo contienen información detallada sobre la actividad del nodo blockchain, incluyendo sincronización, procesamiento de bloques, errores y estado de conexión.

**Ubicación del archivo de logs:** `/var/log/node/node.log`

### Ver Últimas Líneas de Logs

Muestra las últimas N líneas de logs del nodo.

#### Usando Interfaz Gráfica (Recomendado)

1. En el submenú **"Node Monitoring"**, selecciona **"View Logs"**

2. La interfaz te permitirá especificar cuántas líneas deseas ver (por defecto, las últimas 50 líneas)

3. Los logs se mostrarán en la pantalla con la información más reciente

#### Usando Línea de Comandos

```bash
# Últimas 50 líneas (por defecto)
./drive.sh exec infinite node-logs

# Últimas N líneas (especificar número)
./drive.sh exec infinite node-logs 100
./drive.sh exec infinite node-logs 200
```

**Qué hace:** Muestra las últimas N líneas del archivo de logs del nodo (`/var/log/node/node.log`).

**Salida esperada:** Entradas de logs recientes mostrando:
- Mensajes de inicio del nodo
- Progreso de sincronización
- Procesamiento de bloques
- Errores o advertencias
- Estado de conexión

**Cuándo usar:** Para revisar actividad reciente del nodo, verificar errores o revisar el progreso de sincronización.

### Seguir Logs en Tiempo Real

Muestra los logs del nodo en tiempo real, actualizándose automáticamente a medida que se escriben nuevas entradas.

#### Usando Interfaz Gráfica (Recomendado)

1. En el submenú **"Node Monitoring"**, selecciona **"Follow Logs"**

2. Los logs comenzarán a mostrarse en tiempo real

3. Para detener el seguimiento, presiona `Ctrl+C`

#### Usando Línea de Comandos

```bash
./drive.sh exec infinite node-logs -f
# o
./drive.sh exec infinite node-logs --follow
```

**Qué hace:** Transmite las entradas de logs en tiempo real a medida que se escriben en el archivo de logs (similar a `tail -f`).

**Salida esperada:** Muestra el mensaje `ℹ️  Following node logs (Ctrl+C to exit)...` seguido de un flujo continuo de entradas de logs. Presiona `Ctrl+C` para detener.

**Cuándo usar:** Monitorear la actividad del nodo mientras está ejecutándose, observar el progreso de sincronización en tiempo real, o depurar problemas mientras ocurren.

## Verificar Sincronización

Después de iniciar tu nodo, comenzará a sincronizar con la red blockchain. Necesitas verificar que la sincronización esté completa antes de proceder con operaciones de validador.

### Usando Interfaz Gráfica (Recomendado)

1. En el submenú **"Node Monitoring"**, selecciona **"Node Status"** o **"View Logs"**

2. Busca indicadores de progreso de sincronización en los logs:
   - Mensajes sobre bloques siendo sincronizados
   - Progreso de sincronización
   - Mensajes indicando que la sincronización está completa

### Usando Línea de Comandos

```bash
./drive.sh exec infinite infinited status
```

**Qué buscar:**
- **`catching_up: false`** - El nodo está completamente sincronizado
- **`catching_up: true`** - El nodo aún está sincronizando (espera hasta que sea `false`)
- **`latest_block_height`** - Altura del bloque actual que el nodo ha sincronizado
- **`earliest_block_height`** - Bloque más antiguo que el nodo tiene

**Cuando la sincronización esté completa:**
- El nodo está listo para operaciones normales
- Para nodos validadores, puedes proceder con crear tu validador en la blockchain
- **Nota:** Las instrucciones para crear validadores en la blockchain se agregarán a la documentación en una actualización futura

## Diagnóstico de Red e Información del Sistema

El submenú **"Node Monitoring"** también incluye opciones para diagnóstico de red e información del sistema.

### Usando Interfaz Gráfica (Recomendado)

1. En el submenú **"Node Monitoring"**, busca opciones como:
   - **Network Diagnosis** - Diagnóstico de conectividad de red
   - **System Information** - Información sobre el sistema y el contenedor

2. Selecciona la opción deseada para ver la información correspondiente

### Información Disponible

Las opciones de diagnóstico y sistema pueden incluir:

- **Estado de conexión de red** - Verificación de conectividad con otros nodos
- **Información del sistema** - Detalles sobre el contenedor y recursos del sistema
- **Configuración de red** - Puertos y configuración de red del nodo
- **Estadísticas del nodo** - Métricas de rendimiento y actividad

## Interpretar los Logs

Los logs del nodo contienen información valiosa sobre el estado y la actividad del nodo. Aquí hay algunos elementos comunes que puedes encontrar:

### Mensajes de Inicio

Cuando el nodo inicia, verás mensajes como:
- Inicialización de componentes
- Carga de configuración
- Conexión a la red

### Progreso de Sincronización

Durante la sincronización, verás mensajes sobre:
- Bloques siendo descargados
- Progreso de sincronización (porcentaje o altura de bloque)
- Tiempo estimado de sincronización

### Procesamiento de Bloques

Una vez sincronizado, verás mensajes sobre:
- Bloques nuevos siendo procesados
- Transacciones siendo validadas
- Estado de la blockchain siendo actualizado

### Errores y Advertencias

Los logs también mostrarán:
- Errores de conexión
- Problemas de sincronización
- Advertencias sobre configuración
- Errores de validación

### Estado de Conexión

Información sobre:
- Conexiones con otros nodos (peers)
- Estado de la red P2P
- Latencia y calidad de conexión

## Solución de Problemas con Logs

Si encuentras problemas con los logs del nodo, consulta la guía centralizada de troubleshooting:

- **[Problemas con Logs del Nodo]({{< relref "../../troubleshooting/node-log-issues" >}})** - Soluciones a problemas comunes relacionados con logs

## Próximos Pasos

Después de monitorear tu nodo:

1. **[Iniciar/Detener Nodo]({{< relref "start-stop-node" >}})** - Gestiona el ciclo de vida del nodo
2. **[Interfaz Gráfica]({{< relref "graphical-interface" >}})** - Usa la interfaz gráfica para todas las operaciones
3. **[Gestión de Claves]({{< relref "keys" >}})** - Si eres validador, gestiona tus claves criptográficas
4. **[Solución de Problemas]({{< relref "../../troubleshooting" >}})** - Si encuentras problemas, consulta la guía de troubleshooting

## Ver También

- [Iniciar/Detener Nodo]({{< relref "start-stop-node" >}}) - Cómo iniciar y detener el nodo
- [Interfaz Gráfica]({{< relref "graphical-interface" >}}) - Guía completa de la interfaz gráfica
- [Gestión de Contenedores]({{< relref "../general/container-management" >}}) - Cómo gestionar el contenedor Docker
- [Solución de Problemas]({{< relref "../../troubleshooting" >}}) - Guías de troubleshooting

