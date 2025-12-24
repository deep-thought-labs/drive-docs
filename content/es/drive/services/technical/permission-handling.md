---
title: "Gestión de Permisos"
weight: 5363
---

> [!WARNING]
> **⚠️ Documentación en Construcción**
>
> Este documento está en construcción y contiene análisis técnico en desarrollo. Está siendo utilizado por los desarrolladores para identificar la mejor solución al problema de permisos entre el sistema host y los contenedores Docker.
>
> **No tomes este documento como una guía de uso aún.** Este es un análisis técnico que puede cambiar significativamente mientras se desarrolla la solución final.

Documentación técnica completa sobre cómo Drive maneja los permisos de archivos entre el sistema host y los contenedores Docker.

## El Problema Fundamental

Docker mapea permisos de archivos usando **UIDs/GIDs numéricos**, no nombres de usuario. Esto significa:

- El contenedor ejecuta como UID 1000 (usuario `ubuntu`)
- El sistema host puede tener un usuario diferente con un UID diferente
- Los bind mounts preservan los UIDs del sistema de archivos del host
- Si el UID del host no coincide con el UID del contenedor, habrá problemas de permisos

## Configuración Actual de Drive

### Usuario del Contenedor

- **Usuario:** `ubuntu`
- **UID:** 1000
- **GID:** 1000
- **Definición:** Establecido en el Dockerfile de la imagen, no en `docker-compose.yml`

### Estrategia de Permisos en drive.sh

El script `drive.sh` intenta resolver problemas de permisos de dos formas:

#### Estrategia 1: Permisos Amplios (sin sudo)

```bash
chmod -R 775 "persistent-data"  # O 777 si 775 falla
```

**Cómo funciona:**
- Permisos 775: `rwxrwxr-x` (propietario y grupo pueden escribir, otros solo leer)
- Permisos 777: `rwxrwxrwx` (todos pueden escribir)
- Permite que UID 1000 (contenedor) escriba incluso si el propietario es otro UID

**Ventajas:**
- No requiere sudo
- Funciona si el usuario tiene permisos de escritura en el directorio padre

**Desventajas:**
- Permisos 777 son menos seguros (cualquier usuario puede escribir)
- No cambia la propiedad, solo los permisos

#### Estrategia 2: Cambio de Propiedad (con sudo)

```bash
chown -R 1000:1000 "persistent-data"
```

**Cómo funciona:**
- Cambia la propiedad del directorio a UID 1000:GID 1000
- El contenedor (UID 1000) ahora es el propietario
- No necesita permisos amplios (puede usar 755 o 700)

**Ventajas:**
- Más seguro (no requiere permisos amplios)
- Solución permanente (la propiedad persiste)

**Desventajas:**
- Requiere sudo
- El usuario del host puede perder acceso directo si no es UID 1000

## Casos de Uso y Soluciones

### Caso 1: Usuario Host es UID 1000

**Situación:** El usuario del host tiene UID 1000 (ej: usuario `kvm` en InterServer)

**Comportamiento:**
- ✅ No hay problemas de permisos
- ✅ El contenedor puede escribir
- ✅ El usuario del host puede escribir
- ✅ No se requieren cambios de permisos

**Ejemplo:**
```bash
$ id -u
1000
# Todo funciona sin configuración adicional
```

### Caso 2: Usuario Host NO es UID 1000, pero tiene permisos de escritura

**Situación:** El usuario del host tiene un UID diferente pero puede escribir en el directorio

**Comportamiento del script:**
1. Detecta que puede escribir (`[ -w "persistent-data" ]`)
2. Aplica `chmod 775` o `777`
3. ✅ El contenedor (UID 1000) puede escribir gracias a permisos amplios

**Ejemplo:**
```bash
$ id -u
1001
$ ls -ld persistent-data
drwxrwxrwx  alberto alberto  persistent-data
# El contenedor puede escribir por permisos 777
```

### Caso 3: Usuario Host NO es UID 1000 y NO tiene permisos de escritura

**Situación:** El usuario no puede escribir y no tiene sudo

**Comportamiento del script:**
- ⚠️ No puede configurar permisos
- ⚠️ Los comandos `chmod`/`chown` fallan silenciosamente (`|| true`)
- ❌ El contenedor no podrá escribir
- ❌ Se producirán errores de permisos

**Solución manual requerida:**
```bash
# Opción 1: Usar sudo
sudo chown -R 1000:1000 persistent-data

# Opción 2: Cambiar a un usuario con UID 1000
su - usuario-con-uid-1000

# Opción 3: Configurar permisos manualmente
sudo chmod -R 775 persistent-data
```

### Caso 4: Usuario Host ejecuta con sudo

**Situación:** El script se ejecuta con `sudo ./drive.sh up -d`

**Comportamiento del script:**
1. Detecta `$SUDO_USER` (usuario que ejecutó sudo)
2. Aplica `chown -R 1000:1000` para cambiar propiedad
3. ✅ El contenedor (UID 1000) es ahora el propietario
4. ✅ Puede escribir sin problemas

**Ejemplo:**
```bash
$ sudo ./drive.sh up -d
# Script cambia propiedad a 1000:1000 automáticamente
# Contenedor puede escribir correctamente
```

## Análisis del Problema Reportado

### Escenario del Usuario

- **VPS Provider:** InterServer
- **Usuario por defecto:** `kvm` (UID 1000)
- **Usuario intentado:** `ubuntu` (UID diferente, no 1000)
- **Problema:** Contenedor no podía escribir en `persistent-data`

### ¿Por qué falló?

1. El usuario `ubuntu` no era UID 1000
2. El script `drive.sh` probablemente no pudo configurar permisos (sin sudo o sin permisos de escritura)
3. Docker creó archivos como UID 1001 (siguiente UID disponible)
4. Ni el host ni el contenedor podían escribir (deadlock de permisos)

### ¿Por qué funcionó con `kvm`?

- El usuario `kvm` es UID 1000
- Coincide con el UID del contenedor
- No se requieren cambios de permisos
- Todo funciona automáticamente

### ¿El script drive.sh está funcionando correctamente?

**Parcialmente:**

✅ **Funciona cuando:**
- Usuario es UID 1000
- Usuario tiene permisos de escritura y el script puede aplicar chmod
- Usuario ejecuta con sudo y el script puede aplicar chown

❌ **No funciona cuando:**
- Usuario no es UID 1000
- Usuario no tiene permisos de escritura
- Usuario no tiene sudo
- El script falla silenciosamente (`|| true` oculta errores)

## Mejoras Recomendadas

### 1. Verificación Post-Configuración

El script debería verificar que los permisos se aplicaron correctamente:

```bash
# Después de chmod/chown, verificar:
if [ -d "persistent-data" ]; then
    PERMS=$(stat -c "%a" persistent-data 2>/dev/null || stat -f "%OLp" persistent-data)
    OWNER=$(stat -c "%u" persistent-data 2>/dev/null || stat -f "%u" persistent-data)
    
    if [ "$OWNER" != "1000" ] && [ "$PERMS" != "775" ] && [ "$PERMS" != "777" ]; then
        echo "⚠️  Advertencia: No se pudieron configurar permisos correctamente"
        echo "   El contenedor (UID 1000) puede no poder escribir"
    fi
fi
```

### 2. Mensajes Informativos

El script debería informar al usuario sobre el estado de los permisos:

```bash
if [ "$OWNER" = "1000" ]; then
    echo "✅ Permisos configurados: persistent-data es propiedad de UID 1000"
elif [ "$PERMS" = "775" ] || [ "$PERMS" = "777" ]; then
    echo "✅ Permisos configurados: persistent-data tiene permisos amplios (775/777)"
else
    echo "⚠️  Advertencia: Permisos pueden no ser compatibles con el contenedor"
fi
```

### 3. Fallback más Robusto

Si `chmod` falla, intentar otras estrategias antes de continuar:

```bash
# Intentar múltiples estrategias
if ! chmod 775 persistent-data 2>/dev/null; then
    if ! chmod 777 persistent-data 2>/dev/null; then
        if [ -n "$SUDO_USER" ]; then
            if ! sudo chown 1000:1000 persistent-data 2>/dev/null; then
                echo "❌ Error: No se pudieron configurar permisos"
                exit 1
            fi
        else
            echo "⚠️  Advertencia: No se pudieron configurar permisos. Puede requerir sudo."
        fi
    fi
fi
```

## Resumen

### Estado Actual

- ✅ Funciona en la mayoría de casos comunes
- ⚠️ Tiene limitaciones en casos edge (usuario sin permisos y sin sudo)
- ⚠️ Falla silenciosamente en algunos casos (`|| true`)

### Recomendaciones

1. **Para usuarios:** Verificar UID antes de usar Drive (ver [Verificar Instalación]({{< relref "../../quick-start/managing-services" >}}))
2. **Para desarrollo:** Mejorar el script con verificaciones y mensajes más informativos
3. **Para documentación:** Explicar claramente los requisitos de permisos

## Ver También

- [Estructura de Docker Compose]({{< relref "docker-compose-structure" >}}) - Cómo se configura el contenedor
- [Análisis del Script drive.sh]({{< relref "drive-script-analysis" >}}) - Implementación actual del script
- [Verificar Instalación]({{< relref "../../quick-start/managing-services" >}}) - Cómo verificar permisos antes de usar Drive
- [Problemas Comunes]({{< relref "../../troubleshooting/common-issues" >}}) - Soluciones a problemas de permisos

