from fastapi.responses import Response
from fastapi import FastAPI
from fastapi import Request
import httpx

app = FastAPI()

# Локальный сервер (замени порт на тот, где работает сайт)
LOCAL_SERVER = "http://localhost:3000"

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"])
async def proxy(request: Request, path: str):
    """
    Прокси-запросы к локальному серверу.
    """
    url = f"{LOCAL_SERVER}/{path}"  # Полный путь к локальному серверу
    method = request.method  # Метод запроса (GET, POST и т.д.)
    headers = {key: value for key, value in request.headers.items() if key != "host"}
    body = await request.body()  # Получаем тело запроса

    # Асинхронный HTTP-запрос к локальному серверу
    async with httpx.AsyncClient() as client:
        response = await client.request(method, url, headers=headers, content=body)

    # Возвращаем ответ удалённому клиенту
    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="http://192.168.0.2", port=8080)  # Заменить порт, если нужно