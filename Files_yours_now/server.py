from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List, Dict
import json
import uvicorn
from pydantic import BaseModel

app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"🔌 Новый клиент подключен. Всего подключений: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"❌ Клиент отключился. Осталось подключений: {len(self.active_connections)}")

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()

commands_state: Dict[str, str] = {}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Обрабатывает подключение клиентов"""
    await manager.connect(websocket)
    try:
        while True:

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
        manager.disconnect(websocket)
class CommandRequest(BaseModel):
    command: str
    path: str
@app.post("/send-command")
async def send_command(request: CommandRequest):
    """Получение команды через тело запроса"""
    command = request.command
    path = request.path
    if not manager.active_connections:
        return {"error": "Нет подключенных клиентов"}
    try:
        await manager.broadcast(json.dumps({"action": "command", "command": command, "path": path}))
        return {"status": "Команда отправлена", "command": command, "path" : path}
    except Exception as e:
        return {"error": f"Не удалось отправить команду: {str(e)}"}

@app.get("/commands")
async def get_commands():
    """Возвращает состояние выполненных команд"""
    return commands_state

if __name__ == "__main__":
    uvicorn.run(app, host="192.168.0.108", port=8000)