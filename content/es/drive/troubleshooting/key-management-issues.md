---
title: "Problemas de Gestión de Claves"
weight: 544
---

Soluciones a problemas comunes relacionados con la gestión de claves criptográficas en el keyring.

## No puedo ver mi frase semilla

Si usaste el método "Generate and Save Key" y no viste la frase semilla:

- La frase semilla puede no mostrarse por defecto en algunos casos
- Considera usar el método "dry-run" para asegurarte de ver y respaldar la frase semilla

**Solución:**
1. Usa el método [Generar Clave (Dry-Run)]({{< relref "../guides/blockchain-nodes/keys/operations#generar-clave-dry-run" >}}) para generar una nueva clave y ver la frase semilla
2. Si ya generaste la clave, puedes intentar agregarla nuevamente usando el método dry-run con un nombre diferente para ver la frase semilla

Para más información sobre cómo generar claves, consulta [Operaciones de Gestión de Claves]({{< relref "../guides/blockchain-nodes/keys/operations" >}}).

## Olvidé mi contraseña del keyring

Si olvidaste la contraseña del keyring:

- Puedes usar la opción "Reset Keyring Password" en la interfaz gráfica o línea de comandos
- **⚠️ ADVERTENCIA:** Esto creará un nuevo keyring y perderás acceso a todas las claves guardadas
- **Importante:** Si tienes claves guardadas, necesitarás tus frases semilla para restaurarlas después de restablecer la contraseña

**Solución:**
1. Si tienes las frases semilla respaldadas:
   - Restablece la contraseña del keyring usando [Restablecer Contraseña del Keyring]({{< relref "../guides/blockchain-nodes/keys/operations#restablecer-contraseña-del-keyring" >}})
   - Restaura todas tus claves usando [Agregar Clave Existente desde Frase Semilla]({{< relref "../guides/blockchain-nodes/keys/operations#agregar-clave-existente-desde-frase-semilla" >}})
2. Si no tienes las frases semilla respaldadas:
   - **No hay forma de recuperar las claves** sin la contraseña original
   - Si eres validador y no tienes la frase semilla, perderás permanentemente el acceso a tu validador

**Prevención:**
- Guarda tu contraseña del keyring en un lugar seguro (separado de la frase semilla)
- Considera usar un gestor de contraseñas seguro
- Consulta [Mejores Prácticas de Seguridad]({{< relref "../guides/blockchain-nodes/keys/security" >}}) para más recomendaciones

## Necesito recuperar una clave eliminada

Si eliminaste una clave por error:

- Si tienes la frase semilla respaldada, puedes agregarla nuevamente usando `node-keys add` o la interfaz gráfica
- Si no tienes la frase semilla respaldada, **no hay forma de recuperar la clave**

**Solución:**
1. Si tienes la frase semilla respaldada:
   - Usa [Agregar Clave Existente desde Frase Semilla]({{< relref "../guides/blockchain-nodes/keys/operations#agregar-clave-existente-desde-frase-semilla" >}}) para restaurar la clave
2. Si no tienes la frase semilla respaldada:
   - **No hay forma de recuperar la clave** sin la frase semilla
   - Si eres validador y no tienes la frase semilla, perderás permanentemente el acceso a tu validador

**Prevención:**
- Siempre respalda tu frase semilla antes de eliminar una clave
- Considera hacer un respaldo adicional antes de eliminar claves importantes
- Consulta [Mejores Prácticas de Seguridad]({{< relref "../guides/blockchain-nodes/keys/security" >}}) para más recomendaciones

## Error: Clave no encontrada

Si recibes un error de "clave no encontrada" al usar comandos que requieren claves:

### Verificación paso a paso

1. **Verifica que estás en el directorio correcto:**
   ```bash
   pwd  # Debe mostrar la ruta del servicio, ej: .../services/node0-infinite
   ```

2. **Verifica que el keyring existe:**
   ```bash
   ls -la persistent-data/  # Debe mostrar el contenido del directorio
   ```

3. **Lista las claves disponibles:**
   ```bash
   # Sintaxis simplificada (recomendada)
   ./drive.sh node-keys list
   
   # Sintaxis completa (alternativa)
   ./drive.sh exec infinite node-keys list
   ```

4. **Si la clave no está en la lista:**
   - Agrega la clave usando [Agregar Clave Existente desde Frase Semilla]({{< relref "../guides/blockchain-nodes/keys/operations#agregar-clave-existente-desde-frase-semilla" >}}) o la interfaz gráfica
   - Asegúrate de usar el nombre correcto de la clave
   - Si necesitas crear múltiples claves desde la misma frase semilla, ver [Múltiples Keys de una Misma Frase Semilla]({{< relref "../guides/blockchain-nodes/keys/multiple-keys-from-seed" >}})

### Causas Comunes

- **Directorio incorrecto:** Estás ejecutando el comando desde un directorio diferente al del servicio
- **Keyring no existe:** El keyring aún no ha sido creado (se crea la primera vez que guardas una clave)
- **Nombre incorrecto:** Estás usando un nombre de clave diferente al que guardaste
- **Clave eliminada:** La clave fue eliminada del keyring

### Solución

1. Navega al directorio correcto del servicio:
   ```bash
   cd services/node0-infinite  # O el nombre de tu servicio
   ```

2. Verifica que el keyring existe y lista las claves:
   ```bash
   # Sintaxis simplificada (recomendada)
   ./drive.sh node-keys list
   
   # Sintaxis completa (alternativa)
   ./drive.sh exec infinite node-keys list
   ```

3. Si la clave no está en la lista, agrégala:
   ```bash
   # Sintaxis simplificada (recomendada)
   ./drive.sh node-keys add my-validator
   
   # Sintaxis completa (alternativa)
   ./drive.sh exec infinite node-keys add my-validator
   ```
   
   > [!TIP]
   > **No necesitas especificar `-it`**
   >
   > El script `drive.sh` detecta automáticamente que `node-keys add` requiere modo interactivo y agrega `-it` por ti.

4. Si no tienes la frase semilla, no podrás agregar la clave. En este caso, necesitarás generar una nueva clave.

Para más información sobre cómo usar claves en comandos, consulta [Usar Claves en Comandos]({{< relref "../guides/blockchain-nodes/keys/operations#usar-claves-en-comandos" >}}) en Operaciones de Gestión de Claves.

## Ver También

- [Operaciones de Gestión de Claves]({{< relref "../guides/blockchain-nodes/keys/operations" >}}) - Guía completa de todas las operaciones disponibles
- [Múltiples Keys de una Misma Frase Semilla]({{< relref "../guides/blockchain-nodes/keys/multiple-keys-from-seed" >}}) - Crear múltiples claves desde una frase semilla
- [Workflow para Validadores]({{< relref "../guides/blockchain-nodes/keys/validator-workflow" >}}) - Guía paso a paso para configurar claves como validador
- [Mejores Prácticas de Seguridad]({{< relref "../guides/blockchain-nodes/keys/security" >}}) - Recomendaciones de seguridad
- [Keyring]({{< relref "../../../../concepts/keyring" >}}) - Qué es un keyring y cómo funciona
- [Key]({{< relref "../../../../concepts/key" >}}) - Qué es una clave criptográfica

