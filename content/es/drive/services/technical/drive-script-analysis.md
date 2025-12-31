---
title: "Análisis del Script drive.sh"
weight: 5362
---

> [!WARNING]
> **⚠️ Documentación en Construcción**
>
> Este documento está en construcción y contiene análisis técnico en desarrollo. Está siendo utilizado por los desarrolladores para identificar la mejor solución al problema de permisos entre el sistema host y los contenedores Docker.
>
> **No tomes este documento como una guía de uso aún.** Este es un análisis técnico que puede cambiar significativamente mientras se desarrolla la solución final.

Análisis técnico completo del script `drive.sh` que gestiona los servicios de Drive.

## Ubicación del Script

Cada servicio tiene su propio script `drive.sh` en su directorio:

```
services/
└── <service-name>/
    └── drive.sh
```

## Propósito del Script

El script `drive.sh` es un wrapper alrededor de Docker Compose que:

1. **Gestiona permisos automáticamente** - Configura permisos de `persistent-data` para el contenedor
2. **Abstrae la complejidad** - Proporciona una interfaz simple para comandos de Docker Compose
3. **Maneja sudo automáticamente** - Funciona con o sin `sudo`
4. **Muestra logs automáticamente** - Al iniciar servicios, muestra los logs automáticamente
5. **Sintaxis simplificada** - Detecta comandos `node-*` y completa automáticamente `exec` y nombre del servicio
6. **Detección automática de modo interactivo** - Agrega `-it` automáticamente cuando es necesario

## Estructura del Script

### 1. Inicialización y Validación

```bash
# Obtiene el directorio del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Verifica disponibilidad de docker-compose
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null 2>&1; then
    DOCKER_COMPOSE_CMD="docker compose"
```

**Funcionalidad:**
- Detecta automáticamente si usar `docker-compose` (legacy) o `docker compose` (nuevo)
- Cambia al directorio del script para ejecutar comandos en el contexto correcto
- Valida que `docker-compose.yml` existe antes de continuar

### 2. Gestión de Permisos de persistent-data

Esta es la sección más crítica del script:

```bash
# El contenedor ejecuta como usuario 'ubuntu' (UID 1000)
if [ -d "persistent-data" ]; then
    if [ -w "persistent-data" ] || [ -n "$SUDO_USER" ]; then
        # Opción 1: Permisos 775/777 (permite escritura a grupo/otros)
        chmod -R 775 "persistent-data" 2>/dev/null || chmod -R 777 "persistent-data" 2>/dev/null || true
        
        # Opción 2: Si hay sudo, cambiar propiedad a UID 1000
        if [ -n "$SUDO_USER" ]; then
            chown -R 1000:1000 "persistent-data" 2>/dev/null || true
        fi
    fi
else
    # Crear directorio con permisos correctos
    mkdir -p "persistent-data"
    chmod 775 "persistent-data" 2>/dev/null || chmod 777 "persistent-data" 2>/dev/null || true
    if [ -n "$SUDO_USER" ]; then
        chown -R 1000:1000 "persistent-data" 2>/dev/null || true
    fi
fi
```

**Análisis de la Lógica:**

1. **Condición de ejecución:** Solo intenta cambiar permisos si:
   - El usuario actual puede escribir en `persistent-data`, O
   - El script se ejecutó con `sudo` (detectado por `$SUDO_USER`)

2. **Estrategia de permisos (sin sudo):**
   - Intenta `chmod 775` (lectura/escritura para propietario y grupo, lectura para otros)
   - Si falla, intenta `chmod 777` (lectura/escritura para todos)
   - Usa `|| true` para evitar que el script falle si no tiene permisos

3. **Estrategia de permisos (con sudo):**
   - Además de `chmod`, intenta `chown 1000:1000` para cambiar la propiedad a UID 1000
   - Esto es más seguro que permisos 777, pero requiere sudo

**Limitaciones identificadas:**

- Si el usuario no tiene permisos de escritura en `persistent-data` Y no tiene sudo, el script no puede configurar permisos
- Los comandos usan `|| true` para no fallar, pero esto puede ocultar problemas de permisos
- No verifica si los permisos se aplicaron correctamente después de intentar cambiarlos

### 3. Detección de Comando 'up -d'

```bash
SHOW_LOGS=false
if [ "$1" = "up" ]; then
    for arg in "$@"; do
        if [ "$arg" = "-d" ] || [ "$arg" = "--detach" ]; then
            SHOW_LOGS=true
            break
        fi
    done
fi
```

**Funcionalidad:**
- Detecta cuando se ejecuta `./drive.sh up -d`
- Activa la visualización automática de logs después de iniciar el contenedor

### 4. Ejecución de Docker Compose

```bash
if [ -n "$SUDO_USER" ]; then
    sudo -E $DOCKER_COMPOSE_CMD "$@" || EXIT_CODE=$?
else
    $DOCKER_COMPOSE_CMD "$@" || EXIT_CODE=$?
fi
```

**Funcionalidad:**
- Si se ejecutó con `sudo`, usa `sudo` para Docker Compose también
- `-E` preserva las variables de entorno
- Captura el código de salida para manejo de errores

### 5. Detección Automática de Comandos `node-*`

El script detecta cuando el usuario ejecuta un comando `node-*` directamente (sin `exec` y nombre de servicio):

```bash
# Si el usuario ejecuta: ./drive.sh node-init
# El script automáticamente transforma a: ./drive.sh exec <service-name> node-init
```

**Funcionalidad:**
- Detecta comandos que empiezan con `node-`
- Obtiene el nombre del servicio del `docker-compose.yml` del directorio actual usando `get_service_name()`
- Reconstruye los argumentos agregando `exec` y el nombre del servicio
- Mantiene compatibilidad con la sintaxis completa si el usuario ya especificó `exec`

**Método `get_service_name()`:**
- Intenta usar `docker compose config --services` (método preferido)
- Fallback a parsing directo del YAML usando `awk` o `grep`
- Retorna el primer servicio encontrado en `docker-compose.yml`

### 6. Detección Automática de Modo Interactivo

El script detecta comandos que requieren modo interactivo y agrega `-it` automáticamente:

**Comandos que siempre requieren interactivo:**
- `node-ui` - Interfaz gráfica siempre requiere TTY

**Comandos que requieren interactivo para ciertas operaciones:**
- `node-init` - Requiere interactivo (solicita moniker o seed phrase)
- `node-keys` - Requiere interactivo para `create`, `add`, `delete`, `reset-password`
- `node-logs` - Requiere interactivo cuando se usa `-f` o `--follow`

**Funcionalidad:**
- Verifica si `-it`, `-i`, o `--interactive` ya están presentes
- Si no están presentes, analiza los argumentos para determinar si se necesita modo interactivo
- Inserta `-it` después de `exec` si es necesario
- Preserva todos los demás argumentos

### 7. Visualización Automática de Logs

Si se ejecutó `up -d`, el script:
- Espera a que el contenedor esté ejecutándose
- Verifica que haya logs disponibles
- Muestra los logs en tiempo real con `logs -f`
- Maneja Ctrl+C elegantemente

## Análisis de Gestión de Permisos

### ¿Está funcionando correctamente?

**Sí, en la mayoría de casos:**

1. **Caso ideal (UID 1000):** Si el usuario del host es UID 1000, no hay problemas
2. **Caso con permisos de escritura:** Si el usuario puede escribir, `chmod 775/777` permite que UID 1000 escriba
3. **Caso con sudo:** Si se usa `sudo`, `chown 1000:1000` cambia la propiedad correctamente

**No, en casos edge:**

1. **Usuario sin permisos y sin sudo:** El script no puede configurar permisos
2. **Permisos 777:** Aunque funciona, es menos seguro
3. **Fallo silencioso:** Los `|| true` pueden ocultar problemas

### Mejoras Potenciales

1. **Verificación post-configuración:** Verificar que los permisos se aplicaron correctamente
2. **Mensajes de advertencia:** Informar al usuario si no se pudieron configurar permisos
3. **Fallback más robusto:** Intentar más estrategias antes de fallar silenciosamente

## Flujo de Ejecución

```
1. Validar entorno (docker-compose disponible, docker-compose.yml existe)
   ↓
2. Configurar permisos de persistent-data
   ├─ Si existe: intentar chmod/chown
   └─ Si no existe: crear con permisos correctos
   ↓
3. Detectar tipo de comando
   ├─ Si es 'up -d': activar visualización de logs
   └─ Otros: ejecutar normalmente
   ↓
4. Ejecutar docker-compose con argumentos
   ↓
5. Si fue 'up -d': mostrar logs automáticamente
```

## Ver También

- [Estructura de Docker Compose]({{< relref "docker-compose-structure" >}}) - Cómo se configura el contenedor
- [Gestión de Permisos]({{< relref "permission-handling" >}}) - Documentación técnica completa sobre permisos
- [Gestión de Contenedores]({{< relref "../../guides/general/container-management" >}}) - Guía de uso del script

