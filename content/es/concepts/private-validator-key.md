---
title: "Private Validator Key"
weight: 5
---

El **Private Validator Key** (`priv_validator_key.json`) es una clave criptográfica única que identifica y autoriza a tu validador en la blockchain. Es fundamental entender su importancia y cómo se relaciona con otros componentes del sistema.

## ¿Qué es el Private Validator Key?

Cuando inicializas un nodo blockchain, el sistema genera automáticamente un archivo llamado `priv_validator_key.json` (Private Validator Key). Este archivo contiene una clave criptográfica única que:

- **Identifica tu validador** en la blockchain
- **Firma los bloques** que tu validador propone y valida
- **Está permanentemente ligada** a tu validador una vez que lo registras en la blockchain

## Analogía: El "DNI" de tu Validador

**Piensa en el Private Validator Key como el "DNI" de tu validador**: una vez que registras tu validador en la blockchain usando esta clave, esa identidad queda permanentemente asociada a ella. Si quieres mover tu validador a otro servidor o restaurarlo después de un fallo, necesitarás exactamente la misma `priv_validator_key`.

## Importancia para Validadores

El Private Validator Key es **crítica** para validadores porque:

- **Sin ella, no puedes firmar bloques** - Tu validador no podrá participar en el consenso
- **Está permanentemente ligada a tu validador** - Una vez registrado en la blockchain, no se puede cambiar
- **Es necesaria para restaurar tu validador** - Si pierdes el servidor, necesitas esta clave para restaurar tu validador

**⚠️ CRÍTICO:** Si pierdes tu `priv_validator_key` y no la puedes recuperar (porque no usaste recovery mode), perderás permanentemente el control de tu validador.

## Generación del Private Validator Key

El Private Validator Key se genera durante la inicialización del nodo. El modo de inicialización determina si la clave será recuperable:

- **Inicialización Simple:** Genera una clave aleatoria y única que **no se puede recuperar**
- **Inicialización con Recovery:** Genera siempre la misma clave usando una frase semilla, **recuperable en cualquier momento**

Para más detalles, consulta [Inicialización de Nodo]({{< relref "../drive/guides/blockchain-nodes/initialization" >}}).

## Ubicación

El Private Validator Key se almacena en:

- **Ruta en el host:** `./persistent-data/config/priv_validator_key.json` (relativa al directorio del servicio)
- **Ruta en el contenedor:** `/home/ubuntu/.infinited/config/priv_validator_key.json`

## Ver También

- [Keyring vs Private Validator Key]({{< relref "keyring-vs-validator-key" >}}) - Diferencias detalladas entre keyring y Private Validator Key
- [Keyring]({{< relref "keyring" >}}) - Qué es un keyring y cómo funciona
- [Inicialización de Nodo]({{< relref "../drive/guides/blockchain-nodes/initialization" >}}) - Guía completa sobre modos de inicialización y recuperabilidad
- [Entender las Claves]({{< relref "../drive/guides/blockchain-nodes/keys/understanding-keys" >}}) - Guía aplicada sobre cómo se relacionan estos conceptos
