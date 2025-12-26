---
title: "Arquitectura del Contenedor"
weight: 406
---

El contenedor Docker de Drive está construido a partir de un Dockerfile que define la imagen base, instala dependencias, descarga el binario del nodo, y configura el entorno. Esta sección documenta la arquitectura completa del contenedor.

## Imagen Base

### Base Image

```dockerfile
FROM ubuntu:24.04
```

**Características:**
- Basado en Ubuntu 24.04 LTS
- Imagen mínima y ligera
- Soporte para múltiples arquitecturas (amd64, arm64)

## Instalación de Dependencias

### Dependencias del Sistema

```dockerfile
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    ca-certificates \
    tar \
    libc6 \
    libgcc-s1 \
    procps \
    net-tools \
    jq \
    dialog \
    bc \
    util-linux \
    && rm -rf /var/lib/apt/lists/*
```

**Propósito de cada dependencia:**

- **wget:** Descargar el binario del nodo desde GitHub
- **curl:** Hacer peticiones HTTP a la API de GitHub
- **ca-certificates:** Certificados SSL/TLS para conexiones seguras
- **tar:** Extraer el archivo comprimido del binario
- **libc6, libgcc-s1:** Bibliotecas C requeridas por el binario
- **procps:** Herramientas para gestión de procesos (`pgrep`, `ps`, etc.)
- **net-tools:** Herramientas de red (`netstat`, etc.)
- **jq:** Procesar JSON (para parsear respuestas de la API de GitHub)
- **dialog:** Interfaz gráfica de terminal (TUI) para `node-ui`
- **bc:** Calculadora para operaciones matemáticas
- **util-linux:** Utilidades del sistema (`setsid`, etc.)

**Optimización:**
- `rm -rf /var/lib/apt/lists/*` - Limpia la caché de apt para reducir el tamaño de la imagen

## Multi-Arquitectura

### Build Arguments

```dockerfile
ARG TARGETARCH
ARG TARGETPLATFORM
```

**Propósito:**
- `TARGETARCH`: Arquitectura objetivo (amd64, arm64)
- `TARGETPLATFORM`: Plataforma completa (linux/amd64, linux/arm64)

**Uso:**
- Automáticamente establecidos por Docker Buildx
- Permiten construir imágenes para múltiples arquitecturas
- Usados para seleccionar el binario correcto

## Descarga del Binario

### Proceso de Descarga

El Dockerfile descarga automáticamente la última versión del binario desde GitHub:

```dockerfile
# 1. Obtener última versión desde GitHub
LATEST_VERSION=$(curl -s https://api.github.com/repos/deep-thought-labs/infinite/releases/latest | jq -r '.tag_name')

# 2. Construir URL del binario basado en arquitectura
if [ "$TARGETARCH" = "arm64" ]; then
    FINAL_BINARY_URL="https://github.com/deep-thought-labs/infinite/releases/download/${LATEST_VERSION}/infinite_Linux_ARM64.tar.gz"
elif [ "$TARGETARCH" = "amd64" ]; then
    FINAL_BINARY_URL="https://github.com/deep-thought-labs/infinite/releases/download/${LATEST_VERSION}/infinite_Linux_x86_64.tar.gz"
fi

# 3. Descargar, extraer e instalar
wget --tries=3 --timeout=30 --progress=bar:force:noscroll \
    -O /tmp/infinite.tar.gz "$FINAL_BINARY_URL"
tar -xzf /tmp/infinite.tar.gz -C /tmp/extract
BINARY_PATH=$(find /tmp/extract -type f \( -name "infinited" -o -name "infinite" -o -name "infinite*" \) -executable 2>/dev/null | head -n 1)
mv "${BINARY_PATH}" /usr/local/bin/infinited
chmod +x /usr/local/bin/infinited
```

**Características:**
- Descarga automática de la última versión
- Soporte para múltiples arquitecturas
- Validación del archivo descargado
- Búsqueda automática del binario en el archivo extraído
- Instalación en `/usr/local/bin/infinited`

### Validaciones

El proceso incluye múltiples validaciones:

1. **Verificación de versión:**
   ```bash
   if [ -z "$LATEST_VERSION" ] || [ "$LATEST_VERSION" = "null" ]; then
       echo "Error: Could not fetch latest version from GitHub"
       exit 1
   fi
   ```

2. **Verificación de arquitectura:**
   ```bash
   if [ "$TARGETARCH" != "arm64" ] && [ "$TARGETARCH" != "amd64" ]; then
       echo "Error: Unsupported architecture: ${TARGETARCH}"
       exit 1
   fi
   ```

3. **Verificación de descarga:**
   ```bash
   test -f /tmp/infinite.tar.gz || (echo "Error: La descarga falló" && exit 1)
   test -s /tmp/infinite.tar.gz || (echo "Error: El archivo está vacío" && exit 1)
   ```

4. **Verificación de extracción:**
   ```bash
   tar -tzf /tmp/infinite.tar.gz > /dev/null 2>&1 || (echo "Error: No es un tar.gz válido" && exit 1)
   ```

5. **Verificación de binario:**
   ```bash
   if [ -z "${BINARY_PATH}" ]; then
       echo "Error: No se encontró el binario"
       exit 1
   fi
   ```

## Configuración de Directorios

### Creación de Directorios

```dockerfile
RUN mkdir -p /home/ubuntu/.infinited /var/log/node /home/ubuntu/.node && \
    chown -R 1000:1000 /home/ubuntu /var/log/node
```

**Directorios creados:**

1. **`/home/ubuntu/.infinited`** - Directorio home del nodo (configuración y datos)
2. **`/var/log/node`** - Directorio para logs del sistema
3. **`/home/ubuntu/.node`** - Directorio de control (PIDs, flags)

**Permisos:**
- Propietario: `ubuntu` (UID 1000)
- Grupo: `ubuntu` (GID 1000)
- Permisos: `755` (rwxr-xr-x)

## Instalación de Scripts

### Copia de Scripts

```dockerfile
COPY scripts/ /tmp/scripts/
RUN chmod +x /tmp/scripts/*.sh && \
    mv /tmp/scripts/styles.sh /usr/local/bin/styles.sh && \
    mv /tmp/scripts/node-config.sh /usr/local/bin/node-config.sh && \
    mv /tmp/scripts/node-init.sh /usr/local/bin/node-init && \
    mv /tmp/scripts/node-keys.sh /usr/local/bin/node-keys && \
    mv /tmp/scripts/node-start.sh /usr/local/bin/node-start && \
    mv /tmp/scripts/node-stop.sh /usr/local/bin/node-stop && \
    mv /tmp/scripts/node-logs.sh /usr/local/bin/node-logs && \
    mv /tmp/scripts/node-update-genesis.sh /usr/local/bin/node-update-genesis && \
    mv /tmp/scripts/node-network-diagnosis.sh /usr/local/bin/node-network-diagnosis && \
    mv /tmp/scripts/node-process-status.sh /usr/local/bin/node-process-status && \
    mv /tmp/scripts/node-help.sh /usr/local/bin/node-help && \
    mv /tmp/scripts/node-ui.sh /usr/local/bin/node-ui && \
    mv /tmp/scripts/node-supervisor.sh /usr/local/bin/node-supervisor && \
    mv /tmp/scripts/node-auto-start.sh /usr/local/bin/node-auto-start && \
    mv /tmp/scripts/node-validate-genesis.sh /usr/local/bin/node-validate-genesis && \
    mv /tmp/scripts/node-clean-data.sh /usr/local/bin/node-clean-data && \
    mv /tmp/scripts/container-info.sh /usr/local/bin/container-info.sh && \
    mv /tmp/scripts/dialog-theme.sh /usr/local/bin/dialog-theme.sh && \
    chown -R 1000:1000 /usr/local/bin/node-* /usr/local/bin/styles.sh /usr/local/bin/node-config.sh /usr/local/bin/container-info.sh /usr/local/bin/dialog-theme.sh && \
    rm -rf /tmp/scripts
```

**Proceso:**

1. **Copia:** Todos los scripts se copian a `/tmp/scripts/`
2. **Permisos:** Se hacen ejecutables con `chmod +x`
3. **Instalación:** Se mueven a `/usr/local/bin/` (sin extensión `.sh` para la mayoría)
4. **Propiedad:** Se cambia la propiedad a `ubuntu:ubuntu`
5. **Limpieza:** Se elimina el directorio temporal

**Scripts instalados:**

- Scripts de utilidad: `styles.sh`, `node-config.sh`, `container-info.sh`, `dialog-theme.sh`
- Scripts principales: `node-init`, `node-start`, `node-stop`, `node-logs`, `node-keys`
- Scripts de sistema: `node-supervisor`, `node-auto-start`
- Scripts de gestión: `node-clean-data`, `node-process-status`, `node-network-diagnosis`
- Scripts de UI: `node-ui`
- Scripts de ayuda: `node-help`, `node-update-genesis`, `node-validate-genesis`

## Configuración del Usuario

### Usuario por Defecto

```dockerfile
USER 1000:1000
```

**Características:**
- Usuario: `ubuntu` (UID 1000)
- Grupo: `ubuntu` (GID 1000)
- Todos los procesos se ejecutan como este usuario
- Evita problemas de permisos con volúmenes montados

### Directorio de Trabajo

```dockerfile
WORKDIR /home/ubuntu
```

**Propósito:**
- Establece el directorio de trabajo por defecto
- Los comandos se ejecutan desde este directorio
- Facilita el uso de rutas relativas

## Entrypoint y CMD

### Comando de Inicio

```dockerfile
CMD ["/bin/bash", "-c", "/usr/local/bin/node-auto-start > /dev/null 2>&1; sleep infinity"]
```

**Explicación:**

1. **`/usr/local/bin/node-auto-start`** - Ejecuta el script de auto-start
   - Verifica si el nodo debe iniciarse automáticamente
   - Inicia el nodo si el flag de auto-start existe
   - Redirige salida a `/dev/null` para evitar ruido en logs del contenedor

2. **`sleep infinity`** - Mantiene el contenedor corriendo
   - El contenedor debe permanecer activo para que el nodo funcione
   - `sleep infinity` es un proceso que nunca termina
   - Permite que el contenedor siga ejecutándose indefinidamente

**Flujo completo:**

```
Contenedor inicia
    ↓
Ejecuta node-auto-start
    ↓
¿Flag auto-start existe?
    ├─ Sí → Inicia nodo
    └─ No → No hace nada
    ↓
sleep infinity (mantiene contenedor vivo)
```

## Estructura Final del Contenedor

### Sistema de Archivos

```
/
├── usr/
│   └── local/
│       └── bin/
│           ├── infinited              # Binario del nodo
│           ├── node-init              # Scripts de gestión
│           ├── node-start
│           ├── node-stop
│           ├── node-logs
│           ├── node-keys
│           ├── node-supervisor
│           ├── node-auto-start
│           ├── node-config.sh          # Configuración
│           ├── styles.sh               # Estilos
│           └── ...                     # Otros scripts
│
├── home/
│   └── ubuntu/
│       ├── .infinited/                 # Datos del nodo
│       └── .node/                      # Control del nodo
│
└── var/
    └── log/
        └── node/                       # Logs del sistema
```

## Variables de Entorno

Las variables de entorno se pueden pasar al contenedor mediante:

1. **`docker-compose.yml`:**
   ```yaml
   environment:
     - NODE_CHAIN_ID=infinite_421018-1
     - NODE_P2P_SEEDS=...
   ```

2. **Archivo `.env`:**
   ```
   NODE_CHAIN_ID=infinite_421018-1
   ```

3. **Línea de comando:**
   ```bash
   docker compose run -e NODE_CHAIN_ID=test infinite-drive node-start
   ```

## Volúmenes Persistentes

Los directorios de datos se mapean a volúmenes persistentes:

```yaml
volumes:
  - ./persistent-data/.infinited:/home/ubuntu/.infinited
  - ./persistent-data/.node:/home/ubuntu/.node
  - ./persistent-data/logs:/var/log/node
```

**Ventajas:**
- Los datos persisten entre reinicios del contenedor
- Accesibles desde el host
- No se pierden al recrear el contenedor

## Optimizaciones

### Reducción de Tamaño

1. **Limpieza de apt cache:** `rm -rf /var/lib/apt/lists/*`
2. **Eliminación de archivos temporales:** `rm -rf /tmp/scripts`
3. **Uso de imagen base mínima:** Ubuntu sin paquetes innecesarios

### Multi-Stage Build

Aunque no se usa actualmente, se podría implementar un multi-stage build para reducir aún más el tamaño de la imagen final.

## Ver También

- [Estructura Interna de Directorios]({{< relref "directory-structure" >}}) - Dónde se almacenan los datos
- [Sistema de Configuración Interna]({{< relref "configuration-system" >}}) - Cómo se configura el contenedor
- [Scripts Internos del Contenedor]({{< relref "internal-scripts" >}}) - Qué scripts se instalan

