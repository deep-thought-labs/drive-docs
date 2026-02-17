---
title: "Obtener Genesis desde URL"
weight: 4010
---

# Obtener Archivo Genesis desde URL

Esta guía te muestra cómo descargar el archivo genesis oficial para Infinite Improbability Drive mainnet o testnet al unirte a una red existente.

> [!IMPORTANT]
> **Cuándo Usar Esta Guía**
> 
> Usa esta guía cuando:
> - Te estás uniendo a una red existente (mainnet o testnet)
> - Quieres ejecutar un nodo con la configuración genesis oficial
> - Estás configurando un nuevo nodo después de que la cadena ha sido lanzada
> 
> **Si estás participando en un lanzamiento de cadena**, usa la guía [Crear Gentx]({{< relref "create-gentx" >}}) en su lugar.

## Prerrequisitos

Antes de comenzar, asegúrate de tener:

- ✅ **Drive instalado y configurado** con al menos un servicio de nodo blockchain
- ✅ **Nodo inicializado** (o listo para inicializar)
- ✅ **Acceso al bash del contenedor** del servicio correspondiente

## URLs Oficiales de Genesis

Los archivos genesis oficiales están alojados en:

- **Mainnet**: `https://assets.infinitedrive.xyz/mainnet/genesis.json`
- **Testnet**: `https://assets.infinitedrive.xyz/testnet/genesis.json`

## Método 1: Usando Drive (Recomendado)

Si estás usando Drive, el comando `node-init` descarga automáticamente el archivo genesis oficial desde la URL configurada. Este es el método más fácil:

### Para Mainnet

```bash
# 1. Navegar al directorio del servicio mainnet
cd drive/services/node0-infinite

# 2. Iniciar el contenedor (si no está ejecutándose)
./drive.sh up -d

# 3. Inicializar el nodo (descarga genesis automáticamente)
./drive.sh node-init
```

### Para Testnet

```bash
# 1. Navegar al directorio del servicio testnet
cd drive/services/node1-infinite-testnet

# 2. Iniciar el contenedor (si no está ejecutándose)
./drive.sh up -d

# 3. Inicializar el nodo (descarga genesis automáticamente)
./drive.sh node-init
```

El comando `node-init`:
- Descarga el archivo genesis oficial desde la URL configurada
- Lo coloca en la ubicación correcta (`~/.infinited/config/genesis.json`)
- Valida el archivo genesis automáticamente

## Método 2: Descarga Manual (Instalación Directa)

Si estás ejecutando un nodo sin Drive (instalación directa), puedes descargar el archivo genesis manualmente:

### Para Mainnet

```bash
# 1. Inicializar el nodo (si no se ha hecho)
infinited init my-node --chain-id infinite_421018-1 --home ~/.infinited

# 2. Descargar el archivo genesis oficial
curl -o ~/.infinited/config/genesis.json \
  https://assets.infinitedrive.xyz/mainnet/genesis.json

# 3. Validar el archivo genesis
infinited genesis validate-genesis --home ~/.infinited

# 4. Iniciar el nodo
infinited start --chain-id infinite_421018-1 --evm.evm-chain-id 421018 --home ~/.infinited
```

### Para Testnet

```bash
# 1. Inicializar el nodo (si no se ha hecho)
infinited init my-node --chain-id infinite_421018001-1 --home ~/.infinited

# 2. Descargar el archivo genesis oficial
curl -o ~/.infinited/config/genesis.json \
  https://assets.infinitedrive.xyz/testnet/genesis.json

# 3. Validar el archivo genesis
infinited genesis validate-genesis --home ~/.infinited

# 4. Iniciar el nodo
infinited start --chain-id infinite_421018001-1 --evm.evm-chain-id 421018001 --home ~/.infinited
```

## Verificar el Archivo Genesis

Después de descargar, verifica que el archivo genesis sea correcto:

### Verificar Chain ID

```bash
# Desde dentro del contenedor (si usas Drive)
cat ~/.infinited/config/genesis.json | jq -r '.chain_id'

# Chain IDs Esperados:
# Mainnet: infinite_421018-1
# Testnet: infinite_421018001-1
```

### Validar Estructura Genesis

```bash
infinited genesis validate-genesis --home ~/.infinited
```

**Esto verifica:**
- ✅ Consistencia de denominaciones
- ✅ El suministro total coincide con la suma de todos los balances
- ✅ La estructura JSON es correcta
- ✅ La configuración básica de genesis es válida

## Qué Está Incluido en el Genesis Oficial

El archivo genesis oficial incluye:

- ✅ **Todas las personalizaciones de Infinite Drive** (denominaciones, metadata de tokens, parámetros de módulos)
- ✅ **ModuleAccounts** para los 6 pools de tokenomics (strategic_delegation, security_rewards, perpetual_rd, fish_bootstrap, privacy_resistance, community_growth)
- ✅ **Cuentas de vesting** con 100M tokens bloqueados durante 42 años
- ✅ **Suministro líquido inicial** de 200 Improbability [42] (100 para validadores + 100 para pools)
- ✅ **Parámetros específicos de red** (configuraciones mainnet/testnet)

No se necesita personalización adicional—el archivo genesis está listo para usar.

## Solución de Problemas

### Error: "Failed to download genesis"

**Causa:** Problema de conectividad de red o URL incorrecta.

**Solución:** 
- Verifica tu conexión a internet
- Verifica que la URL sea correcta: `https://assets.infinitedrive.xyz/<network>/genesis.json`
- Intenta descargar manualmente con `curl` o `wget`

### Error: "Invalid genesis file"

**Causa:** El archivo descargado está corrupto o incompleto.

**Solución:**
- Vuelve a descargar el archivo genesis
- Verifica que el tamaño del archivo sea razonable (los archivos genesis típicamente son varios MB)
- Verifica que el archivo sea JSON válido: `cat ~/.infinited/config/genesis.json | jq .`

### Error: "Chain ID mismatch"

**Causa:** El Chain ID en el genesis no coincide con la configuración de tu nodo.

**Solución:**
- Verifica que descargaste el genesis correcto para tu red (mainnet vs testnet)
- Verifica el Chain ID en el genesis: `cat ~/.infinited/config/genesis.json | jq -r '.chain_id'`
- Asegúrate de que tu nodo esté inicializado con el Chain ID coincidente

## Próximos Pasos

Después de obtener y validar el archivo genesis:

1. **Inicia tu nodo** usando Drive o instalación directa
2. **Monitorea la sincronización del nodo** para asegurar que se está poniendo al día con la red
3. **Verifica que tu nodo esté conectado** a la red verificando peers y altura de bloque

> 📖 **Iniciar Nodo**: Para información sobre cómo iniciar tu nodo, consulta [Iniciar/Detener Nodo]({{< relref "../../../drive/guides/blockchain-nodes/start-stop-node" >}}) en la documentación de Drive.

## Ver También

- [Archivo Genesis]({{< relref "../../../concepts/genesis-file" >}}) - Concepto de archivo genesis
- [Crear Gentx]({{< relref "create-gentx" >}}) - Para participación en lanzamiento de cadena
- [Resumen de la Red]({{< relref "../overview" >}}) - Identidad de red y Chain IDs
- [Tokenomics]({{< relref "../tokenomics" >}}) - Qué está incluido en el archivo genesis
