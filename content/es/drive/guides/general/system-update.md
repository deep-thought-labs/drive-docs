---
title: "Actualización del Sistema"
weight: 5212
---

Cómo actualizar el sistema Drive y las imágenes Docker.

Esta guía explica cómo actualizar tu sistema Drive, que consiste en múltiples contenedores Docker Compose que pueden estar en ejecución. El proceso de actualización asegura que obtengas los últimos cambios de código e imágenes Docker mientras evitas conflictos.

## Resumen del Proceso de Actualización

El proceso de actualización consiste en cuatro pasos principales:

1. **Detener todos los contenedores** - Detener todos los servicios Docker Compose en ejecución
2. **Actualizar el repositorio Git** - Restaurar y descargar los últimos cambios del repositorio
3. **Actualizar las imágenes Docker** - Descargar las últimas imágenes Docker utilizadas por los contenedores
4. **Reiniciar los contenedores** - Iniciar los servicios que desees utilizar

## Paso 1: Detener Todos los Contenedores

Antes de actualizar, necesitas detener y eliminar todos los contenedores en ejecución para evitar conflictos y asegurar una actualización limpia. Usar `down` elimina los contenedores, lo cual es necesario para actualizarlos correctamente.

Navega a cada directorio de servicio y deténlo:

```bash
# Detener y eliminar cada servicio individualmente
cd services/node0-infinite
./drive.sh down

cd ../node1-infinite-testnet
./drive.sh down

cd ../node2-infinite-creative
./drive.sh down

cd ../node3-qom
./drive.sh down
```

**Alternativa:** Detener todos los servicios a la vez usando un bucle:

```bash
# Desde el directorio raíz de drive
for service in services/node*/; do
    cd "$service"
    ./drive.sh down
    cd ../..
done
```

> [!NOTE]
> **¿Por qué usar `down` en lugar de `stop`?**
>
> El comando `down` detiene y elimina los contenedores, lo cual es necesario para actualizarlos correctamente. Esto asegura que cuando reinicies los servicios, usarán la configuración e imágenes actualizadas.

## Paso 2: Actualizar el Repositorio Git

Una vez que todos los contenedores estén detenidos, actualiza el repositorio Git para obtener los últimos cambios de código.

### Restaurar el Estado del Repositorio

Primero, restaura el repositorio para evitar conflictos con cambios locales:

```bash
# Navega al directorio raíz de drive
cd /ruta/a/drive  # Reemplaza con la ruta real de tu directorio drive

# Restaurar todos los archivos para que coincidan con el repositorio remoto
git restore .
```

Este comando descarta cualquier cambio local y asegura que tu repositorio coincida con el estado remoto, previniendo conflictos durante la actualización.

### Descargar los Últimos Cambios

Después de restaurar, descarga los últimos cambios del repositorio:

```bash
# Descargar los últimos cambios
git pull
```

**Alternativa:** Si prefieres especificar la rama explícitamente:

```bash
# Obtener los últimos cambios
git fetch origin

# Obtener el nombre de la rama actual
CURRENT_BRANCH=$(git branch --show-current)

# Restaurar y resetear para coincidir con el remoto
git restore .
git reset --hard origin/$CURRENT_BRANCH

# Descargar los últimos cambios
git pull
```

> [!IMPORTANT]
> **Seguridad de los Datos Persistentes**
>
> El comando `git restore` solo afecta los archivos rastreados por Git en el repositorio. Tus datos persistentes (datos del nodo, estado de blockchain, claves, etc.) almacenados en directorios `persistent-data/` **NO se ven afectados** y permanecerán intactos.

## Paso 3: Actualizar las Imágenes Docker

Después de actualizar el repositorio, actualiza las imágenes Docker utilizadas por tus contenedores.

Navega a **cualquier directorio de servicio** y descarga la última imagen:

```bash
# Navega a cualquier directorio de servicio
cd services/node0-infinite

# Descargar la última imagen Docker
docker compose pull
```

**Importante:** Solo necesitas ejecutar este comando **una vez desde cualquier directorio de servicio**. Todos los servicios comparten la misma imagen Docker, por lo que una vez que la actualices, todos los servicios usarán la imagen actualizada cuando los reinicies.

**Qué hace esto:**
- Descarga/actualiza la imagen Docker especificada en tu archivo `docker-compose.yml`
- La versión de la imagen depende de tu configuración (revisa `docker-compose.yml` para ver qué versión estás usando)
- Las imágenes Docker se comparten a nivel del sistema, por lo que actualizarla una vez la actualiza para todos los servicios

**Verificar que la imagen se actualizó:**

```bash
# Verificar detalles de la imagen
docker images | grep "deepthoughtlabs/infinite-drive"
```

> [!NOTE]
> **Versión de la Imagen**
>
> La versión de la imagen que estás usando está especificada en el archivo `docker-compose.yml` de cada servicio bajo el campo `image:`. Asegúrate de estar descargando la versión correcta para tu entorno.

## Paso 4: Reiniciar los Contenedores

Después de actualizar tanto el repositorio como las imágenes Docker, puedes reiniciar los contenedores que desees usar. No necesitas reiniciar todos—solo los que decidas usar.

### Reiniciar Servicios Individuales

```bash
# Reiniciar cada servicio que quieras usar
cd services/node0-infinite
./drive.sh up -d

cd ../node1-infinite-testnet
./drive.sh up -d

# Continuar con otros servicios según sea necesario
```

### Reiniciar Todos los Servicios

Si quieres reiniciar todos los servicios a la vez:

```bash
# Desde el directorio raíz de drive
for service in services/node*/; do
    cd "$service"
    ./drive.sh up -d
    cd ../..
done
```

## Ejemplo Completo de Actualización

Aquí tienes un ejemplo completo del proceso de actualización:

```bash
# Paso 1: Detener y eliminar todos los contenedores
for service in services/node*/; do
    cd "$service"
    ./drive.sh down
    cd ../..
done

# Paso 2: Actualizar el repositorio Git (desde la raíz de drive)
cd /ruta/a/drive
git restore .
git pull

# Paso 3: Actualizar las imágenes Docker (desde cualquier directorio de servicio - solo una vez necesario)
cd services/node0-infinite
docker compose pull

# Paso 4: Reiniciar los contenedores que quieras usar
cd ../node0-infinite
./drive.sh up -d

# Solo reinicia los servicios que necesites
# cd ../node1-infinite-testnet
# ./drive.sh up -d
```

## Lista de Verificación de Actualización

Usa esta lista de verificación para asegurar una actualización completa:

- [ ] Detener y eliminar todos los servicios en ejecución (`./drive.sh down` en cada servicio)
- [ ] Navegar al directorio raíz de drive
- [ ] Restaurar el estado del repositorio (`git restore .`)
- [ ] Descargar los últimos cambios de Git (`git pull`)
- [ ] Navegar a cualquier directorio de servicio
- [ ] Descargar la última imagen Docker (`docker compose pull`) - solo una vez necesario
- [ ] Reiniciar los servicios que quieras usar (`./drive.sh up -d`)
- [ ] Verificar que los servicios estén ejecutándose (`./drive.sh ps`)

## Solución de Problemas

Para problemas relacionados con la actualización del sistema, consulta la sección [Solución de Problemas]({{< relref "../../troubleshooting" >}}), que cubre:

- Problemas comunes y soluciones
- Diagnóstico de red
- Problemas de inicio/detención del nodo
- Problemas de permisos
- Problemas de gestión de claves
- Problemas de logs del nodo

## Ver También

- [Gestión de Contenedores]({{< relref "container-management" >}}) - Comandos generales de gestión de contenedores
- [Iniciar/Detener Nodo]({{< relref "../blockchain-nodes/start-stop-node" >}}) - Operaciones específicas de inicio/detención del nodo
