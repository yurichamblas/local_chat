# chainlit_app.py

import chainlit as cl
from app.agent import agent

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content="👋 ¡Bienvenido! Soy tu asistente IA local. Puedes preguntarme sobre archivos o carpetas de tu directorio compartido. "
                "Por ejemplo: 'Lista los archivos en E:/proyectos/2024' o 'Ábreme el archivo memoria.txt'."
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    prompt = message.content
    # LangChain agents NO son asíncronos, así que usamos run() y no await/acall.
    try:
        response = agent.run(prompt)
        await cl.Message(content=str(response)).send()
    except Exception as e:
        await cl.Message(content=f"⚠️ Error: {e}").send()
