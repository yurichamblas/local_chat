# 🧠 Local Chat con Qwen3 + MCP + Chainlit

**Local Chat** es un asistente conversacional basado en LLMs que funciona completamente en local, capaz de listar, leer, buscar y resumir archivos desde tu sistema de archivos, usando un modelo de lenguaje como `Qwen3:8b` (Ollama) y el servidor de archivos `MCP`.

## ✨ Funcionalidades principales

- 📂 **Listar directorios** locales accesibles.
- 📄 **Leer archivos** de texto (`.txt`, `.md`, `.json`, `.py`), PDF, Word (`.docx`), Excel (`.xlsx`, `.xls`).
- 🔍 **Buscar texto** dentro de archivos en carpetas.
- 🧾 **Resumir archivos individuales**.
- 🗂 **Resumir automáticamente todos los archivos compatibles** en una carpeta.
- 💬 **Interfaz amigable** usando [Chainlit](https://docs.chainlit.io/).

## 🚀 Cómo usar

### 1. Instala dependencias
```bash
pip install -r requirements.txt
````

### 2. Activa tu entorno virtual (opcional pero recomendado)

```bash
venv\Scripts\activate    # Windows
source venv/bin/activate # macOS/Linux
```

### 3. Asegúrate que Ollama esté corriendo con el modelo `Qwen3:8b`

```bash
ollama run qwen3:8b
```

### 4. Lanza el servidor de archivos MCP en la ruta deseada

```bash
npx @modelcontextprotocol/server-filesystem D:/PERSONAL/YURI/X-DI
```

### 5. Ejecuta la app Chainlit

```bash
chainlit run chainlit_app.py --port 8000
```

> Puedes editar la ruta base y configuración en `config.py`.

## 📁 Carpeta base usada

Por defecto, Local Chat accede a:

```
D:/PERSONAL/YURI/X-DI
```

## 🧠 Modelo LLM usado

El modelo local utilizado es:

* `Qwen3:8b` (ejecutado vía [Ollama](https://ollama.com))

## 🧰 Tecnologías

* [Chainlit](https://docs.chainlit.io/) — interfaz de chat local.
* [LangChain](https://www.langchain.com/) — agente y herramientas.
* [Ollama](https://ollama.com) — ejecución local de LLMs.
* [Model Context Protocol](https://modelcontextprotocol.io) — acceso a archivos locales.
* Python: `pdfplumber`, `python-docx`, `pandas`, `openpyxl`.

---

¡Ya estás listo para usar tu propio copiloto IA local! 🤖
