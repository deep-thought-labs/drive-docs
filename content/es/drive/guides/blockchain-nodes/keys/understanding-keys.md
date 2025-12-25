---
title: "Entender las Claves"
weight: 52220
---

Esta guía explica las diferencias entre validadores y full nodes en cuanto a la gestión de claves, especialmente sobre cuándo y por qué necesitas preocuparte por la recuperabilidad de la Private Validator Key durante la inicialización.

> [!NOTE]
> **Conceptos Fundamentales**
>
> Antes de continuar, asegúrate de entender los conceptos básicos:
>
> - [Key]({{< relref "../../../../../concepts/key" >}}) - Qué es una clave criptográfica y para qué se usa en blockchains
> - [Keyring]({{< relref "../../../../../concepts/keyring" >}}) - Qué es un keyring y cómo funciona
> - [Private Validator Key]({{< relref "../../../../../concepts/private-validator-key" >}}) - Qué es el Private Validator Key y su importancia
> - [Keyring vs Private Validator Key]({{< relref "../../../../../concepts/keyring-vs-validator-key" >}}) - Diferencias detalladas entre ambos componentes
> - [Inicializar Nodo]({{< relref "../initialize-node" >}}) - Guía completa sobre modos de inicialización y recuperabilidad

## Diferencias entre Validadores y Full Nodes en la Gestión de Claves

### Uso de Claves en General

**Importante:** Tanto validadores como full nodes pueden usar [claves de cuenta]({{< relref "../../../../../concepts/key" >}}) (account keys) almacenadas en el [keyring]({{< relref "../../../../../concepts/keyring" >}}) para realizar operaciones como:
- Firmar transacciones on-chain
- Delegar tokens
- Participar en gobernanza
- Cualquier operación que requiera autenticación criptográfica

La diferencia crítica **NO** está en el uso de claves en general, sino en la **recuperabilidad de la Private Validator Key durante la inicialización del nodo**.

### Full Nodes

Los full nodes (nodos completos) **NO necesitan preocuparse por la recuperabilidad de la Private Validator Key** porque:

- **No participan en el consenso** - Solo verifican y almacenan bloques
- **No firman bloques** - No necesitan una identidad permanente en la blockchain
- **Private Validator Key no crítica** - El nodo genera automáticamente una Private Validator Key para su funcionamiento interno, pero esta no es crítica porque no está registrada en la blockchain
- **Sin riesgo de pérdida permanente** - Si pierden la Private Validator Key, simplemente pueden reinicializar el nodo con una nueva

**Para full nodes:**
- Puedes usar [inicialización simple]({{< relref "../initialize-node#inicialización-simple" >}}) sin preocuparte por la recuperabilidad de la Private Validator Key
- El nodo generará automáticamente una Private Validator Key para su funcionamiento interno
- No necesitas respaldar la Private Validator Key porque no representa una identidad crítica en la blockchain
- **SÍ puedes usar claves de cuenta** en el keyring para operaciones si lo necesitas (transacciones, delegaciones, etc.)

### Validadores

Los validadores **DEBEN preocuparse por la recuperabilidad de la Private Validator Key** porque:

- **Participan en el consenso** - Proponen y validan bloques
- **Identidad permanente** - Una vez registrado en la blockchain, el validador está permanentemente ligado a su [Private Validator Key]({{< relref "../../../../../concepts/private-validator-key" >}})
- **Firma bloques** - Necesitan su Private Validator Key para firmar cada bloque que proponen
- **Riesgo de pérdida permanente** - Si pierden su Private Validator Key y no pueden recuperarla (porque no usaron recovery mode), pierden su validador para siempre

**Para validadores:**
- **DEBES** inicializar con [recovery mode]({{< relref "../initialize-node#inicialización-con-recovery" >}}) usando una frase semilla para asegurar la recuperabilidad de la Private Validator Key
- **DEBES** respaldar tu frase semilla de forma segura
- Es recomendable usar la misma frase semilla para inicializar el nodo (generar la Private Validator Key) y para el [keyring]({{< relref "../../../../../concepts/keyring" >}}) (claves de cuenta para operaciones)
- Si pierdes tu `priv_validator_key` y no usaste recovery mode, perderás tu validador permanentemente

## Relación entre Keyring y Private Validator Key

Para entender en detalle cómo se relacionan estos componentes y por qué es recomendable usar la misma frase semilla para ambos, consulta [Keyring vs Private Validator Key]({{< relref "../../../../../concepts/keyring-vs-validator-key" >}}).

**Resumen:** Aunque técnicamente es posible usar diferentes claves, **es altamente recomendable usar la misma frase semilla para ambos** para simplicidad, consistencia y recuperación unificada.

## Resumen: Validadores vs Full Nodes

| Aspecto | Full Node | Validador |
|---------|-----------|-----------|
| **Uso de claves de cuenta (keyring)** | ✅ Opcional - para operaciones si se necesita | ✅ Recomendado - para operaciones on-chain |
| **Recuperabilidad de Private Validator Key** | ❌ No necesaria - puede usar inicialización simple | ✅ **CRÍTICA** - DEBE usar recovery mode |
| **Inicialización del nodo** | [Simple]({{< relref "../initialize-node#inicialización-simple" >}}) está bien | **DEBE ser con [recovery]({{< relref "../initialize-node#inicialización-con-recovery" >}})** |
| **Riesgo de perder Private Validator Key** | Bajo impacto - puede reinicializar | **Pérdida permanente del validador** |
| **Respaldar frase semilla** | No necesario para Private Validator Key | **OBLIGATORIO** para Private Validator Key |

## Próximos Pasos

Ahora que entiendes los conceptos fundamentales:

- **[Operaciones de Gestión]({{< relref "operations" >}})** - Aprende a realizar operaciones de gestión de claves
- **[Mejores Prácticas de Seguridad]({{< relref "security" >}})** - Protege tus claves siguiendo estas recomendaciones
- **[Workflow para Validadores]({{< relref "validator-workflow" >}})** - Si eres validador, sigue este workflow paso a paso
- **[Inicializar Nodo]({{< relref "../initialize-node" >}})** - Guía práctica para inicializar un nodo
- **[Interfaz Gráfica]({{< relref "../graphical-interface" >}})** - Usa la interfaz gráfica para gestionar tu nodo

