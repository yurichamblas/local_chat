# app/agent.py

from langchain.llms import Ollama
from langchain.agents import initialize_agent, AgentType
from config import OLLAMA_MODEL, OLLAMA_URL, VERBOSE
from .tools import TOOLS_LIST

def get_llm():
    """
    Devuelve la instancia del modelo Qwen3:8B corriendo en Ollama.
    """
    return Ollama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_URL,
        verbose=VERBOSE,
        temperature=0.1  # puedes ajustar según resultados
    )

def get_agent():
    """
    Inicializa y devuelve el agente de LangChain listo para conversar.
    """
    llm = get_llm()
    # Elegimos el agente "openai-functions" si tu modelo soporta function calling.
    # Si no, puedes probar con AgentType.ZERO_SHOT_REACT_DESCRIPTION.
    agent = initialize_agent(
        tools=TOOLS_LIST,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # usa el agente react clásico
        verbose=VERBOSE
    )
    return agent

# Si quieres exponer como variable global para importar:
agent = get_agent()
