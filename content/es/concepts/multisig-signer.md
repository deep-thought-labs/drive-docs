---
title: "Firmante Multifirma"
weight: 6
---

Un **firmante multifirma** (multisig signer) es un participante que posee una de las claves privadas necesarias para firmar transacciones desde una [wallet multifirma]({{< relref "multisig-wallet" >}}).

## ¿Qué es un Firmante?

Un firmante es:

- **Poseedor de una clave privada** - Tiene acceso a una de las claves que forman parte de la wallet multifirma
- **Participante autorizado** - Puede firmar transacciones para la wallet multifirma
- **Parte del consenso** - Su firma cuenta hacia el [umbral]({{< relref "multisig-threshold" >}}) requerido

## Rol del Firmante

### Responsabilidades

1. **Mantener su clave privada segura** - Proteger su frase semilla y clave privada
2. **Firmar transacciones cuando se solicite** - Revisar y firmar transacciones propuestas
3. **Verificar transacciones** - Asegurarse de que las transacciones son legítimas antes de firmar
4. **Coordinar con otros firmantes** - Comunicarse para completar transacciones que requieren múltiples firmas

### Poderes

- ✅ **Puede firmar transacciones** - Su firma cuenta hacia el umbral requerido
- ✅ **Puede verificar transacciones** - Puede revisar transacciones antes de firmar
- ❌ **No puede autorizar solo** - Necesita que otros firmantes también firmen (a menos que el umbral sea 1)

## Cómo se Agregan Firmantes

Para agregar un firmante a una wallet multifirma:

1. **El firmante genera o exporta su clave pública** - Sin compartir la clave privada
2. **Se agrega la clave pública a la wallet** - Se combina con las otras claves públicas
3. **Se actualiza la configuración** - La wallet se recrea con el nuevo conjunto de firmantes

> [!NOTE]
> **No se Comparten Claves Privadas**
>
> Los firmantes **nunca** comparten sus claves privadas o frases semilla. Solo comparten sus claves públicas para crear la wallet multifirma.

## Cómo se Remueven Firmantes

Para remover un firmante:

1. **Se recrea la wallet** - Se crea una nueva wallet multifirma sin la clave pública del firmante a remover
2. **Se migran los fondos** - Se transfieren los fondos de la wallet antigua a la nueva
3. **Se actualiza la configuración** - Todos los participantes actualizan su configuración local

> [!WARNING]
> **Remover Firmantes Requiere Migración**
>
> Remover un firmante requiere crear una nueva wallet y migrar los fondos. No es posible simplemente "remover" una clave de una wallet existente.

## Tipos de Firmantes

### Firmante Activo

- Participa regularmente en la firma de transacciones
- Mantiene su clave accesible y disponible
- Responde rápidamente a solicitudes de firma

### Firmante de Respaldo

- Tiene una clave pero no participa activamente
- Se usa como respaldo en caso de pérdida de otras claves
- Solo se activa cuando es necesario para alcanzar el umbral

### Firmante de Emergencia

- Tiene una clave almacenada de forma ultra-segura (ej: caja de seguridad)
- Solo se usa en situaciones de emergencia
- Puede ayudar a recuperar acceso si se pierden otras claves

## Seguridad del Firmante

### Protección de la Clave Privada

Cada firmante debe:

- **Respaldar su frase semilla** - Guardarla de forma segura y fuera de línea
- **Usar almacenamiento seguro** - Considerar hardware wallets o almacenamiento encriptado
- **No compartir nunca** - Nunca compartir la clave privada o frase semilla con nadie
- **Usar canales seguros** - Comunicarse con otros firmantes a través de canales encriptados

### Gestión de Acceso

- **Distribución geográfica** - Idealmente, los firmantes están en ubicaciones diferentes
- **Independencia** - Cada firmante debe ser independiente y no controlado por otros
- **Rotación** - Considerar rotar firmantes periódicamente para mayor seguridad

## Coordinación entre Firmantes

### Proceso de Firma

1. **Un coordinador genera la transacción** - Crea la transacción sin firmar
2. **Distribuye la transacción** - Comparte la transacción con todos los firmantes
3. **Cada firmante revisa y firma** - Cada uno firma con su clave privada
4. **Se combinan las firmas** - El coordinador combina las firmas
5. **Se envía la transacción** - La transacción firmada se envía a la blockchain

### Comunicación

- **Canales seguros** - Usar comunicación encriptada (Signal, PGP, etc.)
- **Verificación** - Cada firmante debe verificar la transacción antes de firmar
- **Transparencia** - Todos los firmantes deben poder ver las transacciones propuestas

## Ver También

- [Wallet Multifirma]({{< relref "multisig-wallet" >}}) - Qué es una wallet multifirma
- [Umbral Multifirma]({{< relref "multisig-threshold" >}}) - Cómo funciona el umbral M-of-N
- [Key]({{< relref "key" >}}) - Conceptos básicos de claves criptográficas
- [Operaciones Multifirma]({{< relref "../drive/guides/blockchain-nodes/keys/multisig-operations" >}}) - Cómo agregar y gestionar firmantes
- [Seguridad Multifirma]({{< relref "../drive/guides/blockchain-nodes/keys/multisig-security" >}}) - Mejores prácticas de seguridad para firmantes

