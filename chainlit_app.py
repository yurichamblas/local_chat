# chainlit_app.py

import chainlit as cl
import asyncio
from agent import get_agent

# Inicializa el agente una sola vez
agent = get_agent()

@cl.on_message
async def main(message: cl.Message):
    user_input = message.content

    # Muestra un mensaje de "procesando..."
    await cl.Message(content="🤖 Estoy procesando tu solicitud...").send()

    try:
        # Usa .run() para obtener directamente el texto en lenguaje natural
        raw = await asyncio.to_thread(agent.run, user_input)
    except Exception as e:
        raw = f"❌ Ocurrió un error interno:\n{e}"

    # Envía la respuesta como texto plano (Chainlit aplicará saltos de línea y viñetas)
    await cl.Message(content=raw).send()
