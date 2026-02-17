---
title: "Múltiples Keys de una Misma Frase Semilla"
weight: 52223
---

Aprende cómo crear múltiples keys desde una sola frase semilla usando diferentes índices de cuenta. Esto es útil para organizar keys por propósito (principal, respaldo, prueba) o gestionar múltiples cuentas desde un solo mnemónico.

## Resumen Rápido

**Lo que puedes hacer:**
- Crear múltiples keys desde la misma frase semilla
- Cada key tiene una dirección única
- Organizar keys por propósito (principal, respaldo, prueba, etc.)
- Todas las keys son recuperables con la misma frase semilla

**Cuándo usar:**
- Quieres keys separadas para diferentes propósitos (cuenta principal, respaldo, pruebas)
- Necesitas múltiples cuentas pero quieres gestionarlas con una frase semilla
- Estás migrando desde un wallet que usa diferentes índices de cuenta
- Quieres organizar tus keys por propósito o entorno

## Entendiendo la Derivación de Claves

> [!NOTE]
> **Conceptos Fundamentales**
>
> Antes de continuar, asegúrate de entender los conceptos básicos:
>
> - [Derivación de Claves]({{< relref "../../../../../concepts/key-derivation" >}}) - Cómo se generan múltiples claves desde una frase semilla
> - [Índice de Cuenta]({{< relref "../../../../../concepts/account-index" >}}) - Cómo los índices de cuenta determinan qué clave se crea
> - [Ruta de Derivación]({{< relref "../../../../../concepts/derivation-path" >}}) - Entender las rutas de derivación y su estructura

La **derivación de claves** es el proceso de generar múltiples claves criptográficas desde una sola frase semilla. Esta guía te muestra cómo usarla en la práctica.

### Resumen Rápido

Cuando agregas una key con una frase semilla, el sistema usa [derivación de claves]({{< relref "../../../../../concepts/key-derivation" >}}) para generar la key. La [ruta de derivación]({{< relref "../../../../../concepts/derivation-path" >}}) incluye un [índice de cuenta]({{< relref "../../../../../concepts/account-index" >}}) que determina qué clave específica se crea.

**Comportamiento por defecto:**
- Si no especificas un índice de cuenta, usa `0` (primera cuenta)
- Cada índice de cuenta crea una key y dirección diferente
- Todas las keys provienen de la misma frase semilla pero son completamente independientes

**Ejemplo:**
```
Misma frase semilla + cuenta 0 → Key A (dirección: infinite1abc...)
Misma frase semilla + cuenta 1 → Key B (dirección: infinite1xyz...)
Misma frase semilla + cuenta 2 → Key C (dirección: infinite1def...)
```

Para información detallada sobre cómo funciona la derivación de claves, ver [Derivación de Claves]({{< relref "../../../../../concepts/key-derivation" >}}).

## Casos de Uso Comunes

### Caso de Uso 1: Keys Principal y de Respaldo

Crea una key principal para operaciones diarias y una key de respaldo para emergencias:

```bash
# Key principal (cuenta 0 - por defecto)
./drive.sh exec infinite node-keys add my-main-key

# Key de respaldo (cuenta 1)
./drive.sh exec infinite node-keys add my-backup-key --account 1
```

**Qué sucede:**
- Ambas keys usan la misma frase semilla cuando las agregas
- `my-main-key` usa índice de cuenta 0
- `my-backup-key` usa índice de cuenta 1
- Tienen direcciones diferentes y son independientes

### Caso de Uso 2: Keys Separadas para Diferentes Redes

Organiza keys por red o entorno:

```bash
# Key de mainnet
./drive.sh exec infinite node-keys add my-mainnet-key

# Key de testnet
./drive.sh exec infinite node-keys add my-testnet-key --account 1

# Key de desarrollo
./drive.sh exec infinite node-keys add my-dev-key --account 2
```

### Caso de Uso 3: Keys para Diferentes Propósitos

Organiza keys según su uso previsto:

```bash
# Cuenta personal
./drive.sh exec infinite node-keys add my-personal-key

# Cuenta de negocios
./drive.sh exec infinite node-keys add my-business-key --account 1

# Cuenta de ahorros
./drive.sh exec infinite node-keys add my-savings-key --account 2
```

## Cómo Agregar Keys con Diferentes Índices

### Sintaxis Básica

**Por defecto (cuenta 0):**
```bash
./drive.sh exec infinite node-keys add <nombre-key>
```

**Con índice de cuenta:**
```bash
./drive.sh exec infinite node-keys add <nombre-key> --account <índice>
```

### Ejemplo Paso a Paso

Vamos a crear tres keys desde la misma frase semilla:

**Paso 1: Agregar primera key (cuenta 0)**
```bash
./drive.sh exec infinite node-keys add my-main-key
# Ingresa tu frase semilla cuando se solicite
```

**Paso 2: Agregar segunda key (cuenta 1)**
```bash
./drive.sh exec infinite node-keys add my-backup-key --account 1
# Ingresa la MISMA frase semilla cuando se solicite
```

**Paso 3: Agregar tercera key (cuenta 2)**
```bash
./drive.sh exec infinite node-keys add my-test-key --account 2
# Ingresa la MISMA frase semilla cuando se solicite
```

**Paso 4: Verificar todas las keys**
```bash
./drive.sh exec infinite node-keys list
```

Deberías ver las tres keys listadas con direcciones diferentes.

## Avanzado: Rutas de Derivación Personalizadas

Para usuarios avanzados, puedes especificar una ruta HD completa:

```bash
./drive.sh exec infinite node-keys add <nombre-key> --hd-path "m/44'/60'/0'/0/0"
```

> [!WARNING]
> **⚠️ EXPERIMENTAL: Hardware Wallets y Rutas Personalizadas**
>
> **Esta sección es experimental y necesita ser probada y validada.**
>
> Si estás leyendo esto, siéntete libre de realizar pruebas, pero hasta que estas instrucciones sean confirmadas por el equipo de desarrollo, **toma esta documentación solo de manera ilustrativa y recuerda: no confíes, verifica.**
>
> Las rutas de derivación personalizadas y la compatibilidad con hardware wallets aún están siendo validadas. Úsalas bajo tu propio riesgo y siempre verifica los resultados.

**Cuándo usar:**
- Necesitas compatibilidad con un wallet específico
- Quieres coincidir con una ruta de derivación específica
- Estás migrando desde otro sistema

> [!NOTE]
> **Tipo de Moneda por Defecto**
>
> Drive usa el tipo de moneda `60` (compatible con Ethereum) por defecto. La ruta por defecto es `m/44'/60'/cuenta'/0/0`.

## Notas Importantes

### ✅ Lo que Funciona

- Todas las keys de la misma frase semilla son recuperables con esa frase semilla
- Cada key tiene una dirección única
- Las keys son independientes (los fondos en una no afectan a la otra)
- Puedes agregar keys en cualquier orden

### ⚠️ Consideraciones Importantes

- **Misma frase semilla**: Debes usar la **misma frase semilla exacta** para todas las keys
- **Índice de cuenta**: Cada índice de cuenta crea una key diferente
- **Nombres de keys**: Usa nombres descriptivos para recordar qué key es cuál
- **Respaldo**: Siempre haz respaldo de tu frase semilla - es la única forma de recuperar todas las keys

### ❌ Errores Comunes

- **Usar diferentes frases semilla**: Cada frase semilla crea keys diferentes. Para obtener múltiples keys de una semilla, debes usar la misma frase con diferentes índices de cuenta.
- **Olvidar el índice de cuenta**: Si olvidas qué índice de cuenta usaste, necesitarás probar diferentes índices o revisar tus registros.
- **Confundir nombres de keys**: Usa nombres claros y descriptivos para evitar confusión.

## Verificación

Después de agregar keys, verifica que se crearon correctamente:

```bash
# Listar todas las keys
./drive.sh exec infinite node-keys list

# Mostrar detalles de una key específica
./drive.sh exec infinite node-keys show <nombre-key>
```

Cada key debería mostrar una dirección diferente, confirmando que son keys separadas.

## Solución de Problemas

**Problema: Agregué una key pero obtuve la misma dirección que antes**

**Solución:** Asegúrate de estar usando un índice de cuenta diferente. Verifica el comando que usaste - si no especificaste `--account`, por defecto es 0.

**Problema: No recuerdo qué índice de cuenta usé**

**Solución:** Intenta agregar la key nuevamente con diferentes índices de cuenta (0, 1, 2, etc.) hasta encontrar el que coincida con tu dirección esperada. Puedes verificar direcciones con `node-keys show`.

**Problema: La dirección de la key no coincide con lo que esperaba**

**Solución:** Verifica que estés usando la frase semilla correcta y el índice de cuenta correcto. Diferentes frases semilla o índices producirán direcciones diferentes.

## Ver También

- **[Operaciones de Gestión de Keys]({{< relref "operations" >}})** - Guía completa de todas las operaciones de keys
- **[Entendiendo las Keys]({{< relref "understanding-keys" >}})** - Aprende sobre diferentes tipos de keys
- **[Mejores Prácticas de Seguridad]({{< relref "security" >}})** - Protege tus keys y frases semilla
