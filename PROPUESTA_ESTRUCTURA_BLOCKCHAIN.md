# Propuesta de Estructura para la Sección Blockchain

## Análisis de la Situación Actual

### Estado Actual
- ✅ La carpeta `content/es/blockchain/` existe pero está vacía (solo contiene `_index.md`)
- ✅ Ya está configurada en el menú lateral (`main.yaml`) con `weight: 40`
- ✅ El `_index.md` actual tiene `sidebar: exclude: true`, lo que significa que no aparece en el sidebar

### Diferencia Clave: Drive vs Blockchain

**Drive:**
- Cómo usar Drive como herramienta
- Operar nodos en el entorno de Drive
- Gestión de servicios y contenedores
- Configuración de Drive
- Operaciones relacionadas con la infraestructura

**Blockchain:**
- Operaciones directamente relacionadas con la cadena
- Transacciones on-chain
- Operaciones con Genesis
- Configuraciones sobre Genesis
- Operaciones de validadores en la cadena
- Gobernanza y votación
- Operaciones de red (chain launch, upgrades)

---

## Propuesta de Estructura

### Estructura de Carpetas Propuesta

```
blockchain/
├── _index.md                    # Página principal de Blockchain
├── genesis/                      # Operaciones relacionadas con Genesis
│   ├── _index.md
│   ├── create-gentx.md          # ⭐ PRIMERA: Cómo crear una gentx
│   ├── customize-genesis.md     # Personalizar archivo genesis
│   ├── validate-genesis.md      # Validar archivo genesis
│   ├── distribute-genesis.md    # Distribuir genesis a nodos
│   └── collect-gentxs.md        # Recopilar gentxs de múltiples validadores
├── transactions/                 # Transacciones on-chain
│   ├── _index.md
│   ├── create-validator.md       # Crear validador en la cadena
│   ├── delegate.md              # Delegar tokens
│   ├── undelegate.md            # Desdelegar tokens
│   ├── redelegate.md            # Redelegar tokens
│   ├── transfer.md              # Transferir tokens
│   └── validator-operations.md  # Actualizar comisión, descripción, etc.
├── governance/                   # Gobernanza y DAO
│   ├── _index.md
│   ├── create-proposal.md       # Crear propuesta de gobernanza
│   ├── vote.md                  # Votar en propuestas
│   └── query-proposals.md       # Consultar propuestas
├── chain-operations/             # Operaciones de red/cadena
│   ├── _index.md
│   ├── chain-launch.md          # Proceso completo de lanzamiento de cadena
│   ├── upgrade.md               # Actualizaciones de la cadena
│   └── network-parameters.md    # Consultar parámetros de red
└── queries/                      # Consultas a la cadena
    ├── _index.md
    ├── account-info.md          # Información de cuentas
    ├── validator-info.md       # Información de validadores
    ├── staking-info.md          # Información de staking
    └── network-status.md        # Estado de la red
```

---

## Descripción Detallada de Cada Sección

### 1. `genesis/` - Operaciones con Genesis

**Propósito:** Guías para trabajar con archivos Genesis y gentxs (transacciones genesis).

**Contenido Propuesto:**

#### `create-gentx.md` ⭐ (PRIMERA INFORMACIÓN)
- **Descripción:** Guía completa paso a paso para crear una gentx
- **Contenido basado en:** `how-to-create-gentx.md` del blog
- **Incluye:**
  - Requisitos previos (Go, jq, repositorio Infinite)
  - Compilar binario `infinited`
  - Inicializar cadena y restaurar cuenta
  - Aplicar personalización de Infinite Drive
  - Crear cuenta y añadir fondos
  - Generar gentx con parámetros de validador
  - Validar y distribuir genesis
- **Referencias:**
  - Conceptos: Genesis File, Node Initialization
  - Drive: Inicialización de nodo (para contexto)

#### `customize-genesis.md`
- Cómo personalizar un archivo genesis
- Usar `customize_genesis.sh`
- Parámetros configurables
- Diferencias entre mainnet, testnet y creative

#### `validate-genesis.md`
- Validar un archivo genesis antes de usar
- Comando `infinited genesis validate-genesis`
- Qué verifica el comando
- Errores comunes y soluciones

#### `distribute-genesis.md`
- Distribuir genesis a múltiples nodos
- Métodos de distribución (scp, rsync, etc.)
- Verificar que todos los nodos tienen el mismo genesis
- Importancia de la consistencia

#### `collect-gentxs.md`
- Recopilar gentxs de múltiples validadores
- Comando `infinited genesis collect-gentxs`
- Proceso de compilación
- Verificación del genesis final

---

### 2. `transactions/` - Transacciones On-Chain

**Propósito:** Guías para realizar transacciones directamente en la cadena.

**Contenido Propuesto:**

#### `create-validator.md`
- Crear un validador en la cadena
- Transacción `create-validator`
- Parámetros requeridos (comisión, descripción, etc.)
- Verificación después de crear

#### `delegate.md`
- Delegar tokens a un validador
- Comando y parámetros
- Verificar delegación
- Recompensas y comisiones

#### `undelegate.md`
- Desdelegar tokens
- Período de unbonding
- Cuándo se liberan los tokens

#### `redelegate.md`
- Redelegar tokens entre validadores
- Evitar período de unbonding
- Límites y restricciones

#### `transfer.md`
- Transferir tokens entre cuentas
- Comandos básicos
- Verificar transferencias

#### `validator-operations.md`
- Actualizar comisión del validador
- Actualizar descripción
- Cambiar dirección de comisión
- Otras operaciones de validadores

---

### 3. `governance/` - Gobernanza y DAO

**Propósito:** Guías para participar en la gobernanza de la cadena.

**Contenido Propuesto:**

#### `create-proposal.md`
- Crear una propuesta de gobernanza
- Tipos de propuestas
- Parámetros requeridos
- Depositar tokens para la propuesta

#### `vote.md`
- Votar en propuestas
- Opciones de voto (Yes, No, Abstain, NoWithVeto)
- Poder de voto y delegaciones
- Consultar votos

#### `query-proposals.md`
- Consultar propuestas activas
- Ver detalles de propuestas
- Estado de propuestas
- Resultados de votación

---

### 4. `chain-operations/` - Operaciones de Red/Cadena

**Propósito:** Guías para operaciones a nivel de red y cadena.

**Contenido Propuesto:**

#### `chain-launch.md`
- Proceso completo de lanzamiento de cadena
- Pasos desde genesis base hasta lanzamiento
- Coordinación entre validadores
- Verificaciones finales

#### `upgrade.md`
- Actualizaciones de la cadena
- Proceso de upgrade
- Preparación de nodos
- Verificación post-upgrade

#### `network-parameters.md`
- Consultar parámetros de la red
- Parámetros de consenso
- Parámetros de gobernanza
- Parámetros económicos

---

### 5. `queries/` - Consultas a la Cadena

**Propósito:** Guías para consultar información de la cadena.

**Contenido Propuesto:**

#### `account-info.md`
- Consultar información de cuentas
- Balance de tokens
- Historial de transacciones
- Delegaciones activas

#### `validator-info.md`
- Información de validadores
- Estado (activo/inactivo/jailed)
- Comisión y descripción
- Poder de voto

#### `staking-info.md`
- Información de staking
- Total staked
- Validadores activos
- Distribución de poder

#### `network-status.md`
- Estado general de la red
- Altura del bloque
- Validadores conectados
- Sincronización

---

## Estructura del Menú Lateral Propuesta

```yaml
- name: "Blockchain"
  ref: "/blockchain"
  weight: 40
  icon: "gdoc_link"
  sub:
    - name: "Genesis"
      ref: "/blockchain/genesis"
      weight: 401
      sub:
        - name: "Create Gentx"
          ref: "/blockchain/genesis/create-gentx"
          weight: 4011
        - name: "Customize Genesis"
          ref: "/blockchain/genesis/customize-genesis"
          weight: 4012
        - name: "Validate Genesis"
          ref: "/blockchain/genesis/validate-genesis"
          weight: 4013
        - name: "Distribute Genesis"
          ref: "/blockchain/genesis/distribute-genesis"
          weight: 4014
        - name: "Collect Gentxs"
          ref: "/blockchain/genesis/collect-gentxs"
          weight: 4015
    - name: "Transactions"
      ref: "/blockchain/transactions"
      weight: 402
      sub:
        - name: "Create Validator"
          ref: "/blockchain/transactions/create-validator"
          weight: 4021
        - name: "Delegate"
          ref: "/blockchain/transactions/delegate"
          weight: 4022
        - name: "Undelegate"
          ref: "/blockchain/transactions/undelegate"
          weight: 4023
        - name: "Redelegate"
          ref: "/blockchain/transactions/redelegate"
          weight: 4024
        - name: "Transfer"
          ref: "/blockchain/transactions/transfer"
          weight: 4025
        - name: "Validator Operations"
          ref: "/blockchain/transactions/validator-operations"
          weight: 4026
    - name: "Governance"
      ref: "/blockchain/governance"
      weight: 403
      sub:
        - name: "Create Proposal"
          ref: "/blockchain/governance/create-proposal"
          weight: 4031
        - name: "Vote"
          ref: "/blockchain/governance/vote"
          weight: 4032
        - name: "Query Proposals"
          ref: "/blockchain/governance/query-proposals"
          weight: 4033
    - name: "Chain Operations"
      ref: "/blockchain/chain-operations"
      weight: 404
      sub:
        - name: "Chain Launch"
          ref: "/blockchain/chain-operations/chain-launch"
          weight: 4041
        - name: "Upgrade"
          ref: "/blockchain/chain-operations/upgrade"
          weight: 4042
        - name: "Network Parameters"
          ref: "/blockchain/chain-operations/network-parameters"
          weight: 4043
    - name: "Queries"
      ref: "/blockchain/queries"
      weight: 405
      sub:
        - name: "Account Info"
          ref: "/blockchain/queries/account-info"
          weight: 4051
        - name: "Validator Info"
          ref: "/blockchain/queries/validator-info"
          weight: 4052
        - name: "Staking Info"
          ref: "/blockchain/queries/staking-info"
          weight: 4053
        - name: "Network Status"
          ref: "/blockchain/queries/network-status"
          weight: 4054
```

---

## Plan de Implementación Fase 1 (Inicial)

### Paso 1: Actualizar `_index.md` de Blockchain

```markdown
---
title: "Blockchain"
type: "docs"
weight: 2
---

Documentación sobre operaciones directamente relacionadas con la cadena de bloques Infinite Improbability Drive.

## ¿Qué es esta sección?

Esta sección contiene guías para realizar operaciones directamente en la blockchain, incluyendo:

- **Operaciones con Genesis**: Crear gentxs, personalizar y validar archivos genesis
- **Transacciones On-Chain**: Crear validadores, delegar tokens, transferencias
- **Gobernanza**: Crear propuestas, votar, consultar propuestas
- **Operaciones de Red**: Lanzamiento de cadena, actualizaciones, parámetros
- **Consultas**: Consultar información de cuentas, validadores, staking, red

## Diferencia con Drive

- **Drive**: Cómo usar Drive como herramienta para gestionar nodos y servicios
- **Blockchain**: Operaciones directamente con la cadena (transacciones, genesis, gobernanza)

## Orden Recomendado de Lectura

1. **[Genesis]({{< relref "genesis" >}})** - Comienza aquí si necesitas crear una gentx o trabajar con genesis
2. **[Transacciones]({{< relref "transactions" >}})** - Aprende a realizar transacciones on-chain
3. **[Gobernanza]({{< relref "governance" >}})** - Participa en la gobernanza de la cadena
4. **[Operaciones de Red]({{< relref "chain-operations" >}})** - Operaciones a nivel de red
5. **[Consultas]({{< relref "queries" >}})** - Consultar información de la cadena
```

### Paso 2: Crear estructura de carpetas

Crear las carpetas:
- `blockchain/genesis/`
- `blockchain/transactions/`
- `blockchain/governance/`
- `blockchain/chain-operations/`
- `blockchain/queries/`

### Paso 3: Crear `genesis/_index.md`

```markdown
---
title: "Genesis"
weight: 401
---

Guías para trabajar con archivos Genesis y gentxs (transacciones genesis).

## Guías Disponibles

- **[Crear Gentx]({{< relref "create-gentx" >}})** - Guía completa para crear una gentx
- **[Personalizar Genesis]({{< relref "customize-genesis" >}})** - Personalizar archivo genesis
- **[Validar Genesis]({{< relref "validate-genesis" >}})** - Validar archivo genesis
- **[Distribuir Genesis]({{< relref "distribute-genesis" >}})** - Distribuir genesis a nodos
- **[Recopilar Gentxs]({{< relref "collect-gentxs" >}})** - Recopilar gentxs de múltiples validadores
```

### Paso 4: Crear `genesis/create-gentx.md` ⭐

Este será el primer documento completo. Basado en `how-to-create-gentx.md` del blog, pero adaptado para la documentación:

- Estructura más técnica y detallada
- Referencias cruzadas a conceptos
- Ejemplos para las tres cadenas (mainnet, testnet, creative)
- Troubleshooting común
- Referencias a Drive cuando sea relevante

---

## Consideraciones de Diseño

### Estructura de Peso (Weight)

- **Blockchain:** `weight: 40` (ya configurado)
- **Genesis:** `weight: 401`
  - Create Gentx: `4011`
  - Customize Genesis: `4012`
  - Validate Genesis: `4013`
  - Distribute Genesis: `4014`
  - Collect Gentxs: `4015`
- **Transactions:** `weight: 402`
  - Create Validator: `4021`
  - Delegate: `4022`
  - Undelegate: `4023`
  - Redelegate: `4024`
  - Transfer: `4025`
  - Validator Operations: `4026`
- **Governance:** `weight: 403`
- **Chain Operations:** `weight: 404`
- **Queries:** `weight: 405`

### Referencias Cruzadas

Cada documento debe incluir:
- Referencias a conceptos relevantes (`/concepts/`)
- Referencias a Drive cuando sea necesario (`/drive/`)
- Referencias entre documentos de Blockchain cuando sea relevante

### Ejemplo de Estructura de `create-gentx.md`

```markdown
---
title: "Crear Gentx"
weight: 4011
---

Guía completa paso a paso para crear una gentx (transacción genesis) que se agregará al archivo genesis de una cadena.

> [!NOTE]
> **Conceptos Previos**
> 
> Antes de continuar, asegúrate de entender:
> - [Genesis File]({{< relref "../../../concepts/genesis-file" >}}) - Qué es un archivo genesis
> - [Node Initialization]({{< relref "../../../concepts/node-initialization" >}}) - Proceso de inicialización

## ¿Qué es una Gentx?

Una gentx (genesis transaction) es una transacción que se incluye en el archivo genesis de una cadena. Permite crear validadores desde el bloque 1.

## Requisitos Previos

- Go 1.21+ instalado
- jq instalado
- Repositorio Infinite clonado
- [Nodo inicializado]({{< relref "../../../drive/guides/blockchain-nodes/initialization" >}}) (opcional, pero recomendado)

## Pasos

[Contenido detallado...]
```

---

## Ventajas de esta Estructura

1. **Clara Separación:** Drive vs Blockchain está bien definida
2. **Escalable:** Fácil agregar nuevas guías en cada categoría
3. **Lógica:** Organización por tipo de operación
4. **Navegable:** Estructura de menú clara y jerárquica
5. **Completa:** Cubre todas las operaciones on-chain necesarias
6. **Consistente:** Sigue el mismo patrón que la sección Drive

---

## Próximos Pasos

1. ✅ Revisar y aprobar esta propuesta
2. Crear estructura de carpetas
3. Actualizar `_index.md` de Blockchain
4. Crear `genesis/_index.md`
5. Crear `genesis/create-gentx.md` (primera guía completa)
6. Actualizar menú lateral (`data/menu/main.yaml`)
7. Agregar referencias desde otros documentos cuando sea relevante

