---
title: "Tokenomics"
weight: 200
---

# Tokenomics – Pool Allocation

## Total Supply

**Total Supply (Initial):** `100,000,200 Improbability [42]` (100,000,200 cups)

- **Circulating (Liquid):** `200 Improbability [42]` (200 cups) – Distributed at genesis
- **Locked (Vesting):** `100,000,000 Improbability [42]` (100,000,000 cups) – Released gradually over **42 years**, controlled by on-chain DAO

## Why 100 Million Tokens?

Just like we use **100 tokens** in genesis for easy percentage visualization (40 tokens = 40%), we use **100 million tokens** as the total supply because it makes it **intuitively easy to understand** the project's lifecycle and market cap evolution:

- **Percentage calculations are straightforward**: 40% = 40 million, 25% = 25 million, etc.
- **Market cap tracking is simple**: At any price point, you can easily calculate total market cap
- **Supply growth is transparent**: As tokens unlock and inflation adds new tokens, the math remains clear and verifiable
- **No "magic numbers"**: Using a round number (100M) makes the tokenomics more accessible and easier to communicate

## Pool Allocation

**Sole Controller:** On-chain DAO from block 1, with lab oversight on development operations  
**Inflation:** Dynamic, target-bonded, and governance-adjustable

| **Pool** | **ModuleAccount** | **% of Supply** | **Tokens Locked** | **Operational Mandate** |
|----------|-------------------|-----------------|-------------------|--------------------------|
| **A** | `strategic_delegation` | 40% | 40,000,000 Improbability [42] (40M cups) | Never spent — only delegated to validators |
| **B** | `security_rewards` | 25% | 25,000,000 Improbability [42] (25M cups) | Validator + staker rewards |
| **C** | `perpetual_rd` | 15% | 15,000,000 Improbability [42] (15M cups) | Institutional funding (Deep Thought Labs) |
| **D** | `fish_bootstrap` | 10% | 10,000,000 Improbability [42] (10M cups) | Seed liquidity pools |
| **E** | `privacy_resistance` | 7% | 7,000,000 Improbability [42] (7M cups) | ZK, anti-censura R&D |
| **F** | `community_growth` | 3% | 3,000,000 Improbability [42] (3M cups) | Grants, education, integrations |
| **TOTAL** | - | **100%** | **100,000,000 Improbability [42]** (100M cups) | - |

> **Note**: All pools are implemented as ModuleAccounts in genesis. The table above shows the **locked tokens** (100,000,000) that will unlock over 42 years.

## Genesis Bootstrap (200 [42])

At **Block 1**, exactly **200 Improbability [42]** (200 cups) are minted as liquid tokens and distributed as follows:

### 100 [42] → Initial Validator Set

- **Purpose:** Bootstrap the network and enable immediate block production
- **Distribution:** Held by the initial validator, who distributes them pro-rata to the **first set of validators** as they join the chain
- **Function:** As new validators join, they receive tokens from this pool to enable staking and block production
- **From this seed, inflation begins**, and the network self-sustains

### 100 [42] → Tokenomics Pools (ModuleAccounts)

- **Purpose:** Provide **visual clarity and educational understanding** of the tokenomics distribution
- **Distribution:** Split proportionally across all 6 pools according to their tokenomics percentages:
  - **Pool A (40%):** `40 [42]` → `strategic_delegation`
  - **Pool B (25%):** `25 [42]` → `security_rewards`
  - **Pool C (15%):** `15 [42]` → `perpetual_rd`
  - **Pool D (10%):** `10 [42]` → `fish_bootstrap`
  - **Pool E (7%):** `7 [42]` → `privacy_resistance`
  - **Pool F (3%):** `3 [42]` → `community_growth`
- **Why 100 tokens?** This makes it **intuitively easy to understand** the distribution:
  - When you see `40 [42]` in the genesis file or on-chain, you immediately understand it represents **40% of the total allocation**
  - The numbers directly correspond to percentages, making the tokenomics **visually transparent** from day one
  - Anyone can verify the distribution by simply looking at the balances: 40 + 25 + 15 + 10 + 7 + 3 = 100

> **Complete Supply at Genesis:**  
> - **200 Improbability [42] liquid** (200 cups: 100 for validators + 100 for tokenomics pools visibility)  
> - **100,000,000 Improbability [42] locked** (100M cups) in vesting accounts (unlock linearly over 42 years)  
> - **Total: 100,000,200 Improbability [42]** (100,000,200 cups)  
> The 100 tokens in ModuleAccounts are **governed by the DAO** and represent the initial liquid allocation visible at chain launch.

## Market Birth & Liquidity Path

1. **Block 1:** `200 Improbability [42]` (200 cups) liquid:
   - `100 [42]` (100 cups) → initial validator (distributes to first validator set)
   - `100 [42]` (100 cups) → tokenomics pools (40+25+15+10+7+3, visible on-chain)
2. **Staking begins** → validators start producing blocks  
3. **Inflation kicks in** → new tokens minted per block  
4. **Year 1+:** Pools unlock gradually over 42 years → delegated/spent via DAO governance  
5. **Validators control market release** → Bitcoin-style organic liquidity

## Perpetual Commitment

- **All pools unlock gradually over 42 years**, aligned with operational horizons  
- **DAO governs destination of every unlock and inflation stream**  
- **Lab retains operational control over Pool C (perpetual_rd)**  
- **Each pool's ModuleAccounts are continuously refilled via block fees + inflation**  
- **No token enters circulation without validator custody first**  
- **Security, alignment, and long-term resilience from genesis**

## Related Documentation

- **[Network Parameters]({{< relref "network-parameters" >}})** - Inflation model and dynamic adjustment strategy
- **[Genesis]({{< relref "genesis" >}})** - Technical implementation of ModuleAccounts and vesting accounts
- **[Overview]({{< relref "overview" >}})** - Network identity and token details
