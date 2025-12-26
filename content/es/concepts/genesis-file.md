---
title: "Archivo Génesis"
weight: 4
---

El **archivo génesis** (`genesis.json`) es el documento que define el estado inicial de una blockchain. Contiene toda la información necesaria para que un nodo pueda comenzar a sincronizar con la red desde el bloque inicial (bloque 0).

## ¿Qué es el Archivo Génesis?

El archivo génesis es un archivo JSON que actúa como el "punto de partida" de la blockchain. Define:

- **El estado inicial** de la blockchain
- **Los validadores iniciales** de la red
- **Los parámetros de consenso** y gobernanza
- **La configuración de la aplicación** blockchain
- **El Chain ID** que identifica la red

## Propósito del Archivo Génesis

### Estado Inicial de la Blockchain

El archivo génesis establece el estado inicial de la blockchain, incluyendo:

- Distribución inicial de tokens
- Cuentas iniciales y sus balances
- Contratos inteligentes desplegados inicialmente (si aplica)
- Configuración de módulos y parámetros

### Validadores Iniciales

Define quiénes son los validadores que participan en el consenso desde el inicio:

- Direcciones de los validadores
- Poder de voto inicial (staking)
- Información de consenso

### Parámetros de la Red

Establece los parámetros de operación de la red:

- Parámetros de consenso
- Configuración de gobernanza
- Parámetros económicos (inflación, recompensas, etc.)
- Límites y restricciones de la red

### Chain ID

El archivo génesis define el **Chain ID**, que es un identificador único para la red blockchain. Este ID:

- Identifica la red específica
- Previene ataques de replay entre diferentes redes
- Permite que los nodos se conecten a la red correcta

## Descarga Durante la Inicialización

Durante la [inicialización del nodo]({{< relref "node-initialization" >}}), el sistema:

1. **Genera un archivo génesis inicial** usando el comando `infinited init`
2. **Descarga automáticamente el archivo génesis oficial** de la red desde el repositorio oficial
3. **Reemplaza el génesis generado** con el oficial si la descarga es exitosa y el archivo es JSON válido
4. **Mantiene el génesis generado** si la descarga falla o el archivo descargado no es válido

**Ubicación:**
- **Ruta en el host:** `./persistent-data/config/genesis.json` (relativa al directorio del servicio)
- **Ruta en el contenedor:** `/home/ubuntu/.infinited/config/genesis.json`

**Nota:** El sistema verifica que el archivo descargado sea JSON válido antes de reemplazar el génesis generado. Si la descarga falla, el nodo puede funcionar con el génesis generado inicialmente, aunque es recomendable tener el génesis oficial.

## Importancia del Archivo Génesis

El archivo génesis es crítico porque:

- **Permite la sincronización** - Sin él, el nodo no puede comenzar a sincronizar con la blockchain
- **Garantiza la consistencia** - Todos los nodos deben usar el mismo archivo génesis para estar en la misma red
- **Define la identidad de la red** - El Chain ID y los parámetros identifican la red específica
- **Establece las reglas** - Los parámetros definen cómo opera la blockchain

## Verificación del Archivo Génesis

Después de inicializar un nodo, puedes verificar que el archivo génesis se descargó correctamente:

```bash
# Verifica que el archivo existe
ls -la persistent-data/config/genesis.json

# Verifica el Chain ID
cat persistent-data/config/genesis.json | grep chain_id
```

## Ver También

- [Inicialización de Nodo]({{< relref "node-initialization" >}}) - Qué es la inicialización y qué componentes crea
- [Data del Nodo]({{< relref "node-data" >}}) - Qué es la data del nodo y dónde se almacena
- [Inicialización de Nodo]({{< relref "../drive/guides/blockchain-nodes/initialization" >}}) - Guía práctica para inicializar un nodo

