---
title: "Parámetros Testnet"
weight: 320
---

# Parámetros de Red Testnet

Referencia completa de todos los parámetros de red configurados para Infinite Improbability Drive **testnet**.

## Identidad de Red

- **Nombre de la Cadena**: `infinite`
- **Cosmos Chain ID**: `infinite_421018001-1`
- **EVM Chain ID**: `421018001`
- **Prefijo Bech32**: `infinite`

## Configuración del Token

- **Denominación Base**: `tdrop`
- **Denominación Display**: `TestImprobability`
- **Símbolo**: `TEST42`
- **Nombre del Token**: `TestImprobability`
- **Descripción**: `TestImprobability Token — Project 42 Testnet: Sovereign, Perpetual, DAO-Governed`

## Módulo Auth

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `tx_sig_limit` | `10` | Número máximo de firmas permitidas para wallets multisig |

## Módulo Staking

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `bond_denom` | `tdrop` | Denominación para bonds de staking |
| `unbonding_time` | `1814400s` (21 días) | Tiempo requerido para desvincular tokens |
| `max_validators` | `100` | Número máximo de validadores |
| `historical_entries` | `10000` | Número de entradas históricas a mantener |
| `max_entries` | `7` | Máximo de entradas de unbonding/delegación |
| `min_commission_rate` | `0.000000000000000000` (0%) | Tasa de comisión mínima del validador |

## Módulo Mint (Inflación)

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `mint_denom` | `tdrop` | Denominación para tokens acuñados |
| `inflation_min` | `0.070000000000000000` (7%) | Tasa de inflación anual mínima |
| `inflation_max` | `0.200000000000000000` (20%) | Tasa de inflación anual máxima |
| `inflation_rate_change` | `0.130000000000000000` (13%) | Tasa máxima de cambio anual |
| `goal_bonded` | `0.670000000000000000` (67%) | Porcentaje objetivo de tokens vinculados |
| `blocks_per_year` | `6311520` | Bloques estimados por año |
| `initial_inflation` | `0.100000000000000000` (10%) | Tasa de inflación inicial en genesis |
| `initial_annual_provisions` | `0.000000000000000000` | Provisiones anuales iniciales (calculadas automáticamente) |

## Módulo Governance

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `min_deposit` | `1000000000000000000` (1 token) | Depósito mínimo requerido para crear una propuesta |
| `expedited_min_deposit` | `5000000000000000000` (5 tokens) | Depósito mínimo para propuestas expeditas |
| `max_deposit_period` | `172800s` (2 días) | Tiempo máximo para recolectar depósitos |
| `voting_period` | `172800s` (2 días) | Período de tiempo para votar en propuestas |
| `expedited_voting_period` | `86400s` (1 día) | Período de tiempo para propuestas expeditas |
| `quorum` | `0.334000000000000000` (33.4%) | Participación mínima de poder de voto requerida |
| `threshold` | `0.500000000000000000` (50%) | Porcentaje mínimo de votos Sí para aprobar |
| `veto_threshold` | `0.334000000000000000` (33.4%) | Porcentaje mínimo de votos Veto para rechazar |

## Módulo Slashing

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `signed_blocks_window` | `10000` | Número de bloques monitoreados para actividad de firma del validador |
| `min_signed_per_window` | `0.050000000000000000` (5%) | Porcentaje mínimo de bloques que deben ser firmados dentro de la ventana para evitar slashing |
| `downtime_jail_duration` | `600s` (10 minutos) | Duración que un validador permanece en cárcel **después** de que se detecta el downtime (no es el período de tolerancia antes de la detección) |
| `slash_fraction_double_sign` | `0.050000000000000000` (5%) | Fracción de stake slasheado por doble firma |
| `slash_fraction_downtime` | `0.000100000000000000` (0.01%) | Fracción de stake slasheado por downtime |

> **Tolerancia de Downtime:** Con `signed_blocks_window` de 10,000 bloques y `min_signed_per_window` de 5%, los validadores pueden estar offline aproximadamente **13.9 horas** (a ~5 segundos por bloque) antes de ser penalizados. El `downtime_jail_duration` de 10 minutos es el período de cárcel **después** de que se detecta el downtime, no la ventana de tolerancia antes de la detección.

## Módulo Fee Market (EIP-1559)

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `no_base_fee` | `false` | Si el base fee está deshabilitado |
| `base_fee` | `1000000000` | Base fee inicial (1 Gwei) |
| `min_gas_price` | `0` | Precio mínimo de gas |
| `min_gas_multiplier` | `0.500000000000000000` (0.5) | Multiplicador mínimo de precio de gas |
| `base_fee_change_denominator` | `8` | Denominador para cambios de base fee |
| `elasticity_multiplier` | `2` | Multiplicador de elasticidad para cálculo de fees |
| `enable_height` | `0` | Altura de bloque en la que se habilita el fee market |
| `block_gas` | `0` | Límite de gas objetivo del bloque |

## Módulo Distribution

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `community_tax` | `0.020000000000000000` (2%) | Porcentaje de fees enviados al community pool |
| `base_proposer_reward` | `0.010000000000000000` (1%) | Recompensa base para proponente de bloque |
| `bonus_proposer_reward` | `0.040000000000000000` (4%) | Recompensa bonus para proponente de bloque |
| `withdraw_addr_enabled` | `true` | Si las direcciones de retiro pueden ser cambiadas |

## Parámetros de Consenso

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `max_gas` | `10000000` | Gas máximo por bloque |
| `max_bytes` | `22020096` | Bytes máximo por bloque |
| `evidence_max_age_duration` | `172800000000000` (2 días) | Edad máxima de evidencia (nanosegundos) |
| `evidence_max_age_num_blocks` | `100000` | Edad máxima de evidencia (bloques) |
| `evidence_max_bytes` | `1048576` (1 MB) | Tamaño máximo de evidencia |

## Diferencias con Mainnet

Testnet usa los mismos parámetros que mainnet, con las siguientes diferencias:

- **Denominaciones de tokens**: Usa `tdrop` en lugar de `drop`
- **Metadata de tokens**: Nombre display, símbolo y descripción diferentes
- **Chain IDs**: Chain IDs de Cosmos y EVM diferentes

## Documentación Relacionada

- **[Resumen de Parámetros de Red]({{< relref ".." >}})** - Comparación entre redes
- **[Parámetros Mainnet]({{< relref "mainnet" >}})** - Configuración de mainnet
- **[Parámetros Creative]({{< relref "creative" >}})** - Configuración de red creative
