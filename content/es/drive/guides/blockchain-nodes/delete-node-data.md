---
title: "Borrar Data del Nodo"
weight: 5225
---

Guía para eliminar la data del nodo blockchain. Esta operación elimina todos los datos del nodo, incluyendo bloques sincronizados, estado de la aplicación y claves criptográficas.

> [!WARNING]
> **⚠️ ADVERTENCIA CRÍTICA: Borrar Data del Nodo**
>
> **Esta operación elimina permanentemente:**
> - Todos los bloques sincronizados
> - El estado de la aplicación
> - Las claves criptográficas (si no están respaldadas)
> - Los archivos de configuración
>
> **Asegúrate de tener respaldos antes de borrar la data, especialmente si eres validador.**
>
> **Para validadores:** Si usaste inicialización con recovery, puedes recuperar tu Private Validator Key usando tu frase semilla. Si no tienes la frase semilla respaldada, perderás permanentemente el acceso a tu validador.

## ¿Cuándo Borrar la Data del Nodo?

Puedes necesitar borrar la data del nodo en los siguientes casos:

- **Reinicializar el nodo** - Para cambiar el modo de inicialización (simple a recovery o viceversa)
- **Resolver problemas de sincronización** - Para empezar desde cero si el nodo tiene problemas de sincronización
- **Cambiar de red** - Para conectarte a una red diferente
- **Verificar recuperabilidad** - Para probar que puedes recuperar tu validador usando tu frase semilla (ver [Verificación Post-Inicialización]({{< relref "initialization/verification#verificación-especial-para-recovery-mode" >}}))

## Requisitos Previos

Antes de borrar la data del nodo:

1. **Detén el nodo** - El nodo debe estar detenido antes de borrar la data
2. **Respaldos** - Asegúrate de tener respaldos de:
   - Tu frase semilla (si usaste recovery mode)
   - Tu Private Validator Key (`priv_validator_key.json`) si no usaste recovery
   - Cualquier configuración personalizada que hayas hecho

> [!IMPORTANT]
> **Diferencia entre Contenedor y Nodo**
>
> Es importante entender la diferencia:
> - **Contenedor:** Es el entorno Docker donde vive el nodo
> - **Nodo:** Es el proceso blockchain que corre dentro del contenedor
>
> Para borrar la data del nodo, necesitas **detener el nodo** (no necesariamente el contenedor) y luego **eliminar los datos del nodo** antes de reinicializar.

## Usando Interfaz Gráfica (Recomendado)

La interfaz gráfica es la forma más segura y clara de borrar la data del nodo, ya que muestra advertencias claras antes de proceder.

### Paso 1: Detener el Nodo

Primero, asegúrate de que el nodo esté detenido:

1. Abre la interfaz gráfica:

   ```bash
   cd services/node0-infinite  # O cualquier otro servicio
   ./drive.sh up -d            # Asegúrate de que el contenedor esté ejecutándose
   ./drive.sh exec infinite node-ui
   ```

2. En el menú principal, selecciona **"Node Operations"**

   ![Menú Principal - Node Operations seleccionada](/images/node-ui-op2-operations.png)

3. Selecciona **"Stop Node"** si el nodo está ejecutándose

   ![Node Operations - Stop Node seleccionada](/images/node-ui-operations-op2-stop.png)

### Paso 2: Borrar la Data del Nodo

Una vez que el nodo esté detenido:

1. En el menú principal, selecciona **"Node Operations"**

   ![Menú Principal - Node Operations seleccionada](/images/node-ui-op2-operations.png)

2. Selecciona **"Advanced Operations"**

   ![Node Operations - Advanced Operations seleccionada](/images/node-ui-operations-op4-advanced-operations.png)

3. Selecciona **"Delete Node Data"** (o "Clean Node Data")

   ![Advanced Operations - Delete Node Data seleccionada](/images/node-ui-advanced-operations-op4-clean-data.png)

4. **Lee cuidadosamente la advertencia** que se muestra sobre la pérdida permanente de datos

5. Confirma la operación cuando se solicite

La interfaz gráfica eliminará automáticamente todos los datos del nodo de forma segura.

## Usando Línea de Comandos

Si prefieres usar la línea de comandos, puedes borrar la data del nodo manualmente.

### Paso 1: Detener el Nodo

Primero, asegúrate de que el nodo esté detenido:

```bash
cd services/node0-infinite  # O cualquier otro servicio
./drive.sh exec infinite node-stop
```

Verifica que el nodo esté detenido:

```bash
./drive.sh exec infinite node-process-status
```

### Paso 2: Eliminar la Data del Nodo

Tienes dos opciones para eliminar la data:

#### Opción A: Eliminar desde el Host (Recomendado)

Esta es la forma más directa y recomendada:

```bash
cd services/node0-infinite  # O cualquier otro servicio

# Eliminar todo el contenido del directorio persistent-data
rm -rf ./persistent-data/*

# O eliminar solo la data del nodo (manteniendo otros datos si los hay)
rm -rf ./persistent-data/data
rm -rf ./persistent-data/config
```

#### Opción B: Eliminar desde el Contenedor

Si prefieres hacerlo desde dentro del contenedor:

```bash
cd services/node0-infinite  # O cualquier otro servicio

# Acceder al shell del contenedor
./drive.sh exec infinite bash

# Dentro del contenedor, eliminar la data
rm -rf /home/ubuntu/.infinited/data
rm -rf /home/ubuntu/.infinited/config

# Salir del shell
exit
```

## Qué se Elimina

Cuando borras la data del nodo, se eliminan los siguientes componentes:

### Base de Datos de la Blockchain

- **`persistent-data/data/`** - Contiene:
  - Todos los bloques sincronizados
  - Historial de transacciones
  - Estado de la aplicación
  - Índices para búsquedas rápidas

### Archivos de Configuración

- **`persistent-data/config/`** - Contiene:
  - `config.toml` - Configuración general del nodo
  - `app.toml` - Configuración de la aplicación blockchain
  - `client.toml` - Configuración del cliente
  - `genesis.json` - Archivo génesis de la blockchain
  - `priv_validator_key.json` - Private Validator Key (crítico para validadores)

### Qué NO se Elimina (si existe)

- **`persistent-data/keys/`** - Keyring (si está en una ubicación separada)
- Otros directorios que puedas haber creado en `persistent-data/`

## Después de Borrar la Data

Después de borrar la data del nodo, necesitas reinicializar el nodo:

### Para Validadores

Si eres validador, **DEBES** usar [Inicialización con Recovery]({{< relref "initialization/recovery-initialization" >}}) con tu frase semilla para recuperar tu Private Validator Key:

1. Usa la misma frase semilla que usaste originalmente
2. El nodo generará exactamente la misma Private Validator Key
3. Puedes verificar que la clave es la misma comparándola con un respaldo

Para más información sobre cómo verificar que recuperaste la misma clave, consulta [Verificación Post-Inicialización]({{< relref "initialization/verification#verificación-especial-para-recovery-mode" >}}).

### Para Full Nodes

Si eres full node, puedes usar cualquiera de los dos métodos:

- **[Inicialización Simple]({{< relref "initialization/simple-initialization" >}})** - Genera una nueva clave aleatoria
- **[Inicialización con Recovery]({{< relref "initialization/recovery-initialization" >}})** - Si quieres mantener consistencia

Para más información sobre la inicialización, consulta [Inicialización de Nodo]({{< relref "initialization" >}}).

## Práctica de Verificación: Reinicializar el Nodo

Esta práctica te permite verificar que siempre puedes recuperar exactamente la misma Private Validator Key usando tu frase semilla. Es especialmente útil para validadores que quieren confirmar que su proceso de respaldo funciona correctamente.

> [!TIP]
> **Práctica Recomendada: Verificación de Recuperabilidad**
>
> Antes de crear tu validador en la blockchain, es altamente recomendable que verifiques que puedes recuperar correctamente tu Private Validator Key. Esto te dará confianza de que siempre podrás restaurar tu validador si es necesario.

### Procedimiento Completo

1. **Anota o guarda el contenido de tu Private Validator Key:**
   ```bash
   cat persistent-data/config/priv_validator_key.json > mi-validator-key-backup.json
   ```

2. **Detén el nodo:**
   - Usa la interfaz gráfica: **"Node Operations"** → **"Stop Node"**
   - O usa línea de comandos: `./drive.sh exec infinite node-stop`

3. **Borra la data del nodo:**
   - Usa la interfaz gráfica: **"Node Operations"** → **"Advanced Operations"** → **"Delete Node Data"**
   - O elimina manualmente: `rm -rf ./persistent-data/data ./persistent-data/config`

4. **Reinicializa el nodo con la misma frase semilla:**
   - Sigue el procedimiento completo de [Inicialización con Recovery]({{< relref "initialization/recovery-initialization" >}}) usando exactamente la misma frase semilla que usaste antes

5. **Verifica que se generó exactamente la misma clave:**
   ```bash
   diff persistent-data/config/priv_validator_key.json mi-validator-key-backup.json
   ```

**Resultado esperado:** Debe ser exactamente la misma clave. Si es diferente, algo salió mal en el proceso.

**Beneficios de esta práctica:**
- ✅ Te da confianza de que siempre podrás restaurar tu validador
- ✅ Te ayuda a familiarizarte con el proceso
- ✅ Te permite detectar problemas antes de crear el validador en la blockchain
- ✅ Crea expertise en la gestión de claves

> [!NOTE]
> **Repetir el Procedimiento**
>
> Puedes repetir este procedimiento de verificación 2-3 veces para asegurarte de que siempre obtienes el mismo resultado. Esto te ayudará a estar tranquilo de que si realizas el procedimiento adecuadamente, siempre podrás respaldar o restaurar tu nodo validador cuantas veces sea necesario.

## Solución de Problemas

### No Puedo Borrar la Data del Nodo

Si tienes problemas para borrar la data:

1. **Asegúrate de que el nodo esté detenido:**
   ```bash
   ./drive.sh exec infinite node-process-status
   ```
   Si el nodo está ejecutándose, deténlo primero.

2. **Verifica los permisos del directorio:**
   ```bash
   ls -la ./persistent-data/
   ```

3. **Si hay problemas de permisos, consulta:**
   - [Problemas de Permisos]({{< relref "../../troubleshooting/permission-issues" >}})
   - [Gestión de Contenedores]({{< relref "../general/container-management" >}})

### La Private Validator Key es Diferente Después de Reinicializar

Si usaste recovery mode y la clave es diferente después de reinicializar:

1. **Verifica que ingresaste exactamente la misma frase semilla:**
   - No debe haber espacios extra al inicio o final
   - Todas las palabras deben estar escritas correctamente
   - Debe ser exactamente la misma frase (12 o 24 palabras)

2. **Verifica que usaste el formato BIP39 estándar:**
   - La frase semilla debe ser válida según el estándar BIP39

3. **Considera reinicializar con la frase semilla correcta:**
   - Si hay alguna duda, vuelve a intentar con la frase semilla correcta

### Perdí mi Frase Semilla

Si perdiste tu frase semilla y borraste la data del nodo:

- **Para validadores:** Si no tienes la frase semilla respaldada, **no hay forma de recuperar tu Private Validator Key**. Perderás permanentemente el acceso a tu validador.
- **Para full nodes:** Puedes reinicializar con una nueva clave, pero perderás la identidad anterior del nodo.

**Prevención:**
- Siempre respalda tu frase semilla antes de borrar la data
- Consulta [Mejores Prácticas de Seguridad]({{< relref "keys/security" >}}) para recomendaciones de respaldo

## Próximos Pasos

Después de borrar la data del nodo:

1. **[Inicialización de Nodo]({{< relref "initialization" >}})** - Reinicializa el nodo usando el método apropiado
2. **[Verificación Post-Inicialización]({{< relref "initialization/verification" >}})** - Verifica que la inicialización fue exitosa
3. **[Iniciar/Detener Nodo]({{< relref "start-stop-node" >}})** - Inicia tu nodo después de reinicializar

## Ver También

- [Inicialización de Nodo]({{< relref "initialization" >}}) - Cómo inicializar un nodo después de borrar la data
- [Inicialización con Recovery]({{< relref "initialization/recovery-initialization" >}}) - Requerido para validadores
- [Verificación Post-Inicialización]({{< relref "initialization/verification" >}}) - Verificar que la inicialización fue exitosa
- [Iniciar/Detener Nodo]({{< relref "start-stop-node" >}}) - Cómo gestionar el ciclo de vida del nodo
- [Data del Nodo]({{< relref "../../../../concepts/node-data" >}}) - Entender qué es la data del nodo y su importancia
- [Mejores Prácticas de Seguridad]({{< relref "keys/security" >}}) - Cómo respaldar tu frase semilla de forma segura

