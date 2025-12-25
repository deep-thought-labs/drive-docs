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

1. Abre la interfaz gráfica:

   ```bash
   cd services/node0-infinite  # O cualquier otro servicio
   ./drive.sh up -d            # Asegúrate de que el contenedor esté ejecutándose
   ./drive.sh exec infinite node-ui
   ```

2. En el menú principal, selecciona **"Node Operations"**

   ![Menú Principal - Node Operations seleccionada](/images/node-ui-op2-operations.png)

3. Selecciona **"Advanced Operations"**

   ![Node Operations - Advanced Operations seleccionada](/images/node-ui-operations-op4-advanced-operations.png)

4. Selecciona **"Initialize Node (Simple)"**

   ![Advanced Operations - Initialize Node (Simple) seleccionada](/images/node-ui-advanced-operations-op1-init-simple.png)

   Esta opción inicializa el nodo generando una clave aleatoria que no se puede recuperar.

5. Sigue las instrucciones en pantalla para completar la inicialización

## Usando Línea de Comandos

```bash
cd services/node0-infinite  # O cualquier otro servicio
./drive.sh up -d            # Asegúrate de que el contenedor esté ejecutándose
./drive.sh exec infinite node-init
```

### Qué Hace el Comando

El comando de inicialización simple realiza las siguientes operaciones:

- **Crea los archivos de configuración del nodo:**
  - `config.toml` - Configuración general del nodo
  - `app.toml` - Configuración de la aplicación blockchain
  - `client.toml` - Configuración del cliente

- **Genera una [Private Validator Key]({{< relref "../../../../../concepts/private-validator-key" >}}) aleatoria y única:**
  - El archivo `priv_validator_key.json` se crea con una clave aleatoria
  - Esta clave **no se puede recuperar** si la pierdes
  - Cada vez que inicializas de forma simple, obtienes una clave diferente

- **Descarga el [archivo génesis]({{< relref "../../../../../concepts/genesis-file" >}}) oficial de la red:**
  - El archivo `genesis.json` se descarga desde el repositorio oficial
  - Contiene el estado inicial de la blockchain

- **Establece el Chain ID basado en la configuración del servicio:**
  - El Chain ID se configura automáticamente según el servicio

### Salida Esperada

Después de ejecutar el comando, deberías ver:

```
✅ Node initialized successfully!
```

**Ubicación de configuración:**
- **Ruta en el host:** `./persistent-data/config/` (relativa al directorio del servicio)
- **Ruta en el contenedor:** `/home/ubuntu/.infinited/config/`

**Archivos creados:**
- `config.toml`
- `app.toml`
- `client.toml`
- `genesis.json`
- `priv_validator_key.json`

## Verificación

Después de inicializar, verifica que todo se creó correctamente. Consulta [Verificación Post-Inicialización]({{< relref "verification" >}}) para más detalles.

## Solución de Problemas

### Error: "Node already initialized"

Si recibes este error, significa que el nodo ya fue inicializado previamente. Para reinicializar:

1. **Detén el nodo** (si está ejecutándose)
2. **Elimina la data del nodo** usando la interfaz gráfica o comandos
3. **Vuelve a inicializar** con el método que prefieras

Para más detalles sobre cómo limpiar los datos del nodo, consulta [Iniciar/Detener Nodo]({{< relref "../start-stop-node" >}}).

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

