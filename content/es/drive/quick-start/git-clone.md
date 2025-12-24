---
title: "Clonar Repositorio"
weight: 512
---

Clona el repositorio de Drive desde GitHub para obtener el código fuente en tu sistema local.

## Clonar el Repositorio

Ejecuta el siguiente comando para clonar el repositorio:

```bash
git clone https://github.com/deep-thought-labs/drive
```

## Navegar al Repositorio

Una vez clonado, entra al directorio del repositorio:

```bash
cd drive
```

## Estructura del Repositorio

Dentro del repositorio encontrarás la carpeta `services/`, que contiene todos los servicios disponibles. Puedes navegar a cualquier subcarpeta dentro de `services/` para gestionar cada servicio de manera independiente:

```bash
cd services
ls  # Ver todos los servicios disponibles
cd node0-infinite  # Ejemplo: entrar a un servicio específico
```

**Nota:** Si puedes ver la carpeta `services/` y sus contenidos al ejecutar `ls`, esto confirma que el repositorio se ha clonado correctamente.

## Próximos Pasos

Ahora que tienes el repositorio clonado, consulta las siguientes secciones de la documentación:

- [Gestionar Servicios]({{< relref "managing-services" >}}) - Aprende cómo usar servicios en Drive
- [Guías]({{< relref "../guides" >}}) - Guías específicas para operaciones comunes
- [Catálogo de Servicios]({{< relref "../services/catalog" >}}) - Lista completa de servicios disponibles
