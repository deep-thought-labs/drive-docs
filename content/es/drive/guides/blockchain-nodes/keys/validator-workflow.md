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

Este documento proporciona un **workflow sugerido paso a paso** para configurar claves criptográficas cuando actúas como validador en la blockchain. 

> [!NOTE]
> **Información Completa en Otras Secciones**
>
> Este workflow es una guía de pasos sugeridos. La información completa sobre cada operación está documentada en sus respectivas secciones:
>
> - **Crear claves:** [Operaciones de Gestión de Claves]({{< relref "operations" >}})
> - **Inicializar nodo:** [Inicialización de Nodo]({{< relref "../initialization" >}})
> - **Verificar inicialización:** [Verificación Post-Inicialización]({{< relref "../initialization/verification" >}})
> - **Respaldar frase semilla:** [Mejores Prácticas de Seguridad]({{< relref "security" >}})

Para información sobre cómo crear el validador en la blockchain (transacción `create-validator`) y otras operaciones relacionadas con la validación, consulta la documentación específica sobre operaciones de validación.

## Workflow Paso a Paso

Sigue estos pasos en orden para configurar tu validador:

## Paso 1: Crear Clave

Crea una clave criptográfica usando uno de los métodos disponibles. Puedes usar cualquiera de los dos métodos:

- **Dry-Run:** Genera la clave y tú resguardas la frase semilla directamente. No se guarda en el keyring.
- **Generate and Save Key:** Genera la clave y la guarda automáticamente en el keyring.

> [!NOTE]
> **Información Completa**
>
> Para instrucciones detalladas paso a paso sobre cómo crear claves, incluyendo imágenes de la interfaz gráfica y comandos de línea de comandos, consulta [Operaciones de Gestión de Claves]({{< relref "operations" >}}):
> - [Generar Clave (Dry-Run)]({{< relref "operations#generar-clave-dry-run" >}})
> - [Generar y Guardar Clave Directamente]({{< relref "operations#generar-y-guardar-clave-directamente" >}})

> [!IMPORTANT]
> **Clave en el Keyring para Crear Validador**
>
> Si vas a crear un validador nuevo en la blockchain, **es importante que tu clave esté almacenada en el keyring** antes de ejecutar la transacción `create-validator`. Esta transacción requiere una clave del keyring para firmarla.
>
> - Si usaste **"Generate and Save Key"**, la clave ya está en el keyring y puedes continuar.
> - Si usaste **Dry-Run**, asegúrate de agregar la clave al keyring (ver [Paso 4](#paso-4-agregar-clave-al-keyring-si-usaste-dry-run)) antes de crear el validador.

## Paso 2: Respaldar Frase Semilla

**⚠️ CRÍTICO:** Escribe y respalda la frase semilla mostrada inmediatamente, independientemente del método que uses para crear la clave.

> [!NOTE]
> **Información Completa**
>
> Para opciones de respaldo, recomendaciones de seguridad y mejores prácticas, consulta [Mejores Prácticas de Seguridad]({{< relref "security" >}}), que incluye:
> - Opciones de respaldo (papel, metal, almacenamiento encriptado)
> - Qué NUNCA hacer con tu frase semilla
> - Protección del keyring
> - Seguridad general del servidor

## Paso 3: Inicializar Nodo con Recovery

Usa la frase semilla que acabas de crear y respaldar para inicializar tu nodo usando el modo recovery.

> [!IMPORTANT]
> **Requerido para Validadores**
>
> Para validadores, **DEBES usar inicialización con recovery** para asegurar que siempre puedas recuperar tu Private Validator Key. La inicialización simple no es adecuada para validadores.

> [!NOTE]
> **Información Completa**
>
> Para el procedimiento completo de inicialización con recovery, consulta [Inicialización con Recovery]({{< relref "../initialization/recovery-initialization" >}}), que incluye:
> - Qué es la inicialización con recovery y sus características
> - Requisitos previos
> - Instrucciones paso a paso usando la interfaz gráfica (con imágenes)
> - Instrucciones usando línea de comandos
> - Qué hace el proceso de inicialización
> - Ventajas para validadores
> - Solución de problemas
>
> Para entender las diferencias entre modos de inicialización y cuándo usar cada uno, consulta [Inicialización de Nodo]({{< relref "../initialization" >}}).

## Paso 4: Agregar Clave al Keyring (Si Usaste Dry-Run)

> [!IMPORTANT]
> **Necesario para Crear el Validador (Solo para Nuevos Validadores)**
>
> Si usaste el método Dry-Run y **vas a crear un validador nuevo** en la blockchain, **debes agregar la clave al keyring** antes de ejecutar la transacción `create-validator`. Esta transacción requiere una clave del keyring para firmarla.
>
> - Si usaste **"Generate and Save Key"**, la clave ya está en el keyring y puedes continuar al siguiente paso.
> - Si usaste **Dry-Run**, debes agregar la clave al keyring ahora.
>
> **Si ya creaste tu validador previamente** y solo estás restaurando el nodo para que funcione en un servidor diferente, **no es necesario agregar la clave al keyring**. Con solo tener el archivo `priv_validator_key.json` correcto en la carpeta de configuración (`persistent-data/config/priv_validator_key.json`), el nodo validará automáticamente cuando esté activo y sincronizado.

> [!NOTE]
> **Información Completa**
>
> Para instrucciones detalladas paso a paso sobre cómo agregar una clave existente al keyring, incluyendo imágenes de la interfaz gráfica y comandos de línea de comandos, consulta [Agregar Clave Existente desde Frase Semilla]({{< relref "operations#agregar-clave-existente-desde-frase-semilla" >}}) en Operaciones de Gestión de Claves.
>
> **Múltiples Keys de una Misma Frase Semilla:**
>
> Puedes crear múltiples keys desde la misma frase semilla usando diferentes índices de cuenta. Esto es útil si quieres keys separadas para diferentes propósitos (principal, respaldo, prueba). Ver [Múltiples Keys de una Misma Frase Semilla]({{< relref "multiple-keys-from-seed" >}}) para ejemplos detallados.

## Paso 5: Verificar la Private Validator Key

> [!TIP]
> **Práctica Recomendada: Verificación de Recuperabilidad**
>
> Antes de crear tu validador en la blockchain, es altamente recomendable que verifiques que puedes recuperar correctamente tu Private Validator Key. Esto te dará confianza de que siempre podrás restaurar tu validador si es necesario.

### Verificación Básica

Primero, verifica que la inicialización se completó correctamente.

> [!NOTE]
> **Información Completa**
>
> Para la verificación básica post-inicialización, consulta [Verificación Post-Inicialización]({{< relref "../initialization/verification" >}}), que incluye:
> - Verificación de archivos de configuración
> - Verificación de Private Validator Key
> - Verificación de archivo génesis
> - Verificación de Chain ID
> - Checklist de verificación
> - Problemas comunes

### Práctica de Verificación: Reinicializar el Nodo

> [!NOTE]
> **Información Completa**
>
> Para la práctica completa de verificación de recuperabilidad (reinicializar el nodo y verificar que se genera la misma clave), consulta la sección [Verificación Especial para Recovery Mode]({{< relref "../initialization/verification#verificación-especial-para-recovery-mode" >}}) en Verificación Post-Inicialización, que incluye:
> - Procedimiento paso a paso completo
> - Cómo detener el nodo y eliminar los datos
> - Cómo reinicializar con la misma frase semilla
> - Cómo verificar que se generó exactamente la misma clave
> - Beneficios de esta práctica

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
- [Inicialización de Nodo]({{< relref "../initialization" >}}) - Cómo inicializar un nodo usando tus claves
- [Problemas de Gestión de Claves]({{< relref "../../../troubleshooting/key-management-issues" >}}) - Solución de problemas comunes
- [Entender las Claves]({{< relref "understanding-keys" >}}) - Conceptos fundamentales sobre claves y validadores

