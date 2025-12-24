---
title: "Gestión de Contenedores"
weight: 5211
---

Aprende a gestionar contenedores de Drive usando el script `drive.sh`. Todos los servicios de Drive usan este script para operaciones de gestión.

## Ubicación del Script

Cada servicio tiene su propio script `drive.sh` en su directorio:

```bash
cd services/<service-name>
./drive.sh <comando>
```

## Comandos Disponibles

### 🚀 Iniciar Servicio

Inicia el servicio en modo daemon (en segundo plano):

```bash
./drive.sh up -d
```

Este comando crea e inicia el contenedor Docker del servicio.

### 📊 Mostrar Estado del Contenedor

Verifica el estado actual del contenedor:

```bash
./drive.sh ps
```

Muestra información sobre el contenedor: si está ejecutándose, cuándo se inició, etc.

### ⏹️ Detener Servicio

Detiene el servicio de forma controlada:

```bash
./drive.sh stop
```

El contenedor se detiene pero no se elimina, por lo que puedes reiniciarlo más tarde.

### 🗑️ Detener y Eliminar Contenedor

Detiene el servicio y elimina el contenedor:

```bash
./drive.sh down
```

**Nota:** Esto elimina el contenedor pero **no** elimina los datos persistentes almacenados en `persistent-data/`.

### ▶️ Iniciar Servicio (si está detenido)

Si el servicio está detenido pero el contenedor aún existe, puedes iniciarlo:

```bash
./drive.sh start
```

### 🔄 Reiniciar Servicio

Reinicia un servicio que ya está ejecutándose:

```bash
./drive.sh restart
```

Útil cuando necesitas aplicar cambios de configuración o resolver problemas temporales.

### 📋 Ver Registros del Contenedor

Visualiza los logs del contenedor en tiempo real:

```bash
./drive.sh logs
```

Para ver los últimos logs y salir, presiona `Ctrl+C`.

### 💻 Acceder a la Shell del Contenedor

Abre una sesión de shell dentro del contenedor:

```bash
./drive.sh bash
```

Útil para depuración, inspección de archivos dentro del contenedor, o ejecutar comandos manuales.

## Características del Script

- **Manejo automático de permisos** - Funciona con o sin `sudo`
- **Interfaz consistente** - Los mismos comandos funcionan en todos los servicios
- **Gestión simplificada** - Abstrae la complejidad de Docker Compose
