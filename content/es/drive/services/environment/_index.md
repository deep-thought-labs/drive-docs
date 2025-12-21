---
title: "Variables de Entorno"
---

Las variables de entorno son parámetros de configuración pasados a los contenedores Docker que controlan cómo se comportan los servicios. En Drive, todos los servicios pueden tener variables de entorno, y muchos servicios comparten los mismos nombres de variables pero con valores diferentes.

## How Variables de Entorno Work in Drive

- **Variables Compartidas**: Muchos servicios usan los mismos nombres de variables de entorno (ej., `NODE_CHAIN_ID`, `NODE_P2P_SEEDS`)
- **Valores Diferentes**: Lo que hace único a cada servicio es el **valor** asignado a cada variable
- **Específico del Servicio**: El archivo `docker-compose.yml` de cada servicio define los valores específicos para ese servicio
- **Comportamiento del Contenedor**: La combinación de nombres de variables y sus valores determina cómo se ejecuta el contenedor

## Documentación de Variables de Entorno

### Por Tipo de Servicio

- [Nodos Blockchain]({{< relref "blockchain-nodes" >}}) - Variables de entorno utilizadas por servicios de nodos blockchain
- [General]({{< relref "general" >}}) - Variables de entorno globales compartidas entre todos los servicios

## Ver También

- [Catálogo de Servicios]({{< relref "../catalog" >}}) - Configuraciones específicas de servicios con valores reales
- [Estructura del Servicio]({{< relref "../service-structure" >}}) - Cómo se configuran los servicios
