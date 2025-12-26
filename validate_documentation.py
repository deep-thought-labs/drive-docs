#!/usr/bin/env python3
"""
Script de validación de documentación bilingüe
Valida que todos los archivos tengan contenido completo en ambos idiomas (es/en)
"""

import os
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Set

# Configuración
CONTENT_DIR = Path(__file__).parent / "content"
LANGUAGES = ["es", "en"]
MIN_CONTENT_LINES = 3  # Mínimo de líneas de contenido (después del frontmatter)


def extract_frontmatter(content: str) -> Tuple[Dict, str]:
    """Extrae el frontmatter YAML y devuelve el contenido restante."""
    frontmatter = {}
    body = content
    
    # Buscar frontmatter delimitado por ---
    frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(frontmatter_pattern, content, re.DOTALL)
    
    if match:
        frontmatter_text = match.group(1)
        body = match.group(2)
        
        # Parsear frontmatter básico (solo buscamos title y weight)
        for line in frontmatter_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip().strip('"\'')
    
    return frontmatter, body


def count_content_lines(body: str) -> int:
    """Cuenta las líneas de contenido real (excluyendo líneas vacías y solo espacios)."""
    lines = [line.strip() for line in body.split('\n') if line.strip()]
    return len(lines)


def has_placeholder_content(body: str) -> bool:
    """Detecta marcadores de contenido pendiente."""
    placeholders = [
        r'\[Content to be added\]',
        r'\[Contenido por agregar\]',
        r'\[Contenido a agregar\]',
        r'\[TODO\]',
        r'\[PENDIENTE\]',
        r'Content to be added',
        r'Contenido por agregar',
        r'Contenido a agregar',
    ]
    
    body_lower = body.lower()
    for placeholder in placeholders:
        if re.search(placeholder, body_lower, re.IGNORECASE):
            return True
    return False


def is_file_empty(file_path: Path) -> Tuple[bool, int, str]:
    """
    Verifica si un archivo está vacío o tiene muy poco contenido.
    Retorna: (is_empty, content_lines, reason)
    """
    try:
        content = file_path.read_text(encoding='utf-8')
        
        if not content.strip():
            return True, 0, "Archivo completamente vacío"
        
        frontmatter, body = extract_frontmatter(content)
        content_lines = count_content_lines(body)
        
        # Verificar si tiene marcadores de contenido pendiente
        if has_placeholder_content(body):
            return True, content_lines, f"Contiene marcadores de contenido pendiente ({content_lines} líneas)"
        
        if content_lines < MIN_CONTENT_LINES:
            return True, content_lines, f"Solo tiene {content_lines} líneas de contenido (mínimo: {MIN_CONTENT_LINES})"
        
        return False, content_lines, ""
    
    except Exception as e:
        return True, 0, f"Error al leer archivo: {str(e)}"


def find_markdown_files(base_dir: Path, lang: str) -> Set[Path]:
    """Encuentra todos los archivos .md en un directorio de idioma."""
    lang_dir = base_dir / lang
    if not lang_dir.exists():
        return set()
    
    md_files = set()
    for md_file in lang_dir.rglob("*.md"):
        # Obtener ruta relativa desde el directorio de idioma
        rel_path = md_file.relative_to(lang_dir)
        md_files.add(rel_path)
    
    return md_files


def get_file_path(base_dir: Path, lang: str, rel_path: Path) -> Path:
    """Obtiene la ruta completa de un archivo."""
    return base_dir / lang / rel_path


def validate_documentation():
    """Valida la documentación bilingüe."""
    
    print("=" * 80)
    print("VALIDACIÓN DE DOCUMENTACIÓN BILINGÜE")
    print("=" * 80)
    print()
    
    # Encontrar todos los archivos en ambos idiomas
    es_files = find_markdown_files(CONTENT_DIR, "es")
    en_files = find_markdown_files(CONTENT_DIR, "en")
    
    print(f"Archivos encontrados:")
    print(f"  - Español (es): {len(es_files)} archivos")
    print(f"  - Inglés (en):  {len(en_files)} archivos")
    print()
    
    # Encontrar archivos únicos por idioma
    only_es = es_files - en_files
    only_en = en_files - es_files
    common_files = es_files & en_files
    
    # Validar archivos comunes
    empty_files = defaultdict(list)
    issues = []
    
    print("=" * 80)
    print("VALIDANDO ARCHIVOS COMUNES")
    print("=" * 80)
    print()
    
    for rel_path in sorted(common_files):
        es_path = get_file_path(CONTENT_DIR, "es", rel_path)
        en_path = get_file_path(CONTENT_DIR, "en", rel_path)
        
        es_empty, es_lines, es_reason = is_file_empty(es_path)
        en_empty, en_lines, en_reason = is_file_empty(en_path)
        
        if es_empty or en_empty:
            issue = {
                "file": str(rel_path),
                "es": {"empty": es_empty, "lines": es_lines, "reason": es_reason},
                "en": {"empty": en_empty, "lines": en_lines, "reason": en_reason}
            }
            issues.append(issue)
            
            if es_empty:
                empty_files["es"].append((rel_path, es_reason, es_lines))
            if en_empty:
                empty_files["en"].append((rel_path, en_reason, en_lines))
    
    # Reporte de archivos faltantes
    print("=" * 80)
    print("ARCHIVOS FALTANTES")
    print("=" * 80)
    print()
    
    if only_es:
        print(f"❌ Archivos solo en ESPAÑOL (faltan en inglés): {len(only_es)}")
        for rel_path in sorted(only_es):
            print(f"   - {rel_path}")
        print()
    
    if only_en:
        print(f"❌ Archivos solo en INGLÉS (faltan en español): {len(only_en)}")
        for rel_path in sorted(only_en):
            print(f"   - {rel_path}")
        print()
    
    if not only_es and not only_en:
        print("✅ Todos los archivos existen en ambos idiomas")
        print()
    
    # Reporte de archivos vacíos o incompletos
    print("=" * 80)
    print("ARCHIVOS VACÍOS O INCOMPLETOS")
    print("=" * 80)
    print()
    
    if not issues:
        print("✅ Todos los archivos comunes tienen contenido suficiente")
        print()
    else:
        print(f"❌ Se encontraron {len(issues)} archivos con problemas:\n")
        
        for issue in issues:
            print(f"📄 {issue['file']}")
            
            if issue['es']['empty']:
                print(f"   ❌ ESPAÑOL: {issue['es']['reason']} ({issue['es']['lines']} líneas)")
            else:
                print(f"   ✅ ESPAÑOL: OK ({issue['es']['lines']} líneas)")
            
            if issue['en']['empty']:
                print(f"   ❌ INGLÉS:  {issue['en']['reason']} ({issue['en']['lines']} líneas)")
            else:
                print(f"   ✅ INGLÉS:  OK ({issue['en']['lines']} líneas)")
            print()
    
    # Resumen final
    print("=" * 80)
    print("RESUMEN")
    print("=" * 80)
    print()
    
    total_issues = len(only_es) + len(only_en) + len(issues)
    
    print(f"Archivos solo en español:     {len(only_es)}")
    print(f"Archivos solo en inglés:      {len(only_en)}")
    print(f"Archivos vacíos/incompletos:  {len(issues)}")
    print(f"TOTAL DE PROBLEMAS:           {total_issues}")
    print()
    
    if total_issues == 0:
        print("✅ ¡Toda la documentación está completa y sincronizada!")
        return 0
    else:
        print("⚠️  Se encontraron problemas que requieren atención.")
        return 1


if __name__ == "__main__":
    exit_code = validate_documentation()
    exit(exit_code)

