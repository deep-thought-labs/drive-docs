---
title: "Visión General de Wallets Multifirma"
weight: 52224
---

Introducción a wallets multifirma y cuándo usarlas en el ecosistema Drive.

> [!NOTE]
> **Conceptos Fundamentales**
>
> Antes de continuar, asegúrate de entender:
> - [Wallet Multifirma]({{< relref "../../../../../concepts/multisig-wallet" >}}) - Qué es una wallet multifirma y para qué se usa
> - [Umbral Multifirma]({{< relref "../../../../../concepts/multisig-threshold" >}}) - Cómo funciona el umbral M-of-N
> - [Firmante Multifirma]({{< relref "../../../../../concepts/multisig-signer" >}}) - Qué es un firmante y su rol
> - [Key]({{< relref "../../../../../concepts/key" >}}) - Conceptos básicos de claves criptográficas
> - [Keyring]({{< relref "../../../../../concepts/keyring" >}}) - Cómo se almacenan las claves

## ¿Qué es una Wallet Multifirma?

Una [wallet multifirma]({{< relref "../../../../../concepts/multisig-wallet" >}}) es una cuenta blockchain que requiere múltiples firmas para autorizar transacciones, proporcionando seguridad adicional y control compartido sobre los fondos.

A diferencia de una clave simple que requiere una sola firma, una wallet multifirma combina las claves públicas de múltiples participantes y requiere que un número mínimo de ellos (el [umbral]({{< relref "../../../../../concepts/multisig-threshold" >}})) firmen cada transacción.

## Cuándo Usar Multifirma

### Casos de Uso Recomendados

- **Organizaciones** - Fondos corporativos que requieren aprobación de múltiples ejecutivos
- **DAOs** - Tesorerías que requieren consenso de múltiples miembros
- **Validadores** - Fondos de validación que requieren múltiples firmantes
- **Fondos compartidos** - Cuentas con control distribuido entre socios
- **Seguridad personal** - Usuarios que quieren protección adicional contra pérdida de clave única

### Cuándo NO Usar Multifirma

- **Uso personal simple** - Si solo necesitas una cuenta personal, una clave simple es más práctica
- **Transacciones frecuentes** - Las wallets multifirma requieren más tiempo y coordinación
- **Participantes no confiables** - Si no puedes coordinar con otros participantes, una multifirma no es práctica

## Ventajas y Desventajas

### Ventajas

- ✅ **Seguridad mejorada** - Un compromiso de una sola clave no permite robar fondos
- ✅ **Control compartido** - Ideal para organizaciones o fondos compartidos
- ✅ **Resistencia a pérdida** - Puedes perder algunas claves sin perder acceso a los fondos
- ✅ **Auditoría** - Todas las transacciones requieren consenso explícito

### Desventajas

- ⚠️ **Complejidad** - Requiere coordinación entre múltiples participantes
- ⚠️ **Tiempo de procesamiento** - Las transacciones toman más tiempo al requerir múltiples firmas
- ⚠️ **Costos de gas** - Puede requerir más gas debido a múltiples verificaciones de firma

## Diferencias con Claves Simples

| Aspecto | Clave Simple | Wallet Multifirma |
|---------|--------------|-------------------|
| **Firmas requeridas** | 1 | M de N (configurable) |
| **Control** | Individual | Compartido |
| **Seguridad** | Depende de una clave | Depende de múltiples claves |
| **Complejidad** | Baja | Media-Alta |
| **Velocidad** | Rápida | Más lenta (requiere coordinación) |

Para más detalles, consulta [Wallet Multifirma]({{< relref "../../../../../concepts/multisig-wallet" >}}).

## Orden Recomendado de Lectura

Para obtener el mejor provecho de esta documentación sobre wallets multifirma, te recomendamos seguir este orden:

### 1. 📚 Entender los Conceptos

- **[Wallet Multifirma]({{< relref "../../../../../concepts/multisig-wallet" >}})** - Qué es y cómo funciona
- **[Umbral Multifirma]({{< relref "../../../../../concepts/multisig-threshold" >}})** - Cómo funciona M-of-N
- **[Firmante Multifirma]({{< relref "../../../../../concepts/multisig-signer" >}})** - Qué es un firmante

### 2. 🔧 Aprender las Operaciones

- **[Operaciones Multifirma]({{< relref "multisig-operations" >}})** - Cómo crear y usar wallets multifirma:
  - Crear wallet multifirma
  - Firmar transacciones con múltiples firmantes
  - Combinar firmas
  - Enviar transacciones

### 3. 🔐 Mejores Prácticas de Seguridad

- **[Seguridad Multifirma]({{< relref "multisig-security" >}})** - Mejores prácticas específicas:
  - Distribución segura de claves
  - Gestión de firmantes
  - Procedimientos de recuperación

## Limitaciones Actuales

> [!NOTE]
> **Interfaz Gráfica No Disponible**
>
> Actualmente, la interfaz gráfica de Drive no soporta operaciones con wallets multifirma. Todas las operaciones deben realizarse mediante comandos en el bash del contenedor.

Para comandos que no están disponibles a través de `drive.sh`, deberás acceder directamente al bash del contenedor y ejecutar los comandos nativos de `infinited`.

## Próximos Pasos

Ahora que entiendes los conceptos fundamentales:

- **[Operaciones Multifirma]({{< relref "multisig-operations" >}})** - Guía paso a paso para crear y usar wallets multifirma
- **[Seguridad Multifirma]({{< relref "multisig-security" >}})** - Mejores prácticas de seguridad
- **[Operaciones de Gestión de Claves]({{< relref "operations" >}})** - Para operaciones con claves simples que sí están disponibles en la interfaz gráfica

## Ver También

- [Wallet Multifirma]({{< relref "../../../../../concepts/multisig-wallet" >}}) - Concepto atómico sobre wallets multifirma
- [Umbral Multifirma]({{< relref "../../../../../concepts/multisig-threshold" >}}) - Concepto atómico sobre umbrales
- [Firmante Multifirma]({{< relref "../../../../../concepts/multisig-signer" >}}) - Concepto atómico sobre firmantes
- [Key]({{< relref "../../../../../concepts/key" >}}) - Conceptos básicos de claves
- [Keyring]({{< relref "../../../../../concepts/keyring" >}}) - Cómo se almacenan las claves

