---
title: "Verificar Instalación"
weight: 513
---

Antes de continuar, verifica que tu sistema está correctamente configurado y listo para usar Drive. Esta verificación te asegurará que todos los componentes necesarios están funcionando correctamente.

## Verificar Docker

Confirma que Docker está funcionando correctamente:

```bash
docker ps
```

**Resultado esperado:** Deberías ver una lista (posiblemente vacía) de contenedores sin errores. Si ves un error, Docker no está funcionando correctamente.

## Verificar Estructura del Repositorio

Desde el directorio raíz del repositorio clonado (`drive/`), verifica que la carpeta `services/` existe:

```bash
ls services/
```

**Resultado esperado:** Deberías ver una lista de carpetas de servicios (por ejemplo: `node0-infinite`, `node1-infinite-testnet`, etc.).

## Verificar Script de Gestión

Entra a cualquier servicio y verifica que el script `drive.sh` existe y es ejecutable:

```bash
cd services/node0-infinite  # O cualquier otro servicio disponible
ls -la drive.sh
```

**Resultado esperado:** Deberías ver el archivo `drive.sh` con permisos de ejecución (indicado por la `x` en los permisos).

## ✅ Verificación Completa

Si todos los comandos anteriores funcionaron correctamente, tu sistema está configurado y listo para usar Drive.

## Próximos Pasos

Ahora que has completado el Inicio Rápido y verificado tu instalación, puedes continuar con las siguientes secciones según tus necesidades:

- **[Guías]({{< relref "../guides" >}})** - Aprende a realizar operaciones específicas
  - [Gestión de Contenedores]({{< relref "../guides/general/container-management" >}}) - Comandos detallados para gestionar servicios
  - [Nodos Blockchain]({{< relref "../guides/blockchain-nodes" >}}) - Guías específicas para trabajar con nodos blockchain

- **[Servicios]({{< relref "../services" >}})** - Referencia técnica completa
  - [Catálogo de Servicios]({{< relref "../services/catalog" >}}) - Lista completa de servicios disponibles y sus configuraciones
