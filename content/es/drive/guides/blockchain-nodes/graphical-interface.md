---
title: "Interfaz Gráfica"
weight: 5221
---

La interfaz gráfica (node-ui) es el método recomendado para gestionar tus nodos blockchain. Proporciona acceso visual a todas las operaciones sin necesidad de recordar comandos.

## Abrir la Interfaz Gráfica

Para acceder a la interfaz gráfica:

```bash
cd services/node0-infinite  # O cualquier otro servicio
./drive.sh up -d            # Asegúrate de que el contenedor esté ejecutándose
./drive.sh exec infinite node-ui
```

> [!NOTE]
> **Sintaxis de Comandos y Nombres de Contenedores**
>
> Para entender cómo estructurar los comandos con `drive.sh` y conocer los nombres correctos de contenedores para cada servicio, consulta la sección [Comandos que Requieren Nombre de Contenedor]({{< relref "../general/container-management#comandos-que-requieren-nombre-de-contenedor" >}}) en Gestión de Contenedores.

**Ejemplos para diferentes servicios:**

```bash
# Infinite Mainnet
cd services/node0-infinite
./drive.sh exec infinite node-ui

# Infinite Testnet
cd services/node1-infinite-testnet
./drive.sh exec infinite-testnet node-ui

# Infinite Creative
cd services/node2-infinite-creative
./drive.sh exec infinite-creative node-ui

# QOM Network
cd services/node3-qom
./drive.sh exec qom node-ui
```

## Estructura de la Interfaz

La interfaz gráfica está organizada en **submenús** que puedes navegar usando las teclas de flecha y Enter. El menú principal tiene **cuatro opciones principales**, cada una con su propio submenú o función:

### Menú Principal

El menú principal contiene las siguientes opciones:

![Menú Principal de node-ui](/images/node-ui.png)

1. **Key Management** (Gestión de Claves)
2. **Node Operations** (Operaciones del Nodo)
3. **Node Monitoring** (Monitoreo del Nodo)
4. **Help and Documentation** (Ayuda y Documentación)

### Key Management (Gestión de Claves)

Al seleccionar "Key Management" desde el menú principal, accederás al submenú de gestión de claves:

![Submenú Key Management](/images/node-ui-keys.png)

Este submenú contiene todas las opciones relacionadas con la gestión de claves criptográficas.

### Node Operations (Operaciones del Nodo)

Al seleccionar "Node Operations" desde el menú principal, accederás al submenú de operaciones del nodo:

![Submenú Node Operations](/images/node-ui-operations.png)

Este submenú contiene las operaciones básicas del nodo.

#### Node Operations Advanced (Operaciones Avanzadas del Nodo)

Dentro del submenú "Node Operations", encontrarás la opción "Node Operations Advanced" que te lleva a operaciones más avanzadas:

![Submenú Node Operations Advanced](/images/node-ui-operations-advanced.png)

Este submenú contiene operaciones avanzadas como inicialización del nodo y otras configuraciones.

### Node Monitoring (Monitoreo del Nodo)

Al seleccionar "Node Monitoring" desde el menú principal, accederás al submenú de monitoreo:

![Submenú Node Monitoring](/images/node-ui-monitoring.png)

Este submenú contiene todas las opciones para monitorear el estado y los logs del nodo.

### Help and Documentation (Ayuda y Documentación)

La opción "Help and Documentation" imprime en consola información esencial sobre cómo utilizar los comandos directamente sin necesidad de utilizar la interfaz gráfica. Funciona como un sistema de ayuda (help) para las opciones del nodo, proporcionando ejemplos y explicaciones sobre los comandos disponibles.

> [!NOTE]
> **Nota sobre la Información de Ayuda**
>
> Algunos ejemplos de comandos que se muestran en el output de "Help and Documentation" pueden no estar completamente actualizados, especialmente en lo que respecta a:
> - Los nombres de los servicios a llamar
> - Los nombres específicos de algunos comandos
>
> Sin embargo, la explicación general y la estructura de los comandos es correcta y útil como referencia.

## Cómo Navegar

### Movimiento entre Opciones

- Usa **teclas de flecha (↑↓)** para moverte entre opciones
- Presiona **Enter** para seleccionar una opción y entrar a un submenú
- Puedes navegar libremente entre submenús según necesites

### Navegación hacia Atrás

Para volver al menú anterior, tienes dos opciones:

- **Opción "Back"**: Cada submenú tiene una opción "Back" que puedes seleccionar con las flechas y Enter para volver al menú anterior
- **Tecla Esc**: Presiona la tecla **Esc** para volver al menú anterior sin necesidad de seleccionar la opción "Back"

**Consejo:** No te preocupes por perderte - siempre puedes navegar de vuelta al menú principal usando la opción "Back" o la tecla Esc.

### Salir de la Interfaz Gráfica

Para salir completamente de la interfaz gráfica y terminar el proceso, tienes dos opciones:

- **Tecla Esc (desde el menú principal)**: Si estás en el menú principal, puedes presionar la tecla **Esc** para salir de la interfaz gráfica
- **Ctrl+C**: Presiona la combinación de teclas **Ctrl+C** para terminar el proceso y salir completamente de la interfaz gráfica desde cualquier menú o submenú

**Nota sobre Ctrl+C:**
- La combinación **Ctrl+C** funciona igual en macOS, Windows y Linux
- **Cmd+C** no está habilitado para salir de la interfaz
- Esta es la forma estándar de terminar procesos en terminal, similar a cualquier otro proceso que ejecutes en la línea de comandos

Al salir, la interfaz se cerrará inmediatamente y volverás a la línea de comandos de tu terminal.

## Ver También

- [Gestión de Claves]({{< relref "keys" >}}) - Guía completa sobre gestión de claves usando la interfaz
- [Inicializar Nodo]({{< relref "initialize-node" >}}) - Cómo inicializar un nodo usando la interfaz
- [Iniciar/Detener Nodo]({{< relref "start-stop-node" >}}) - Operaciones básicas del nodo
