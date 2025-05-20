@echo off
REM Activa tu venv (ajusta la ruta si lo necesitas)
call E:\Local_Chat\venv\Scripts\activate

REM Ejecuta el proxy que lanza el server-filesystem en stdio (NO pongas flags extra)
mcp-proxy stdio2sse --port 3333 -- npx -y @modelcontextprotocol/server-filesystem D:\PERSONAL\YURI\X-DI

REM Deja la ventana abierta al terminar
pause
