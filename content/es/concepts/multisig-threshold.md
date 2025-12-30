---
title: "Umbral Multifirma"
weight: 5
---

El **umbral multifirma** (multisig threshold) es el número mínimo de firmas requeridas para autorizar una transacción desde una [wallet multifirma]({{< relref "multisig-wallet" >}}).

## ¿Qué es el Umbral?

El umbral es el valor **M** en la notación **M-of-N**:

- **M** - Número mínimo de firmas requeridas (threshold)
- **N** - Número total de participantes (firmantes)

**Ejemplo:** En una configuración **2-of-3**:
- **N = 3** - Hay 3 participantes totales
- **M = 2** - Se requieren al menos 2 firmas para autorizar una transacción

## Cómo Funciona

El umbral determina:

1. **Cuántas firmas se necesitan** - Una transacción requiere exactamente M firmas válidas
2. **Tolerancia a fallos** - Puedes perder hasta (N - M) claves sin perder acceso
3. **Nivel de seguridad** - Un umbral más alto requiere más consenso

## Ejemplos de Configuraciones

### 2-of-3 (Recomendado para 3 Participantes)

- **Firmas requeridas:** 2 de 3
- **Tolerancia:** Puedes perder 1 clave
- **Uso:** Balance entre seguridad y flexibilidad
- **Ejemplo:** 3 socios, 2 deben aprobar cada transacción

### 3-of-5 (Recomendado para 5 Participantes)

- **Firmas requeridas:** 3 de 5
- **Tolerancia:** Puedes perder 2 claves
- **Uso:** Mayor seguridad con más participantes
- **Ejemplo:** DAO con 5 miembros del comité

### 2-of-2 (Control Dual)

- **Firmas requeridas:** Ambas (2 de 2)
- **Tolerancia:** No puedes perder ninguna clave
- **Uso:** Control estricto entre dos partes
- **Ejemplo:** Dos socios que deben aprobar cada transacción

### 1-of-2 (No Recomendado)

- **Firmas requeridas:** 1 de 2
- **Tolerancia:** Puedes perder 1 clave
- **Uso:** ⚠️ **No proporciona seguridad adicional** - Cualquiera puede autorizar
- **Nota:** Esta configuración no tiene sentido para seguridad, solo para redundancia

## Consideraciones para Elegir el Umbral

### Seguridad vs Flexibilidad

- **Umbral alto (ej: 3-of-3)** - Máxima seguridad, pero menos flexibilidad
- **Umbral medio (ej: 2-of-3)** - Balance entre seguridad y flexibilidad
- **Umbral bajo (ej: 1-of-2)** - Poca seguridad adicional

### Tolerancia a Pérdida de Claves

El número de claves que puedes perder sin perder acceso es: **N - M**

- **2-of-3:** Puedes perder 1 clave ✅
- **3-of-5:** Puedes perder 2 claves ✅
- **2-of-2:** No puedes perder ninguna clave ⚠️

### Regla General

Para una configuración segura y práctica:

- **M debe ser mayor que 1** - Al menos 2 firmas requeridas
- **M debe ser menor que N** - No todos deben estar obligados a firmar
- **M debe ser al menos la mitad de N** - Requiere consenso de la mayoría

**Fórmula recomendada:** `M = ⌈N/2⌉ + 1` (más de la mitad)

## Impacto en Operaciones

### Creación de Transacciones

Cuando creas una transacción desde una wallet multifirma:

1. Se genera la transacción sin firmar
2. Se distribuye a todos los participantes
3. Al menos M participantes deben firmarla
4. Las firmas se combinan
5. La transacción se envía a la blockchain

### Tiempo de Procesamiento

- **Umbral bajo:** Más rápido (menos coordinación necesaria)
- **Umbral alto:** Más lento (más participantes deben estar disponibles)

## Ver También

- [Wallet Multifirma]({{< relref "multisig-wallet" >}}) - Qué es una wallet multifirma
- [Firmante Multifirma]({{< relref "multisig-signer" >}}) - Qué es un firmante
- [Operaciones Multifirma]({{< relref "../drive/guides/blockchain-nodes/keys/multisig-operations" >}}) - Cómo crear wallets con diferentes umbrales

