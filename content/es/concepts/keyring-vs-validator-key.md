---
title: "Keyring vs Private Validator Key"
weight: 3
---

Este documento explica las diferencias fundamentales entre el **Keyring** y el **Private Validator Key**, dos componentes criptográficos distintos pero relacionados en los nodos blockchain.

## Resumen de Diferencias

| Aspecto | Private Validator Key | Keyring |
|---------|----------------------|---------|
| **Propósito** | Identificar y firmar bloques como validador | Firmar transacciones y operaciones on-chain |
| **Cuándo se usa** | Automáticamente por el nodo al validar bloques | Manualmente al ejecutar transacciones |
| **Ubicación** | `persistent-data/config/priv_validator_key.json` | `persistent-data/` (keyring encriptado) |
| **Recuperación** | Depende del modo de inicialización | Siempre recuperable con frase semilla |
| **Gestión** | Se genera automáticamente durante la inicialización | Se gestiona manualmente agregando claves |
| **Múltiples claves** | Solo una clave por nodo | Múltiples claves pueden coexistir |
| **Uso en validadores** | Crítica - sin ella no puedes validar bloques | Recomendada - para operaciones on-chain |
| **Uso en full nodes** | No crítica - se genera automáticamente | No necesaria |

## Private Validator Key

El **Private Validator Key** (`priv_validator_key.json`) es la identidad criptográfica de tu validador en la blockchain.

### Características

- **Una sola clave por nodo** - Cada nodo tiene exactamente una Private Validator Key
- **Se genera automáticamente** - Durante la inicialización del nodo
- **Firma bloques** - Usada automáticamente por el nodo para firmar bloques que propone o valida
- **Identidad permanente** - Una vez registrado en la blockchain, está permanentemente ligada a tu validador
- **Recuperabilidad depende del modo** - Solo recuperable si usaste [inicialización con recovery]({{< relref "../drive/guides/blockchain-nodes/initialization/recovery-initialization" >}})

### Cuándo se Usa

- Automáticamente cuando el nodo propone un nuevo bloque
- Automáticamente cuando el nodo valida bloques de otros validadores
- No requiere intervención manual - el nodo la usa internamente

Para más información, consulta [Private Validator Key]({{< relref "private-validator-key" >}}).

## Keyring

El **keyring** es un almacén seguro donde puedes guardar múltiples claves criptográficas para diferentes propósitos.

### Características

- **Múltiples claves** - Puedes tener varias claves en el mismo keyring
- **Gestión manual** - Tú decides qué claves agregar y cuándo
- **Firma transacciones** - Las claves se usan para firmar transacciones on-chain
- **Siempre recuperable** - Siempre puedes restaurar claves usando su frase semilla
- **Protegido por contraseña** - El keyring está encriptado y protegido por una contraseña

### Cuándo se Usa

- Manualmente cuando ejecutas transacciones on-chain
- Para crear un validador (`create-validator`)
- Para delegar tokens
- Para operaciones de gobernanza
- Para cualquier operación que requiera autenticación criptográfica

Para más información, consulta [Keyring]({{< relref "keyring" >}}).

## Relación entre Ambos

Aunque son componentes separados, **es altamente recomendable usar la misma frase semilla para ambos**:

### Ventajas de Usar la Misma Semilla

- ✅ **Simplicidad:** Solo necesitas gestionar una frase semilla
- ✅ **Consistencia:** Tu validador y tus operaciones están vinculadas a la misma identidad
- ✅ **Menos errores:** Evitas confusiones sobre qué clave usar para qué operación
- ✅ **Recuperación unificada:** Si necesitas restaurar todo, solo necesitas una frase semilla

### Ejemplo Práctico

Cuando creas un validador, necesitas:

1. **Inicializar el nodo con [recovery mode]({{< relref "../drive/guides/blockchain-nodes/initialization/recovery-initialization" >}})** usando tu frase semilla → Genera tu `priv_validator_key`
2. **Agregar la misma frase semilla al keyring** → Para poder firmar la transacción `create-validator`

Si usas la misma semilla para ambos, todo funciona de manera coherente y sencilla.

## Independencia de los Componentes

Es importante entender que son **procesos separados**:

- El Private Validator Key se genera durante la inicialización del nodo
- El keyring se gestiona independientemente, agregando claves cuando las necesitas
- Pueden usar la misma frase semilla o diferentes
- Técnicamente es posible usar diferentes claves, pero no es recomendable

## Para Validadores

Si estás configurando un validador:

- **Private Validator Key:** DEBES inicializar con [recovery mode]({{< relref "../drive/guides/blockchain-nodes/initialization/recovery-initialization" >}}) para que sea recuperable
- **Keyring:** Recomendado agregar la misma frase semilla para operaciones on-chain
- **Misma semilla:** Usa la misma frase semilla para ambos para simplicidad y consistencia

## Para Full Nodes

Si estás ejecutando un full node (no validador):

- **Private Validator Key:** Se genera automáticamente, no es crítica
- **Keyring:** No es necesario a menos que quieras realizar transacciones
- **Sin preocupaciones:** No necesitas gestionar claves manualmente

## Ver También

- [Keyring]({{< relref "keyring" >}}) - Qué es un keyring y cómo funciona
- [Private Validator Key]({{< relref "private-validator-key" >}}) - Qué es el Private Validator Key y su importancia
- [Inicialización de Nodo]({{< relref "../drive/guides/blockchain-nodes/initialization" >}}) - Guía completa sobre modos de inicialización y recuperabilidad
- [Entender las Claves]({{< relref "../drive/guides/blockchain-nodes/keys/understanding-keys" >}}) - Guía aplicada sobre cómo se relacionan estos conceptos

