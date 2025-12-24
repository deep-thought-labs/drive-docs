---
title: "Gestionar Servicios"
weight: 513
---

Los servicios de Drive están organizados en el directorio `services/`. Cada servicio es independiente y puede gestionarse por separado.

## Comandos Básicos

Todos los servicios usan `drive.sh` en su directorio:

```bash
cd services/<service-name>

# Iniciar servicio (en segundo plano)
./drive.sh up -d

# Mostrar estado del contenedor
./drive.sh ps

# Detener servicio
./drive.sh stop

# Detener y eliminar contenedor
./drive.sh down

# Iniciar (si está detenido)
./drive.sh start      

# Reiniciar servicio (si ya está ejecutándose)
./drive.sh restart

# Ver registros del contenedor
./drive.sh logs

# Acceder a la shell del contenedor
./drive.sh bash
```

## Tipos de Servicios

Cada tipo de servicio tiene características específicas. **Nodos Blockchain** incluyen una interfaz gráfica y comandos especializados de gestión de nodos.

Para estructura detallada de servicios, configuración y temas avanzados, consulta [Estructura del Servicio]({{< relref "/drive/services/service-structure" >}}).

## Próximos Pasos

- [Catálogo de Servicios]({{< relref "/drive/services/catalog" >}}) - Todos los servicios disponibles
- [Guías de Nodos Blockchain]({{< relref "/drive/guides/blockchain-nodes" >}})
