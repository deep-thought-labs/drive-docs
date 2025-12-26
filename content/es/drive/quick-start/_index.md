---
title: "Inicio Rápido"
weight: 51
---

Pon Drive en funcionamiento rápidamente. Sigue estos pasos en orden:

1. [Arquitectura Overview]({{< relref "architecture" >}}) - Entender cómo funciona Drive
2. [Requisitos Previos]({{< relref "installation" >}}) - Instalar requisitos técnicos
3. [Clonar Repositorio]({{< relref "git-clone" >}}) - Clonar el repositorio de Drive
4. [Verificar Instalación]({{< relref "managing-services" >}}) - Verificar que todo está configurado correctamente

## Configuración de Firewall y Puertos

Una vez que Drive esté instalado y funcionando, es importante configurar el firewall de tu sistema para permitir las conexiones necesarias a los servicios de Drive.

**Configuración de Firewall:**
- Consulta la [Guía de Configuración de Firewall]({{< relref "../services/ports/firewall-configuration" >}}) para instrucciones detalladas sobre cómo configurar el firewall según tu sistema operativo.

**Puertos por Servicio:**
- Cada servicio de Drive tiene puertos específicos asignados que deben estar abiertos en el firewall.
- La configuración de puertos para cada servicio se describe en la documentación individual de cada servicio en el [Catálogo de Servicios]({{< relref "../services/catalog" >}}).
- **Recomendamos leer la documentación de cada servicio** que planeas usar para conocer los puertos específicos que necesita.

**Información General sobre Puertos:**
- Para información general sobre la estrategia de asignación de puertos y configuración global, consulta la sección [Puertos]({{< relref "../services/ports" >}}) en la documentación de Servicios.
