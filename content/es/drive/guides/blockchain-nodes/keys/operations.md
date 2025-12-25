---
title: "Operaciones de Gestión de Claves"
weight: 52221
---

Guía completa de todas las operaciones disponibles para gestionar claves criptográficas en el keyring de tus nodos blockchain.

## Interfaz Gráfica vs Línea de Comandos

Las acciones disponibles a través de la interfaz gráfica son **exactamente las mismas** que si las llamaras desde la línea de comandos. La interfaz gráfica solo proporciona un entorno visual para navegar entre opciones y seleccionar la acción deseada, pero **no agrega funcionalidades diferentes**.

Esto significa que:
- Generar una clave desde la interfaz gráfica produce el mismo resultado que hacerlo desde la línea de comandos
- Restablecer la contraseña del keyring desde la interfaz gráfica tiene las mismas consecuencias que hacerlo desde la línea de comandos
- Todas las operaciones son equivalentes, independientemente del método que uses

## Submenú de Gestión de Claves

Para acceder a la gestión de claves, abre la interfaz gráfica y navega al submenú "Key Management":

```bash
cd services/node0-infinite  # O cualquier otro servicio
./drive.sh up -d            # Asegúrate de que el contenedor esté ejecutándose
./drive.sh exec infinite node-ui
```

En el menú principal, selecciona **"Key Management"** (Gestión de Claves). Verás el siguiente submenú:

![Submenú Key Management](/images/node-ui-keys.png)

> [!NOTE]
> **Sintaxis de Comandos y Nombres de Contenedores**
>
> Para entender cómo estructurar los comandos con `drive.sh` y conocer los nombres correctos de contenedores para cada servicio, consulta la sección [Comandos que Requieren Nombre de Contenedor]({{< relref "../../general/container-management#comandos-que-requieren-nombre-de-contenedor" >}}) en Gestión de Contenedores.

## Operaciones de Gestión de Claves

A continuación se describen todas las operaciones disponibles para gestionar claves, mostrando tanto el método de línea de comandos como el método de interfaz gráfica para cada una.

### 🔑 Generar Clave (Dry-Run)

Genera una clave criptográfica y muestra tu frase semilla **sin guardarla** en el keyring. Esto te permite respaldar la frase semilla antes de usarla para inicializar tu nodo.

**Qué logra:**
- Genera una clave criptográfica nueva
- **Muestra tu frase semilla (12 o 24 palabras)**
- **NO guarda** la clave en el keyring (por eso se llama "dry-run")
- Te permite respaldar la frase semilla antes de comprometerte

**Diferencia clave:** A diferencia de "Generate and Save Key", este método **no guarda** la clave en el [keyring]({{< relref "../../../../../concepts/keyring" >}}). Tú resguardas la frase semilla de manera directa y la usas para inicializar el nodo en [modo recovery]({{< relref "../initialize-node#inicialización-con-recovery" >}}).

#### Usando Línea de Comandos

```bash
cd services/node0-infinite  # O cualquier otro servicio
./drive.sh exec infinite node-keys create my-validator --dry-run
```

**Salida esperada:**
- Muestra la frase semilla generada
- Muestra la dirección de la clave
- Instrucciones para respaldar la frase semilla

**⚠️ CRÍTICO:** Escribe y respalda esta frase semilla inmediatamente. Esta es la única forma de recuperar tu clave.

#### Usando Interfaz Gráfica

1. En el submenú "Key Management", selecciona **"Generate Key (Dry-Run - Recommended)"**

   ![Generate Key (Dry-Run) - Opción seleccionada](/images/node-ui-key-op1-generate-key-dryrun.png)

   Esta opción genera una clave y muestra tu frase semilla **sin guardarla** en el keyring.

2. Ingresa un nombre para tu clave (ej: `my-validator`)
3. El sistema generará y **mostrará tu frase semilla** (12 o 24 palabras)
4. **⚠️ CRÍTICO:** Escribe y respalda esta frase semilla inmediatamente
5. La clave **NO se guarda** en el keyring
6. Usa esta frase semilla para inicializar tu nodo en [modo recovery]({{< relref "../initialize-node#inicialización-con-recovery" >}})

**Cuándo usar:** Cuando quieras crear una nueva clave y tener control completo sobre tu frase semilla antes de usarla.

### 💾 Generar y Guardar Clave Directamente

Genera una clave nueva y la guarda automáticamente en el keyring en un solo paso.

**Qué logra:**
- Genera una clave nueva
- Guarda la clave en el keyring automáticamente
- Puede mostrar la frase semilla (dependiendo de la configuración)

**Diferencia clave:** A diferencia de "Dry-Run", este método **guarda** la clave en el [keyring]({{< relref "../../../../../concepts/keyring" >}}), permitiéndote usarla directamente en operaciones del nodo sin tener que agregarla manualmente después.

**Nota:** Si usas este método, asegúrate de respaldar tu frase semilla si se muestra.

#### Usando Línea de Comandos

```bash
cd services/node0-infinite
./drive.sh exec -it infinite node-keys create my-validator
```

**Qué hace:**
- Te solicita una contraseña para el keyring (si es la primera vez)
- Genera y guarda la clave en el keyring automáticamente
- Puede mostrar la frase semilla (dependiendo de la configuración)

**Nota:** Usa `-it` (interactive) para poder ingresar la contraseña del keyring si es necesario.

#### Usando Interfaz Gráfica

1. En el submenú "Key Management", selecciona **"Generate and Save Key"**

   ![Generate and Save Key - Opción seleccionada](/images/node-ui-key-op2-generate-key-save.png)

   Esta opción genera una clave y la guarda automáticamente en el keyring.

2. Ingresa un nombre para tu clave
3. Ingresa una contraseña para proteger el keyring (si es la primera vez)
4. El sistema generará la clave y la guardará automáticamente
5. **⚠️ IMPORTANTE:** Asegúrate de respaldar tu frase semilla si se muestra

**Cuándo usar:** Cuando quieras generar y guardar una clave en un solo paso, listo para usar en operaciones del nodo.

### ➕ Agregar Clave Existente desde Frase Semilla

Si ya tienes una frase semilla (de un nodo anterior, de otro sistema, o de una clave que creaste con dry-run), puedes agregarla al keyring para uso futuro.

**Qué logra:**
- Restaura una clave existente usando su frase semilla
- Agrega la clave al keyring para uso futuro
- Permite usar la clave en operaciones del nodo sin tener que ingresar la frase semilla cada vez

#### Usando Línea de Comandos

```bash
cd services/node0-infinite
./drive.sh exec -it infinite node-keys add my-validator
```

**Qué hace:**
- Te solicita ingresar tu frase semilla (12 o 24 palabras)
- Te solicita la contraseña del keyring si es necesario
- Agrega la clave al keyring

**Cuándo usar:** Cuando quieras restaurar una clave existente o agregar una clave de otro nodo.

#### Usando Interfaz Gráfica

1. En el submenú "Key Management", selecciona **"Add Existing Key from Seed Phrase"**

   ![Add Existing Key from Seed Phrase - Opción seleccionada](/images/node-ui-key-op3-add-key.png)

   Esta opción te permite agregar una clave existente al keyring usando su frase semilla.

2. Ingresa un nombre para la clave
3. Ingresa tu frase semilla (12 o 24 palabras) cuando se solicite
4. Ingresa la contraseña del keyring si es necesario
5. La clave se agregará a tu keyring

### 📋 Listar Todas las Claves

Muestra todas las claves que tienes almacenadas en tu keyring.

**Qué logra:**
- Muestra una lista de todos los nombres de claves en el keyring
- Te permite ver qué claves tienes disponibles
- Útil para verificar que una clave fue agregada correctamente

#### Usando Línea de Comandos

```bash
cd services/node0-infinite
./drive.sh exec infinite node-keys list
```

**Salida esperada:** Lista de nombres de todas las claves almacenadas en el keyring.

#### Usando Interfaz Gráfica

1. En el submenú "Key Management", selecciona **"List All Keys"**

   ![List All Keys - Opción seleccionada](/images/node-ui-key-op4-list.png)

   Esta opción muestra todas las claves almacenadas en tu keyring.

2. Verás una lista de todos los nombres de claves almacenadas

### 🔍 Mostrar Detalles de una Clave

Muestra información detallada sobre una clave específica almacenada en tu keyring.

**Qué logra:**
- Muestra información completa sobre una clave específica
- Incluye detalles como la dirección, tipo de clave, etc.
- Útil para verificar información de una clave antes de usarla

#### Usando Línea de Comandos

```bash
cd services/node0-infinite
./drive.sh exec infinite node-keys show my-validator
```

**Salida esperada:**
- Nombre de la clave
- Tipo de clave
- Dirección asociada
- Otra información relevante

#### Usando Interfaz Gráfica

1. En el submenú "Key Management", selecciona **"Show Key Details"**

   ![Show Key Details - Opción seleccionada](/images/node-ui-key-op5-show-key-details.png)

   Esta opción muestra información detallada sobre una clave específica.

2. Ingresa el nombre de la clave
3. Verás información como la dirección, tipo de clave, etc.

### 🗑️ Eliminar una Clave

Elimina permanentemente una clave del keyring.

**Qué logra:**
- Elimina una clave del keyring
- **⚠️ ADVERTENCIA:** Esta acción no se puede deshacer
- La clave se elimina del keyring pero si tienes la frase semilla respaldada, puedes agregarla nuevamente

**Cuándo usar:** Solo cuando estés seguro de que ya no necesitas la clave. Considera respaldar la frase semilla antes de eliminar.

#### Usando Línea de Comandos

```bash
cd services/node0-infinite
./drive.sh exec infinite node-keys delete my-validator --yes
```

**⚠️ ADVERTENCIA:** Esta acción elimina permanentemente la clave del keyring. No se puede deshacer.

#### Usando Interfaz Gráfica

1. En el submenú "Key Management", selecciona **"Delete Key"**

   ![Delete Key - Opción seleccionada](/images/node-ui-key-op6-delete-key.png)

   Esta opción elimina permanentemente una clave del keyring.

2. Ingresa el nombre de la clave a eliminar
3. Confirma la eliminación
4. **⚠️ ADVERTENCIA:** Esta acción no se puede deshacer

### 🔒 Restablecer Contraseña del Keyring

> [!WARNING]
> **⚠️ ADVERTENCIA CRÍTICA: Restablecer Contraseña del Keyring**
>
> **Restablecer la contraseña del keyring crea un nuevo keyring con una nueva contraseña, causando que ya NO tengas acceso a las claves que previamente habías guardado.**
>
> Esta acción:
> - Crea un nuevo keyring encriptado con la nueva contraseña
> - **Elimina el acceso a todas las claves guardadas en el keyring anterior**
> - Las claves anteriores no se pueden recuperar sin la contraseña original
>
> **Solo usa esta opción si:**
> - Estás seguro de que ya no necesitas las claves guardadas anteriormente
> - Tienes las frases semilla respaldadas para restaurar las claves después
> - Estás empezando desde cero y no tienes claves importantes guardadas
>
> Esta advertencia se muestra durante el proceso tanto en la interfaz gráfica como cuando se ejecuta desde la línea de comandos.

Permite cambiar la contraseña que protege tu keyring. **Importante:** Esta operación crea un nuevo keyring, perdiendo acceso a las claves guardadas anteriormente.

**Qué logra:**
- Crea un nuevo keyring con una nueva contraseña
- **⚠️ ADVERTENCIA:** Perderás acceso a todas las claves guardadas en el keyring anterior
- Útil solo si estás empezando desde cero o tienes todas tus frases semilla respaldadas

#### Usando Interfaz Gráfica

1. En el submenú "Key Management", selecciona **"Reset Keyring Password"**

   ![Reset Keyring Password - Opción seleccionada](/images/node-ui-key-op7-reset-keyring-password.png)

   Esta opción restablece la contraseña del keyring, creando un nuevo keyring y perdiendo acceso a las claves anteriores.

2. **Lee la advertencia** que se muestra sobre la pérdida de acceso a las claves anteriores
3. Confirma que entiendes las consecuencias
4. Sigue las instrucciones para establecer una nueva contraseña

#### Usando Línea de Comandos

Esta operación está disponible principalmente a través de la interfaz gráfica. Si necesitas restablecer la contraseña desde la línea de comandos, el proceso es equivalente a crear un nuevo keyring, lo cual eliminará todas las claves guardadas. Asegúrate de tener tus frases semilla respaldadas antes de proceder.

## Usar Claves en Comandos

Cuando uses comandos que requieren claves (como transacciones u operaciones on-chain), el sistema buscará las claves en el [keyring]({{< relref "../../../../../concepts/keyring" >}}) almacenado en la carpeta de datos persistentes.

Para más información sobre la ubicación del keyring y cómo funciona, consulta [Keyring]({{< relref "../../../../../concepts/keyring" >}}).

**Ejemplo:**
```bash
# Asegúrate de estar en el directorio del servicio
cd services/node0-infinite

# Verifica que el keyring existe y contiene tu clave
./drive.sh exec infinite node-keys list

# Ahora puedes usar comandos que requieren claves
# El sistema buscará automáticamente en persistent-data
```

**Si recibes un error de "clave no encontrada":**
1. Verifica que estás en el directorio correcto del servicio
2. Verifica que el keyring existe en `persistent-data`
3. Lista las claves disponibles con `node-keys list`
4. Si la clave no está, agrégala usando `node-keys add` o la interfaz gráfica

Para más información sobre solución de problemas, consulta [Problemas de Gestión de Claves]({{< relref "../../../troubleshooting/key-management-issues" >}}).

## Ver También

- [Workflow para Validadores]({{< relref "validator-workflow" >}}) - Guía paso a paso para configurar claves como validador
- [Mejores Prácticas de Seguridad]({{< relref "security" >}}) - Recomendaciones de seguridad
- [Problemas de Gestión de Claves]({{< relref "../../../troubleshooting/key-management-issues" >}}) - Solución de problemas comunes
- [Keyring]({{< relref "../../../../../concepts/keyring" >}}) - Qué es un keyring y cómo funciona
- [Interfaz Gráfica]({{< relref "../graphical-interface" >}}) - Guía completa de la interfaz gráfica

