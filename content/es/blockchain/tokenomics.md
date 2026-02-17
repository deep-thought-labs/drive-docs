---
title: "Tokenomics"
weight: 200
---

# Tokenomics – Asignación de Pools

## Suministro Total

**Suministro Total (Inicial):** `100,000,200 Improbability [42]` (100,000,200 cups)

- **Circulante (Líquido):** `200 Improbability [42]` (200 cups) – Distribuido en genesis
- **Bloqueado (Vesting):** `100,000,000 Improbability [42]` (100,000,000 cups) – Liberado gradualmente durante **42 años**, controlado por DAO on-chain

## ¿Por qué 100 Millones de Tokens?

Así como usamos **100 tokens** en genesis para visualización fácil de porcentajes (40 tokens = 40%), usamos **100 millones de tokens** como suministro total porque hace que sea **intuitivamente fácil de entender** el ciclo de vida del proyecto y la evolución del market cap:

- **Los cálculos de porcentaje son directos**: 40% = 40 millones, 25% = 25 millones, etc.
- **El seguimiento del market cap es simple**: En cualquier punto de precio, puedes calcular fácilmente el market cap total
- **El crecimiento del suministro es transparente**: A medida que los tokens se desbloquean y la inflación agrega nuevos tokens, las matemáticas permanecen claras y verificables
- **Sin "números mágicos"**: Usar un número redondo (100M) hace que las tokenomics sean más accesibles y fáciles de comunicar

## Asignación de Pools

**Controlador Único:** DAO on-chain desde el bloque 1, con supervisión del laboratorio en operaciones de desarrollo  
**Inflación:** Dinámica, target-bonded, y ajustable por gobernanza

| **Pool** | **ModuleAccount** | **% del Suministro** | **Tokens Bloqueados** | **Mandato Operacional** |
|----------|-------------------|---------------------|----------------------|-------------------------|
| **A** | `strategic_delegation` | 40% | 40,000,000 Improbability [42] (40M cups) | Nunca gastado — solo delegado a validadores |
| **B** | `security_rewards` | 25% | 25,000,000 Improbability [42] (25M cups) | Recompensas de validadores + stakers |
| **C** | `perpetual_rd` | 15% | 15,000,000 Improbability [42] (15M cups) | Financiamiento institucional (Deep Thought Labs) |
| **D** | `fish_bootstrap` | 10% | 10,000,000 Improbability [42] (10M cups) | Pools de liquidez inicial |
| **E** | `privacy_resistance` | 7% | 7,000,000 Improbability [42] (7M cups) | I+D ZK, anti-censura |
| **F** | `community_growth` | 3% | 3,000,000 Improbability [42] (3M cups) | Grants, educación, integraciones |
| **TOTAL** | - | **100%** | **100,000,000 Improbability [42]** (100M cups) | - |

> **Nota**: Todos los pools están implementados como ModuleAccounts en genesis. La tabla anterior muestra los **tokens bloqueados** (100,000,000) que se desbloquearán durante 42 años.

**Filosofía de Diseño:** Infinite Improbability Drive es una **blockchain de infraestructura operacional**, no un sistema monetario de reserva de valor. El modelo de inflación y la estrategia de distribución de tokens están diseñados para sostener las operaciones de la red, incentivos de validadores y desarrollo del ecosistema—no para preservar poder adquisitivo o funcionar como dinero digital duro. A diferencia del modelo deflacionario de Bitcoin optimizado para preservación de valor, nuestra inflación controlada asegura que la red permanezca económicamente viable para servicios de infraestructura, operaciones de protocolo y sostenibilidad a largo plazo.

## Genesis Bootstrap (200 [42])

En el **Bloque 1**, exactamente **200 Improbability [42]** (200 cups) se acuñan como tokens líquidos y se distribuyen de la siguiente manera:

### 100 [42] → Conjunto Inicial de Validadores

- **Propósito:** Inicializar la red y permitir la producción inmediata de bloques
- **Distribución:** Mantenidos por el validador inicial, quien los distribuye pro-rata al **primer conjunto de validadores** a medida que se unen a la cadena
- **Función:** A medida que nuevos validadores se unen, reciben tokens de este pool para permitir staking y producción de bloques
- **Desde esta semilla, comienza la inflación**, y la red se auto-sustenta

### 100 [42] → Pools de Tokenomics (ModuleAccounts)

- **Propósito:** Proporcionar **claridad visual y comprensión educativa** de la distribución de tokenomics
- **Distribución:** Divididos proporcionalmente entre los 6 pools según sus porcentajes de tokenomics:
  - **Pool A (40%):** `40 [42]` → `strategic_delegation`
  - **Pool B (25%):** `25 [42]` → `security_rewards`
  - **Pool C (15%):** `15 [42]` → `perpetual_rd`
  - **Pool D (10%):** `10 [42]` → `fish_bootstrap`
  - **Pool E (7%):** `7 [42]` → `privacy_resistance`
  - **Pool F (3%):** `3 [42]` → `community_growth`
- **¿Por qué 100 tokens?** Esto hace que sea **intuitivamente fácil de entender** la distribución:
  - Cuando ves `40 [42]` en el archivo genesis o on-chain, inmediatamente entiendes que representa **40% de la asignación total**
  - Los números corresponden directamente a porcentajes, haciendo las tokenomics **visualmente transparentes** desde el primer día
  - Cualquiera puede verificar la distribución simplemente mirando los balances: 40 + 25 + 15 + 10 + 7 + 3 = 100

> **Suministro Completo en Genesis:**  
> - **200 Improbability [42] líquidos** (200 cups: 100 para validadores + 100 para visibilidad de pools de tokenomics)  
> - **100,000,000 Improbability [42] bloqueados** (100M cups) en cuentas de vesting (se desbloquean linealmente durante 42 años)  
> - **Total: 100,000,200 Improbability [42]** (100,000,200 cups)  
> Los 100 tokens en ModuleAccounts están **gobernados por el DAO** y representan la asignación líquida inicial visible en el lanzamiento de la cadena.

## Nacimiento del Mercado y Ruta de Liquidez

1. **Bloque 1:** `200 Improbability [42]` (200 cups) líquidos:
   - `100 [42]` (100 cups) → validador inicial (distribuye al primer conjunto de validadores)
   - `100 [42]` (100 cups) → pools de tokenomics (40+25+15+10+7+3, visible on-chain)
2. **Comienza el staking** → los validadores comienzan a producir bloques  
3. **Comienza la inflación** → nuevos tokens acuñados por bloque  
4. **Año 1+:** Los pools se desbloquean gradualmente durante 42 años → delegados/gastados vía gobernanza DAO  
5. **Los validadores controlan la liberación del mercado** → liquidez orgánica estilo Bitcoin

## Compromiso Perpetuo

- **Todos los pools se desbloquean gradualmente durante 42 años**, alineados con horizontes operacionales  
- **El DAO gobierna el destino de cada desbloqueo y flujo de inflación**  
- **El laboratorio retiene control operacional sobre Pool C (perpetual_rd)**  
- **Los ModuleAccounts de cada pool se rellenan continuamente vía fees de bloque + inflación**  
- **Ningún token entra en circulación sin custodia de validador primero**  
- **Seguridad, alineación y resiliencia a largo plazo desde genesis**

## Documentación Relacionada

- **[Parámetros de Red]({{< relref "network-parameters" >}})** - Modelo de inflación y estrategia de ajuste dinámico
- **[Genesis]({{< relref "genesis" >}})** - Implementación técnica de ModuleAccounts y cuentas de vesting
- **[Resumen de la Red]({{< relref "overview" >}})** - Identidad de la red y detalles del token
