---
title: "Keyring"
weight: 2
---

Un **keyring** (anillo de claves) es un almacén seguro y encriptado donde se guardan tus claves criptográficas. Drive genera y gestiona automáticamente el keyring para cada nodo.

## ¿Qué es un Keyring?

Piensa en el keyring como una **billetera (wallet)** donde puedes tener múltiples cuentas o claves:

- **Agregar claves al keyring** es como agregar cuentas a tu billetera
- Puedes tener **múltiples claves** en el mismo keyring para diferentes propósitos
- Las claves en el keyring se usan para **firmar transacciones** y realizar operaciones on-chain
- Por ejemplo, la transacción para crear un validador (`create-validator`) requiere una clave del keyring

## Ubicación del Keyring

El keyring se guarda en la carpeta de datos persistentes del nodo:

- **Ruta en el host:** `./persistent-data` (relativa al directorio del servicio)
- **Ruta en el contenedor:** `/home/ubuntu/.infinited`

Cuando uses comandos que requieren claves (como transacciones u operaciones on-chain), el sistema buscará las claves en esta ubicación. Si el comando no puede encontrar la clave, verifica que estés trabajando desde el directorio correcto del servicio y que el keyring exista en `persistent-data`.

## Protección del Keyring

El keyring está protegido por una contraseña que estableces la primera vez que guardas una clave. Esta contraseña es necesaria para acceder a las claves almacenadas.

## Uso en Operaciones

Las claves almacenadas en el keyring se utilizan para:

- Firmar transacciones on-chain
- Crear validadores (`create-validator`)
- Delegar tokens
- Realizar operaciones de gobernanza
- Cualquier operación que requiera autenticación criptográfica

## Ver También

- [Keyring vs Private Validator Key]({{< relref "keyring-vs-validator-key" >}}) - Diferencias detalladas entre keyring y Private Validator Key
- [Private Validator Key]({{< relref "private-validator-key" >}}) - Qué es el Private Validator Key
- [Inicializar Nodo]({{< relref "../drive/guides/blockchain-nodes/initialize-node" >}}) - Guía completa sobre modos de inicialización
- [Gestión de Claves]({{< relref "../drive/guides/blockchain-nodes/keys" >}}) - Guía práctica para gestionar claves en el keyring
