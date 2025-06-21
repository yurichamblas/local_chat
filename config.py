# config.py

# Dirección del modelo Ollama (Qwen3:8b)
OLLAMA_MODEL = "qwen3:8b"
OLLAMA_URL = "http://localhost:11434"

# Dirección del servidor MCP filesystem
MCP_URL = "http://localhost:3333"

# Carpeta raíz expuesta.
# Modifica esta ruta según tus necesidades. Por defecto se usa el
# directorio personal del usuario actual.
from pathlib import Path
BASE_PATH = str(Path.home())

# Otros parámetros opcionales:
LANGUAGE = "es"  # "es" para español, puedes cambiar si usas otro idioma

# Parámetros de logging o debug
VERBOSE = True
