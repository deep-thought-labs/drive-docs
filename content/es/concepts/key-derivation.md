---
title: "Derivación de Claves"
weight: 4
---

La **derivación de claves** (también llamada **derivación de claves HD** o **derivación determinista jerárquica**) es el proceso de generar múltiples claves criptográficas desde una sola frase semilla usando algoritmos matemáticos y rutas de derivación.

## ¿Qué es la Derivación de Claves?

La derivación de claves es un proceso criptográfico que te permite:

- Generar múltiples claves únicas desde una frase semilla
- Crear claves de forma determinista (la misma frase semilla + misma ruta = misma clave)
- Organizar claves jerárquicamente para diferentes propósitos
- Mantener compatibilidad con sistemas de wallets estándar

En lugar de generar cada clave de forma independiente, la derivación de claves usa tu frase semilla como "fuente maestra" y aplica diferentes [rutas de derivación]({{< relref "derivation-path" >}}) para crear claves únicas.

## Cómo Funciona

Cuando derivas una clave desde una frase semilla, el sistema sigue este proceso:

1. **Toma tu frase semilla** - La fuente maestra (12 o 24 palabras)
2. **Usa una ruta de derivación** - Una secuencia que especifica qué clave crear (ej: `m/44'/60'/0'/0/0`)
3. **Aplica un algoritmo matemático** - Genera una clave privada única basada en la frase semilla y la ruta
4. **Crea una dirección única** - Deriva una dirección de blockchain desde la clave generada

La misma frase semilla con diferentes rutas de derivación producirá diferentes claves, pero el proceso es **determinista** - las mismas entradas siempre producen las mismas salidas.

## El Estándar BIP44

La derivación de claves en Drive sigue el **estándar BIP44**, que es un formato ampliamente utilizado que asegura:

- **Compatibilidad** - Funciona con wallets y herramientas estándar
- **Consistencia** - Generación de claves predecible entre sistemas
- **Organización** - Estructura jerárquica para gestionar múltiples claves

El estándar BIP44 define cómo se estructuran las rutas de derivación y asegura que diferentes wallets puedan generar las mismas claves desde la misma frase semilla.

## Componentes de la Derivación de Claves

La derivación de claves involucra varios componentes:

- **[Frase Semilla]({{< relref "key" >}}#frase-semilla-seed-phrase)** - La fuente maestra (12 o 24 palabras)
- **[Ruta de Derivación]({{< relref "derivation-path" >}})** - La "dirección" que especifica qué clave generar
- **[Índice de Cuenta]({{< relref "account-index" >}})** - Un componente de la ruta de derivación que determina qué cuenta/clave crear
- **Algoritmo Matemático** - La función criptográfica que genera la clave

## Por Qué Esto Importa

La derivación de claves es fundamental porque:

- **Simplifica el respaldo** - Una frase semilla puede recuperar todas tus claves
- **Permite organización** - Crear claves separadas para diferentes propósitos (principal, respaldo, prueba)
- **Asegura compatibilidad** - Funciona con wallets y herramientas estándar
- **Proporciona seguridad** - Cada clave derivada es criptográficamente independiente
- **Permite recuperación** - Todas las claves pueden regenerarse desde la frase semilla

## Ejemplo

```
Misma frase semilla + cuenta 0 → Key A (dirección: infinite1abc...)
Misma frase semilla + cuenta 1 → Key B (dirección: infinite1xyz...)
Misma frase semilla + cuenta 2 → Key C (dirección: infinite1def...)
```

Las tres claves provienen de la misma frase semilla pero son completamente independientes. Puedes recuperarlas todas usando solo la frase semilla.

## Ver También

- [Key]({{< relref "key" >}}) - Qué es una clave criptográfica y frases semilla
- [Ruta de Derivación]({{< relref "derivation-path" >}}) - Entender las rutas de derivación y su estructura
- [Índice de Cuenta]({{< relref "account-index" >}}) - Cómo funcionan los índices de cuenta en la derivación de claves
- [Keyring]({{< relref "keyring" >}}) - Dónde se almacenan las claves derivadas
- [Múltiples Keys de una Misma Frase Semilla]({{< relref "../drive/guides/blockchain-nodes/keys/multiple-keys-from-seed" >}}) - Guía práctica para usar la derivación de claves
