# tools_local.py

import os
from pathlib import Path
import re
import pdfplumber
import docx
import pandas as pd
import config  # usa BASE_PATH desde config.py

# Carpetas raíz permitidas
BASE_DIRS = [
    Path(config.BASE_PATH).resolve(),
    Path(r"E:/Local_Chat").resolve()
]

# ---------- utilidades internas ---------- #
def _is_within_base(path: Path) -> bool:
    """
    Comprueba que 'path' está dentro de alguna carpeta de BASE_DIRS.
    """
    try:
        path = path.resolve()
    except Exception:
        return False
    for base in BASE_DIRS:
        try:
            path.relative_to(base)
            return True
        except ValueError:
            continue
    return False


# ---------- API pública ---------- #
def resolve_path(path_str: str) -> Path:
    """
    Devuelve un Path absoluto y seguro dentro de BASE_DIRS.

    - Acepta rutas absolutas o relativas.
    - Lanza:
        * PermissionError si la ruta está fuera de las carpetas permitidas.
        * FileNotFoundError si la ruta no existe dentro de las permitidas.
    """
    cleaned = path_str.strip().strip('"').strip("'")
    p = Path(cleaned).expanduser()

    # 1. Ruta absoluta
    if p.is_absolute():
        if not _is_within_base(p):
            raise PermissionError(f"Ruta fuera de las carpetas permitidas: {p}")
        if not p.exists():
            raise FileNotFoundError(f"La ruta indicada no existe: {p}")
        return p

    # 2. Ruta relativa
    for base in BASE_DIRS:
        candidate = (base / p).resolve()
        if candidate.exists() and _is_within_base(candidate):
            return candidate

    raise FileNotFoundError(f"La ruta no se encontró o está fuera del alcance: {cleaned}")


def list_directory(path: str):
    try:
        dir_path = resolve_path(path)
        return [entry.name for entry in dir_path.iterdir()]
    except Exception as e:
        return f"❌ Error al listar '{path}': {e}"


def read_file(filepath: str, max_size: int = 200_000):
    try:
        file_path = resolve_path(filepath)
        size = file_path.stat().st_size
        if size > max_size:
            return (f"❌ Archivo muy grande: '{filepath}' "
                    f"({size} bytes, límite: {max_size})")
        return file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return f"❌ Error al leer '{filepath}': {e}"


def read_pdf(path: str):
    try:
        pdf_path = resolve_path(path)
        text_pages = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_pages.append(page_text)
        return "\n\n---\n\n".join(text_pages)
    except Exception as e:
        return f"❌ Error al leer PDF '{path}': {e}"


def read_docx(path: str):
    try:
        doc_path = resolve_path(path)
        doc = docx.Document(doc_path)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except Exception as e:
        return f"❌ Error al leer DOCX '{path}': {e}"


def read_excel(path: str, sheet_name=0):
    try:
        xlsx_path = resolve_path(path)
        df = pd.read_excel(xlsx_path, sheet_name=sheet_name)
        return df.to_dict(orient="records")
    except Exception as e:
        return f"❌ Error al leer Excel '{path}': {e}"


def search_in_files(directory: str, query: str, file_extensions=None):
    if file_extensions is None:
        file_extensions = ['.txt', '.md', '.py', '.json']

    results = []
    try:
        root_dir = resolve_path(directory)
        for file in root_dir.rglob('*'):
            if file.is_file() and file.suffix.lower() in file_extensions:
                try:
                    text = file.read_text(encoding="utf-8", errors="ignore")
                    if query.lower() in text.lower():
                        results.append(str(file))
                except Exception:
                    continue
        return results
    except Exception as e:
        return f"❌ Error buscando '{query}' en '{directory}': {e}"
