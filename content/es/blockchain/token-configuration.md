---
title: "Configuración del Token"
weight: 250
---

# Configuración del Token

Referencia completa de denominaciones de tokens y metadata configurada para cada red de Infinite Improbability Drive.

## Denominaciones de Tokens

Cada red usa diferentes denominaciones base:

| Red | Denom Base | Denom Display | Símbolo | Nombre del Token |
|---------|-----------|---------------|--------|------------|
| **Mainnet** | `drop` | `Improbability` | `42` | `Improbability` |
| **Testnet** | `tdrop` | `TestImprobability` | `TEST42` | `TestImprobability` |
| **Creative** | `cdrop` | `CreativeImprobability` | `CRE42` | `CreativeImprobability` |

## Configuración del Token Mainnet

- **Denominación Base**: `drop`
- **Denominación Display**: `Improbability`
- **Símbolo**: `42`
- **Nombre del Token**: `Improbability`
- **Descripción**: `Improbability Token — Project 42: Sovereign, Perpetual, DAO-Governed`
- **URI**: `https://assets.infinitedrive.xyz/tokens/42/icon.png`

## Configuración del Token Testnet

- **Denominación Base**: `tdrop`
- **Denominación Display**: `TestImprobability`
- **Símbolo**: `TEST42`
- **Nombre del Token**: `TestImprobability`
- **Descripción**: `TestImprobability Token — Project 42 Testnet: Sovereign, Perpetual, DAO-Governed`
- **URI**: `https://assets.infinitedrive.xyz/tokens/42/icon.png`

## Configuración del Token Creative

- **Denominación Base**: `cdrop`
- **Denominación Display**: `CreativeImprobability`
- **Símbolo**: `CRE42`
- **Nombre del Token**: `CreativeImprobability`
- **Descripción**: `CreativeImprobability Token — Project 42 Creative: Experimental Playground Network`
- **URI**: `https://assets.infinitedrive.xyz/tokens/42/icon.png`

## Unidades de Denominación

Todas las redes usan la misma estructura de unidades de denominación:

- **Unidad Base**: `drop` / `tdrop` / `cdrop` (exponente: 0)
- **Unidad Display**: `Improbability` / `TestImprobability` / `CreativeImprobability` (exponente: 18)
- **Conversión**: 1 unidad display = 10¹⁸ unidades base

## Denominaciones de Módulos

Todos los módulos están configurados para usar la denominación base específica de la red:

- **Módulo Staking**: `bond_denom` = denom base
- **Módulo Mint**: `mint_denom` = denom base
- **Módulo EVM**: `evm_denom` = denom base
- **Módulo Governance**: `min_deposit` y `expedited_min_deposit` usan denom base

## Metadata del Token

La metadata del token se almacena en `denom_metadata` del módulo Bank:

```json
{
  "description": "Improbability Token — Project 42: Sovereign, Perpetual, DAO-Governed",
  "denom_units": [
    {
      "denom": "drop",
      "exponent": 0,
      "aliases": []
    },
    {
      "denom": "Improbability",
      "exponent": 18,
      "aliases": ["improbability"]
    }
  ],
  "base": "drop",
  "display": "Improbability",
  "name": "Improbability",
  "symbol": "42",
  "uri": "https://assets.infinitedrive.xyz/tokens/42/icon.png",
  "uri_hash": ""
}
```

## Equivalencias

- **1 Improbability [42]** = **1 cup** (1 taza de Improbability)
- **1 cup** = **10¹⁸ drop**
- **1 drop** = **10⁻¹⁸ Improbability [42]** = **10⁻¹⁸ cup**

## Ejemplos

- `10 cups` = 10 Improbability [42] = 10 × 10¹⁸ drop
- `50 cups` = 50 Improbability [42] = 50 × 10¹⁸ drop
- `100 cups of Improbability` = 100 Improbability [42] = 100 × 10¹⁸ drop

## Documentación Relacionada

- **[Resumen de la Red]({{< relref "overview" >}})** - Identidad de la red y detalles del token
- **[Parámetros de Red]({{< relref "network-parameters" >}})** - Configuraciones específicas de red
- **[Tokenomics]({{< relref "tokenomics" >}})** - Suministro y distribución de tokens
