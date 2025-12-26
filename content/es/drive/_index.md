---
title: "Drive"
type: "docs"
weight: 1
---

Drive es una herramienta de gestión de infraestructura descentralizada que permite a los usuarios desplegar y gestionar nodos blockchain, servicios y protocolos en sus propios sistemas—ya sean máquinas locales, servidores personales o su propia infraestructura de internet.

Cuando se combina con otros usuarios independientes ejecutando Drive, crea una super-malla sincronizada de servicios, protocolos y cadenas, formando una red de infraestructura distribuida gestionada completamente por usuarios independientes. Drive capacita a los individuos para participar y contribuir a un ecosistema descentralizado mientras mantienen el control total sobre su infraestructura.

## Orden Recomendado de Lectura

Para obtener el mejor provecho de esta documentación, te recomendamos seguir este orden:

1. **[Inicio Rápido]({{< relref "quick-start" >}})** - Comienza aquí para poner Drive en funcionamiento rápidamente
   - [Arquitectura de Drive]({{< relref "quick-start/architecture" >}}) - Entender cómo funciona Drive
   - [Requisitos Previos]({{< relref "quick-start/installation" >}}) - Instalar las herramientas necesarias
   - [Clonar Repositorio]({{< relref "quick-start/git-clone" >}}) - Obtener el código fuente
   - [Verificar Instalación]({{< relref "quick-start/managing-services" >}}) - Verificar que todo está configurado correctamente

2. **[Guías]({{< relref "guides" >}})** - Aprende a realizar operaciones específicas
   - [General]({{< relref "guides/general" >}}) - Operaciones generales de gestión
   - [Nodos Blockchain]({{< relref "guides/blockchain-nodes" >}}) - Guías para trabajar con nodos blockchain

3. **[Servicios]({{< relref "services" >}})** - Referencia técnica completa
   - [Estructura del Servicio]({{< relref "services/service-structure" >}}) - Arquitectura técnica
   - [Catálogo de Servicios]({{< relref "services/catalog" >}}) - Todos los servicios disponibles
   - [Variables de Entorno]({{< relref "services/environment" >}}) - Configuración de servicios
   - [Estrategia de Puertos]({{< relref "services/ports" >}}) - Configuración de red

4. **[Funcionamiento Interno]({{< relref "internal-workings" >}})** - Documentación técnica del sistema interno
   - [Sistema de Supervisor y Auto-Start]({{< relref "internal-workings/supervisor-auto-start" >}}) - Monitoreo y reinicio automático
   - [Gestión de Procesos Interna]({{< relref "internal-workings/process-management" >}}) - Daemonización y tracking de procesos
   - [Estructura Interna de Directorios]({{< relref "internal-workings/directory-structure" >}}) - Organización de archivos y directorios
   - [Sistema de Configuración Interna]({{< relref "internal-workings/configuration-system" >}}) - Variables y configuración centralizada
   - [Sistema de Logs Interno]({{< relref "internal-workings/logging-system" >}}) - Estructura y gestión de logs
   - [Arquitectura del Contenedor]({{< relref "internal-workings/container-architecture" >}}) - Build y configuración del Dockerfile
   - [Flujo de Inicialización Técnico]({{< relref "internal-workings/initialization-flow" >}}) - Proceso interno de inicialización
   - [Scripts Internos del Contenedor]({{< relref "internal-workings/internal-scripts" >}}) - Descripción de todos los scripts

5. **[Solución de Problemas]({{< relref "troubleshooting" >}})** - Cuando encuentres problemas
   - [Problemas Comunes]({{< relref "troubleshooting/common-issues" >}}) - Soluciones a errores frecuentes
   - [Diagnóstico de Red]({{< relref "troubleshooting/network-diagnosis" >}}) - Herramientas de diagnóstico
