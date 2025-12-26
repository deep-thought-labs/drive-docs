---
title: "Crear Gentx"
weight: 4011
---

Guía paso a paso para crear una gentx (transacción genesis) a partir de un archivo genesis base proporcionado por el equipo de desarrollo.

> [!IMPORTANT]
> **Contexto y Uso de esta Guía**
> 
> Las operaciones relacionadas con gentx se utilizan exclusivamente durante **el lanzamiento o creación de una cadena de bloques**. Este proceso no forma parte del ciclo de vida diario de una blockchain, sino que ocurre únicamente cuando se está lanzando una nueva cadena, ya sea una cadena de prueba o la mainnet definitiva.
> 
> Si estás leyendo esta guía, es porque estás participando activamente en el lanzamiento de una cadena. Esta guía proporciona una explicación global del flujo completo, pero **el equipo de desarrollo te proporcionará instrucciones específicas** para cada lanzamiento, incluyendo:
> - URL y comando específico para descargar el genesis base
> - Montos específicos para la creación de cuentas
> - Parámetros específicos para la gentx según el contexto
> 
> **Siempre sigue las instrucciones específicas proporcionadas por el equipo de desarrollo para cada lanzamiento particular.**

Antes de continuar, asegúrate de entender los conceptos fundamentales: [Genesis File]({{< relref "../../../concepts/genesis-file" >}}), [Key]({{< relref "../../../concepts/key" >}}), y [Keyring]({{< relref "../../../concepts/keyring" >}}).

## ¿Qué es una Gentx?

Una **gentx** (genesis transaction) es una transacción que se incluye en el archivo genesis de una cadena. Permite crear validadores desde el bloque 1 (genesis block) de la cadena.

Cuando participas en el lanzamiento de una cadena, creas tu gentx a partir de un genesis base proporcionado por el equipo de desarrollo. Tu gentx contiene la información necesaria para registrar tu validador en el genesis final.

## Requisitos Previos

Antes de comenzar, asegúrate de tener:

- ✅ **Drive instalado y configurado** con al menos un servicio de nodo blockchain
- ✅ **Nodo inicializado** (el proceso de inicialización crea las carpetas necesarias)
- ✅ **Acceso al bash del contenedor** del servicio correspondiente
- ✅ **Seed phrase** de tu cuenta de validador guardada de forma segura

**Sobre el binario `infinited`**: Aunque puedes revisar el código fuente en el [repositorio oficial de Infinite](https://github.com/deep-thought-labs/infinite), **no es necesario compilar el binario por ti mismo**. El binario `infinited` ya está incluido dentro de cada servicio de Drive. Solo necesitas acceder al bash del contenedor y ejecutar los comandos desde ahí:

```bash
# Mainnet
cd services/node0-infinite
./drive.sh exec infinite bash

# Testnet
cd services/node1-infinite-testnet
./drive.sh exec infinite-testnet bash

# Creative
cd services/node2-infinite-creative
./drive.sh exec infinite-creative bash
```

Una vez dentro del bash del contenedor, el binario `infinited` estará disponible directamente. Todas las operaciones descritas en este documento se realizarán desde dentro del contenedor. Para más información, consulta [Gestión de Contenedores]({{< relref "../../../drive/guides/general/container-management#acceder-a-la-shell-del-contenedor" >}}).

## Paso 1: Obtener el Genesis Base

El equipo de desarrollo te proporcionará el archivo genesis base necesario para crear tu gentx. El equipo se encargará de proporcionar:

- **URL específica** desde donde descargar el genesis base
- **Comando específico** para descargar el archivo que ya especificará la ruta final donde debe estar el genesis

El comando proporcionado por el equipo descargará el genesis base directamente a la ubicación correcta (`~/.infinited/config/genesis.json` o la ruta que uses con `--home`), reemplazando el archivo genesis que se generó durante la inicialización de tu nodo.

**⚠️ Importante:**
- Asegúrate de estar dentro del bash del contenedor antes de ejecutar el comando
- El archivo descargado reemplazará el genesis existente
- Verifica que el archivo sea válido JSON después de descargarlo

### Verificar el Chain ID

Después de descargar el genesis base, verifica el Chain ID para asegurarte de que es el correcto:

```bash
cat ~/.infinited/config/genesis.json | jq -r '.chain_id'
```

**Chain IDs esperados:**
- **Mainnet:** `infinite_421018-1`
- **Testnet:** `infinite_421018001-1`
- **Creative:** `infinite_421018002-1`

Anota el Chain ID, lo necesitarás más adelante al generar tu gentx.

### Validar el Genesis Base

Antes de proceder a crear tu gentx, valida que el genesis base descargado es correcto:

```bash
infinited genesis validate-genesis --home ~/.infinited
```

**Esto verifica:**
- ✅ Consistencia de las denominaciones
- ✅ El suministro total coincide con la suma de todos los saldos
- ✅ La estructura JSON es correcta
- ✅ La configuración básica del genesis es válida

Si la validación es exitosa, puedes proceder con confianza a crear tu gentx. Si hay errores, contacta al equipo de desarrollo antes de continuar.

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

Agrega tu cuenta al genesis con el saldo inicial necesario para crear el validador. **El equipo de desarrollo te especificará el monto exacto** que debes usar durante el proceso de lanzamiento. Los valores mostrados aquí son ejemplos generales:

**Ejemplo general:**

```bash
# Mainnet (ejemplo)
infinited genesis add-genesis-account validator 1000000000000000000000drop \
  --keyring-backend file \
  --home ~/.infinited

# Testnet (ejemplo)
infinited genesis add-genesis-account validator 1000000000000000000000tdrop \
  --keyring-backend file \
  --home ~/.infinited

# Creative (ejemplo)
infinited genesis add-genesis-account validator 1000000000000000000000cdrop \
  --keyring-backend file \
  --home ~/.infinited
```

**Parámetros:**
- `validator`: Nombre de la cuenta que acabas de crear/recuperar
- **Cantidad**: El equipo de desarrollo te indicará el monto exacto a usar (en unidades atómicas)
- Denominaciones:
  - Mainnet: `drop`
  - Testnet: `tdrop`
  - Creative: `cdrop`

**⚠️ Importante:**
- Utiliza siempre unidades atómicas (10¹⁸)
- Incluye el sufijo de denominación correcto según la red
- **Usa los montos específicos proporcionados por el equipo de desarrollo** para el lanzamiento en curso
- Asegúrate de tener suficientes tokens para la autodelegación mínima requerida

---

## Paso 3: Generar la Gentx

### 3-1. Crear la Gentx del Validador

Genera tu gentx con los parámetros de tu validador. **El equipo de desarrollo puede especificar valores particulares** para algunos parámetros (como tasas de comisión, autodelegación mínima, etc.) según el contexto del lanzamiento. Los valores mostrados aquí son ejemplos generales:

**Ejemplo general para Mainnet:**
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

**Ejemplo general para Testnet:**
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

**Ejemplo general para Creative:**
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
- **Cantidad de autodelegación**: El equipo de desarrollo te indicará el monto exacto a usar
  - Ejemplos generales:
    - Mainnet: `10000000000000000000drop` (10 tokens)
    - Testnet: `10000000000000000000tdrop` (10 tokens)
    - Creative: `10000000000000000000cdrop` (10 tokens)
- `--chain-id`: Debe coincidir exactamente con el Chain ID del genesis base proporcionado por el equipo
- `--commission-rate`: Tasa de comisión inicial (el equipo puede especificar valores particulares)
- `--commission-max-rate`: Tasa de comisión máxima permitida (el equipo puede especificar valores particulares)
- `--commission-max-change-rate`: Cambio máximo de tasa por actualización (el equipo puede especificar valores particulares)
- `--min-self-delegation`: Autodelegación mínima requerida (el equipo puede especificar valores particulares)

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
1. Descargar genesis base usando comando proporcionado por el equipo
   ↓
2. Verificar Chain ID del genesis descargado
   ↓
3. Recuperar cuenta desde seed phrase
   ↓
4. Agregar cuenta con fondos al genesis (montos especificados por el equipo)
   ↓
5. Generar gentx con parámetros del validador (valores especificados por el equipo)
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
3. **Valida el genesis final antes de iniciar el nodo:**
   ```bash
   infinited genesis validate-genesis --home ~/.infinited
   ```
   Esta validación verifica que el genesis es correcto y está listo para usar. Es importante ejecutarla antes de iniciar el nodo para evitar problemas.
4. Iniciarás tu nodo con el genesis final
5. Tu validador estará activo desde el bloque 1

> 📖 **Iniciar Nodo**: Para información sobre cómo iniciar tu nodo, consulta [Iniciar/Detener Nodo]({{< relref "../../../drive/guides/blockchain-nodes/start-stop-node" >}}) en la documentación de Drive.

---

## Ver También

- [Genesis File]({{< relref "../../../concepts/genesis-file" >}}) - Concepto de archivo genesis
- [Gestión de Claves]({{< relref "../../../drive/guides/blockchain-nodes/keys" >}}) - Gestión de claves criptográficas

