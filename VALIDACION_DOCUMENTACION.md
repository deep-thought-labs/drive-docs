# Validación de Documentación Bilingüe

Este documento describe el sistema de validación para asegurar que toda la documentación esté completa en ambos idiomas (español e inglés).

## Script de Validación

El script `validate_documentation.py` valida automáticamente que:

1. **Todos los archivos existan en ambos idiomas** - Verifica que cada archivo `.md` tenga su equivalente en español e inglés
2. **Ningún archivo esté vacío** - Detecta archivos que solo contienen frontmatter sin contenido
3. **No haya marcadores de contenido pendiente** - Identifica archivos con marcadores como:
   - `[Content to be added]`
   - `[Contenido por agregar]`
   - `[Contenido a agregar]`
   - `[TODO]`
   - `[PENDIENTE]`
4. **Contenido mínimo suficiente** - Verifica que cada archivo tenga al menos 3 líneas de contenido real (excluyendo frontmatter y líneas vacías)

## Uso

Para ejecutar la validación:

```bash
cd drive-docs
python3 validate_documentation.py
```

El script generará un reporte detallado mostrando:
- Archivos que solo existen en un idioma
- Archivos vacíos o con contenido insuficiente
- Archivos con marcadores de contenido pendiente
- Resumen de problemas encontrados

## Criterios de Validación

### Archivo Válido
Un archivo se considera válido si:
- Tiene al menos 3 líneas de contenido real (después del frontmatter)
- No contiene marcadores de contenido pendiente
- Existe en ambos idiomas (es y en)

### Archivo Inválido
Un archivo se marca como inválido si:
- Está completamente vacío
- Solo tiene frontmatter sin contenido
- Tiene menos de 3 líneas de contenido
- Contiene marcadores de contenido pendiente
- Solo existe en un idioma

## Resultados Actuales

**Última validación:** Ejecutar `python3 validate_documentation.py` para ver el estado actual.

### Problemas Comunes Encontrados

1. **Archivos índice con poco contenido** - Algunos `_index.md` pueden tener contenido mínimo pero válido
2. **Archivos con marcadores de contenido pendiente** - Varios archivos tienen `[Content to be added]` o `[Contenido por agregar]`
3. **Secciones en desarrollo** - Algunas secciones están marcadas como en construcción

## Integración en CI/CD

Este script puede integrarse en pipelines de CI/CD para:
- Validar automáticamente antes de hacer merge
- Generar reportes en cada pull request
- Asegurar que nuevas traducciones estén completas

Ejemplo de integración:

```yaml
# .github/workflows/validate-docs.yml
name: Validate Documentation
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: cd drive-docs && python3 validate_documentation.py
```

## Mantenimiento

- Ejecutar la validación regularmente durante el desarrollo
- Corregir problemas antes de hacer commit
- Actualizar este documento si se cambian los criterios de validación

