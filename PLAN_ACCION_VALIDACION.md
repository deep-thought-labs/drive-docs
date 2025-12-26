# Plan de Acción: Validación y Mejora de Documentación

## 🎯 Objetivo Principal
Asegurar que toda la documentación esté fundamentada en la implementación real del sistema y que esté organizada de forma clara y modular.

## ❌ Errores Críticos Encontrados

### 1. Error en start-stop-node.md
**Problema:** La documentación dice que `node-start` verifica `config.toml`, pero el script real verifica `genesis.json` (NODE_GENESIS_FILE).

**Línea afectada:** Línea 50 y 164 en `start-stop-node.md`

**Corrección necesaria:**
- Cambiar "comprueba la existencia de `config.toml`" por "comprueba la existencia de `genesis.json`"
- Actualizar el comando de verificación en troubleshooting

## 📋 Tareas Prioritarias

### Fase 1: Validación y Corrección de Errores (PRIORIDAD MÁXIMA)

#### 1.1 Corregir Errores de Implementación vs Documentación
- [ ] Corregir verificación de inicialización en `start-stop-node.md` (genesis.json vs config.toml)
- [ ] Verificar que todos los comandos documentados coincidan con los scripts reales
- [ ] Validar que las rutas y variables documentadas sean correctas
- [ ] Verificar que los flujos documentados coincidan con la lógica real
- [ ] Revisar todos los mensajes de error y salidas esperadas

#### 1.2 Revisar Conceptos contra Implementación Real
- [ ] Verificar `node-initialization.md` - ¿Coincide con lo que hace `node-init.sh`?
- [ ] Verificar `node-data.md` - ¿La estructura de directorios es correcta?
- [ ] Verificar `key.md` - ¿La explicación de claves es precisa?
- [ ] Verificar `keyring.md` - ¿Coincide con el uso real del keyring?
- [ ] Verificar `private-validator-key.md` - ¿La explicación es correcta?
- [ ] Verificar `genesis-file.md` - ¿El proceso de descarga es correcto?

### Fase 2: Centralización de Troubleshooting

#### 2.1 Identificar Troubleshooting Disperso
- [ ] `start-stop-node.md` - Sección "Solución de Problemas" (líneas 156-200)
- [ ] `node-monitoring.md` - Sección "Solución de Problemas con Logs" (líneas 234-271)
- [ ] Otros documentos con secciones de troubleshooting

#### 2.2 Mover a Troubleshooting Centralizado
- [ ] Crear `troubleshooting/node-start-stop-issues.md` con problemas de inicio/detención
- [ ] Crear `troubleshooting/node-log-issues.md` con problemas de logs
- [ ] Actualizar `troubleshooting/common-issues.md` con problemas generales
- [ ] Remover secciones de troubleshooting de documentos individuales
- [ ] Agregar referencias a troubleshooting centralizado en documentos originales

### Fase 3: Refactorización de start-stop-node.md

#### 3.1 Análisis del Contenido Actual
El documento `start-stop-node.md` contiene:
- Iniciar Nodo ✅ (coincide con título)
- Detener Nodo ✅ (coincide con título)
- Verificar Estado y Sincronización ❌ (redirige a node-monitoring, OK)
- Reiniciar Nodo ❌ (no está en el título)
- Solución de Problemas ❌ (debería estar en troubleshooting)

#### 3.2 Opciones de Refactorización

**Opción A: Renombrar y Expandir**
- Renombrar a `node-operations.md` o `essential-operations.md`
- Mantener todo en un documento pero con título más amplio
- **Ventaja:** Simple, no rompe referencias
- **Desventaja:** Documento sigue siendo largo

**Opción B: Separar en Múltiples Documentos (RECOMENDADO)**
- `start-stop-node.md` - Solo iniciar y detener
- `restart-node.md` - Reiniciar nodo (nuevo documento)
- Troubleshooting movido a `troubleshooting/`
- **Ventaja:** Modular, claro, fácil de mantener
- **Desventaja:** Requiere actualizar referencias

#### 3.3 Decisión: Opción B (Separar)
- [ ] Crear `restart-node.md` con contenido de reinicio
- [ ] Limpiar `start-stop-node.md` - solo iniciar/detener
- [ ] Mover troubleshooting a `troubleshooting/node-start-stop-issues.md`
- [ ] Actualizar todas las referencias cruzadas
- [ ] Actualizar índices

### Fase 4: Actualización de Referencias

#### 4.1 Actualizar Referencias Cruzadas
- [ ] Actualizar referencias a `start-stop-node.md` en otros documentos
- [ ] Agregar referencias a `restart-node.md` donde sea apropiado
- [ ] Actualizar referencias a troubleshooting centralizado
- [ ] Verificar que todos los `{{< relref >}}` funcionen correctamente

#### 4.2 Actualizar Índices
- [ ] Actualizar `guides/_index.md` con nuevos documentos
- [ ] Actualizar `guides/blockchain-nodes/_index.md`
- [ ] Actualizar `troubleshooting/_index.md`

## 🔍 Checklist de Validación Final

Antes de considerar completado, verificar:

### Validación de Implementación
- [ ] Todos los comandos documentados funcionan en la implementación real
- [ ] Todas las rutas y variables son correctas
- [ ] Todos los flujos coinciden con la lógica real
- [ ] Todos los mensajes de error y salidas son precisos

### Validación de Estructura
- [ ] No hay troubleshooting disperso en documentos individuales
- [ ] Todos los documentos tienen títulos que coinciden con su contenido
- [ ] La estructura es modular y clara
- [ ] Las referencias cruzadas funcionan correctamente

### Validación de Conceptos
- [ ] Todos los conceptos están alineados con la implementación real
- [ ] Las explicaciones son precisas y completas
- [ ] No hay información contradictoria

## 📝 Orden de Ejecución

1. **Fase 1.1** - Corregir errores críticos (genesis.json vs config.toml)
2. **Fase 1.2** - Revisar conceptos
3. **Fase 2** - Centralizar troubleshooting
4. **Fase 3** - Refactorizar start-stop-node.md
5. **Fase 4** - Actualizar referencias

## 🎯 Resultado Esperado

- Documentación 100% alineada con implementación real
- Troubleshooting completamente centralizado
- Documentos modulares con títulos que coinciden con contenido
- Conceptos precisos y verificados
- Referencias cruzadas funcionando correctamente

