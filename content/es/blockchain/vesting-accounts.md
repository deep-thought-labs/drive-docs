---
title: "Cuentas de Vesting"
weight: 500
---

# Cuentas de Vesting

Documentación técnica para cuentas de vesting configuradas en archivos genesis de Infinite Improbability Drive.

## ¿Qué son las Cuentas de Vesting?

Las cuentas de vesting son tipos especiales de cuentas en Cosmos SDK que mantienen tokens que se desbloquean gradualmente con el tiempo. Se usan para implementar bloqueos de tokens y horarios de liberación gradual.

## Cuentas de Vesting en Genesis

Infinite Improbability Drive usa cuentas de vesting para bloquear **100,000,000 Improbability [42]** (100M cups) que se desbloquean linealmente durante **42 años**, controlados por DAO on-chain.

## Archivos de Configuración

Las cuentas de vesting se configuran mediante archivos JSON:

- **Mainnet**: `scripts/genesis-configs/mainnet-vesting-accounts.json`
- **Testnet**: `scripts/genesis-configs/testnet-vesting-accounts.json`
- **Creative**: `scripts/genesis-configs/creative-vesting-accounts.json`

## Estructura de Cuenta de Vesting

Cada cuenta de vesting se define con:

```json
{
  "address": "infinite10fhk6nsvuw4mhfdtv6zux754n8mz2z39ynqqf7",
  "amount_tokens": 100000000,
  "vesting_type": "continuous",
  "vesting_start_time": 1769666400,
  "vesting_end_time": 3095388000
}
```

- **`address`**: La dirección pública de la cuenta de vesting (wallet multisig)
- **`amount_tokens`**: Cantidad total de tokens a ser vestidos (en unidades de token completas)
- **`vesting_type`**: Tipo de vesting (`continuous` o `delayed`)
- **`vesting_start_time`**: Timestamp Unix cuando comienza el vesting
- **`vesting_end_time`**: Timestamp Unix cuando se completa el vesting

## Tipos de Vesting

### Vesting Continuo

Los tokens se desbloquean **linealmente** entre `start_time` y `end_time`:

- **En `start_time`**: 0% desbloqueado
- **En `end_time`**: 100% desbloqueado
- **Entre**: Desbloqueo lineal (ej., al 50% del tiempo, 50% desbloqueado)

### Vesting Retrasado

Los tokens se desbloquean **todos a la vez** en `end_time`:

- **Antes de `end_time`**: 0% desbloqueado
- **En `end_time`**: 100% desbloqueado

## Configuración de Vesting Mainnet/Testnet

Tanto mainnet como testnet tienen la misma configuración de vesting:

| **Parámetro** | **Valor** | **Descripción** |
|---------------|-----------|-----------------|
| **Dirección** | `infinite10fhk6nsvuw4mhfdtv6zux754n8mz2z39ynqqf7` | Dirección de wallet multisig |
| **Cantidad** | 100,000,000 tokens | Cantidad total vestida |
| **Tipo** | `continuous` | Desbloqueo lineal con el tiempo |
| **Tiempo de Inicio** | `1769666400` (2026-01-29 Jueves) | Timestamp de inicio de vesting |
| **Tiempo de Fin** | `3095388000` (2068-02-02 Jueves) | Timestamp de fin de vesting |
| **Duración** | 42 años | Período total de vesting |

## Conversión de Tokens

El valor `amount_tokens` en la configuración JSON se convierte a unidades atómicas al crear la cuenta de vesting:

- **Conversión**: `amount_tokens × 10¹⁸` (para convertir de tokens completos a unidades atómicas `drop`)
- **Ejemplo**: `100000000 tokens` → `100000000000000000000000000 drop`

## Cálculo de Timestamps

Los timestamps de vesting son timestamps Unix (segundos desde epoch):

- **Tiempo de Inicio**: Establecido al próximo Jueves después del lanzamiento de la cadena
- **Tiempo de Fin**: Exactamente 42 años desde el tiempo de inicio (también un Jueves)
- **Cálculo**: Asegura que ambas fechas caigan en el mismo día de la semana

## Comportamiento Antes del Lanzamiento de la Cadena

Si `vesting_start_time` está establecido **antes** de la fecha real de lanzamiento de la cadena:

- **Antes del Lanzamiento**: La cuenta de vesting existe pero ningún token está desbloqueado aún
- **En el Lanzamiento**: La cuenta comienza con 0% desbloqueado (incluso si `start_time` ha pasado)
- **Después del Lanzamiento**: Los tokens comienzan a desbloquearse linealmente desde la fecha de lanzamiento (o `start_time`, el que sea posterior)

Esto asegura que el vesting solo comience **después** de que la cadena esté activa, independientemente de cuándo se establezca `start_time`.

## Setup Automático

Las cuentas de vesting se crean automáticamente por `setup_vesting_accounts.sh` al ejecutar `customize_genesis.sh`:

```bash
./scripts/customize_genesis.sh ~/.infinited/config/genesis.json --network mainnet
```

El script:
1. Lee el archivo de configuración de cuentas de vesting para la red especificada
2. Crea cada cuenta de vesting con los parámetros especificados
3. Valida la estructura de la cuenta de vesting
4. Asegura consistencia cuenta-balance

## Consultar Cuentas de Vesting

Puedes consultar cuentas de vesting on-chain:

```bash
# Consultar información de cuenta
infinited query auth account <dirección-cuenta-vesting>

# Consultar balance de cuenta (total)
infinited query bank balances <dirección-cuenta-vesting>

# Consultar balance gastable (tokens desbloqueados)
infinited query bank spendable-balances <dirección-cuenta-vesting>
```

## Visualización de Balance

Al consultar una cuenta de vesting:

- **Balance `total`**: Muestra la **cantidad completa** (100M tokens), incluyendo tokens bloqueados
- **Balance `spendable`**: Muestra solo los **tokens desbloqueados** (aumenta gradualmente con el tiempo)

Este es el comportamiento esperado - la cantidad completa es visible, pero solo la porción desbloqueada es gastable.

## Control DAO

La cuenta de vesting está controlada por un **wallet multisig** que está gobernado por el DAO on-chain:

- **Dirección**: `infinite10fhk6nsvuw4mhfdtv6zux754n8mz2z39ynqqf7`
- **Control**: Gobernanza DAO vía firmas multisig
- **Propósito**: Asegura que los tokens se gasten de acuerdo con las decisiones del DAO

## Documentación Relacionada

- **[Tokenomics]({{< relref "tokenomics" >}})** - Resumen de tokenomics y desglose de suministro
- **[Parámetros de Red]({{< relref "network-parameters" >}})** - Configuraciones específicas de red
- **[Cuentas Módulo]({{< relref "module-accounts" >}})** - Configuración de ModuleAccounts
- **[Genesis]({{< relref "genesis" >}})** - Cómo se crean los archivos genesis
