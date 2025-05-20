# Local Chat con Qwen3 y MCP

1. Instala dependencias: `pip install -r requirements.txt`
2. Asegúrate que Ollama esté corriendo con Qwen3:8b (`ollama run qwen3:8b`)
3. Lanza el servidor MCP filesystem (`npx @modelcontextprotocol/server-filesystem E:/TU/DIRECTORIO`)
4. Ejecuta la app: `chainlit run chainlit_app.py`
