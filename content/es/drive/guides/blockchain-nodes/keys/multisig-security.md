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

### ⚠️ NUNCA

- Compartas claves privadas o frases semilla
- Compartas archivos del keyring
- Uses canales de comunicación no encriptados
- Confíes en una sola fuente para las claves públicas

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
> **Remover Firmantes Requiere Migración**
>
> Remover un firmante requiere crear una nueva wallet y migrar los fondos. No es posible simplemente "remover" una clave de una wallet existente.

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

## Rotación de Claves

### Cuándo Rotar

Considera rotar firmantes o recrear la wallet multifirma cuando:

- Un firmante ya no es confiable
- Un firmante ha sido comprometido
- Cambios organizacionales requieren nuevos firmantes
- Períodos regulares de rotación (ej: anualmente)

### Proceso de Rotación

1. **Seleccionar nuevos firmantes** - Identifica quién será agregado/removido
2. **Obtener claves públicas** - Recibe las claves públicas de los nuevos firmantes
3. **Recrear wallet** - Crea una nueva wallet multifirma con el nuevo conjunto
4. **Migrar fondos** - Transfiere los fondos de la wallet antigua a la nueva
5. **Actualizar configuración** - Todos los participantes actualizan su configuración

## Consideraciones de Custodia

### Custodia Distribuida

- **Distribución geográfica** - Idealmente, las claves están en ubicaciones diferentes
- **Independencia** - Cada firmante debe tener control independiente de su clave
- **Respaldo** - Cada firmante debe tener su propio respaldo de su frase semilla

### Custodia Institucional

Si usas una institución para custodia:

- **Verificar reputación** - Asegúrate de que la institución es confiable
- **Contratos claros** - Ten contratos claros sobre responsabilidades
- **Auditoría** - Realiza auditorías regulares de las operaciones

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

## Ver También

- [Firmante Multifirma]({{< relref "../../../../../concepts/multisig-signer" >}}) - Concepto atómico sobre firmantes
- [Wallet Multifirma]({{< relref "../../../../../concepts/multisig-wallet" >}}) - Concepto atómico sobre wallets multifirma
- [Mejores Prácticas de Seguridad]({{< relref "security" >}}) - Seguridad general de claves
- [Operaciones Multifirma]({{< relref "multisig-operations" >}}) - Cómo crear y usar wallets multifirma

