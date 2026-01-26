---
title: "Genesis"
weight: 401
---

Guías para trabajar con archivos Genesis y gentxs (transacciones genesis).

## ¿Qué es Genesis?

El archivo genesis define el estado inicial de una blockchain. Contiene información sobre cuentas iniciales, validadores, parámetros de red y configuración de módulos.

## Guías Disponibles

- **[Obtener Genesis desde URL]({{< relref "obtain-genesis" >}})** - Descargar el archivo genesis oficial para mainnet o testnet (para unirse a una red existente)
- **[Crear Gentx]({{< relref "create-gentx" >}})** - Guía completa para crear una gentx desde un genesis base (para participación en lanzamiento de cadena)

## Cuándo Usar Cada Guía

**Usa "Obtener Genesis desde URL" si:**
- Te estás uniendo a una red existente (mainnet o testnet)
- Quieres ejecutar un nodo con la configuración genesis oficial
- Estás configurando un nuevo nodo después de que la cadena ha sido lanzada

**Usa "Crear Gentx" si:**
- Estás participando en un lanzamiento de cadena
- El equipo de desarrollo te ha pedido crear una gentx
- Eres un validador uniéndote a la red en genesis

## Conceptos Relacionados

Para entender mejor los conceptos fundamentales, consulta:

- [Archivo Genesis]({{< relref "../../concepts/genesis-file" >}}) - Qué es un archivo genesis y su propósito
- [Inicialización de Nodo]({{< relref "../../concepts/node-initialization" >}}) - Proceso de inicialización de nodo

## Documentación Relacionada

- **[Tokenomics]({{< relref "../tokenomics" >}})** - Aprende sobre ModuleAccounts y cuentas de vesting en genesis
- **[Resumen de la Red]({{< relref "../overview" >}})** - Identidad de red y Chain IDs
