---
title: "Ruta de Derivación"
weight: 6
---

Una **ruta de derivación** (también llamada **ruta HD** o **ruta BIP44**) es una secuencia de números que especifica qué clave específica generar desde una frase semilla durante la [derivación de claves]({{< relref "key-derivation" >}}).

## ¿Qué es una Ruta de Derivación?

Piensa en una ruta de derivación como una "dirección" única que le dice al sistema qué clave específica crear desde tu frase semilla. Es como coordenadas en un mapa - la misma frase semilla con diferentes rutas producirá diferentes claves.

La ruta de derivación sigue el **estándar BIP44**, que asegura compatibilidad entre diferentes wallets y sistemas.

## Estructura de una Ruta de Derivación

Una ruta de derivación BIP44 tiene la siguiente estructura:

```
m / 44' / coin_type' / account' / change / address_index
```

**Componentes:**

- **`m`** - Indicador de clave maestra
- **`44'`** - Propósito BIP44 (hardened)
- **`coin_type'`** - Identificador de blockchain (hardened)
  - `60'` para cadenas compatibles con Ethereum (Drive usa esto)
  - `118'` para Cosmos Hub
- **`account'`** - [Índice de Cuenta]({{< relref "account-index" >}}) (hardened)
- **`change`** - Cadena de cambio (usualmente `0` para direcciones externas/receptoras)
- **`address_index`** - Índice de dirección (usualmente `0` para la primera dirección)

## Hardened vs No Hardened

**Derivación hardened** (indicada por `'` después del número):
- Proporciona un aislamiento de seguridad más fuerte
- Usado para: propósito, tipo de moneda, e índice de cuenta
- Ejemplo: `44'`, `60'`, `0'`

**Derivación no hardened** (sin `'`):
- Permite derivación normal
- Usado para: change e índice de dirección
- Ejemplo: `0`, `0`

## Ruta por Defecto en Drive

Drive usa la siguiente ruta de derivación por defecto:

```
m/44'/60'/account'/0/0
```

Donde:
- `44'` - Propósito BIP44
- `60'` - Tipo de moneda compatible con Ethereum
- `account'` - El [índice de cuenta]({{< relref "account-index" >}}) que especificas (por defecto: `0`)
- `0` - Cadena de cambio (direcciones externas)
- `0` - Índice de dirección (primera dirección)

## Ejemplos

**Ejemplo 1: Ruta por defecto (cuenta 0)**
```
m/44'/60'/0'/0/0
```
Esta es la ruta usada cuando no especificas un índice de cuenta.

**Ejemplo 2: Índice de cuenta 1**
```
m/44'/60'/1'/0/0
```
Esta ruta genera una clave diferente usando el índice de cuenta 1.

**Ejemplo 3: Índice de cuenta 2**
```
m/44'/60'/2'/0/0
```
Esta ruta genera otra clave diferente usando el índice de cuenta 2.

## Rutas de Derivación Personalizadas

Para usuarios avanzados, puedes especificar una ruta de derivación completa personalizada:

```bash
./drive.sh exec infinite node-keys add <nombre-key> --hd-path "m/44'/60'/0'/0/0"
```

> [!WARNING]
> **⚠️ EXPERIMENTAL: Rutas Personalizadas**
>
> Las rutas de derivación personalizadas son experimentales y necesitan ser probadas y validadas. Úsalas bajo tu propio riesgo y siempre verifica los resultados.

**Cuándo usar rutas personalizadas:**
- Necesitas compatibilidad con un wallet específico
- Quieres coincidir con una ruta de derivación específica de otro sistema
- Estás migrando desde otra blockchain o wallet

## Por Qué Importan las Rutas de Derivación

Las rutas de derivación son importantes porque:

- **Permiten múltiples claves** - Misma frase semilla, diferentes rutas = diferentes claves
- **Aseguran compatibilidad** - Formato estándar funciona entre wallets
- **Proporcionan organización** - Estructura jerárquica para gestionar claves
- **Permiten recuperación** - Misma ruta + misma semilla = misma clave (determinista)

## Ver También

- [Derivación de Claves]({{< relref "key-derivation" >}}) - Cómo la derivación de claves usa rutas de derivación
- [Índice de Cuenta]({{< relref "account-index" >}}) - Entender el componente de cuenta de la ruta
- [Key]({{< relref "key" >}}) - Qué es una clave criptográfica
- [Múltiples Keys de una Misma Frase Semilla]({{< relref "../drive/guides/blockchain-nodes/keys/multiple-keys-from-seed" >}}) - Guía práctica con ejemplos
