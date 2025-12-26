---
title: "Crear Gentx"
weight: 4011
---

Guía paso a paso para crear una gentx (transacción genesis) a partir de un archivo genesis base proporcionado por el equipo de desarrollo.

> [!NOTE]
> **Conceptos Previos**
> 
> Antes de continuar, asegúrate de entender:
> - [Genesis File]({{< relref "../../../concepts/genesis-file" >}}) - Qué es un archivo genesis
> - [Key]({{< relref "../../../concepts/key" >}}) - Qué son las claves criptográficas
> - [Keyring]({{< relref "../../../concepts/keyring" >}}) - Sistema de almacenamiento de claves

## ¿Qué es una Gentx?

Una **gentx** (genesis transaction) es una transacción que se incluye en el archivo genesis de una cadena. Permite crear validadores desde el bloque 1 (genesis block) de la cadena.

Cuando participas en el lanzamiento de una cadena, creas tu gentx a partir de un genesis base proporcionado por el equipo de desarrollo. Tu gentx contiene la información necesaria para registrar tu validador en el genesis final.

## Requisitos Previos

Antes de comenzar, asegúrate de tener:

- ✅ **Binario `infinited`** instalado y disponible en tu PATH
- ✅ **Archivo genesis base** proporcionado por el equipo de desarrollo
- ✅ **Seed phrase** de tu cuenta de validador guardada de forma segura
- ✅ **Comprensión básica** de cómo funcionan las claves y el keyring

> 📖 **Instalación del binario**: Si necesitas instalar el binario `infinited`, consulta la documentación del repositorio [Infinite](https://github.com/deep-thought-labs/infinite).

## Paso 1: Preparar el Entorno

### 1-1. Copiar el Genesis Base

El equipo de desarrollo te proporcionará un archivo genesis base. Copia este archivo a la ubicación donde trabajarás:

```bash
# Crear directorio de trabajo (si no existe)
mkdir -p ~/.infinited/config

# Copiar el genesis base proporcionado
cp /ruta/al/genesis-base.json ~/.infinited/config/genesis.json
```

**⚠️ Importante:**
- El archivo debe llamarse exactamente `genesis.json`
- Debe estar en `~/.infinited/config/genesis.json` (o la ruta que uses con `--home`)
- Verifica que el archivo sea válido JSON antes de continuar

### 1-2. Verificar el Chain ID

Verifica el Chain ID del genesis base:

```bash
cat ~/.infinited/config/genesis.json | jq -r '.chain_id'
```

**Chain IDs esperados:**
- **Mainnet:** `infinite_421018-1`
- **Testnet:** `infinite_421018001-1`
- **Creative:** `infinite_421018002-1`

Anota el Chain ID, lo necesitarás más adelante.

---

## Paso 2: Crear o Recuperar tu Cuenta

### 2-1. Recuperar tu Cuenta desde Seed Phrase

⚠️ **Continúa solo si ya tienes un mnemónico (seed phrase) almacenado de forma segura.**

```bash
infinited keys add validator --recover --keyring-backend file --home ~/.infinited
```

- `validator`: Nombre de la cuenta (puedes usar cualquier nombre)
- `--recover`: Modo de recuperación usando seed phrase
- `--keyring-backend file`: Usar keyring basado en archivos
- `--home ~/.infinited`: Directorio home del nodo

El sistema te pedirá ingresar tu seed phrase. Asegúrate de tenerla a mano y de ingresarla correctamente.

> 📖 **Gestión de Keys**: Para más información sobre cómo gestionar claves, consulta [Gestión de Claves]({{< relref "../../../drive/guides/blockchain-nodes/keys" >}}) en la documentación de Drive.

### 2-2. Agregar Fondos a la Cuenta en Genesis

Agrega tu cuenta al genesis con el saldo inicial necesario para crear el validador:

```bash
# Mainnet
infinited genesis add-genesis-account validator 1000000000000000000000drop \
  --keyring-backend file \
  --home ~/.infinited

# Testnet
infinited genesis add-genesis-account validator 1000000000000000000000tdrop \
  --keyring-backend file \
  --home ~/.infinited

# Creative
infinited genesis add-genesis-account validator 1000000000000000000000cdrop \
  --keyring-backend file \
  --home ~/.infinited
```

**Parámetros:**
- `validator`: Nombre de la cuenta que acabas de crear/recuperar
- `1000000000000000000000drop`: Cantidad en unidades atómicas (100 tokens × 10¹⁸)
- Denominaciones:
  - Mainnet: `drop`
  - Testnet: `tdrop`
  - Creative: `cdrop`

**⚠️ Importante:**
- Utiliza siempre unidades atómicas (10¹⁸)
- Incluye el sufijo de denominación correcto según la red
- Asegúrate de tener suficientes tokens para la autodelegación mínima requerida

---

## Paso 3: Generar la Gentx

### 3-1. Crear la Gentx del Validador

Genera tu gentx con los parámetros de tu validador:

**Mainnet:**
```bash
infinited genesis gentx validator 10000000000000000000drop \
  --chain-id infinite_421018-1 \
  --commission-rate "0.10" \
  --commission-max-rate "0.20" \
  --commission-max-change-rate "0.01" \
  --min-self-delegation "1000000000000000000" \
  --keyring-backend file \
  --home ~/.infinited
```

**Testnet:**
```bash
infinited genesis gentx validator 10000000000000000000tdrop \
  --chain-id infinite_421018001-1 \
  --commission-rate "0.10" \
  --commission-max-rate "0.20" \
  --commission-max-change-rate "0.01" \
  --min-self-delegation "1000000000000000000" \
  --keyring-backend file \
  --home ~/.infinited
```

**Creative:**
```bash
infinited genesis gentx validator 10000000000000000000cdrop \
  --chain-id infinite_421018002-1 \
  --commission-rate "0.01" \
  --commission-max-rate "0.05" \
  --commission-max-change-rate "0.01" \
  --min-self-delegation "1000000000000000000" \
  --keyring-backend file \
  --home ~/.infinited
```

**Parámetros explicados:**
- `validator`: Nombre de la cuenta (debe existir en el keyring y tener fondos en genesis)
- **Cantidad de autodelegación:**
  - Mainnet: `10000000000000000000drop` (10 tokens)
  - Testnet: `10000000000000000000tdrop` (10 tokens)
  - Creative: `10000000000000000000cdrop` (10 tokens)
- `--chain-id`: Debe coincidir exactamente con el Chain ID del genesis base
- `--commission-rate`: Tasa de comisión inicial (ej: 10% = "0.10")
- `--commission-max-rate`: Tasa de comisión máxima permitida (ej: 20% = "0.20")
- `--commission-max-change-rate`: Cambio máximo de tasa por actualización (ej: 1% = "0.01")
- `--min-self-delegation`: Autodelegación mínima requerida (en unidades atómicas)

**Ubicación de la gentx generada:**
La gentx se generará en: `~/.infinited/config/gentx/gentx-<moniker>.json`

---

## Paso 4: Validar la Gentx

### 4-1. Verificar que la Gentx se Creó Correctamente

```bash
# Listar gentxs generadas
ls -la ~/.infinited/config/gentx/
```

Deberías ver un archivo con el formato `gentx-<moniker>.json`.

### 4-2. Validar el Genesis con tu Gentx

Antes de entregar tu gentx, valida que el genesis funciona correctamente con ella:

```bash
# Recopilar gentxs (incluye la tuya)
infinited genesis collect-gentxs --home ~/.infinited

# Validar el genesis resultante
infinited genesis validate-genesis --home ~/.infinited
```

**Esto verifica:**
- ✅ Consistencia de las denominaciones
- ✅ El suministro total coincide con la suma de todos los saldos
- ✅ La configuración del validador es válida
- ✅ La estructura JSON es correcta

Si la validación es exitosa, tu gentx está lista para entregar.

---

## Paso 5: Entregar tu Gentx

### 5-1. Localizar tu Archivo Gentx

Tu gentx está en:
```bash
~/.infinited/config/gentx/gentx-<moniker>.json
```

### 5-2. Entregar al Equipo de Desarrollo

Sigue las instrucciones del equipo de desarrollo para entregar tu gentx. Esto puede ser:

- Subir el archivo a un repositorio específico
- Enviarlo por un canal de comunicación seguro
- Otra forma indicada por el equipo

**⚠️ Importante:**
- Solo entrega el archivo gentx, NO el genesis completo
- Verifica que estás entregando el archivo correcto
- Mantén una copia de seguridad de tu gentx

---

## Resumen del Proceso

```
1. Recibir genesis base del equipo
   ↓
2. Copiar genesis base a ~/.infinited/config/genesis.json
   ↓
3. Recuperar cuenta desde seed phrase
   ↓
4. Agregar cuenta con fondos al genesis
   ↓
5. Generar gentx con parámetros del validador
   ↓
6. Validar gentx y genesis
   ↓
7. Entregar gentx al equipo de desarrollo
```

---

## Troubleshooting

### Error: "account does not exist"

**Causa:** La cuenta no existe en el keyring o el nombre es incorrecto.

**Solución:** Verifica que hayas creado/recuperado la cuenta correctamente:
```bash
infinited keys list --keyring-backend file --home ~/.infinited
```

### Error: "insufficient funds"

**Causa:** No hay suficientes fondos en la cuenta para la autodelegación.

**Solución:** Aumenta la cantidad de fondos agregados al genesis en el Paso 2-2.

### Error: "chain-id mismatch"

**Causa:** El Chain ID usado no coincide con el del genesis base.

**Solución:** Verifica el Chain ID del genesis base y úsalo exactamente:
```bash
cat ~/.infinited/config/genesis.json | jq -r '.chain_id'
```

### Error: "gentx file not found"

**Causa:** La gentx no se generó correctamente o está en otra ubicación.

**Solución:** Verifica que el comando `genesis gentx` se ejecutó sin errores y revisa:
```bash
ls -la ~/.infinited/config/gentx/
```

---

## Próximos Pasos

Una vez que el equipo de desarrollo compile todas las gentxs en el genesis final:

1. Recibirás el genesis final compilado
2. Reemplazarás tu genesis local con el genesis final
3. Iniciarás tu nodo con el genesis final
4. Tu validador estará activo desde el bloque 1

> 📖 **Iniciar Nodo**: Para información sobre cómo iniciar tu nodo, consulta [Iniciar/Detener Nodo]({{< relref "../../../drive/guides/blockchain-nodes/start-stop-node" >}}) en la documentación de Drive.

---

## Ver También

- [Genesis File]({{< relref "../../../concepts/genesis-file" >}}) - Concepto de archivo genesis
- [Gestión de Claves]({{< relref "../../../drive/guides/blockchain-nodes/keys" >}}) - Gestión de claves criptográficas

