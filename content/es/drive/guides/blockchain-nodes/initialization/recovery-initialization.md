---
title: "Inicialización con Recovery"
weight: 52232
---

Guía paso a paso para inicializar un nodo blockchain usando el modo recovery. Este modo es **requerido para [nodos validadores]({{< relref "../keys/understanding-keys" >}})** y altamente recomendado para cualquier nodo que necesite recuperar su identidad.

## ¿Qué es la Inicialización con Recovery?

La inicialización con recovery usa una frase semilla para generar **siempre la misma** [Private Validator Key]({{< relref "../../../../../concepts/private-validator-key" >}}), permitiéndote recuperarla en cualquier momento.

**Características:**
- ✅ **Recuperable** - Siempre puedes regenerar la misma clave con la frase semilla
- ✅ **Consistente** - La misma semilla siempre genera la misma clave
- ✅ **Portable** - Puedes restaurar tu validador en cualquier servidor
- ✅ **Requerido para validadores** - Te permite recuperar tu validador si algo falla

## Requisitos Previos

Antes de inicializar con recovery, necesitas:

- **Una frase semilla (12 o 24 palabras)** - Puedes crear una usando [Gestión de Claves]({{< relref "../keys" >}})
- **Respaldo seguro de la frase semilla** - Asegúrate de tenerla respaldada antes de continuar

Para más información sobre cómo crear y respaldar una frase semilla, consulta:
- [Operaciones de Gestión de Claves]({{< relref "../keys/operations" >}}) - Cómo generar claves y obtener tu frase semilla
- [Mejores Prácticas de Seguridad]({{< relref "../keys/security" >}}) - Cómo respaldar tu frase semilla de forma segura

## Usando Interfaz Gráfica

1. Abre la interfaz gráfica (ver [Interfaz Gráfica]({{< relref "../graphical-interface" >}}))

2. Navega: Menú Principal → **"Node Operations"** → **"Advanced Operations"** → **"Initialize with Recovery (Validator)"**

   ![Initialize with Recovery seleccionada](/images/node-ui-advanced-operations-op2-init-revery.png)

3. Cuando se solicite, ingresa tu frase semilla (12 o 24 palabras)

4. Sigue las instrucciones en pantalla para completar la inicialización

## Usando Línea de Comandos

```bash
./drive.sh exec -it infinite node-init --recover
```

**Nota:** Usa `-it` (interactive) para poder ingresar la frase semilla.

> [!NOTE]
> **Qué Hace el Comando**
>
> El comando solicita tu frase semilla, genera siempre la misma [Private Validator Key]({{< relref "../../../../../concepts/private-validator-key" >}}) usando tu frase semilla, crea los archivos de configuración, y descarga el [archivo génesis]({{< relref "../../../../../concepts/genesis-file" >}}) oficial. Para detalles técnicos del proceso, consulta [Flujo de Inicialización Técnico]({{< relref "../../../internal-workings/initialization-flow" >}}).

### Salida Esperada

Después de ejecutar el comando, deberías ver:

```
Enter your bip39 mnemonic
```

Ingresa tu frase semilla (12 o 24 palabras) cuando se solicite.

Después de ingresar la frase semilla correctamente:

```
✅ Node initialized successfully!
```

> [!NOTE]
> **Archivos Creados**
>
> Los archivos de configuración se crean en `./persistent-data/config/` (host) o `/home/ubuntu/.infinited/config/` (contenedor). Para más detalles sobre la estructura de datos, consulta [Data del Nodo]({{< relref "../../../../../concepts/node-data" >}}). (contenido determinístico basado en tu frase semilla)

## Ventajas para Validadores

Si inicializas con recovery usando una frase semilla, puedes restaurar tu validador en cualquier momento, en cualquier servidor, simplemente usando la misma frase semilla. Esto te permite:

- **Mover tu validador a otro servidor** - Simplemente inicializa con la misma frase semilla en el nuevo servidor
- **Restaurar tu validador después de un fallo del sistema** - No pierdes tu validador si el servidor falla
- **Tener la certeza de recuperación** - Siempre tendrás acceso a tu validador mientras tengas tu frase semilla

> [!NOTE]
> **Workflow para Validadores**
>
> Si estás siguiendo el workflow completo para validadores, después de inicializar con recovery, continúa con los siguientes pasos del workflow:
> - Agregar la clave al keyring (si usaste Dry-Run)
> - Verificar la Private Validator Key
> - Crear el validador en la blockchain
>
> Consulta [Workflow para Validadores]({{< relref "../keys/validator-workflow" >}}) para el flujo completo paso a paso.

## Verificación

Después de inicializar, verifica que todo se creó correctamente. Consulta [Verificación Post-Inicialización]({{< relref "verification" >}}) para más detalles.

**Importante:** Para validadores, es especialmente importante verificar que la Private Validator Key se generó correctamente y que puedes recuperarla usando la misma frase semilla.

## Solución de Problemas

### Error: "Invalid mnemonic"

Si recibes este error al usar recovery mode:

- **Verifica que ingresaste exactamente la misma frase semilla** (12 o 24 palabras)
- **Asegúrate de no tener espacios extra** al inicio o final
- **Verifica que todas las palabras estén escritas correctamente**
- **Asegúrate de usar el formato BIP39 estándar**

### Error: "Node already initialized"

Si recibes este error, significa que el nodo ya fue inicializado previamente. Para reinicializar:

1. **Detén el nodo** (si está ejecutándose)
2. **Elimina la data del nodo** usando la interfaz gráfica o comandos
3. **Vuelve a inicializar** con el método que prefieras

Para más detalles sobre cómo eliminar los datos del nodo, consulta [Borrar Data del Nodo]({{< relref "../delete-node-data" >}}).

### No Puedo Encontrar mis Archivos de Configuración

Los archivos de configuración se almacenan en:

- **Ruta en el host:** `./persistent-data/config/` (relativa al directorio del servicio)
- **Ruta en el contenedor:** `/home/ubuntu/.infinited/config/`

Asegúrate de estar en el directorio correcto del servicio cuando busques estos archivos.

## Próximos Pasos

Después de inicializar tu nodo:

1. **[Verificación Post-Inicialización]({{< relref "verification" >}})** - Verifica que todo se creó correctamente
2. **[Iniciar/Detener Nodo]({{< relref "../start-stop-node" >}})** - Aprende a iniciar y detener tu nodo
3. **[Interfaz Gráfica]({{< relref "../graphical-interface" >}})** - Usa la interfaz gráfica para gestionar tu nodo

> [!NOTE]
> **Si eres Validador**
>
> Si estás configurando un validador, después de inicializar con recovery, consulta [Workflow para Validadores]({{< relref "../keys/validator-workflow" >}}) para los pasos adicionales necesarios (agregar clave al keyring, verificar Private Validator Key, crear el validador en la blockchain).

## Ver También

- [Inicialización Simple]({{< relref "simple-initialization" >}}) - Si no necesitas recuperabilidad (solo full nodes)
- [Verificación Post-Inicialización]({{< relref "verification" >}}) - Verifica que la inicialización fue exitosa
- [Inicialización de Nodo]({{< relref "." >}}) - Comparación de modos y cuándo usar cada uno
- [Gestión de Claves]({{< relref "../keys" >}}) - Guía completa para gestionar claves criptográficas
- [Private Validator Key]({{< relref "../../../../../concepts/private-validator-key" >}}) - Qué es el Private Validator Key

