---
title: "Cuentas Módulo"
weight: 400
---

# Cuentas Módulo

Documentación técnica para ModuleAccounts configurados en archivos genesis de Infinite Improbability Drive.

## ¿Qué son los ModuleAccounts?

Los ModuleAccounts son cuentas especiales en Cosmos SDK que representan módulos on-chain. Tienen permisos para realizar acciones específicas (como acuñar tokens, distribuir recompensas) y no pueden ser controlados por claves privadas. Están gobernados por el DAO a través de gobernanza on-chain.

## ModuleAccounts en Genesis

Todos los pools de tokenomics están implementados como **ModuleAccounts** en genesis. Estas cuentas mantienen tokens que están gobernados por el DAO y representan la asignación líquida inicial visible en el lanzamiento de la cadena.

## Archivos de Configuración

Los ModuleAccounts se configuran mediante archivos JSON:

- **Mainnet**: `scripts/genesis-configs/mainnet-module-accounts.json`
- **Testnet**: `scripts/genesis-configs/testnet-module-accounts.json`
- **Creative**: `scripts/genesis-configs/creative-module-accounts.json`

## Estructura de ModuleAccount

Cada ModuleAccount se define con:

```json
{
  "name": "strategic_delegation",
  "amount_tokens": 40
}
```

- **`name`**: El nombre del ModuleAccount (identificador on-chain)
- **`amount_tokens`**: Cantidad inicial de tokens (en unidades de token completas, no unidades atómicas)

## ModuleAccounts Mainnet/Testnet

Tanto mainnet como testnet tienen los mismos 6 ModuleAccounts:

| **Nombre** | **Cantidad (Tokens)** | **% del Suministro** | **Mandato Operacional** |
|----------|---------------------|---------------------|-------------------------|
| `strategic_delegation` | 40 | 40% | Nunca gastado — solo delegado a validadores |
| `security_rewards` | 25 | 25% | Recompensas de validadores + stakers |
| `perpetual_rd` | 15 | 15% | Financiamiento institucional (Deep Thought Labs) |
| `fish_bootstrap` | 10 | 10% | Pools de liquidez inicial |
| `privacy_resistance` | 7 | 7% | I+D ZK, anti-censura |
| `community_growth` | 3 | 3% | Grants, educación, integraciones |
| **TOTAL** | **100** | **100%** | - |

> **Nota**: Estos 100 tokens son la **asignación líquida inicial** visible en el lanzamiento de la cadena. Representan la distribución de tokenomics de manera didáctica (40 tokens = 40% de asignación).

## ModuleAccounts de Red Creative

La red Creative tiene solo un ModuleAccount:

| **Nombre** | **Cantidad (Tokens)** | **Propósito** |
|----------|---------------------|-------------|
| `faucet` | Variable | Distribución de tokens de prueba |

## Direcciones On-Chain

Los ModuleAccounts tienen direcciones determinísticas basadas en su nombre. El formato de dirección sigue las convenciones de Cosmos SDK:

- **Formato**: `infinite1<hash-module-account>`
- **Derivación**: Basada en el nombre del módulo y el tipo de cuenta módulo

## Genesis Bootstrap (100 Tokens)

En el **Bloque 1**, exactamente **100 Improbability [42]** (100 cups) se distribuyen a ModuleAccounts:

- **Propósito:** Proporcionar **claridad visual y comprensión educativa** de la distribución de tokenomics
- **Distribución:** Divididos proporcionalmente entre los 6 pools según sus porcentajes de tokenomics
- **¿Por qué 100 tokens?** Esto hace que sea **intuitivamente fácil de entender** la distribución:
  - Cuando ves `40 [42]` en el archivo genesis o on-chain, inmediatamente entiendes que representa **40% de la asignación total**
  - Los números corresponden directamente a porcentajes, haciendo las tokenomics **visualmente transparentes** desde el primer día
  - Cualquiera puede verificar la distribución simplemente mirando los balances: 40 + 25 + 15 + 10 + 7 + 3 = 100

## Conversión de Tokens

El valor `amount_tokens` en la configuración JSON se convierte a unidades atómicas al crear el ModuleAccount:

- **Conversión**: `amount_tokens × 10¹⁸` (para convertir de tokens completos a unidades atómicas `drop`)
- **Ejemplo**: `40 tokens` → `40000000000000000000 drop`

## Setup Automático

Los ModuleAccounts se crean automáticamente por `setup_module_accounts.sh` al ejecutar `customize_genesis.sh`:

```bash
./scripts/customize_genesis.sh ~/.infinited/config/genesis.json --network mainnet
```

El script:
1. Lee el archivo de configuración de ModuleAccount para la red especificada
2. Crea cada ModuleAccount con la cantidad especificada
3. Valida la estructura del ModuleAccount
4. Asegura consistencia cuenta-balance

## Permisos de ModuleAccount

Los ModuleAccounts tienen permisos específicos basados en su tipo de módulo:

- **Módulo Bank**: Puede mantener y transferir tokens
- **Módulo Staking**: Puede delegar tokens a validadores
- **Módulo Distribution**: Puede distribuir recompensas
- **Gobernanza**: Controlado por propuestas DAO

## Consultar ModuleAccounts

Puedes consultar ModuleAccounts on-chain:

```bash
# Listar todas las cuentas módulo
infinited query auth module-accounts

# Consultar balance de cuenta módulo específica
infinited query bank balances <dirección-module-account>
```

## Documentación Relacionada

- **[Tokenomics]({{< relref "tokenomics" >}})** - Resumen de tokenomics y asignación de pools
- **[Parámetros de Red]({{< relref "network-parameters" >}})** - Configuraciones específicas de red
- **[Cuentas de Vesting]({{< relref "vesting-accounts" >}})** - Configuración de cuentas de vesting
- **[Genesis]({{< relref "genesis" >}})** - Cómo se crean los archivos genesis
