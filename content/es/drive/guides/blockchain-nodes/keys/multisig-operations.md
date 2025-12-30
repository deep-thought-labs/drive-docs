---
title: "Operaciones con Wallets Multifirma"
weight: 52225
---

Guía paso a paso para crear y usar wallets multifirma en el ecosistema Drive.

> [!NOTE]
> **Conceptos Fundamentales**
>
> Antes de continuar, asegúrate de entender:
> - [Wallet Multifirma]({{< relref "../../../../../concepts/multisig-wallet" >}}) - Qué es una wallet multifirma
> - [Umbral Multifirma]({{< relref "../../../../../concepts/multisig-threshold" >}}) - Cómo funciona M-of-N
> - [Firmante Multifirma]({{< relref "../../../../../concepts/multisig-signer" >}}) - Qué es un firmante
> - [Key]({{< relref "../../../../../concepts/key" >}}) - Conceptos básicos de claves
> - [Keyring]({{< relref "../../../../../concepts/keyring" >}}) - Cómo se almacenan las claves

> [!NOTE]
> **Interfaz Gráfica No Disponible**
>
> Actualmente, la interfaz gráfica de Drive no soporta operaciones con wallets multifirma. Todas las operaciones deben realizarse mediante comandos en el bash del contenedor.

## Preparación: Crear Claves Individuales

Antes de crear una wallet multifirma, cada participante debe tener su propia clave individual. Estas claves se usarán para formar la wallet multifirma.

### Paso 1: Cada Participante Crea su Clave

Cada participante debe crear su propia clave individual. **Esta operación está completamente soportada por la interfaz gráfica**, por lo que puedes elegir el método que prefieras.

> [!NOTE]
> **Interfaz Gráfica Disponible**
>
> A diferencia de las operaciones de multifirma (que requieren línea de comandos), **crear y agregar claves individuales SÍ está disponible en la interfaz gráfica**. Puedes usar cualquiera de los dos métodos según tu preferencia.

#### Opción 1: Usando Interfaz Gráfica (Recomendado)

1. Abre la interfaz gráfica: `./drive.sh exec infinite node-ui`
2. Navega a **"Key Management"**
3. Selecciona:
   - **"Generate Key (Dry-Run - Recommended)"** - Para crear una clave nueva y respaldar la frase semilla
   - **"Generate and Save Key"** - Para crear y guardar directamente
   - **"Add Existing Key from Seed Phrase"** - Si ya tienes una frase semilla

Para más información sobre cómo usar la interfaz gráfica, consulta [Operaciones de Gestión de Claves]({{< relref "operations" >}}).

#### Opción 2: Usando Línea de Comandos

```bash
cd drive/services/node0-infinite  # O tu servicio correspondiente

# Crear clave con dry-run (recomendado para respaldar frase semilla)
./drive.sh node-keys create participante1 --dry-run

# O crear y guardar directamente
./drive.sh node-keys create participante1
```

Para más información sobre cómo crear claves desde línea de comandos, consulta [Operaciones de Gestión de Claves]({{< relref "operations" >}}).

> [!IMPORTANT]
> **Respaldar Frase Semilla**
>
> Cada participante debe respaldar su frase semilla de forma segura. Esta es la única forma de recuperar su clave. Para más información, consulta [Mejores Prácticas de Seguridad]({{< relref "security" >}}).

### Paso 2: Exportar Claves Públicas

Cada participante debe exportar su clave pública (sin compartir la clave privada ni la frase semilla).

**Acceder al bash del contenedor:**

```bash
cd drive/services/node0-infinite
./drive.sh exec infinite bash
```

**Dentro del contenedor, exportar la clave pública:**

```bash
# Mostrar la clave pública en formato JSON
infinited keys show participante1 \
  --pubkey \
  --output json \
  --keyring-backend file \
  --home ~/.infinited

# O mostrar solo la clave pública en formato texto
infinited keys show participante1 \
  --pubkey \
  --keyring-backend file \
  --home ~/.infinited
```

**Ejemplo de salida (formato JSON):**
```json
{
  "@type": "/cosmos.crypto.secp256k1.PubKey",
  "key": "A/pubkey/base64/aqui"
}
```

> [!WARNING]
> **Solo Compartir Claves Públicas**
>
> ⚠️ **NUNCA** compartas tu clave privada, frase semilla, o archivo del keyring. Solo comparte la clave pública (pubkey).

Cada participante debe enviar su clave pública al coordinador de forma segura (email encriptado, Signal, PGP, etc.).

## Crear Wallet Multifirma

El coordinador (uno de los participantes) será responsable de crear la wallet multifirma combinando las claves públicas.

### Paso 1: Importar Claves Públicas al Keyring

El coordinador debe importar cada clave pública como una clave "solo-pública" (offline) en su keyring.

**Acceder al bash del contenedor:**

```bash
cd drive/services/node0-infinite
./drive.sh exec infinite bash
```

**Dentro del contenedor, importar cada clave pública:**

```bash
# Importar clave pública del participante 1
infinited keys add participante1_pub \
  --pubkey '{"@type":"/cosmos.crypto.secp256k1.PubKey","key":"A/pubkey/base64/participante1"}' \
  --keyring-backend file \
  --home ~/.infinited

# Importar clave pública del participante 2
infinited keys add participante2_pub \
  --pubkey '{"@type":"/cosmos.crypto.secp256k1.PubKey","key":"A/pubkey/base64/participante2"}' \
  --keyring-backend file \
  --home ~/.infinited

# Importar clave pública del participante 3
infinited keys add participante3_pub \
  --pubkey '{"@type":"/cosmos.crypto.secp256k1.PubKey","key":"A/pubkey/base64/participante3"}' \
  --keyring-backend file \
  --home ~/.infinited
```

> [!NOTE]
> **Formato de Clave Pública**
>
> Reemplaza `"A/pubkey/base64/participanteX"` con la clave pública real de cada participante en formato base64. El formato completo debe ser un JSON válido con el tipo de clave.

### Paso 2: Crear la Wallet Multifirma

Una vez importadas todas las claves públicas, crear la wallet multifirma:

**Ejemplo para 2-of-3 (2 firmas requeridas de 3 participantes):**

```bash
infinited keys add mi_multisig \
  --multisig participante1_pub,participante2_pub,participante3_pub \
  --multisig-threshold 2 \
  --keyring-backend file \
  --home ~/.infinited
```

**Ejemplo para 3-of-5 (3 firmas requeridas de 5 participantes):**

```bash
infinited keys add mi_multisig \
  --multisig participante1_pub,participante2_pub,participante3_pub,participante4_pub,participante5_pub \
  --multisig-threshold 3 \
  --keyring-backend file \
  --home ~/.infinited
```

### Paso 3: Obtener la Dirección de la Wallet Multifirma

```bash
infinited keys show mi_multisig \
  -a \
  --keyring-backend file \
  --home ~/.infinited
```

**Ejemplo de salida:**
```
infinite1abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
```

Comparte esta dirección con todos los participantes para verificación. Cada participante puede recrear la wallet multifirma localmente con las mismas claves públicas para confirmar que la dirección coincide.

## Firmar Transacciones con Multifirma

Para enviar una transacción desde una wallet multifirma, se requiere un proceso de firma distribuida.

### Paso 1: Generar Transacción Sin Firmar

El coordinador genera la transacción sin firmar:

```bash
# Ejemplo: Transferencia de tokens
infinited tx bank send \
  $(infinited keys show mi_multisig -a --keyring-backend file --home /home/ubuntu/.infinited) \
  infinite1destinatario123... \
  1000000drop \
  --chain-id infinite_421018-1 \
  --generate-only \
  --keyring-backend file \
  --home ~/.infinited \
  > tx_unsigned.json
```

### Paso 2: Cada Firmante Firma la Transacción

Cada participante debe firmar la transacción con su clave privada. Esto se hace de forma distribuida:

**Cada participante (en su propio nodo o máquina):**

```bash
# Acceder al bash del contenedor
cd drive/services/node0-infinite
./drive.sh exec infinite bash

# Firmar la transacción con la clave del participante
infinited tx sign tx_unsigned.json \
  --from participante1 \
  --multisig $(infinited keys show mi_multisig -a --keyring-backend file --home /home/ubuntu/.infinited) \
  --sign-mode amino-json \
  --keyring-backend file \
  --home ~/.infinited \
  --output-document firma_participante1.json
```

Repite este proceso para cada participante que debe firmar (al menos el número requerido por el umbral).

### Paso 3: Combinar Firmas

El coordinador combina las firmas de todos los participantes que firmaron:

```bash
infinited tx multisign \
  tx_unsigned.json \
  mi_multisig \
  firma_participante1.json \
  firma_participante2.json \
  --keyring-backend file \
  --home ~/.infinited \
  > tx_signed.json
```

> [!NOTE]
> **Número de Firmas**
>
> Debes incluir al menos el número de firmas requerido por el umbral (M). Puedes incluir más firmas si lo deseas, pero solo se necesitan M.

### Paso 4: Enviar la Transacción

Una vez combinadas las firmas, enviar la transacción:

```bash
infinited tx broadcast tx_signed.json \
  --chain-id infinite_421018-1 \
  --keyring-backend file \
  --home ~/.infinited
```

## Verificar Wallet Multifirma

Para verificar que una wallet multifirma se creó correctamente:

```bash
# Mostrar información de la wallet multifirma
infinited keys show mi_multisig \
  --keyring-backend file \
  --home ~/.infinited

# Mostrar solo la dirección
infinited keys show mi_multisig \
  -a \
  --keyring-backend file \
  --home ~/.infinited

# Mostrar la clave pública
infinited keys show mi_multisig \
  --pubkey \
  --keyring-backend file \
  --home ~/.infinited
```

## Listar Wallets Multifirma

Para ver todas las claves (incluyendo wallets multifirma) en tu keyring:

```bash
# Usando comandos de Drive (si la wallet está en el keyring)
cd drive/services/node0-infinite
./drive.sh node-keys list

# O directamente en el contenedor
./drive.sh exec infinite bash
infinited keys list \
  --keyring-backend file \
  --home ~/.infinited
```

## Ver También

- [Wallet Multifirma]({{< relref "../../../../../concepts/multisig-wallet" >}}) - Concepto atómico sobre wallets multifirma
- [Umbral Multifirma]({{< relref "../../../../../concepts/multisig-threshold" >}}) - Concepto atómico sobre umbrales
- [Firmante Multifirma]({{< relref "../../../../../concepts/multisig-signer" >}}) - Concepto atómico sobre firmantes
- [Operaciones de Gestión de Claves]({{< relref "operations" >}}) - Para operaciones con claves simples
- [Seguridad Multifirma]({{< relref "multisig-security" >}}) - Mejores prácticas de seguridad
- [Mejores Prácticas de Seguridad]({{< relref "security" >}}) - Seguridad general de claves

