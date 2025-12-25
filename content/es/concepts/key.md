---
title: "Key"
weight: 1
---

Una **key** (clave) es un componente criptográfico fundamental en las blockchains que permite identificar, autenticar y autorizar operaciones en la red.

## ¿Qué es una Clave?

Una clave criptográfica es un par de claves relacionadas matemáticamente:

- **Clave Privada** - Se mantiene secreta y nunca se comparte. Se usa para firmar transacciones y bloques.
- **Clave Pública** - Se deriva de la clave privada y puede compartirse públicamente. Se usa para verificar firmas y generar direcciones.

## Propósito en Blockchains

Las claves criptográficas en blockchains se utilizan para:

- **Identificar entidades** - Cada clave genera una dirección única en la blockchain
- **Firmar transacciones** - La clave privada firma transacciones para demostrar propiedad
- **Firmar bloques** - Los validadores usan claves para firmar bloques que proponen
- **Autenticación** - Verificar que una operación fue autorizada por el propietario de la clave
- **Gestionar fondos** - Las direcciones derivadas de claves pueden recibir y almacenar tokens

## Frase Semilla (Seed Phrase)

Las claves se generan típicamente a partir de una **frase semilla** (seed phrase o mnemonic phrase):

- **12 o 24 palabras** - Una secuencia de palabras que representa la clave privada
- **Estándar BIP39** - Formato estándar utilizado en la mayoría de blockchains
- **Recuperación** - La misma frase semilla siempre genera la misma clave
- **Respaldo crítico** - Si pierdes tu frase semilla, pierdes acceso permanente a tus claves

**⚠️ IMPORTANTE:** La frase semilla es la única forma de recuperar tus claves. Si la pierdes, no hay forma de recuperar el acceso.

## Uso de Claves en Nodos Blockchain

En el contexto de nodos blockchain, las claves se utilizan de diferentes maneras:

### Tipos de Claves Específicas

Existen dos tipos principales de claves en nodos blockchain:

1. **Claves de Cuenta (Account Keys)** - Claves estándar que se almacenan en el [keyring]({{< relref "keyring" >}}) y se usan para:
   - Firmar transacciones on-chain
   - Crear validadores (`create-validator`)
   - Delegar tokens
   - Realizar operaciones de gobernanza
   - Cualquier operación que requiera autenticación criptográfica desde el usuario
   
   Estas son las claves "normales" que gestionas manualmente y que puedes agregar al keyring según tus necesidades.

2. **[Private Validator Key]({{< relref "private-validator-key" >}})** - Tipo específico de clave que identifica y autoriza a un validador para firmar bloques. Se genera automáticamente durante la inicialización del nodo y se usa internamente por el nodo para participar en el consenso.

### Sistemas de Almacenamiento

- **[Keyring]({{< relref "keyring" >}})** - Sistema de almacenamiento seguro donde se guardan las **claves de cuenta** (account keys) para firmar transacciones on-chain

**Importante:** 
- El keyring es un **almacén** donde guardas claves de cuenta (account keys)
- Las claves de cuenta son el tipo "normal" de clave que usas para operaciones on-chain
- El Private Validator Key es un **tipo específico de clave** con un propósito particular (firmar bloques como validador)
- Ambos tipos de claves son diferentes y se usan para propósitos distintos

Para entender mejor cómo se relacionan estos componentes, consulta [Keyring vs Private Validator Key]({{< relref "keyring-vs-validator-key" >}}).

## Seguridad de las Claves

Las claves criptográficas son fundamentales para la seguridad:

- **Nunca compartas tu clave privada** - Quien tenga acceso a tu clave privada tiene control total
- **Respaldar la frase semilla** - Guarda tu frase semilla en un lugar seguro y fuera de línea
- **Usar almacenamiento seguro** - Considera usar hardware wallets o keyrings encriptados
- **Múltiples copias** - Crea varias copias de tu frase semilla en ubicaciones separadas

## Ver También

- [Keyring]({{< relref "keyring" >}}) - Almacén seguro de múltiples claves
- [Private Validator Key]({{< relref "private-validator-key" >}}) - Clave específica para validadores
- [Keyring vs Private Validator Key]({{< relref "keyring-vs-validator-key" >}}) - Diferencias entre tipos de claves
- [Inicializar Nodo]({{< relref "../drive/guides/blockchain-nodes/initialize-node" >}}) - Cómo se generan las claves durante la inicialización
- [Gestión de Claves]({{< relref "../drive/guides/blockchain-nodes/keys" >}}) - Guía práctica para gestionar claves

