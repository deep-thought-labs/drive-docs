---
title: "Flujo de Inicialización Técnico"
weight: 407
---

El proceso de inicialización del nodo es un flujo complejo que involucra múltiples pasos, validaciones y configuraciones. Esta sección documenta el flujo técnico completo de inicialización.

## Visión General

El proceso de inicialización (`node-init`) realiza las siguientes tareas:

1. Verificación de estado previo
2. Obtención del moniker
3. Ejecución del comando `infinited init`
4. Descarga y validación del genesis oficial
5. Configuración final

## Flujo Detallado

### 1. Verificación de Estado Previo

Antes de comenzar, el script verifica si el nodo ya está inicializado:

```bash
if [ -f "$NODE_GENESIS_FILE" ]; then
    print_warning "The node is already initialized."
    echo "   Genesis file found: ${CYAN}$NODE_GENESIS_FILE${RESET}"
    echo "   To reinitialize, delete the directory: ${CYAN}rm -rf ${NODE_HOME}/*${RESET}"
    exit 1
fi
```

**Verificación:**
- Busca el archivo `genesis.json` en `~/.infinited/config/`
- Si existe, asume que el nodo ya está inicializado
- Proporciona instrucciones para reinicializar si es necesario

### 2. Parsing de Argumentos

El script parsea los argumentos de la línea de comando:

```bash
RECOVERY_MODE=false
MONIKER=""

for arg in "$@"; do
    case $arg in
        --recover|-r)
            RECOVERY_MODE=true
            ;;
        *)
            # Si no es un flag y moniker está vacío, tratar como moniker
            if [ -z "$MONIKER" ] && [ "$arg" != "--recover" ] && [ "$arg" != "-r" ]; then
                MONIKER="$arg"
            fi
            ;;
    esac
done
```

**Argumentos soportados:**
- `--recover` o `-r`: Activa modo de recuperación
- Primer argumento no-flag: Tratado como moniker

**Ejemplos:**
```bash
node-init my-node                    # Moniker: "my-node"
node-init --recover my-node         # Modo recuperación, moniker: "my-node"
node-init my-node --recover         # Moniker: "my-node", modo recuperación
```

### 3. Obtención del Moniker

El moniker se obtiene de dos formas:

#### Desde Argumento

Si se proporciona como argumento, se valida:

```bash
if [ -n "$provided_moniker" ]; then
    provided_moniker=$(echo "$provided_moniker" | xargs)  # Trim whitespace
    if [ -z "$provided_moniker" ] || [ -z "${provided_moniker// }" ]; then
        print_error "Moniker cannot be empty or whitespace only"
        provided_moniker=""
    else
        echo "$provided_moniker"
        return 0
    fi
fi
```

#### Interactivamente

Si no se proporciona y el terminal es interactivo:

```bash
if is_interactive; then
    while true; do
        read -p "Moniker: " input_moniker < /dev/tty
        input_moniker=$(echo "$input_moniker" | xargs)  # Trim
        if [ -z "$input_moniker" ] || [ -z "${input_moniker// }" ]; then
            print_error "Moniker cannot be empty or whitespace only. Please try again."
            continue
        else
            echo "$input_moniker"
            return 0
        fi
    done
fi
```

**Validaciones:**
- No puede estar vacío
- No puede ser solo espacios en blanco
- Se trima automáticamente

### 4. Modo de Inicialización

El script soporta dos modos de inicialización:

#### Modo Simple (Sin Seed Phrase)

```bash
if [ "$RECOVERY_MODE" != true ]; then
    # Mostrar advertencias sobre claves aleatorias
    print_warning "IMPORTANT: Random Keys Will Be Generated"
    
    # Confirmación interactiva
    if is_interactive; then
        echo "Do you want to continue with random key generation? (yes/no)"
        read -p "Continue? " response
        case $response in
            [Yy][Ee][Ss]|y|Y)
                break
                ;;
            [Nn][Oo]|n|N)
                exit 0
                ;;
        esac
    fi
    
    # Ejecutar init sin --recover
    "${NODE_BINARY_PATH}" init "${MONIKER}" \
        --chain-id "${NODE_CHAIN_ID}" \
        --home "${NODE_HOME}" > /dev/null 2>&1
fi
```

**Características:**
- Genera claves aleatorias automáticamente
- No muestra ni guarda la seed phrase
- No es recuperable con seed phrase
- Adecuado para nodos full (no validadores)

#### Modo Recuperación (Con Seed Phrase)

```bash
if [ "$RECOVERY_MODE" = true ]; then
    print_step "Recovery Mode Activated"
    print_warning "IMPORTANT: You will be prompted to enter your seed phrase."
    
    # Ejecutar init con --recover
    "${NODE_BINARY_PATH}" init "${MONIKER}" \
        --chain-id "${NODE_CHAIN_ID}" \
        --home "${NODE_HOME}" \
        --recover > /dev/null
fi
```

**Características:**
- Solicita seed phrase al usuario
- Valida el formato de la seed phrase
- Permite recuperar claves existentes
- Adecuado para validadores o nodos que necesitan recuperación

**Nota:** La salida de `infinited init --recover` se redirige solo a `/dev/null` (stdout), manteniendo stderr para los prompts interactivos de la seed phrase.

### 5. Verificación Post-Inicialización

Después de ejecutar `infinited init`, el script verifica que fue exitoso:

```bash
if [ ! -f "$NODE_GENESIS_FILE" ]; then
    print_error "The genesis.json file was not generated correctly."
    exit 1
fi
```

**Verificación:**
- Confirma que `genesis.json` fue creado
- Si no existe, el proceso falla con error

### 6. Descarga del Genesis Oficial

El script descarga el genesis oficial desde el repositorio:

```bash
print_step "Downloading Official Genesis File"
echo "Source: ${CYAN}${NODE_GENESIS_URL}${RESET}"

# Descargar genesis
if wget --tries=3 --timeout=30 --quiet \
    --output-document="${NODE_GENESIS_FILE}.tmp" \
    "${NODE_GENESIS_URL}"; then
    
    # Validar JSON
    if jq empty "${NODE_GENESIS_FILE}.tmp" > /dev/null 2>&1; then
        mv "${NODE_GENESIS_FILE}.tmp" "$NODE_GENESIS_FILE"
        print_success "Official genesis file implemented correctly"
    else
        print_warning "The downloaded file is not valid JSON."
        rm -f "${NODE_GENESIS_FILE}.tmp"
    fi
else
    print_warning "Could not download the official genesis."
    rm -f "${NODE_GENESIS_FILE}.tmp" 2>/dev/null || true
fi
```

**Proceso:**

1. **Descarga:** Usa `wget` con 3 intentos y timeout de 30 segundos
2. **Validación JSON:** Usa `jq` para validar que el archivo es JSON válido
3. **Reemplazo:** Si es válido, reemplaza el genesis generado por `init`
4. **Fallback:** Si falla la descarga o validación, mantiene el genesis generado por `init`

**Características:**
- Descarga silenciosa (`--quiet`)
- Validación de formato JSON
- Manejo graceful de errores
- Archivo temporal para evitar corrupción

### 7. Configuración Final

Después de la inicialización, el script muestra información de resumen:

```bash
print_success "Node initialized successfully!"
echo "   Configuration location: ${CYAN}${NODE_HOME}${RESET}"

echo "${BOLD}To start the node:${RESET}"
print_code "Inside container: node-start"
print_code "From host: ./drive.sh node-start"
```

## Flujo Completo

```
Usuario ejecuta: node-init [--recover] [moniker]
    ↓
¿Ya está inicializado?
    ├─ Sí → Mostrar advertencia y salir
    └─ No → Continuar
    ↓
Parsear argumentos (--recover, moniker)
    ↓
¿Moniker proporcionado?
    ├─ No → Solicitar interactivamente
    └─ Sí → Validar y usar
    ↓
¿Modo recuperación?
    ├─ Sí → Ejecutar: infinited init --recover
    │       (solicita seed phrase interactivamente)
    └─ No → Mostrar advertencia sobre claves aleatorias
            ¿Confirmar?
            ├─ No → Salir
            └─ Sí → Ejecutar: infinited init
    ↓
¿Genesis.json creado?
    ├─ No → Error y salir
    └─ Sí → Continuar
    ↓
Descargar genesis oficial
    ↓
¿Descarga exitosa?
    ├─ Sí → ¿JSON válido?
    │       ├─ Sí → Reemplazar genesis
    │       └─ No → Mantener genesis generado
    └─ No → Mantener genesis generado
    ↓
Mostrar resumen y finalizar
```

## Archivos Creados Durante la Inicialización

### Estructura Generada

```
~/.infinited/
├── config/
│   ├── genesis.json          # Genesis (oficial o generado)
│   ├── config.toml           # Configuración del nodo
│   ├── app.toml              # Configuración de la aplicación
│   └── client.toml           # Configuración del cliente
├── data/                     # Directorio de datos (vacío inicialmente)
└── keyring-file/             # Keyring con claves generadas
```

### Archivos de Configuración

**`config.toml`:**
- Configuración de red P2P
- Puertos (26656 para P2P, 26657 para RPC)
- Configuración de peers y seeds
- Configuración de timeouts

**`app.toml`:**
- Configuración de la aplicación blockchain
- Límites de gas
- Configuración de APIs
- Configuración de gRPC

**`client.toml`:**
- Configuración del cliente CLI
- Chain ID
- Keyring backend
- Output format

## Variables de Entorno Utilizadas

```bash
NODE_CHAIN_ID              # Chain ID para inicialización
NODE_HOME                  # Directorio home del nodo
NODE_BINARY_PATH           # Ruta al binario infinited
NODE_GENESIS_FILE          # Ruta al archivo genesis
NODE_GENESIS_URL           # URL del genesis oficial
```

## Manejo de Errores

### Errores Comunes

1. **Nodo ya inicializado:**
   - Mensaje claro indicando que ya está inicializado
   - Instrucciones para reinicializar

2. **Moniker inválido:**
   - Validación en tiempo real
   - Mensajes de error claros
   - Reintento en modo interactivo

3. **Fallo en descarga de genesis:**
   - Advertencia, no error fatal
   - Usa genesis generado por `init`
   - Proceso continúa

4. **Genesis JSON inválido:**
   - Validación con `jq`
   - Mantiene genesis generado si el descargado es inválido

## Modo No Interactivo

El script soporta modo no interactivo para automatización:

```bash
# Modo simple
node-init my-node-name

# Modo recuperación
node-init --recover my-node-name
```

**Limitaciones:**
- No puede solicitar moniker interactivamente
- No puede solicitar confirmación para claves aleatorias
- No puede solicitar seed phrase (debe proporcionarse de otra forma)

## Ver También

- [Sistema de Configuración Interna]({{< relref "configuration-system" >}}) - Variables usadas en inicialización
- [Estructura Interna de Directorios]({{< relref "directory-structure" >}}) - Dónde se crean los archivos
- [Scripts Internos del Contenedor]({{< relref "internal-scripts" >}}) - Implementación del script node-init

