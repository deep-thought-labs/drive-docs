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
- ✅ **Nodo inicializado** usando el proceso de recuperación (recovery) con tu seed phrase de validador
- ✅ **Llave agregada al keyring** usando la misma seed phrase de validador que usaste para inicializar el nodo
- ✅ **Conocer el nombre de la llave** que agregaste al keyring (este nombre lo elegiste cuando agregaste la llave)
- ✅ **Acceso al bash del contenedor** del servicio correspondiente

**⚠️ Importante sobre la llave:**
- Debes haber inicializado tu nodo usando el proceso de recuperación con tu seed phrase de validador
- Debes haber agregado esa misma seed phrase como una llave al keyring con un nombre específico (por ejemplo: `validator`, `my-validator`, etc.)
- **Debes recordar y tener claro cuál es el nombre de esa llave**, ya que lo necesitarás en todos los comandos de este documento
- Este nombre de llave es el que usarás en los comandos `add-genesis-account` y `genesis gentx`

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

## Paso 2: Verificar tu Llave en el Keyring

Antes de continuar, verifica que tu llave existe en el keyring y recuerda su nombre:

```bash
infinited keys list --keyring-backend file --home ~/.infinited
```

Este comando mostrará todas las llaves que tienes en el keyring. **Identifica y anota el nombre de la llave** que corresponde a tu validador (la que agregaste usando tu seed phrase de validador).

**Ejemplo de salida:**
```
- name: validator
  type: local
  address: infinite1abc123...
  pubkey: '{"@type":"/cosmos.crypto.secp256k1.PubKey","key":"..."}'
```

En este ejemplo, el nombre de la llave es `validator`. **Usa este mismo nombre** en los siguientes pasos.

> 📖 **Gestión de Keys**: Para más información sobre cómo gestionar claves, consulta [Gestión de Claves]({{< relref "../../../drive/guides/blockchain-nodes/keys" >}}) en la documentación de Drive.

---

## Paso 3: Agregar Fondos a la Cuenta en Genesis

**💡 Sugerencia:** Antes de ejecutar el comando, puedes prepararlo en un editor de texto plano para mayor facilidad. Esto te permitirá revisar y editar el comando completo (incluyendo el nombre de tu llave y el monto) antes de copiarlo y pegarlo en la consola.

Agrega tu cuenta al genesis con el saldo inicial necesario para crear el validador. **El equipo de desarrollo te especificará el monto exacto** que debes usar durante el proceso de lanzamiento. Los valores mostrados aquí son ejemplos generales:

**Ejemplo general:**

```bash
# Mainnet (ejemplo)
infinited genesis add-genesis-account <nombre-de-tu-llave> 1000000000000000000000drop \
  --keyring-backend file \
  --home ~/.infinited

# Testnet (ejemplo)
infinited genesis add-genesis-account <nombre-de-tu-llave> 1000000000000000000000tdrop \
  --keyring-backend file \
  --home ~/.infinited

# Creative (ejemplo)
infinited genesis add-genesis-account <nombre-de-tu-llave> 1000000000000000000000cdrop \
  --keyring-backend file \
  --home ~/.infinited
```

**Parámetros:**
- `<nombre-de-tu-llave>`: **Usa el nombre exacto de tu llave** que verificaste en el Paso 2 (por ejemplo: `validator`, `my-validator`, etc.). Reemplaza `<nombre-de-tu-llave>` con el nombre real de tu llave.
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

### Verificar que la Cuenta fue Agregada Correctamente

Antes de generar la gentx, es recomendable verificar que tu cuenta fue agregada correctamente al genesis. Puedes hacerlo consultando el contenido del genesis:

```bash
cat ~/.infinited/config/genesis.json | jq '.app_state.bank.balances'
```

Este comando mostrará todos los balances en el genesis. Busca tu dirección pública (la misma que viste cuando listaste tus llaves) y verifica que tiene el monto correcto.

**Ejemplo de salida esperada para Mainnet:**
```json
[
  {
    "address": "infinite1rs3s0jx0rvnsjwfjch59lg9ypp6k3vmg2cn68j",
    "coins": [
      {
        "denom": "drop",
        "amount": "1000000000000000000000"
      }
    ]
  }
]
```

**Ejemplo de salida esperada para Testnet:**
```json
[
  {
    "address": "infinite1rs3s0jx0rvnsjwfjch59lg9ypp6k3vmg2cn68j",
    "coins": [
      {
        "denom": "tdrop",
        "amount": "1000000000000000000000"
      }
    ]
  }
]
```

**Ejemplo de salida esperada para Creative:**
```json
[
  {
    "address": "infinite1rs3s0jx0rvnsjwfjch59lg9ypp6k3vmg2cn68j",
    "coins": [
      {
        "denom": "cdrop",
        "amount": "1000000000000000000000"
      }
    ]
  }
]
```

También puedes verificar la información de la cuenta en la sección de accounts:

```bash
cat ~/.infinited/config/genesis.json | jq '.app_state.auth.accounts'
```

**Ejemplo de salida esperada:**
```json
[
  {
    "@type": "/cosmos.auth.v1beta1.BaseAccount",
    "address": "infinite1rs3s0jx0rvnsjwfjch59lg9ypp6k3vmg2cn68j",
    "pub_key": null,
    "account_number": "0",
    "sequence": "0"
  }
]
```

Si ves tu dirección con el monto correcto y la denominación adecuada según la network (Mainnet: `drop`, Testnet: `tdrop`, Creative: `cdrop`), puedes proceder con confianza a generar tu gentx.

---

## Paso 4: Generar la Gentx

**💡 Sugerencia:** Antes de ejecutar el comando, puedes prepararlo en un editor de texto plano para mayor facilidad. Esto te permitirá revisar y editar el comando completo (incluyendo el nombre de tu llave y todos los parámetros) antes de copiarlo y pegarlo en la consola.

### 3-1. Crear la Gentx del Validador

Genera tu gentx con los parámetros de tu validador. **El equipo de desarrollo puede especificar valores particulares** para algunos parámetros (como tasas de comisión, autodelegación mínima, etc.) según el contexto del lanzamiento. Los valores mostrados aquí son ejemplos generales:

**Ejemplo general para Mainnet:**
```bash
infinited genesis gentx <nombre-de-tu-llave> 10000000000000000000drop \
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
infinited genesis gentx <nombre-de-tu-llave> 10000000000000000000tdrop \
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
infinited genesis gentx <nombre-de-tu-llave> 10000000000000000000cdrop \
  --chain-id infinite_421018002-1 \
  --commission-rate "0.01" \
  --commission-max-rate "0.05" \
  --commission-max-change-rate "0.01" \
  --min-self-delegation "1000000000000000000" \
  --keyring-backend file \
  --home ~/.infinited
```

**⚠️ Importante:** Reemplaza `<nombre-de-tu-llave>` con el nombre exacto de tu llave que verificaste en el Paso 2.

**Parámetros explicados:**
- `<nombre-de-tu-llave>`: **Usa el nombre exacto de tu llave** que verificaste en el Paso 2 (debe existir en el keyring y tener fondos en genesis)
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
La gentx se generará en: `~/.infinited/config/gentx/` con un formato de hash único, similar a: `gentx-adba573456c82908c3221163185703c421a2dd1f.json`

**⚠️ Importante:** El nombre del archivo NO incluye tu moniker, sino un hash único generado automáticamente. **NO debes renombrar este archivo JSON**.

---

## Paso 5: Validar la Gentx

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

## Paso 6: Entregar tu Gentx

### 6-1. Localizar tu Archivo Gentx

Tu gentx se generó en:
```bash
~/.infinited/config/gentx/
```

El archivo gentx tiene un formato con un hash único, similar a: `gentx-adba573456c82908c3221163185703c421a2dd1f.json`

**⚠️ Importante:** El nombre del archivo NO incluye tu moniker, sino un hash único generado automáticamente. **NO debes renombrar este archivo JSON**.

Para ver el nombre exacto de tu archivo:
```bash
ls -la ~/.infinited/config/gentx/
```

### 6-2. Preparar el Archivo para Entrega

**Si necesitas extraer el archivo del servidor:**

El archivo gentx está almacenado en el volumen persistente de Docker, por lo que es accesible desde el sistema host:

```bash
# Desde el sistema host, navega al directorio del servicio
cd services/<nombre-del-servicio>

# Copia el archivo manteniendo su nombre original (reemplaza <hash> con el hash real)
cp persistent-data/.infinited/config/gentx/gentx-<hash>.json ~/
```

**Si estás en un servidor remoto**, puedes usar `scp` para descargarlo a tu computadora local:

```bash
# Desde tu computadora local (reemplaza <hash> con el hash real de tu archivo)
scp usuario@servidor:/ruta/a/drive/services/<nombre-del-servicio>/persistent-data/.infinited/config/gentx/gentx-<hash>.json ~/
```

**Explicación del comando `scp`:**
- `usuario`: Es el nombre de usuario con el que inicias sesión en tu servidor
- `@servidor`: Se refiere a la dirección IP o el nombre de dominio de tu servidor (por ejemplo: `@192.168.1.100` o `@mi-servidor.com`)
- La ruta después de los dos puntos (`:`) es la ruta completa al archivo en el servidor
- `~/` es el directorio destino en tu computadora local (tu directorio home)

**⚠️ Importante:** Al ejecutar este comando, es muy probable que el sistema te solicite credenciales o autorización para realizar la transferencia. Estas son las mismas credenciales que usas cuando inicias sesión en tu servidor (contraseña o clave SSH).

**Ejemplo completo:** Si tu usuario es `ubuntu`, tu servidor tiene la IP `192.168.1.100`, el servicio es `node2-infinite-creative`, y tu archivo se llama `gentx-adba573456c82908c3221163185703c421a2dd1f.json`:
```bash
scp ubuntu@192.168.1.100:/home/ubuntu/drive/services/node2-infinite-creative/persistent-data/.infinited/config/gentx/gentx-adba573456c82908c3221163185703c421a2dd1f.json ~/gentx-round-1/
```

**Si necesitas comprimir el archivo:**

**⚠️ Importante:** 
- El archivo JSON gentx debe mantener su nombre original (con el hash, no lo renombres)
- El archivo comprimido SÍ puede incluir tu moniker en su nombre para facilitar la identificación

```bash
# Crear un archivo comprimido con tu moniker (reemplaza <moniker> con tu moniker y <hash> con el hash del archivo)
tar -czf gentx-<moniker>.tar.gz gentx-<hash>.json

# O usando zip
zip gentx-<moniker>.zip gentx-<hash>.json
```

**Estructura del archivo comprimido:**
- **Nombre del archivo comprimido:** `gentx-<tu-moniker>.tar.gz` (puede incluir tu moniker para identificación)
- **Contenido del archivo comprimido:** `gentx-<hash>.json` (el archivo JSON original con su nombre original)

### 6-3. Entregar al Equipo de Desarrollo

Sigue las instrucciones del equipo de desarrollo para entregar tu gentx. Esto puede ser:

- Subir el archivo a un repositorio específico
- Enviarlo por un canal de comunicación seguro (como Telegram)
- Otra forma indicada por el equipo

**⚠️ Importante:**
- Solo entrega el archivo gentx, NO el genesis completo
- Verifica que estás entregando el archivo correcto
- Mantén una copia de seguridad de tu gentx
- Si comprimes el archivo, el archivo comprimido puede tener tu moniker, pero el JSON dentro debe mantener su nombre original

---

## Resumen del Proceso

```
1. Descargar genesis base usando comando proporcionado por el equipo
   ↓
2. Verificar Chain ID del genesis descargado
   ↓
3. Verificar que tu llave existe en el keyring y recordar su nombre
   ↓
4. Agregar cuenta con fondos al genesis usando el nombre de tu llave (montos especificados por el equipo)
   ↓
5. Generar gentx usando el nombre de tu llave con parámetros del validador (valores especificados por el equipo)
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

