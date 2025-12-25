---
title: "Inicializar Nodo"
weight: 5223
---

Guía completa para inicializar un nodo blockchain. La inicialización es el proceso de configurar el estado inicial del nodo, incluyendo la generación de [claves]({{< relref "../../../../concepts/key" >}}) y la descarga del [archivo génesis]({{< relref "../../../../concepts/genesis-file" >}}).

> [!NOTE]
> **Conceptos Fundamentales**
>
> Antes de continuar, asegúrate de entender los conceptos básicos:
>
> - [Inicialización de Nodo]({{< relref "../../../../concepts/node-initialization" >}}) - Qué es la inicialización y qué componentes crea
> - [Archivo Génesis]({{< relref "../../../../concepts/genesis-file" >}}) - Qué es el archivo génesis y su propósito
> - [Data del Nodo]({{< relref "../../../../concepts/node-data" >}}) - Qué es la data del nodo y dónde se almacena
> - [Private Validator Key]({{< relref "../../../../concepts/private-validator-key" >}}) - Qué es el Private Validator Key y su importancia

## ¿Qué es la Inicialización?

La inicialización de un nodo blockchain es el proceso de configurar su estado inicial. Durante este proceso:

- Se crean los archivos de configuración del nodo (`config.toml`, `app.toml`, `client.toml`)
- Se generan las [claves criptográficas]({{< relref "../../../../concepts/key" >}}) necesarias, incluyendo la [Private Validator Key]({{< relref "../../../../concepts/private-validator-key" >}})
- Se descarga el [archivo génesis]({{< relref "../../../../concepts/genesis-file" >}}) oficial de la red
- Se establece el Chain ID basado en la configuración del servicio

Para más detalles sobre qué componentes se crean durante la inicialización, consulta [Inicialización de Nodo]({{< relref "../../../../concepts/node-initialization" >}}).

## Modos de Inicialización

Existen dos modos de inicialización disponibles, cada uno con características diferentes:

### Inicialización Simple

La inicialización simple genera una [Private Validator Key]({{< relref "../../../../concepts/private-validator-key" >}}) **aleatoria y única** que **no se puede recuperar** si la pierdes.

**Características:**
- ✅ **Rápida y sencilla** - No requiere gestionar frases semilla
- ✅ **Adecuada para full nodes** - No necesitas recuperar la clave
- ❌ **No recuperable** - Si pierdes el archivo `priv_validator_key.json`, no hay forma de recuperarlo
- ❌ **Diferente cada vez** - Cada inicialización genera una clave nueva

### Inicialización con Recovery

La inicialización con recovery usa una frase semilla para generar **siempre la misma** [Private Validator Key]({{< relref "../../../../concepts/private-validator-key" >}}), permitiéndote recuperarla en cualquier momento.

**Características:**
- ✅ **Recuperable** - Siempre puedes regenerar la misma clave con la frase semilla
- ✅ **Consistente** - La misma semilla siempre genera la misma clave
- ✅ **Portable** - Puedes restaurar tu validador en cualquier servidor
- ✅ **Requerido para validadores** - Te permite recuperar tu validador si algo falla

## Comparación de Modos

| Aspecto | Inicialización Simple | Inicialización con Recovery |
|---------|----------------------|----------------------------|
| **Comando** | `node-init` | `node-init --recover` |
| **Requiere frase semilla** | ❌ No | ✅ Sí |
| **Clave generada** | Aleatoria, única | Determinística (misma semilla = misma clave) |
| **Recuperable** | ❌ No | ✅ Sí |
| **Adecuada para full nodes** | ✅ Sí | ✅ Sí |
| **Adecuada para validadores** | ❌ **NO** | ✅ **SÍ (Requerido)** |
| **Riesgo de pérdida** | Alto (pérdida permanente) | Bajo (recuperable con semilla) |

## Impacto en la Recuperabilidad

### Con Inicialización Simple

```
Inicialización 1 → priv_validator_key: ABC123...
Inicialización 2 → priv_validator_key: XYZ789... (diferente)
Inicialización 3 → priv_validator_key: DEF456... (diferente)
```

**Problema:** Si pierdes el archivo `priv_validator_key.json` de la inicialización 1, no hay forma de recuperarlo.

### Con Inicialización con Recovery

```
Inicialización 1 (semilla: "palabra1 palabra2 ...") → priv_validator_key: ABC123...
Inicialización 2 (semilla: "palabra1 palabra2 ...") → priv_validator_key: ABC123... (misma)
Inicialización 3 (semilla: "palabra1 palabra2 ...") → priv_validator_key: ABC123... (misma)
```

**Ventaja:** Siempre puedes regenerar la misma clave usando la misma frase semilla.

## Cuándo Usar Cada Modo

### Para Full Nodes

- Puedes usar **inicialización simple** sin preocuparte por las claves
- El nodo generará claves automáticamente para su funcionamiento interno
- No necesitas respaldar estas claves porque no representan una identidad crítica en la blockchain

### Para Validadores

- **DEBES** usar **inicialización con recovery** usando una frase semilla
- **DEBES** respaldar tu frase semilla de forma segura
- Si pierdes tu `priv_validator_key` (y no usaste recovery), perderás tu validador permanentemente

> [!WARNING]
> **⚠️ Advertencia para Validadores**
>
> Si inicializas tu nodo de forma simple y luego creas un validador con esa clave, **NO podrás recuperar esa clave si la pierdes**. Si pierdes el archivo `priv_validator_key.json`, perderás permanentemente el control de tu validador.
>
> **NO uses inicialización simple para validadores.**

## Inicialización Simple

Este modo es adecuado para [full nodes]({{< relref "keys/understanding-keys" >}}) que no actuarán como validadores.

### Usando Interfaz Gráfica

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

### Usando Línea de Comandos

```bash
cd services/node0-infinite  # O cualquier otro servicio
./drive.sh up -d            # Asegúrate de que el contenedor esté ejecutándose
./drive.sh exec infinite node-init
```

**Qué hace:**
- Crea los archivos de configuración del nodo
- Genera una [Private Validator Key]({{< relref "../../../../concepts/private-validator-key" >}}) aleatoria y única
- Descarga el [archivo génesis]({{< relref "../../../../concepts/genesis-file" >}}) oficial de la red
- Establece el Chain ID basado en la configuración del servicio

**Salida esperada:**
- Mensaje de éxito: `✅ Node initialized successfully!`
- Ubicación de configuración: `persistent-data/config/`
- Instrucciones para iniciar el nodo

> [!NOTE]
> **Si el nodo ya está inicializado**
>
> Si el nodo ya está inicializado, el comando mostrará un error. Para reinicializar, primero debes eliminar la [data del nodo]({{< relref "../../../../concepts/node-data" >}}). Consulta [Iniciar/Detener Nodo]({{< relref "start-stop-node" >}}) para más información sobre cómo limpiar los datos del nodo.

## Inicialización con Recovery

Este modo es **requerido para [nodos validadores]({{< relref "keys/understanding-keys" >}})** y altamente recomendado para cualquier nodo que necesite recuperar su identidad.

### Usando Interfaz Gráfica

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

4. Selecciona **"Initialize with Recovery (Validator)"**

   ![Advanced Operations - Initialize with Recovery (Validator) seleccionada](/images/node-ui-advanced-operations-op2-init-revery.png)

   Esta opción inicializa el nodo usando una frase semilla, asegurando que siempre generes la misma Private Validator Key.

5. Cuando se solicite, ingresa tu frase semilla (12 o 24 palabras)

6. Sigue las instrucciones en pantalla para completar la inicialización

### Usando Línea de Comandos

```bash
cd services/node0-infinite  # O cualquier otro servicio
./drive.sh up -d            # Asegúrate de que el contenedor esté ejecutándose
./drive.sh exec -it infinite node-init --recover
```

**Qué hace:**
- Te solicita ingresar tu frase semilla (12 o 24 palabras)
- Usando esa frase semilla, genera **siempre la misma** [Private Validator Key]({{< relref "../../../../concepts/private-validator-key" >}})
- Crea los archivos de configuración del nodo
- Descarga el [archivo génesis]({{< relref "../../../../concepts/genesis-file" >}}) oficial de la red
- Establece el Chain ID basado en la configuración del servicio

**Salida esperada:**
- Prompt: `Enter your bip39 mnemonic`
- Ingresa tu frase semilla (12 o 24 palabras)
- Mensaje de éxito: `✅ Node initialized successfully!`
- Ubicación de configuración: `persistent-data/config/`

**Nota:** Usa `-it` (interactive) para poder ingresar la frase semilla.

### Ventajas para Validadores

Si inicializas con recovery usando una frase semilla, puedes restaurar tu validador en cualquier momento, en cualquier servidor, simplemente usando la misma frase semilla. Esto te permite:

- Mover tu validador a otro servidor
- Restaurar tu validador después de un fallo del sistema
- Tener la certeza de que siempre tendrás acceso a tu validador mientras tengas tu frase semilla

Para más información sobre el workflow completo para validadores, consulta [Workflow para Validadores]({{< relref "keys/validator-workflow" >}}).

## Verificación Post-Inicialización

Después de inicializar el nodo, verifica que todo se creó correctamente:

### Verificar Archivos de Configuración

```bash
# Verifica que los archivos de configuración existen
ls -la persistent-data/config/

# Archivos esperados:
# - config.toml
# - app.toml
# - client.toml
# - genesis.json
# - priv_validator_key.json
```

### Verificar Private Validator Key

```bash
# Verifica que el archivo existe
ls -la persistent-data/config/priv_validator_key.json

# Revisa el contenido (opcional, para verificar)
cat persistent-data/config/priv_validator_key.json
```

> [!IMPORTANT]
> **El Archivo Siempre se Crea**
>
> Cuando inicializas un nodo, **siempre se crea el archivo `priv_validator_key.json`**, sin importar el método de inicialización que uses (simple o recovery). La diferencia está en el **contenido** del archivo:
>
> - **Inicialización simple:** El contenido es aleatorio y diferente cada vez que inicializas
> - **Inicialización con recovery:** El contenido es siempre el mismo si usas la misma frase semilla

### Verificar Archivo Génesis

```bash
# Verifica que el archivo génesis existe
ls -la persistent-data/config/genesis.json

# Verifica el Chain ID (opcional)
cat persistent-data/config/genesis.json | grep chain_id
```

## Solución de Problemas

### Error: "Node already initialized"

Si recibes este error, significa que el nodo ya fue inicializado previamente. Para reinicializar:

1. **Detén el nodo** (si está ejecutándose)
2. **Elimina la data del nodo** usando la interfaz gráfica o comandos
3. **Vuelve a inicializar** con el método que prefieras

Para más detalles sobre cómo limpiar los datos del nodo, consulta [Iniciar/Detener Nodo]({{< relref "start-stop-node" >}}).

### Error: "Invalid mnemonic" (Recovery Mode)

Si recibes este error al usar recovery mode:

- Verifica que ingresaste exactamente la misma frase semilla (12 o 24 palabras)
- Asegúrate de no tener espacios extra al inicio o final
- Verifica que todas las palabras estén escritas correctamente
- Asegúrate de usar el formato BIP39 estándar

### No Puedo Encontrar mis Archivos de Configuración

Los archivos de configuración se almacenan en:

- **Ruta en el host:** `./persistent-data/config/` (relativa al directorio del servicio)
- **Ruta en el contenedor:** `/home/ubuntu/.infinited/config/`

Asegúrate de estar en el directorio correcto del servicio cuando busques estos archivos.

## Próximos Pasos

Después de inicializar tu nodo:

1. **[Iniciar/Detener Nodo]({{< relref "start-stop-node" >}})** - Aprende a iniciar y detener tu nodo
2. **[Gestión de Claves]({{< relref "keys" >}})** - Si eres validador, gestiona tus claves criptográficas
3. **[Interfaz Gráfica]({{< relref "graphical-interface" >}})** - Usa la interfaz gráfica para gestionar tu nodo

## Ver También

### Conceptos Fundamentales

- [Inicialización de Nodo]({{< relref "../../../../concepts/node-initialization" >}}) - Qué es la inicialización y qué componentes crea
- [Archivo Génesis]({{< relref "../../../../concepts/genesis-file" >}}) - Qué es el archivo génesis y su propósito
- [Data del Nodo]({{< relref "../../../../concepts/node-data" >}}) - Qué es la data del nodo y dónde se almacena
- [Private Validator Key]({{< relref "../../../../concepts/private-validator-key" >}}) - Qué es el Private Validator Key y su importancia
- [Key]({{< relref "../../../../concepts/key" >}}) - Qué es una clave criptográfica

### Guías Relacionadas

- [Workflow para Validadores]({{< relref "keys/validator-workflow" >}}) - Guía paso a paso para validadores
- [Entender las Claves]({{< relref "keys/understanding-keys" >}}) - Diferencias entre validadores y full nodes
- [Iniciar/Detener Nodo]({{< relref "start-stop-node" >}}) - Cómo iniciar y detener tu nodo
- [Interfaz Gráfica]({{< relref "graphical-interface" >}}) - Usa la interfaz gráfica para gestionar tu nodo
