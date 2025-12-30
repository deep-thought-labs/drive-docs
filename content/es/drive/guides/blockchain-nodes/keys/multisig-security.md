---
title: "Seguridad Multifirma"
weight: 52226
---

Mejores prácticas de seguridad específicas para wallets multifirma.

> [!NOTE]
> **Conceptos Fundamentales**
>
> Antes de continuar, asegúrate de entender:
> - [Wallet Multifirma]({{< relref "../../../../../concepts/multisig-wallet" >}}) - Qué es una wallet multifirma
> - [Firmante Multifirma]({{< relref "../../../../../concepts/multisig-signer" >}}) - Qué es un firmante
> - [Mejores Prácticas de Seguridad]({{< relref "security" >}}) - Seguridad general de claves

## Distribución Segura de Claves Públicas

Cuando creas una wallet multifirma, solo se comparten claves públicas, pero aún así debes hacerlo de forma segura.

### Recomendaciones

1. **Canales encriptados** - Usa comunicación encriptada para compartir claves públicas:
   - Email encriptado (PGP)
   - Signal o Telegram con encriptación
   - Canales privados seguros
   - Nunca uses email plano o mensajería sin encriptar

2. **Verificación** - Cada participante debe verificar que recibió la clave pública correcta:
   - Comparar con la clave pública que exportaron
   - Verificar que la dirección de la wallet multifirma coincide

3. **Transparencia** - Todos los participantes deben poder ver todas las claves públicas que forman parte de la wallet

4. **Verificación múltiple** - Verifica las claves públicas a través de múltiples canales o fuentes:
   - Recibe la clave pública directamente del participante
   - Verifica que la dirección de la wallet multifirma coincide cuando todos la recrean
   - Compara las claves públicas recibidas con las que cada participante exportó
   - No confíes solo en un intermediario o un solo canal de comunicación

### ⚠️ NUNCA

- Compartas claves privadas o frases semilla
- Compartas archivos del keyring
- Uses canales de comunicación no encriptados
- Confíes en una sola fuente o intermediario para recibir las claves públicas sin verificación

## Gestión de Firmantes

### Selección de Firmantes

1. **Independencia** - Cada firmante debe ser independiente y no controlado por otros
2. **Distribución geográfica** - Idealmente, los firmantes están en ubicaciones diferentes
3. **Confiabilidad** - Los firmantes deben ser personas o entidades confiables
4. **Disponibilidad** - Los firmantes deben estar disponibles cuando se necesiten firmas

### Agregar Firmantes

Para agregar un nuevo firmante:

1. **Verificar identidad** - Asegúrate de que el nuevo firmante es quien dice ser
2. **Obtener clave pública** - Recibe la clave pública del nuevo firmante de forma segura
3. **Recrear wallet** - Crea una nueva wallet multifirma con el nuevo conjunto de firmantes
4. **Migrar fondos** - Transfiere los fondos de la wallet antigua a la nueva
5. **Actualizar configuración** - Todos los participantes actualizan su configuración local

### Remover Firmantes

Para remover un firmante:

1. **Recrear wallet** - Crea una nueva wallet multifirma sin la clave del firmante a remover
2. **Migrar fondos** - Transfiere los fondos de la wallet antigua a la nueva
3. **Actualizar configuración** - Todos los participantes actualizan su configuración local

> [!WARNING]
> **Agregar o Remover Firmantes Crea una Nueva Wallet**
>
> ⚠️ **IMPORTANTE:** Agregar o remover firmantes **NO modifica** la wallet existente. En su lugar, se crea una **nueva wallet multifirma con una nueva dirección pública**.
>
> **Consecuencias:**
> - La dirección de la wallet antigua permanece inalterada
> - La nueva wallet tiene una dirección completamente diferente
> - Debes migrar todos los fondos de la wallet antigua a la nueva
> - Cualquier referencia a la dirección antigua (contratos, configuraciones, etc.) debe actualizarse
>
> **No es posible modificar firmantes de una wallet existente sin cambiar su dirección.**

## Protección Contra Compromiso Parcial

Una de las ventajas de las wallets multifirma es que un compromiso de una sola clave no permite robar fondos. Sin embargo, debes proteger contra compromisos parciales:

### Recomendaciones

1. **Umbral adecuado** - Usa un umbral que requiera más de una firma (M > 1)
2. **Distribución de claves** - No almacenes todas las claves en el mismo lugar
3. **Monitoreo** - Monitorea las transacciones para detectar actividad sospechosa
4. **Rotación** - Considera rotar firmantes periódicamente

### Protección de Cada Firmante

Cada firmante debe seguir las [mejores prácticas de seguridad]({{< relref "security" >}}):

- **Respaldar frase semilla** - Guardarla de forma segura y fuera de línea
- **Usar almacenamiento seguro** - Considerar hardware wallets o almacenamiento encriptado
- **No compartir nunca** - Nunca compartir la clave privada o frase semilla
- **Usar canales seguros** - Comunicarse con otros firmantes a través de canales encriptados

## Procedimientos de Recuperación

### Pérdida de una Clave

Si un firmante pierde su clave:

1. **Verificar umbral** - Asegúrate de que aún tienes suficientes firmantes para alcanzar el umbral
2. **Continuar operaciones** - Puedes continuar usando las claves restantes
3. **Opcional: Reemplazar firmante** - Si es necesario, puedes agregar un nuevo firmante y recrear la wallet

### Pérdida de Múltiples Claves

Si pierdes demasiadas claves y no puedes alcanzar el umbral:

1. **Evaluar situación** - Determina cuántas claves tienes disponibles
2. **Contactar otros firmantes** - Coordina con otros firmantes para recuperar acceso
3. **Considerar migración** - Si es necesario, recrea la wallet con un nuevo conjunto de firmantes

> [!WARNING]
> **Pérdida de Acceso**
>
> Si pierdes suficientes claves para no poder alcanzar el umbral, perderás acceso permanente a los fondos en la wallet multifirma. Asegúrate de tener un plan de respaldo.

## Rotación de Firmantes

> [!NOTE]
> **¿Qué es la Rotación de Firmantes?**
>
> La rotación de firmantes se refiere al proceso de **reemplazar algunos o todos los firmantes** de una wallet multifirma por nuevos firmantes. Esto puede implicar:
> - Remover firmantes que ya no son confiables o disponibles
> - Agregar nuevos firmantes para reemplazar a los removidos
> - Cambiar el conjunto completo de firmantes por razones de seguridad
>
> **Importante:** La rotación **NO es recomendable hacerla frecuentemente** porque:
> - Requiere crear una nueva wallet con nueva dirección
> - Requiere migrar todos los fondos
> - Puede interrumpir operaciones en curso
> - Puede causar confusión si se hace demasiado seguido

### Cuándo Rotar

Considera rotar firmantes o recrear la wallet multifirma **solo cuando sea necesario**:

- Un firmante ya no es confiable o ha sido comprometido
- Un firmante ha perdido su clave y no puede recuperarla
- Cambios organizacionales importantes requieren nuevos firmantes
- **NO rotes periódicamente** a menos que haya una razón de seguridad específica

> [!WARNING]
> **Rotación Frecuente No es Recomendable**
>
> La rotación de firmantes debe ser un proceso **excepcional**, no rutinario. Cada rotación:
> - Crea una nueva wallet con nueva dirección
> - Requiere migración de fondos
> - Puede interrumpir operaciones
> - Aumenta el riesgo de errores
>
> **Mejor práctica:** Diseña tu wallet multifirma con firmantes confiables desde el inicio y solo rota cuando sea absolutamente necesario.

### Proceso de Rotación

1. **Seleccionar nuevos firmantes** - Identifica quién será agregado/removido
2. **Obtener claves públicas** - Recibe las claves públicas de los nuevos firmantes
3. **Recrear wallet** - Crea una nueva wallet multifirma con el nuevo conjunto
4. **Migrar fondos** - Transfiere los fondos de la wallet antigua a la nueva
5. **Actualizar configuración** - Todos los participantes actualizan su configuración
6. **Actualizar referencias** - Actualiza cualquier referencia a la dirección antigua (contratos, configuraciones, etc.)

## Consideraciones de Custodia

### Custodia Distribuida

- **Distribución geográfica** - Idealmente, las claves están en ubicaciones diferentes
- **Independencia** - Cada firmante debe tener control independiente de su clave
- **Respaldo** - Cada firmante debe tener su propio respaldo de su frase semilla

### Custodia Institucional

> [!WARNING]
> **Filosofía Cypherpunk: "No tus llaves, no tus criptos"**
>
> La filosofía cypherpunk promueve la **autocustodia** y la **desconfianza en instituciones centralizadas**. Se recomienda:
>
> - ✅ **Gestionar tus propias claves** de manera segura sin confiar en organizaciones externas
> - ✅ **Usar custodia distribuida** entre participantes confiables
> - ✅ **Mantener control total** sobre tus claves privadas
> - ❌ **Evitar custodia institucional** a menos que sea absolutamente necesario
>
> La custodia institucional solo es recomendable en casos específicos donde:
> - Requisitos regulatorios o legales lo exijan
> - La organización no tiene capacidad técnica para gestionar claves de forma segura
> - Se trata de fondos corporativos que requieren cumplimiento específico
>
> **En el mejor de los casos, sigue la filosofía cypherpunk y gestiona tus propias claves de manera segura.**

Si **debes** usar una institución para custodia (solo en casos específicos):

- **Verificar reputación** - Asegúrate de que la institución es confiable y tiene un historial comprobado
- **Contratos claros** - Ten contratos claros sobre responsabilidades, límites y procedimientos
- **Auditoría** - Realiza auditorías regulares de las operaciones y verifica que la institución sigue las mejores prácticas
- **Segregación de fondos** - Asegúrate de que tus fondos están segregados y no mezclados con otros
- **Plan de salida** - Ten un plan claro para recuperar tus claves si decides cambiar de institución

## Auditoría y Monitoreo

### Monitoreo de Transacciones

1. **Revisar todas las transacciones** - Cada firmante debe revisar las transacciones antes de firmar
2. **Alertas** - Configura alertas para transacciones desde la wallet multifirma
3. **Registros** - Mantén registros de todas las transacciones y firmas

### Auditoría Regular

1. **Verificar firmantes** - Verifica periódicamente que todos los firmantes siguen siendo confiables
2. **Revisar configuración** - Revisa la configuración de la wallet multifirma
3. **Probar recuperación** - Prueba periódicamente los procedimientos de recuperación

## Comunicación Segura

### Canales de Comunicación

- **Encriptación** - Usa siempre comunicación encriptada
- **Verificación de identidad** - Verifica la identidad de otros firmantes antes de compartir información
- **Canales privados** - Usa canales privados para comunicación sobre transacciones

### Proceso de Firma

1. **Transparencia** - Todos los firmantes deben poder ver las transacciones propuestas
2. **Verificación** - Cada firmante debe verificar la transacción antes de firmar
3. **Confirmación** - Confirma que recibiste y firmaste la transacción correcta

## Wallets Multifirma en Genesis

Si una wallet multifirma está incluida en el archivo `genesis.json`, la dirección pública queda fija desde el inicio de la cadena. La dirección se calcula a partir de las claves públicas de los firmantes, por lo que **no puedes modificar los firmantes sin cambiar la dirección**.

### Consideraciones Antes de Incluir en Genesis

Antes de incluir una wallet multifirma en el genesis, considera:

1. **Selección permanente de firmantes** - Elige firmantes que serán confiables a largo plazo, ya que cambiarlos después del lanzamiento puede no ser viable
2. **Propósito y contexto** - Entiende completamente **por qué** y **cómo** se está usando la wallet en el genesis
3. **Umbral apropiado** - Configura un umbral que permita operaciones incluso si algunos firmantes no están disponibles
4. **Documentación** - Documenta claramente quiénes son los firmantes y cómo contactarlos

### Limitaciones al Cambiar Firmantes Después del Lanzamiento

Cambiar firmantes después del lanzamiento requiere crear una nueva wallet con una nueva dirección. Sin embargo, **dependiendo del contexto, esto puede no ser viable**:

**Casos donde cambiar la dirección NO es posible:**

- **Fondos de desbloqueo programado** - Si la wallet recibe fondos mediante un mecanismo programado en el genesis, el protocolo seguirá enviando fondos a la dirección original. No puedes modificar el mecanismo para que envíe a una dirección diferente.

- **Mecanismos automáticos del protocolo** - Si la wallet recibe recompensas automáticas, distribuciones de gobernanza, o fondos de treasury/módulos, estos mecanismos están hardcodeados en el genesis y seguirán operando con la dirección original. **Estos mecanismos no pueden modificarse después del lanzamiento.**

- **Cuentas de módulo o permisos especiales** - Si la wallet tiene permisos especiales, estos están vinculados a la dirección específica y no pueden transferirse.

**Caso especial: Contratos inteligentes**

- **Contratos inteligentes vinculados** - Si hay contratos programados para enviar fondos a esa dirección, el comportamiento depende del diseño del contrato:
  - **Si el contrato está bien diseñado** - Puede incluir funcionalidad para actualizar direcciones mediante funciones de administración o gobernanza, permitiendo cambiar la dirección de destino sin redesplegar el contrato.
  - **Si el contrato no tiene esta funcionalidad** - Requeriría redesplegar el contrato y migrar toda la lógica, lo cual puede ser complejo o inviable dependiendo del caso.
  
  A diferencia de los mecanismos del genesis que son inmutables, los contratos inteligentes pueden diseñarse con capacidad de actualización si se planifica desde el inicio.

> [!WARNING]
> **Cambiar Firmantes Puede Ser Imposible**
>
> Si la wallet en el genesis tiene un propósito crítico (desbloqueo programado, mecanismos automáticos, etc.), cambiar los firmantes después del lanzamiento puede resultar en que la dirección original siga recibiendo fondos indefinidamente, mientras que la nueva dirección no recibirá esos fondos automáticos.

### Recomendaciones

- Si la wallet tiene un propósito específico y crítico en el genesis, **NO cambies los firmantes** después del lanzamiento
- Si planeas cambiar firmantes frecuentemente, considera **NO incluir la wallet en el genesis** y crearla después del lanzamiento
- Si debes incluirla en el genesis, **asegúrate de que los firmantes sean permanentes y confiables a largo plazo**

## Ver También

- [Firmante Multifirma]({{< relref "../../../../../concepts/multisig-signer" >}}) - Concepto atómico sobre firmantes
- [Wallet Multifirma]({{< relref "../../../../../concepts/multisig-wallet" >}}) - Concepto atómico sobre wallets multifirma
- [Mejores Prácticas de Seguridad]({{< relref "security" >}}) - Seguridad general de claves
- [Operaciones Multifirma]({{< relref "multisig-operations" >}}) - Cómo crear y usar wallets multifirma

