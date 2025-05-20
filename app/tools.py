# app/tools.py

import requests
from config import MCP_URL

### Funciones base que llaman al MCP server ###

def list_directory(path):
    """Lista archivos y carpetas en un directorio usando el servidor MCP."""
    url = f"{MCP_URL}/filesystem/list"
    params = {"path": path}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def read_file(path, max_size=100_000):
    """Lee el contenido de un archivo de texto usando MCP."""
    url = f"{MCP_URL}/filesystem/read"
    params = {"path": path, "max_size": max_size}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        return {"error": str(e)}

def search_files(pattern, root=None, max_results=100):
    """Busca archivos por patrón de nombre usando MCP."""
    url = f"{MCP_URL}/filesystem/search"
    params = {"pattern": pattern, "max_results": max_results}
    if root:
        params["root"] = root
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

### Wrappers para LangChain Tools ###

from langchain.tools import Tool

list_directory_tool = Tool(
    name="list_directory",
    func=lambda path: str(list_directory(path)),
    description=(
        "Lista todos los archivos y carpetas dentro de un directorio especificado por el usuario. "
        "Parámetro: path (ejemplo: 'D:\PERSONAL\YURI\X-DI'). Devuelve lista de archivos y carpetas."
    ),
    args_schema=None  # Puede mejorarse con pydantic para mayor control de parámetros
)

read_file_tool = Tool(
    name="read_file",
    func=lambda path: str(read_file(path)),
    description=(
        "Lee el contenido de un archivo de texto dado el path completo. "
        "Parámetro: path (ejemplo: 'D:\PERSONAL\YURI\X-DI/info.txt'). Devuelve el contenido del archivo (si es texto)."
    ),
    args_schema=None
)

search_files_tool = Tool(
    name="search_files",
    func=lambda pattern: str(search_files(pattern)),
    description=(
        "Busca archivos por patrón de nombre dentro de la carpeta base y subcarpetas. "
        "Parámetro: pattern (ejemplo: '*.pdf' o 'memoria*'). Devuelve lista de rutas encontradas."
    ),
    args_schema=None
)

### Lista para pasar al agente LangChain ###

TOOLS_LIST = [list_directory_tool, read_file_tool, search_files_tool]
