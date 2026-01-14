---
title: "Índice de Cuenta"
weight: 5
---

Un **índice de cuenta** (también llamado **número de cuenta**) es un componente de la [ruta de derivación]({{< relref "derivation-path" >}}) que determina qué clave específica se genera desde una frase semilla durante la [derivación de claves]({{< relref "key-derivation" >}}).

## ¿Qué es un Índice de Cuenta?

Piensa en el índice de cuenta como un "número de ranura" - cada ranura produce una clave diferente desde la misma frase semilla. Cuando especificas un índice de cuenta, le estás diciendo al sistema qué clave específica generar.

**Puntos clave:**
- Cada índice de cuenta crea una **clave diferente** y una **dirección diferente**
- Todas las claves provienen de la **misma frase semilla** pero son **completamente independientes**
- El índice de cuenta es parte de la [ruta de derivación]({{< relref "derivation-path" >}}) usada en la [derivación de claves]({{< relref "key-derivation" >}})

## Cómo Funciona

Cuando agregas una clave con una frase semilla:

1. Si **no especificas** un índice de cuenta, el sistema usa `0` (primera cuenta) por defecto
2. Si **especificas** un índice de cuenta (ej: `--account 1`), el sistema usa ese índice
3. El sistema combina tu frase semilla con el índice de cuenta para generar una clave única
4. Cada índice de cuenta diferente produce una clave y dirección completamente diferentes

## Comportamiento por Defecto

**Índice de cuenta por defecto:** `0`

Si no especificas un índice de cuenta al agregar una clave, el sistema automáticamente usa el índice de cuenta `0`. Esto significa:

```bash
# Estos dos comandos producen la misma clave:
./drive.sh exec infinite node-keys add my-key
./drive.sh exec infinite node-keys add my-key --account 0
```

## Ejemplos

**Ejemplo 1: Diferentes índices de cuenta producen diferentes claves**

```
Misma frase semilla + cuenta 0 → Key A (dirección: infinite1abc...)
Misma frase semilla + cuenta 1 → Key B (dirección: infinite1xyz...)
Misma frase semilla + cuenta 2 → Key C (dirección: infinite1def...)
```

**Ejemplo 2: Usar índices de cuenta en comandos**

```bash
# Cuenta 0 (por defecto)
./drive.sh exec infinite node-keys add my-main-key

# Cuenta 1
./drive.sh exec infinite node-keys add my-backup-key --account 1

# Cuenta 2
./drive.sh exec infinite node-keys add my-test-key --account 2
```

## En la Ruta de Derivación

El índice de cuenta es el tercer componente en una ruta de derivación BIP44:

```
m / 44' / coin_type' / account' / change / address_index
                      ↑
                 Índice de Cuenta
```

El índice de cuenta típicamente es "hardened" (indicado por el `'` después del número), lo que significa que proporciona un aislamiento de seguridad más fuerte entre diferentes cuentas.

## Casos de Uso Comunes

Los índices de cuenta se usan comúnmente para:

- **Organizar claves por propósito** - Cuenta principal (0), cuenta de respaldo (1), cuenta de prueba (2)
- **Separar por red** - Mainnet (0), testnet (1), desarrollo (2)
- **Gestionar múltiples cuentas** - Personal (0), negocios (1), ahorros (2)
- **Migrar desde otros wallets** - Coincidir con índices de cuenta usados en otros sistemas

## Notas Importantes

### ✅ Lo que Funciona

- Cada índice de cuenta crea una clave única e independiente
- Todas las claves son recuperables con la misma frase semilla
- Puedes agregar claves en cualquier orden
- Las claves son criptográficamente independientes (los fondos en una no afectan a la otra)

### ⚠️ Consideraciones Importantes

- **Misma frase semilla requerida** - Debes usar la **misma frase semilla exacta** para todos los índices de cuenta
- **Recordar el índice** - Si olvidas qué índice de cuenta usaste, necesitarás probar diferentes índices
- **Nombres descriptivos** - Usa nombres de claves claros para recordar qué índice de cuenta usa cada clave

### ❌ Errores Comunes

- **Usar diferentes frases semilla** - Cada frase semilla crea claves diferentes. Para obtener múltiples claves desde una semilla, debes usar la misma frase con diferentes índices de cuenta.
- **Olvidar el índice de cuenta** - Si olvidas qué índice usaste, necesitarás probar diferentes índices o revisar tus registros.

## Ver También

- [Derivación de Claves]({{< relref "key-derivation" >}}) - Cómo funciona la derivación de claves
- [Ruta de Derivación]({{< relref "derivation-path" >}}) - Entender las rutas de derivación y dónde encaja el índice de cuenta
- [Key]({{< relref "key" >}}) - Qué es una clave criptográfica
- [Múltiples Keys de una Misma Frase Semilla]({{< relref "../drive/guides/blockchain-nodes/keys/multiple-keys-from-seed" >}}) - Guía práctica con ejemplos
