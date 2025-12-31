---
title: "Inicialización Simple"
weight: 52231
---

Guía paso a paso para inicializar un nodo blockchain usando el modo simple. Este modo es adecuado para [full nodes]({{< relref "../keys/understanding-keys" >}}) que no actuarán como validadores.

## ¿Qué es la Inicialización Simple?

La inicialización simple genera una [Private Validator Key]({{< relref "../../../../../concepts/private-validator-key" >}}) **aleatoria y única** que **no se puede recuperar** si la pierdes. Es el método más rápido y sencillo para inicializar un nodo.

**Características:**
- ✅ **Rápida y sencilla** - No requiere gestionar frases semilla
- ✅ **Adecuada para full nodes** - No necesitas recuperar la clave
- ❌ **No recuperable** - Si pierdes el archivo `priv_validator_key.json`, no hay forma de recuperarlo
- ❌ **Diferente cada vez** - Cada inicialización genera una clave nueva

> [!WARNING]
> **⚠️ NO usar para Validadores**
>
> Si inicializas tu nodo de forma simple y luego creas un validador con esa clave, **NO podrás recuperar esa clave si la pierdes**. Si pierdes el archivo `priv_validator_key.json`, perderás permanentemente el control de tu validador.
>
> **Si eres validador, DEBES usar [Inicialización con Recovery]({{< relref "recovery-initialization" >}}).**

## Usando Interfaz Gráfica

1. Abre la interfaz gráfica (ver [Interfaz Gráfica]({{< relref "../graphical-interface" >}}))

2. Navega: Menú Principal → **"Node Operations"** → **"Advanced Operations"** → **"Initialize Node (Simple)"**

   ![Initialize Node (Simple) seleccionada](/images/node-ui-advanced-operations-op1-init-simple.png)

3. Sigue las instrucciones en pantalla para completar la inicialización

## Usando Línea de Comandos

### Sintaxis Simplificada (Recomendada)

{{< callout type="info" >}}
**Disponible desde Drive v0.1.12 (enero 2026)**

La sintaxis simplificada estará disponible a partir de la versión **Drive v0.1.12** en **enero de 2026**. Si estás usando una versión anterior, usa la sintaxis completa con `exec` y el nombre del servicio.
{{< /callout >}}

```bash
./drive.sh node-init
```

El script automáticamente:
- Detecta que es un comando `node-init`
- Obtiene el nombre del servicio del `docker-compose.yml` del directorio actual
- Agrega `exec` y el nombre del servicio
- Agrega `-it` automáticamente si es necesario (para solicitar el moniker)

### Sintaxis Completa (Alternativa)

Si prefieres especificar explícitamente el nombre del servicio:

```bash
./drive.sh exec infinite node-init
```

> [!NOTE]
> **Qué Hace el Comando**
>
> El comando crea los archivos de configuración, genera una [Private Validator Key]({{< relref "../../../../../concepts/private-validator-key" >}}) aleatoria (no recuperable), y descarga el [archivo génesis]({{< relref "../../../../../concepts/genesis-file" >}}) oficial. Para detalles técnicos del proceso, consulta [Flujo de Inicialización Técnico]({{< relref "../../../internal-workings/initialization-flow" >}}).

### Salida Esperada

Después de ejecutar el comando, deberías ver:

```
✅ Node initialized successfully!
```

> [!NOTE]
> **Archivos Creados**
>
> Los archivos de configuración se crean en `./persistent-data/config/` (host) o `/home/ubuntu/.infinited/config/` (contenedor). Para más detalles sobre la estructura de datos, consulta [Data del Nodo]({{< relref "../../../../../concepts/node-data" >}}).

## Verificación

Después de inicializar, verifica que todo se creó correctamente. Consulta [Verificación Post-Inicialización]({{< relref "verification" >}}) para más detalles.

## Solución de Problemas

### Error: "Node already initialized"

Si recibes este error, significa que el nodo ya fue inicializado previamente. Para reinicializar:

1. **Detén el nodo** (si está ejecutándose)
2. **Elimina la data del nodo** usando la interfaz gráfica o comandos
3. **Vuelve a inicializar** con el método que prefieras

Para más detalles sobre cómo eliminar los datos del nodo, consulta [Borrar Data del Nodo]({{< relref "../delete-node-data" >}}).

### No Puedo Encontrar mis Archivos de Configuración

Los archivos de configuración se almacenan en:

- **Ruta en el host:** `./persistent-data/config/` (relativa al directorio del servicio)
- **Ruta en el contenedor:** `/home/ubuntu/.infinited/config/`

Asegúrate de estar en el directorio correcto del servicio cuando busques estos archivos.

## Próximos Pasos

Después de inicializar tu nodo:

1. **[Verificación Post-Inicialización]({{< relref "verification" >}})** - Verifica que todo se creó correctamente
2. **[Iniciar/Detener Nodo]({{< relref "../start-stop-node" >}})** - Aprende a iniciar y detener tu nodo
3. **[Interfaz Gráfica]({{< relref "../graphical-interface" >}})** - Usa la interfaz gráfica para gestionar tu nodo

## Ver También

- [Inicialización con Recovery]({{< relref "recovery-initialization" >}}) - Si necesitas recuperabilidad (requerido para validadores)
- [Verificación Post-Inicialización]({{< relref "verification" >}}) - Verifica que la inicialización fue exitosa
- [Inicialización de Nodo]({{< relref "." >}}) - Comparación de modos y cuándo usar cada uno
- [Private Validator Key]({{< relref "../../../../../concepts/private-validator-key" >}}) - Qué es el Private Validator Key

