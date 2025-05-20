# agent.py

from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Pattern, Optional
import re
import json

from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_ollama import OllamaLLM as Ollama
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from tools_local import (
    resolve_path,
    list_directory,
    read_file,
    read_pdf,
    read_docx,
    read_excel,
    search_in_files,
)


def get_agent():
    # 1. LLM local
    llm = Ollama(model="qwen3:8b")

    # 2. Cadena de resumen de fragmentos de texto
    summarization_prompt = PromptTemplate(
        input_variables=["text"],
        template=(
            "Por favor, hazme un resumen breve de este contenido:\n\n"
            "{text}\n\nResumen:"
        ),
    )
    summarize_chain = LLMChain(llm=llm, prompt=summarization_prompt)

    # 3a. Resumen de un único archivo
    def summarize_file(path: str) -> str:
        p = resolve_path(path)
        ext = p.suffix.lower()
        if ext == ".pdf":
            content = read_pdf(path)
        elif ext in {".docx", ".doc"}:
            content = read_docx(path)
        elif ext in {".xlsx", ".xls"}:
            rows = read_excel(path)
            # rows es lista de dicts
            content = "\n".join(str(r) for r in rows)
        elif ext in {".txt", ".md", ".py", ".json"}:
            content = read_file(path)
        else:
            return f"⚠️ No sé cómo resumir archivos con extensión {ext}"

        # Llamada con .invoke para compatibilidad
        return summarize_chain.invoke({"text": content})

    # 3b. Resumen de un directorio completo
    def summarize_directory(
        path: str,
        allowed_exts: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
        max_workers: int = 4,
    ) -> Dict[str, str]:
        if allowed_exts is None:
            allowed_exts = [
                ".txt", ".md", ".py", ".json", ".pdf", ".docx", ".xlsx", ".xls"
            ]
        if exclude_patterns is None:
            exclude_patterns = [r"^~\$", r"\.bak$"]

        base_dir = resolve_path(path)
        if not base_dir.exists():
            raise FileNotFoundError(f"La carpeta '{base_dir}' no existe.")

        regexes = [re.compile(p) for p in exclude_patterns]
        files = [
            f for f in base_dir.rglob("*")
            if f.is_file()
            and f.suffix.lower() in allowed_exts
            and not any(rx.search(f.name) for rx in regexes)
        ]

        if not files:
            return {str(base_dir): "No hay archivos compatibles."}

        summaries: Dict[str, str] = {}
        def _worker(f: Path):
            rel = str(f.relative_to(base_dir))
            try:
                return rel, summarize_file(str(f))
            except Exception as e:
                return rel, f"Error al resumir '{rel}': {e}"

        with ThreadPoolExecutor(max_workers=max_workers) as exec:
            futures = [exec.submit(_worker, f) for f in files]
            for fut in as_completed(futures):
                name, res = fut.result()
                summaries[name] = res

        return summaries

    # 3c. Wrappers TEXTUALES (single-input)
    def list_directory_tool(input_str: str) -> str:
        path = input_str.strip()
        try:
            items = list_directory(path)
            if isinstance(items, str):
                # vino un mensaje de error
                return items
            if not items:
                return f"La carpeta '{path}' está vacía."
            return f"La carpeta '{path}' contiene:\n- " + "\n- ".join(items)
        except Exception as e:
            return f"❌ Error listando '{path}': {e}"

    def read_file_tool(input_str: str) -> str:
        path = input_str.strip()
        return read_file(path)

    def read_pdf_tool(input_str: str) -> str:
        path = input_str.strip()
        return read_pdf(path)

    def read_docx_tool(input_str: str) -> str:
        path = input_str.strip()
        return read_docx(path)

    def read_excel_tool(input_str: str) -> str:
        path = input_str.strip()
        try:
            rows = read_excel(path)
            if isinstance(rows, str):
                return rows  # mensaje de error
            # formatear en texto
            lines = [", ".join(f"{k}={v}" for k, v in row.items()) for row in rows]
            return f"Contenido de '{path}' (primeras filas):\n" + "\n".join(lines[:5])
        except Exception as e:
            return f"❌ Error leyendo Excel '{path}': {e}"

    def search_in_files_tool(input_str: str) -> str:
        raw = input_str.strip()
        # esperamos JSON o "dir||query"
        try:
            params = json.loads(raw)
            directory = params["directory"]
            query = params["query"]
        except Exception:
            if "||" in raw:
                directory, query = raw.split("||", 1)
            else:
                return "Formato inválido. Usa JSON con {\"directory\":\"...\",\"query\":\"...\"} o 'dir||query'."
        res = search_in_files(directory.strip(), query.strip())
        if isinstance(res, str):
            return res  # mensaje de error
        if not res:
            return f"No se encontró '{query}' en {directory}."
        return f"Se encontraron {len(res)} coincidencias:\n- " + "\n- ".join(res)

    def summarize_directory_tool(input_str: str) -> str:
        raw = input_str.strip()
        try:
            params = json.loads(raw)
            path = params["path"]
            exts = params.get("allowed_exts")
            pats = params.get("exclude_patterns")
        except Exception:
            path = raw
            exts = None
            pats = None

        try:
            result = summarize_directory(path, exts, pats)
            # si viene un dict, lo volcamos a texto
            if isinstance(result, dict):
                lines = [f"**{f}:** {s}" for f, s in result.items()]
                header = f"🗂 Resumen de '{path}':"
                return header + "\n" + "\n\n".join(lines)
            return str(result)
        except Exception as e:
            return f"❌ Error en Summarize Directory: {e}"

    # 4. Lista de herramientas
    tools = [
        Tool("List Directory", list_directory_tool, "Lista archivos en un directorio."),
        Tool("Read File", read_file_tool, "Muestra contenido de un archivo de texto."),
        Tool("Read PDF", read_pdf_tool, "Extrae texto de un PDF."),
        Tool("Read DOCX", read_docx_tool, "Extrae texto de un DOCX."),
        Tool("Read Excel", read_excel_tool, "Muestra primeras filas de un Excel."),
        Tool("Search in Files", search_in_files_tool, "Busca texto en archivos de un directorio."),
        Tool("Summarize File", summarize_file, "Resume un único archivo."),
        Tool("Summarize Directory", summarize_directory_tool, "Resume todos los archivos de una carpeta."),
    ]

    # 5. Memoria
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # 6. Inicializar agente
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,
        memory=memory,
    )
