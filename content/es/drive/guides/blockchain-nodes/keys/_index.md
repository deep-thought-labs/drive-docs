---
title: "Gestión de Claves"
weight: 5222
---

Guía completa para gestionar claves criptográficas en el keyring de tus nodos blockchain de Drive.

## ¿Qué es la Gestión de Claves?

La gestión de claves es el proceso de crear, almacenar, proteger y usar claves criptográficas que identifican tu nodo en la blockchain y te permiten firmar transacciones y bloques. Esta sección te guía a través de todo lo que necesitas saber para gestionar claves de forma segura y efectiva.

## Orden Recomendado de Lectura

Para obtener el mejor provecho de esta documentación, te recomendamos seguir este orden:

### 1. 📚 Entender los Conceptos Fundamentales

**Empieza aquí si eres nuevo en la gestión de claves:**

- **[Entender las Claves]({{< relref "understanding-keys" >}})** - Explica las diferencias entre validadores y full nodes en cuanto a la gestión de claves, especialmente sobre la recuperabilidad de la Private Validator Key durante la inicialización.

> [!NOTE]
> **Conceptos Previos Recomendados**
>
> Si aún no entiendes los conceptos básicos sobre claves, te recomendamos leer primero los conceptos atómicos:
>
> - [Key]({{< relref "../../../../../concepts/key" >}}) - Qué es una clave criptográfica y para qué se usa en blockchains
> - [Keyring]({{< relref "../../../../../concepts/keyring" >}}) - Qué es un keyring y cómo funciona
> - [Private Validator Key]({{< relref "../../../../../concepts/private-validator-key" >}}) - Qué es el Private Validator Key y su importancia
> - [Keyring vs Private Validator Key]({{< relref "../../../../../concepts/keyring-vs-validator-key" >}}) - Diferencias detalladas entre ambos componentes
> - [Inicializar Nodo]({{< relref "../initialize-node" >}}) - Guía completa sobre modos de inicialización y recuperabilidad

### 2. 🔧 Aprender las Operaciones

**Una vez que entiendes los conceptos, aprende a realizar las operaciones:**

- **[Operaciones de Gestión]({{< relref "operations" >}})** - Guía completa de todas las operaciones disponibles:
  - 🔑 Generar claves (Dry-Run y guardar directamente)
  - ➕ Agregar claves existentes desde frase semilla
  - 📋 Listar y mostrar detalles de claves
  - 🗑️ Eliminar claves
  - 🔒 Restablecer contraseña del keyring

### 3. 🔐 Mejores Prácticas de Seguridad

**Antes de crear o usar claves, aprende a protegerlas correctamente:**

- **[Mejores Prácticas de Seguridad]({{< relref "security" >}})** - Recomendaciones esenciales:
  - Respaldo seguro de frase semilla
  - Protección del keyring
  - Seguridad general del servidor

### 4. 🚀 Workflow para Validadores

**Si actúas como validador, sigue este workflow paso a paso:**

- **[Workflow para Validadores]({{< relref "validator-workflow" >}})** - Guía paso a paso que te lleva desde la creación de claves hasta la inicialización del nodo:
  - Crear y respaldar tu frase semilla
  - Inicializar el nodo con recovery
  - Agregar claves al keyring para operaciones

## ¿Eres Validador o Full Node?

Para entender las diferencias entre validadores y full nodes en cuanto a la gestión de claves, especialmente sobre cuándo y por qué necesitas preocuparte por la recuperabilidad de la Private Validator Key, consulta [Entender las Claves]({{< relref "understanding-keys" >}}).

**Resumen rápido:**
- **Validadores:** DEBEN usar recovery mode durante la inicialización para asegurar la recuperabilidad de su Private Validator Key
- **Full Nodes:** Pueden usar inicialización simple; no necesitan preocuparse por la recuperabilidad de la Private Validator Key, pero SÍ pueden usar claves de cuenta para operaciones

**Rutas recomendadas:**
- **Si eres Validador:** Lee [Entender las Claves]({{< relref "understanding-keys" >}}), aprende las [Mejores Prácticas de Seguridad]({{< relref "security" >}}), y luego sigue el [Workflow para Validadores]({{< relref "validator-workflow" >}})
- **Si eres Full Node:** Puedes usar [Operaciones de Gestión]({{< relref "operations" >}}) si necesitas claves de cuenta para operaciones, o continuar con [Inicializar Nodo]({{< relref "../initialize-node" >}}) si solo quieres ejecutar el nodo

## Solución de Problemas

Si encuentras problemas al gestionar claves, consulta:

- **[Problemas de Gestión de Claves]({{< relref "../../../troubleshooting/key-management-issues" >}})** - Soluciones a problemas comunes como:
  - No puedo ver mi frase semilla
  - Olvidé mi contraseña del keyring
  - Error: Clave no encontrada
  - Necesito recuperar una clave eliminada

## Documentación Relacionada

### Conceptos Fundamentales

- [Key]({{< relref "../../../../../concepts/key" >}}) - Qué es una clave criptográfica y para qué se usa en blockchains
- [Keyring]({{< relref "../../../../../concepts/keyring" >}}) - Qué es un keyring y cómo funciona
- [Private Validator Key]({{< relref "../../../../../concepts/private-validator-key" >}}) - Qué es el Private Validator Key
- [Keyring vs Private Validator Key]({{< relref "../../../../../concepts/keyring-vs-validator-key" >}}) - Diferencias detalladas entre ambos componentes
- [Inicializar Nodo]({{< relref "../initialize-node" >}}) - Guía completa sobre modos de inicialización y recuperabilidad

### Guías Relacionadas

- [Interfaz Gráfica]({{< relref "../graphical-interface" >}}) - Usa la interfaz gráfica para gestionar claves
- [Inicializar Nodo]({{< relref "../initialize-node" >}}) - Cómo inicializar un nodo usando tus claves
- [Iniciar/Detener Nodo]({{< relref "../start-stop-node" >}}) - Cómo iniciar y detener tu nodo después de configurar las claves
