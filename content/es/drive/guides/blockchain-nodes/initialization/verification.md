---
title: "Verificación Post-Inicialización"
weight: 52233
---

Guía para verificar que la inicialización del nodo se completó correctamente y que todos los componentes necesarios fueron creados.

## ¿Por Qué Verificar?

Después de inicializar un nodo, es importante verificar que:

- Todos los archivos de configuración se crearon correctamente
- La [Private Validator Key]({{< relref "../../../../../concepts/private-validator-key" >}}) se generó correctamente
- El [archivo génesis]({{< relref "../../../../../concepts/genesis-file" >}}) se descargó correctamente
- El Chain ID está configurado correctamente

Esta verificación te da confianza de que el nodo está listo para iniciar y sincronizar con la blockchain.

## Verificar Archivos de Configuración

Los archivos de configuración deben estar en la carpeta `persistent-data/config/`:

```bash
# Verifica que los archivos de configuración existen
ls -la persistent-data/config/

# Archivos esperados:
# - config.toml
# - app.toml
# - client.toml
# - genesis.json
# - priv_validator_key.json
```

**Ubicación esperada:**
- **Ruta en el host:** `./persistent-data/config/` (relativa al directorio del servicio)
- **Ruta en el contenedor:** `/home/ubuntu/.infinited/config/`

### Verificar Contenido de Archivos de Configuración (Opcional)

Puedes revisar el contenido de los archivos de configuración para verificar que están correctos:

```bash
# Verifica el Chain ID en config.toml
cat persistent-data/config/config.toml | grep chain_id

# Verifica la configuración de la aplicación
cat persistent-data/config/app.toml | head -20
```

## Verificar Private Validator Key

El archivo `priv_validator_key.json` es crítico para el funcionamiento del nodo, especialmente para validadores.

```bash
# Verifica que el archivo existe
ls -la persistent-data/config/priv_validator_key.json

# Revisa el contenido (opcional, para verificar)
cat persistent-data/config/priv_validator_key.json
```

> [!IMPORTANT]
> **El Archivo Siempre se Crea**
>
> Cuando inicializas un nodo, **siempre se crea el archivo `priv_validator_key.json`**, sin importar el método de inicialización que uses (simple o recovery). La diferencia está en el **contenido** del archivo:
>
> - **Inicialización simple:** El contenido es aleatorio y diferente cada vez que inicializas
> - **Inicialización con recovery:** El contenido es siempre el mismo si usas la misma frase semilla

### Verificación Especial para Recovery Mode

Si usaste [inicialización con recovery]({{< relref "recovery-initialization" >}}), es especialmente importante verificar que puedes recuperar la misma clave usando tu frase semilla.

#### Práctica de Verificación: Reinicializar el Nodo

Esta práctica te permite verificar que siempre puedes recuperar exactamente la misma Private Validator Key usando tu frase semilla.

> [!IMPORTANT]
> **Diferencia entre Contenedor y Nodo**
>
> Es importante entender la diferencia:
> - **Contenedor:** Es el entorno Docker donde vive el nodo
> - **Nodo:** Es el proceso blockchain que corre dentro del contenedor
>
> Para esta práctica, necesitas **detener el nodo** (no el contenedor) y luego **eliminar los datos del nodo** antes de reinicializar.

**Procedimiento:**

1. **Anota o guarda el contenido de tu Private Validator Key:**
   ```bash
   cat persistent-data/config/priv_validator_key.json > mi-validator-key-backup.json
   ```

2. **Detén el nodo y elimina los datos:**
   - Consulta [Iniciar/Detener Nodo]({{< relref "../start-stop-node" >}}) para instrucciones sobre cómo detener el nodo y limpiar los datos del nodo usando la interfaz gráfica.

3. **Reinicializa el nodo con la misma frase semilla:**
   - Sigue el procedimiento completo de [Inicialización con Recovery]({{< relref "recovery-initialization" >}}) usando exactamente la misma frase semilla que usaste antes.

4. **Verifica que se generó exactamente la misma clave:**
   ```bash
   diff persistent-data/config/priv_validator_key.json mi-validator-key-backup.json
   ```

**Resultado esperado:** Debe ser exactamente la misma clave. Si es diferente, algo salió mal en el proceso.

**Beneficios de esta práctica:**
- ✅ Te da confianza de que siempre podrás restaurar tu validador
- ✅ Te ayuda a familiarizarte con el proceso
- ✅ Te permite detectar problemas antes de crear el validador en la blockchain
- ✅ Crea expertise en la gestión de claves

> [!NOTE]
> **Repetir el Procedimiento**
>
> Puedes repetir este procedimiento de verificación 2-3 veces para asegurarte de que siempre obtienes el mismo resultado. Esto te ayudará a estar tranquilo de que si realizas el procedimiento adecuadamente, siempre podrás respaldar o restaurar tu nodo validador cuantas veces sea necesario.

## Verificar Archivo Génesis

El archivo génesis es necesario para que el nodo pueda sincronizar con la blockchain:

```bash
# Verifica que el archivo génesis existe
ls -la persistent-data/config/genesis.json

# Verifica el Chain ID (opcional)
cat persistent-data/config/genesis.json | grep chain_id
```

El archivo génesis debe:
- Existir en la ubicación esperada
- Contener el Chain ID correcto para tu red
- Tener un tamaño razonable (depende de la red)

## Verificar Chain ID

El Chain ID debe ser consistente entre todos los archivos:

```bash
# Verifica el Chain ID en config.toml
cat persistent-data/config/config.toml | grep chain_id

# Verifica el Chain ID en genesis.json
cat persistent-data/config/genesis.json | grep chain_id
```

Ambos deben mostrar el mismo Chain ID, que debe corresponder a la red que estás usando (mainnet, testnet, etc.).

## Checklist de Verificación

Usa este checklist para asegurarte de que todo está correcto:

- [ ] Archivo `config.toml` existe
- [ ] Archivo `app.toml` existe
- [ ] Archivo `client.toml` existe
- [ ] Archivo `genesis.json` existe
- [ ] Archivo `priv_validator_key.json` existe
- [ ] Chain ID es correcto en `config.toml`
- [ ] Chain ID es correcto en `genesis.json`
- [ ] Chain ID coincide entre ambos archivos
- [ ] (Si usaste recovery) Private Validator Key tiene el contenido esperado

## Problemas Comunes

### Archivos Faltantes

Si algún archivo no existe:

1. Verifica que estás en el directorio correcto del servicio
2. Verifica que la inicialización se completó sin errores
3. Revisa los logs del contenedor para ver si hubo errores

### Chain ID Incorrecto

Si el Chain ID no es correcto:

1. Verifica la configuración del servicio en `docker-compose.yml`
2. Verifica las variables de entorno del servicio
3. Consulta la documentación de tu red para el Chain ID correcto

### Private Validator Key Diferente (Recovery Mode)

Si usaste recovery mode y la clave es diferente:

1. Verifica que ingresaste exactamente la misma frase semilla
2. Verifica que no hay espacios extra o errores de tipeo
3. Considera reinicializar con la frase semilla correcta

## Próximos Pasos

Después de verificar que la inicialización fue exitosa:

1. **[Iniciar/Detener Nodo]({{< relref "../start-stop-node" >}})** - Inicia tu nodo para comenzar a sincronizar
2. **[Interfaz Gráfica]({{< relref "../graphical-interface" >}})** - Usa la interfaz gráfica para monitorear tu nodo
3. **[Gestión de Claves]({{< relref "../keys" >}})** - Si eres validador, gestiona tus claves adicionales

## Ver También

- [Inicialización Simple]({{< relref "simple-initialization" >}}) - Procedimiento de inicialización simple
- [Inicialización con Recovery]({{< relref "recovery-initialization" >}}) - Procedimiento de inicialización con recovery
- [Inicialización de Nodo]({{< relref "." >}}) - Comparación de modos y cuándo usar cada uno
- [Private Validator Key]({{< relref "../../../../../concepts/private-validator-key" >}}) - Qué es el Private Validator Key
- [Archivo Génesis]({{< relref "../../../../../concepts/genesis-file" >}}) - Qué es el archivo génesis

