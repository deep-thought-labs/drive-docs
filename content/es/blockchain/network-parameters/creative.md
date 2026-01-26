---
title: "Parámetros Creative"
weight: 330
---

# Parámetros de Red Creative

Referencia completa de todos los parámetros de red configurados para la red **creative** de Infinite Improbability Drive (playground experimental).

## Identidad de Red

- **Nombre de la Cadena**: `infinite`
- **Cosmos Chain ID**: `infinite_421018002-1`
- **EVM Chain ID**: `421018002`
- **Prefijo Bech32**: `infinite`

## Configuración del Token

- **Denominación Base**: `cdrop`
- **Denominación Display**: `CreativeImprobability`
- **Símbolo**: `CRE42`
- **Nombre del Token**: `CreativeImprobability`
- **Descripción**: `CreativeImprobability Token — Project 42 Creative: Experimental Playground Network`

## Módulo Auth

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `tx_sig_limit` | `10` | Número máximo de firmas permitidas para wallets multisig |

## Módulo Staking

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `bond_denom` | `cdrop` | Denominación para bonds de staking |
| `unbonding_time` | `86400s` (1 día) | Tiempo requerido para desvincular tokens |
| `max_validators` | `50` | Número máximo de validadores |
| `historical_entries` | `1000` | Número de entradas históricas a mantener |
| `max_entries` | `7` | Máximo de entradas de unbonding/delegación |
| `min_commission_rate` | `0.000000000000000000` (0%) | Tasa de comisión mínima del validador |

## Módulo Mint (Inflación)

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `mint_denom` | `cdrop` | Denominación para tokens acuñados |
| `inflation_min` | `0.000000000000000000` (0%) | Tasa de inflación anual mínima |
| `inflation_max` | `0.000000000000000000` (0%) | Tasa de inflación anual máxima |
| `inflation_rate_change` | `0.000000000000000000` (0%) | Tasa máxima de cambio anual |
| `goal_bonded` | `0.500000000000000000` (50%) | Porcentaje objetivo de tokens vinculados |
| `blocks_per_year` | `6311520` | Bloques estimados por año |
| `initial_inflation` | `0.000000000000000000` (0%) | Tasa de inflación inicial en genesis |
| `initial_annual_provisions` | `0.000000000000000000` | Provisiones anuales iniciales (calculadas automáticamente) |

> **Nota**: La red Creative tiene **inflación cero** - está diseñada como un playground experimental sin emisión de tokens.

## Módulo Governance

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `min_deposit` | `100000000000000000` (0.1 tokens) | Depósito mínimo requerido para crear una propuesta |
| `expedited_min_deposit` | `1000000000000000000` (1 token) | Depósito mínimo para propuestas expeditas |
| `max_deposit_period` | `3600s` (1 hora) | Tiempo máximo para recolectar depósitos |
| `voting_period` | `3600s` (1 hora) | Período de tiempo para votar en propuestas |
| `expedited_voting_period` | `1800s` (30 minutos) | Período de tiempo para propuestas expeditas |
| `quorum` | `0.100000000000000000` (10%) | Participación mínima de poder de voto requerida |
| `threshold` | `0.500000000000000000` (50%) | Porcentaje mínimo de votos Sí para aprobar |
| `veto_threshold` | `0.200000000000000000` (20%) | Porcentaje mínimo de votos Veto para rechazar |

> **Nota**: La red Creative tiene **períodos de gobernanza más rápidos** (1 hora vs 2 días) para experimentación rápida.

## Módulo Slashing

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `signed_blocks_window` | `5000` | Número de bloques para ventana de slashing |
| `min_signed_per_window` | `0.010000000000000000` (1%) | Bloques mínimos firmados por ventana para evitar slashing |
| `downtime_jail_duration` | `60s` (1 minuto) | Tiempo que un validador está en cárcel por downtime |
| `slash_fraction_double_sign` | `0.010000000000000000` (1%) | Fracción de stake slasheado por doble firma |
| `slash_fraction_downtime` | `0.000010000000000000` (0.001%) | Fracción de stake slasheado por downtime |

> **Nota**: La red Creative tiene **penalizaciones de slashing más ligeras** y duraciones de cárcel más cortas para experimentación.

## Módulo Fee Market (EIP-1559)

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `no_base_fee` | `true` | Si el base fee está deshabilitado |
| `base_fee` | `0` | Base fee inicial (deshabilitado) |
| `min_gas_price` | `0` | Precio mínimo de gas |
| `min_gas_multiplier` | `0.100000000000000000` (0.1) | Multiplicador mínimo de precio de gas |
| `base_fee_change_denominator` | `8` | Denominador para cambios de base fee |
| `elasticity_multiplier` | `2` | Multiplicador de elasticidad para cálculo de fees |
| `enable_height` | `0` | Altura de bloque en la que se habilita el fee market |
| `block_gas` | `0` | Límite de gas objetivo del bloque |

> **Nota**: La red Creative **no tiene base fee** (`no_base_fee: true`) - las transacciones son esencialmente gratuitas para experimentación.

## Módulo Distribution

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `community_tax` | `0.000000000000000000` (0%) | Porcentaje de fees enviados al community pool |
| `base_proposer_reward` | `0.000000000000000000` (0%) | Recompensa base para proponente de bloque |
| `bonus_proposer_reward` | `0.000000000000000000` (0%) | Recompensa bonus para proponente de bloque |
| `withdraw_addr_enabled` | `true` | Si las direcciones de retiro pueden ser cambiadas |

> **Nota**: La red Creative tiene **recompensas de distribución cero** - todos los fees van directamente a los validadores.

## Parámetros de Consenso

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `max_gas` | `20000000` | Gas máximo por bloque (2x mainnet) |
| `max_bytes` | `22020096` | Bytes máximo por bloque |
| `evidence_max_age_duration` | `86400000000000` (1 día) | Edad máxima de evidencia (nanosegundos) |
| `evidence_max_age_num_blocks` | `50000` | Edad máxima de evidencia (bloques) |
| `evidence_max_bytes` | `1048576` (1 MB) | Tamaño máximo de evidencia |

> **Nota**: La red Creative tiene **límite de gas de bloque más alto** (20M vs 10M) para experimentación con transacciones más grandes.

## Diferencias Clave con Mainnet/Testnet

La red Creative está optimizada para experimentación y desarrollo:

| Característica | Mainnet/Testnet | Creative |
|---------|----------------|----------|
| **Inflación** | 7-20% (dinámica) | 0% (deshabilitada) |
| **Base Fee** | Habilitado (1 Gwei) | Deshabilitado (gratis) |
| **Tiempo de Unbonding** | 21 días | 1 día |
| **Períodos de Gobernanza** | 2 días | 1 hora |
| **Penalizaciones de Slashing** | Estándar | Más ligeras |
| **Max Validadores** | 100 | 50 |
| **Límite de Gas de Bloque** | 10M | 20M |
| **Recompensas de Distribución** | 2% community tax | 0% (todo a validadores) |

## Documentación Relacionada

- **[Resumen de Parámetros de Red]({{< relref ".." >}})** - Comparación entre redes
- **[Parámetros Mainnet]({{< relref "mainnet" >}})** - Configuración de mainnet
- **[Parámetros Testnet]({{< relref "testnet" >}})** - Configuración de testnet
