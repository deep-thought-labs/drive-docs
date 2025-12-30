---
title: "Wallet Multifirma"
weight: 4
---

Una **wallet multifirma** (multisig wallet) es una cuenta blockchain que requiere múltiples firmas para autorizar transacciones, proporcionando seguridad adicional y control compartido sobre los fondos.

## ¿Qué es una Wallet Multifirma?

Una wallet multifirma es un tipo especial de cuenta que:

- **Requiere múltiples firmas** - Necesita que varios participantes firmen una transacción antes de que pueda ejecutarse
- **Control compartido** - Ningún individuo puede autorizar transacciones por sí solo
- **Umbral configurable** - Se define cuántas firmas se necesitan (ej: 2 de 3, 3 de 5)
- **Mayor seguridad** - Reduce el riesgo de pérdida de fondos por compromiso de una sola clave

## Cómo Funciona

Una wallet multifirma combina las **claves públicas** de múltiples participantes:

1. **Cada participante tiene su propia clave privada** - Mantenida de forma segura y nunca compartida
2. **Solo se comparten claves públicas** - Las claves públicas se combinan para crear la wallet multifirma
3. **Umbral M-of-N** - Se requiere que M participantes de N totales firmen cada transacción
4. **Firma distribuida** - Cada participante firma la transacción por separado con su clave privada
5. **Combinación de firmas** - Las firmas se combinan para crear una transacción válida

## Notación M-of-N

La configuración de una wallet multifirma se expresa como **M-of-N**:

- **M** - Número mínimo de firmas requeridas (threshold)
- **N** - Número total de participantes (firmantes)

**Ejemplos comunes:**
- **2-of-3** - Requiere 2 firmas de 3 participantes (tolerancia a pérdida de 1 clave)
- **3-of-5** - Requiere 3 firmas de 5 participantes (tolerancia a pérdida de 2 claves)
- **2-of-2** - Requiere ambas firmas (control dual estricto)

## Ventajas

- ✅ **Seguridad mejorada** - Un compromiso de una sola clave no permite robar fondos
- ✅ **Control compartido** - Ideal para organizaciones, DAOs, o fondos compartidos
- ✅ **Resistencia a pérdida** - Puedes perder algunas claves sin perder acceso a los fondos
- ✅ **Auditoría** - Todas las transacciones requieren consenso explícito

## Desventajas

- ⚠️ **Complejidad** - Requiere coordinación entre múltiples participantes
- ⚠️ **Tiempo de procesamiento** - Las transacciones toman más tiempo al requerir múltiples firmas
- ⚠️ **Costos de gas** - Puede requerir más gas debido a múltiples verificaciones de firma

## Casos de Uso Comunes

- **Organizaciones** - Fondos corporativos que requieren aprobación de múltiples ejecutivos
- **DAOs** - Tesorerías que requieren consenso de múltiples miembros
- **Validadores** - Fondos de validación que requieren múltiples firmantes
- **Fondos compartidos** - Cuentas con control distribuido entre socios
- **Seguridad personal** - Usuarios que quieren protección adicional contra pérdida de clave única

## Diferencias con Claves Simples

| Aspecto | Clave Simple | Wallet Multifirma |
|---------|--------------|-------------------|
| **Firmas requeridas** | 1 | M de N (configurable) |
| **Control** | Individual | Compartido |
| **Seguridad** | Depende de una clave | Depende de múltiples claves |
| **Complejidad** | Baja | Media-Alta |
| **Velocidad** | Rápida | Más lenta (requiere coordinación) |

## Creación de Wallet Multifirma

La creación de una wallet multifirma **no requiere compartir claves privadas ni frases semilla**. Solo se necesitan:

1. **Claves públicas de cada participante** - Cada uno exporta su clave pública
2. **Configuración del umbral** - Decidir cuántas firmas se requieren (M-of-N)
3. **Combinación local** - Un coordinador combina las claves públicas para crear la wallet

Para más información sobre cómo crear una wallet multifirma, consulta [Operaciones Multifirma]({{< relref "../drive/guides/blockchain-nodes/keys/multisig-operations" >}}).

## Ver También

- [Umbral Multifirma]({{< relref "multisig-threshold" >}}) - Cómo funciona el umbral M-of-N
- [Firmante Multifirma]({{< relref "multisig-signer" >}}) - Qué es un firmante y su rol
- [Key]({{< relref "key" >}}) - Conceptos básicos de claves criptográficas
- [Keyring]({{< relref "keyring" >}}) - Cómo se almacenan las claves
- [Operaciones Multifirma]({{< relref "../drive/guides/blockchain-nodes/keys/multisig-operations" >}}) - Guía práctica para crear y usar wallets multifirma

