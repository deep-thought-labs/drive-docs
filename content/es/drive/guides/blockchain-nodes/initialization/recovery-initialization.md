---
title: "Inicialización con Recovery"
weight: 52232
---

Guía paso a paso para inicializar un nodo blockchain usando el modo recovery. Este modo es **requerido para [nodos validadores]({{< relref "../keys/understanding-keys" >}})** y altamente recomendado para cualquier nodo que necesite recuperar su identidad.

## ¿Qué es la Inicialización con Recovery?

La inicialización con recovery usa una frase semilla para generar **siempre la misma** [Private Validator Key]({{< relref "../../../../../concepts/private-validator-key" >}}), permitiéndote recuperarla en cualquier momento.

**Características:**
- ✅ **Recuperable** - Siempre puedes regenerar la misma clave con la frase semilla
- ✅ **Consistente** - La misma semilla siempre genera la misma clave
- ✅ **Portable** - Puedes restaurar tu validador en cualquier servidor
- ✅ **Requerido para validadores** - Te permite recuperar tu validador si algo falla

## Requisitos Previos

Antes de inicializar con recovery, necesitas:

- **Una frase semilla (12 o 24 palabras)** - Puedes crear una usando [Gestión de Claves]({{< relref "../keys" >}})
- **Respaldo seguro de la frase semilla** - Asegúrate de tenerla respaldada antes de continuar

Para más información sobre cómo crear y respaldar una frase semilla, consulta:
- [Operaciones de Gestión de Claves]({{< relref "../keys/operations" >}}) - Cómo generar claves y obtener tu frase semilla
- [Mejores Prácticas de Seguridad]({{< relref "../keys/security" >}}) - Cómo respaldar tu frase semilla de forma segura

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

4. Selecciona **"Initialize with Recovery (Validator)"**

   ![Advanced Operations - Initialize with Recovery (Validator) seleccionada](/images/node-ui-advanced-operations-op2-init-revery.png)

   Esta opción inicializa el nodo usando una frase semilla, asegurando que siempre generes la misma Private Validator Key.

5. Cuando se solicite, ingresa tu frase semilla (12 o 24 palabras)

6. Sigue las instrucciones en pantalla para completar la inicialización

## Usando Línea de Comandos

```bash
cd services/node0-infinite  # O cualquier otro servicio
./drive.sh up -d            # Asegúrate de que el contenedor esté ejecutándose
./drive.sh exec -it infinite node-init --recover
```

**Nota:** Usa `-it` (interactive) para poder ingresar la frase semilla.

### Qué Hace el Comando

El comando de inicialización con recovery realiza las siguientes operaciones:

- **Te solicita ingresar tu frase semilla (12 o 24 palabras):**
  - El sistema valida que la frase semilla sea válida (formato BIP39)
  - Debes ingresar exactamente la misma frase semilla que usaste para crear tu clave

- **Genera siempre la misma [Private Validator Key]({{< relref "../../../../../concepts/private-validator-key" >}}):**
  - Usando esa frase semilla, genera **siempre la misma** clave
  - Puedes inicializar el nodo múltiples veces con la misma semilla y obtendrás **exactamente la misma clave**
  - El archivo `priv_validator_key.json` se crea con el contenido determinístico

- **Crea los archivos de configuración del nodo:**
  - `config.toml` - Configuración general del nodo
  - `app.toml` - Configuración de la aplicación blockchain
  - `client.toml` - Configuración del cliente

- **Descarga el [archivo génesis]({{< relref "../../../../../concepts/genesis-file" >}}) oficial de la red:**
  - El archivo `genesis.json` se descarga desde el repositorio oficial
  - Contiene el estado inicial de la blockchain

- **Establece el Chain ID basado en la configuración del servicio:**
  - El Chain ID se configura automáticamente según el servicio

### Salida Esperada

Después de ejecutar el comando, deberías ver:

```
Enter your bip39 mnemonic
```

Ingresa tu frase semilla (12 o 24 palabras) cuando se solicite.

Después de ingresar la frase semilla correctamente:

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
- `priv_validator_key.json` (contenido determinístico basado en tu frase semilla)

## Ventajas para Validadores

Si inicializas con recovery usando una frase semilla, puedes restaurar tu validador en cualquier momento, en cualquier servidor, simplemente usando la misma frase semilla. Esto te permite:

- **Mover tu validador a otro servidor** - Simplemente inicializa con la misma frase semilla en el nuevo servidor
- **Restaurar tu validador después de un fallo del sistema** - No pierdes tu validador si el servidor falla
- **Tener la certeza de recuperación** - Siempre tendrás acceso a tu validador mientras tengas tu frase semilla

> [!NOTE]
> **Workflow para Validadores**
>
> Si estás siguiendo el workflow completo para validadores, después de inicializar con recovery, continúa con los siguientes pasos del workflow:
> - Agregar la clave al keyring (si usaste Dry-Run)
> - Verificar la Private Validator Key
> - Crear el validador en la blockchain
>
> Consulta [Workflow para Validadores]({{< relref "../keys/validator-workflow" >}}) para el flujo completo paso a paso.

## Verificación

Después de inicializar, verifica que todo se creó correctamente. Consulta [Verificación Post-Inicialización]({{< relref "verification" >}}) para más detalles.

**Importante:** Para validadores, es especialmente importante verificar que la Private Validator Key se generó correctamente y que puedes recuperarla usando la misma frase semilla.

## Solución de Problemas

### Error: "Invalid mnemonic"

Si recibes este error al usar recovery mode:

- **Verifica que ingresaste exactamente la misma frase semilla** (12 o 24 palabras)
- **Asegúrate de no tener espacios extra** al inicio o final
- **Verifica que todas las palabras estén escritas correctamente**
- **Asegúrate de usar el formato BIP39 estándar**

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

> [!NOTE]
> **Si eres Validador**
>
> Si estás configurando un validador, después de inicializar con recovery, consulta [Workflow para Validadores]({{< relref "../keys/validator-workflow" >}}) para los pasos adicionales necesarios (agregar clave al keyring, verificar Private Validator Key, crear el validador en la blockchain).

## Ver También

- [Inicialización Simple]({{< relref "simple-initialization" >}}) - Si no necesitas recuperabilidad (solo full nodes)
- [Verificación Post-Inicialización]({{< relref "verification" >}}) - Verifica que la inicialización fue exitosa
- [Inicialización de Nodo]({{< relref "." >}}) - Comparación de modos y cuándo usar cada uno
- [Gestión de Claves]({{< relref "../keys" >}}) - Guía completa para gestionar claves criptográficas
- [Private Validator Key]({{< relref "../../../../../concepts/private-validator-key" >}}) - Qué es el Private Validator Key

