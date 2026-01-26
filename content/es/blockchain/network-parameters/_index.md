---
title: "Parámetros de Red"
weight: 300
---

# Parámetros de Red

Referencia completa de todos los parámetros de red configurados para cada red de Infinite Improbability Drive.

## Redes Disponibles

- **[Parámetros Mainnet]({{< relref "mainnet" >}})** - Configuración de red de producción
- **[Parámetros Testnet]({{< relref "testnet" >}})** - Configuración de red de prueba
- **[Parámetros Creative]({{< relref "creative" >}})** - Red experimental

## Categorías de Parámetros

Cada configuración de red incluye:

- **Identidad de Red**: Chain IDs, prefijo Bech32
- **Configuración de Token**: Denominaciones, metadata
- **Módulo Auth**: Límites de firmas multisig
- **Módulo Staking**: Bonding, unbonding, límites de validadores
- **Módulo Mint**: Parámetros de inflación
- **Módulo Governance**: Parámetros de propuestas y votación
- **Módulo Slashing**: Parámetros de penalización y cárcel
- **Módulo Fee Market**: Parámetros de fees EIP-1559
- **Módulo Distribution**: Parámetros de distribución de fees
- **Parámetros de Consenso**: Tamaño de bloque, límites de gas, evidencia

## Modelo de Inflación Dinámico (Mainnet/Testnet)

Mainnet y testnet usan un **Modelo de Inflación Dinámico Target-Bonded**. Consulta las páginas individuales de red para detalles completos de parámetros.

## Red Creative: Inflación Cero

La red Creative está diseñada como un playground experimental con **inflación cero** y fees mínimos. Consulta [Parámetros Creative]({{< relref "creative" >}}) para detalles.

## Documentación Relacionada

- **[Configuración del Token]({{< relref "../token-configuration" >}})** - Denominaciones y metadata de tokens
- **[Tokenomics]({{< relref "../tokenomics" >}})** - Suministro y distribución de tokens
- **[Cuentas Módulo]({{< relref "../module-accounts" >}})** - Configuración de ModuleAccounts
- **[Cuentas de Vesting]({{< relref "../vesting-accounts" >}})** - Configuración de cuentas de vesting
