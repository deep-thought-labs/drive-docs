---
title: "Workflow para Validadores"
weight: 52223
---

Guía paso a paso para configurar claves criptográficas cuando actúas como validador en la blockchain.

> [!NOTE]
> **Antes de Empezar**
>
> Es altamente recomendable leer primero [Mejores Prácticas de Seguridad]({{< relref "security" >}}) para entender cómo proteger correctamente tus claves antes de seguir este workflow.

## Introducción

Este documento explica cómo gestionar claves criptográficas para validadores. Para información sobre cómo crear el validador en la blockchain (transacción `create-validator`) y otras operaciones relacionadas con la validación, consulta la documentación específica sobre operaciones de validación.

Para nodos validador, puedes usar cualquiera de los dos métodos para crear claves. Ambos son útiles, solo difieren en cómo gestionas tu frase semilla:

- **Dry-Run:** Genera la clave y tú resguardas la frase semilla directamente. No se guarda en el keyring.
- **Generate and Save Key:** Genera la clave y la guarda en el keyring. Puedes ver la frase semilla si se muestra.

Sigue este workflow paso a paso:

## Paso 1: Crear Clave

Primero, abre la interfaz gráfica:

```bash
cd services/node0-infinite  # O cualquier otro servicio
./drive.sh up -d            # Asegúrate de que el contenedor esté ejecutándose
./drive.sh exec infinite node-ui
```

Verás el menú principal de la interfaz gráfica. Puedes usar cualquiera de los dos métodos. Ambos requieren acceder a **"Key Management"** desde el menú principal:

### Opción A: Dry-Run (Generar sin guardar)

1. En el menú principal, selecciona **"Key Management"** y luego **"Generate Key (Dry-Run - Recommended)"**

   ![Key Management - Generate Key (Dry-Run) seleccionada](/images/node-ui-key-op1-generate-key-dryrun.png)

   Esta opción genera una clave y muestra tu frase semilla **sin guardarla** en el keyring.

2. Ingresa un nombre para tu clave (ej: `my-validator`)
3. El sistema generará y **mostrará tu frase semilla** (12 o 24 palabras)
4. **⚠️ CRÍTICO:** Escribe y respalda esta frase semilla inmediatamente

### Opción B: Generate and Save Key (Generar y guardar)

1. En el menú principal, selecciona **"Key Management"** y luego **"Generate and Save Key"**

   ![Key Management - Generate and Save Key seleccionada](/images/node-ui-key-op2-generate-key-save.png)

   Esta opción genera una clave y la guarda automáticamente en el keyring.

2. Ingresa un nombre para tu clave
3. Ingresa una contraseña para proteger el keyring (si es la primera vez)
4. El sistema generará la clave y la guardará automáticamente
5. **⚠️ IMPORTANTE:** Asegúrate de respaldar tu frase semilla si se muestra

**Acción crítica:** Escribe y respalda la frase semilla mostrada, independientemente del método que uses.

Para más detalles sobre estas operaciones, consulta [Operaciones de Gestión de Claves]({{< relref "operations" >}}).

> [!IMPORTANT]
> **Clave en el Keyring para Crear Validador**
>
> Si vas a crear un validador nuevo en la blockchain, **es importante que tu clave esté almacenada en el keyring** antes de ejecutar la transacción `create-validator`. Esta transacción requiere una clave del keyring para firmarla.
>
> - Si usaste **"Generate and Save Key"**, la clave ya está en el keyring y puedes continuar.
> - Si usaste **Dry-Run**, asegúrate de agregar la clave al keyring (ver [Paso 4](#paso-4-agregar-clave-al-keyring-si-usaste-dry-run)) antes de crear el validador.

## Paso 2: Respaldar Frase Semilla

**Opciones de respaldo:**
- **Papel:** Escribe la frase semilla en papel y guárdala en un lugar seguro
- **Metal:** Usa una solución de respaldo en metal (resistente al fuego/agua)
- **Almacenamiento encriptado:** Guarda en almacenamiento encriptado (nunca en texto plano)

**⚠️ NUNCA:**
- Guardes la frase semilla en texto plano en tu computadora
- Compartas la frase semilla con nadie
- La envíes por email o mensajería
- La almacenes en la nube sin encriptar

Para más recomendaciones de seguridad, consulta [Mejores Prácticas de Seguridad]({{< relref "security" >}}).

## Paso 3: Inicializar Nodo con Recovery

Usa la frase semilla que acabas de crear y respaldar para inicializar tu nodo:

1. En la interfaz gráfica, en el menú principal, selecciona **"Node Operations"**

   ![Menú Principal - Node Operations seleccionada](/images/node-ui-op2-operations.png)

2. Selecciona **"Advanced Operations"**

   ![Node Operations - Advanced Operations seleccionada](/images/node-ui-operations-op4-advanced-operations.png)

3. Selecciona **"Initialize with Recovery (Validator)"**

   ![Advanced Operations - Initialize with Recovery (Validator) seleccionada](/images/node-ui-advanced-operations-op2-init-revery.png)

   Esta opción inicializa el nodo usando una frase semilla, asegurando que siempre generes la misma Private Validator Key.

4. Cuando se solicite, ingresa tu frase semilla (12 o 24 palabras)

Para más detalles sobre la inicialización, consulta [Inicializar Nodo]({{< relref "../initialize-node" >}}).

## Paso 4: Agregar Clave al Keyring (Si Usaste Dry-Run)

> [!IMPORTANT]
> **Necesario para Crear el Validador (Solo para Nuevos Validadores)**
>
> Si usaste el método Dry-Run y **vas a crear un validador nuevo** en la blockchain, **debes agregar la clave al keyring** antes de ejecutar la transacción `create-validator`. Esta transacción requiere una clave del keyring para firmarla.
>
> Si usaste "Generate and Save Key", la clave ya está en el keyring y puedes continuar.
>
> **Si ya creaste tu validador previamente** y solo estás restaurando el nodo para que funcione en un servidor diferente, **no es necesario agregar la clave al keyring**. Con solo tener el archivo `priv_validator_key.json` correcto en la carpeta de configuración (`persistent-data/config/priv_validator_key.json`), el nodo validará automáticamente cuando esté activo y sincronizado. El nodo usará esta clave para firmar bloques sin necesidad de tener la clave en el keyring.

1. En la interfaz gráfica, en el menú principal, selecciona **"Key Management"** y luego **"Add Existing Key from Seed Phrase"**

   ![Key Management - Add Existing Key from Seed Phrase seleccionada](/images/node-ui-key-op3-add-key.png)

   Esta opción te permite agregar una clave existente al keyring usando su frase semilla.

2. Ingresa un nombre para la clave
3. Ingresa tu frase semilla (12 o 24 palabras) cuando se solicite
4. Ingresa la contraseña del keyring si es necesario

Para más detalles sobre esta operación, consulta [Agregar Clave Existente desde Frase Semilla]({{< relref "operations#agregar-clave-existente-desde-frase-semilla" >}}) en Operaciones de Gestión de Claves.

## Paso 5: Verificar la Private Validator Key

> [!TIP]
> **Práctica Recomendada: Verificación de Recuperabilidad**
>
> Antes de crear tu validador en la blockchain, es altamente recomendable que verifiques que puedes recuperar correctamente tu Private Validator Key. Esto te dará confianza de que siempre podrás restaurar tu validador si es necesario.

### Verificar la Ubicación y Contenido

> [!IMPORTANT]
> **El Archivo Siempre se Crea**
>
> Cuando inicializas un nodo, **siempre se crea el archivo `priv_validator_key.json`**, sin importar el método de inicialización que uses (simple o recovery). La diferencia está en el **contenido** del archivo:
>
> - **Inicialización simple:** El contenido es aleatorio y diferente cada vez que inicializas
> - **Inicialización con recovery:** El contenido es siempre el mismo si usas la misma frase semilla

Después de inicializar el nodo con recovery, **debes verificar** que la Private Validator Key se generó correctamente:

```bash
# Verifica que el archivo existe
ls -la persistent-data/config/priv_validator_key.json

# REVISA el contenido para verificar la clave generada
cat persistent-data/config/priv_validator_key.json
```

**Ubicación esperada:**
- **En el host:** `persistent-data/config/priv_validator_key.json` (relativa al directorio del servicio)
- **En el contenedor:** `/home/ubuntu/.infinited/config/priv_validator_key.json`

> [!NOTE]
> **Revisar el Contenido es Necesario**
>
> No es opcional revisar el contenido del archivo. Debes hacerlo para verificar que la clave se generó correctamente y para poder compararla después cuando realices la práctica de verificación.

### Práctica de Verificación: Reinicializar el Nodo

> [!IMPORTANT]
> **Diferencia entre Contenedor y Nodo**
>
> Es importante entender la diferencia:
> - **Contenedor:** Es el entorno Docker donde vive el nodo
> - **Nodo:** Es el proceso blockchain que corre dentro del contenedor
>
> Para esta práctica, necesitas **detener el nodo** (no el contenedor) y luego **eliminar los datos del nodo** antes de reinicializar.

Para asegurarte de que siempre puedes recuperar tu validador, realiza esta práctica de verificación usando la interfaz gráfica:

1. **Anota o guarda el contenido de tu Private Validator Key:**
   
   Desde tu terminal, guarda el contenido del archivo:
   ```bash
   cat persistent-data/config/priv_validator_key.json > mi-validator-key-backup.json
   ```

2. **Abre la interfaz gráfica:**
   ```bash
   ./drive.sh exec infinite node-ui
   ```

3. **Detén el nodo:**
   - En el menú principal, selecciona **"Node Operations"** y luego **"Stop Node"**
   
   ![Menú Principal - Node Operations seleccionada](/images/node-ui-op2-operations.png)
   
   ![Node Operations - Stop Node seleccionada](/images/node-ui-operations-op2-stop.png)
   
   Esta opción detiene el proceso del nodo blockchain sin eliminar los datos.

4. **Elimina los datos del nodo:**
   
   > [!WARNING]
   > Esta operación elimina los datos del nodo (incluyendo `priv_validator_key.json`). Asegúrate de tener tu frase semilla respaldada antes de continuar.
   
   - En el menú principal, selecciona **"Node Operations"**, luego **"Advanced Operations"** y finalmente **"Clean Node Data"**
   
   ![Menú Principal - Node Operations seleccionada](/images/node-ui-op2-operations.png)
   
   ![Node Operations - Advanced Operations seleccionada](/images/node-ui-operations-op4-advanced-operations.png)
   
   ![Advanced Operations - Clean Node Data seleccionada](/images/node-ui-advanced-operations-op4-clean-data.png)
   
   Esta opción elimina todos los datos del nodo, incluyendo el archivo `priv_validator_key.json`, permitiéndote reinicializar desde cero.

5. **Reinicializa el nodo con la misma frase semilla:**
   - En el menú principal, selecciona **"Node Operations"**, luego **"Advanced Operations"** y finalmente **"Initialize with Recovery (Validator)"**
   
   ![Menú Principal - Node Operations seleccionada](/images/node-ui-op2-operations.png)
   
   ![Node Operations - Advanced Operations seleccionada](/images/node-ui-operations-op4-advanced-operations.png)
   
   ![Advanced Operations - Initialize with Recovery (Validator) seleccionada](/images/node-ui-advanced-operations-op2-init-revery.png)
   
   - Cuando se solicite, ingresa la misma frase semilla que usaste antes

6. **Verifica que se generó exactamente la misma clave:**
   
   Desde tu terminal, compara el archivo nuevo con tu respaldo:
   ```bash
   diff persistent-data/config/priv_validator_key.json mi-validator-key-backup.json
   ```
   
   > [!NOTE]
   > **El Archivo se Crea Nuevamente**
   >
   > Cuando reinicializas el nodo, el archivo `priv_validator_key.json` se crea nuevamente. Con recovery mode y la misma frase semilla, el **contenido debe ser exactamente el mismo** que antes.

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

## Migración de Validadores Existentes

Si tu validador **ya existe** en la blockchain y estás migrándolo a otro servidor o restaurándolo después de un fallo:

> [!IMPORTANT]
> **No Necesitas Crear el Validador de Nuevo**
>
> La transacción `create-validator` es una acción **única en el ciclo de vida del validador**. Si tu validador ya está registrado en la blockchain, NO necesitas ejecutar esta transacción nuevamente.

**Lo que necesitas hacer:**

1. **Asegúrate de tener un nodo blockchain sincronizado y activo**
2. **Asegúrate de que el nodo tenga el archivo `priv_validator_key.json` correcto** en su carpeta de configuración
   - Ubicación: `persistent-data/config/priv_validator_key.json`
   - Este archivo debe ser exactamente el mismo que tenía tu validador original

**Cómo funciona:**
- Cualquier nodo sincronizado en la cadena que tenga en su carpeta de configuración el archivo `priv_validator_key.json` de tu validador **será efectivamente el validador**
- El nodo usará esta clave para firmar bloques automáticamente
- No necesitas ejecutar ninguna transacción adicional

> [!WARNING]
> **⚠️ ADVERTENCIA CRÍTICA: Doble Firma**
>
> **NUNCA tengas dos nodos blockchain activos con la misma Private Validator Key al mismo tiempo.**
>
> Esto genera una **doble firma** (double signing), que es una mala práctica grave entre los nodos validadores y es castigada severamente en la blockchain:
>
> - ⚠️ **Amonestaciones** en la cadena de bloques
> - ⚠️ **Riesgo de perder parte de tus tokens apostados** debido a la sanción correspondiente
> - ⚠️ **Posible pérdida del validador** en casos extremos
>
> **Siempre asegúrate de:**
> - Detener completamente el nodo anterior antes de iniciar uno nuevo con la misma clave
> - No compartir el archivo `priv_validator_key.json` con otras personas
> - No tener copias del archivo en múltiples servidores activos simultáneamente
> - Verificar que solo un nodo está activo con tu Private Validator Key en cualquier momento

## Resumen del Workflow

### Para Nuevos Validadores

1. ✅ **Crear Clave** - Genera tu clave usando Dry-Run o Generate and Save Key
2. ✅ **Respaldar Frase Semilla** - Guarda tu frase semilla de forma segura
3. ✅ **Inicializar Nodo con Recovery** - Usa tu frase semilla para inicializar el nodo
4. ✅ **Agregar Clave al Keyring** - Asegúrate de que tu clave esté en el keyring (necesaria para `create-validator`)
5. ✅ **Verificar Private Validator Key** - Verifica que la clave se generó correctamente y realiza pruebas de recuperabilidad
6. ✅ **Crear el Validador** - Ejecuta la transacción `create-validator` en la blockchain (consulta la documentación sobre operaciones de validación)

### Para Migración de Validadores Existentes

1. ✅ **Asegurar nodo sincronizado** - Tu nodo debe estar sincronizado con la blockchain
2. ✅ **Tener el `priv_validator_key.json` correcto** - El archivo debe estar en `persistent-data/config/priv_validator_key.json`
3. ✅ **Verificar que solo un nodo está activo** - Asegúrate de que no hay otro nodo activo con la misma clave (evitar doble firma)

## Ver También

- [Operaciones de Gestión de Claves]({{< relref "operations" >}}) - Guía completa de todas las operaciones disponibles
- [Mejores Prácticas de Seguridad]({{< relref "security" >}}) - Recomendaciones de seguridad
- [Inicializar Nodo]({{< relref "../initialize-node" >}}) - Cómo inicializar un nodo usando tus claves
- [Problemas de Gestión de Claves]({{< relref "../../../troubleshooting/key-management-issues" >}}) - Solución de problemas comunes
- [Entender las Claves]({{< relref "understanding-keys" >}}) - Conceptos fundamentales sobre claves y validadores

