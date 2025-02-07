import os
import json
from websocket import WebSocketApp



class WebSocketHandler:
    def __init__(self, url):
        self.ws = WebSocketApp(
            url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        self.current_path = None
        self.history = []

    def on_open(self, ws):
        print("✅ Соединение установлено. Ожидание команды...")

    def on_message(self, ws, message):
        print(f"📩 Получено сообщение: {message}")
        try:
            command = json.loads(message)
            action = command.get("command")
            if action == "list_drives":
                self.list_drives(ws)
            elif action == "list_directory":
                path = command.get("path", self.current_path or "/")
                self.list_directory(ws, path)
            elif action == "navigate":
                path = command.get("path")
                print(path)
                self.navigate(ws, path)
            elif action == "exit":
                print("👋 Завершение программы по команде.")
                ws.close()
            else:
                print("⚠ Неизвестная команда.")
        except json.JSONDecodeError:
            print("⚠ Ошибка: Неверный формат сообщения.")

    def on_error(self, ws, error):
        print(f"⚠ Ошибка WebSocket: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("❌ Соединение закрыто.")

    def list_drives(self, ws):
        """Отправляет список доступных дисков"""
        import platform
        if platform.system() == "Windows":
            import string
            from ctypes import windll
        
            bitmask = windll.kernel32.GetLogicalDrives()
        
            if bitmask == 0:
                print("⚠ Ошибка: функция GetLogicalDrives() вернула 0.")
                return []
        
            drives = []
            for letter in string.ascii_uppercase:
                if bitmask & 1: 
                    drives.append(f"{letter}:\\")
                bitmask >>= 1  
            
        else:
            return ["/"]  
        print(f"📂 Диски: {drives}")
        response = {"action": "list_drives", "data": drives}  
        ws.send(json.dumps(response)) 
         

    def list_directory(self, ws, path):
        """Отправляет содержимое директории"""
        try:
            contents = os.listdir(path)
            print(f"\n📂 Текущая папка: {path}")
            directory_data = []

            for index, item in enumerate(contents):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    directory_data.append({"index": index, "type": "folder", "name": item})
                    print(f"  [{index}] 📁 {item}/")
                else:
                    directory_data.append({"index": index, "type": "file", "name": item})
                    print(f"  [{index}] 📄 {item}")


            print(f"📂 Содержимое папки {path}: {directory_data}")
            self.current_path = path
            response = {"action": "list_directory", "path": path, "data": directory_data}
            ws.send(json.dumps(response))
        except PermissionError:
            print("⛔ Нет доступа к папке.")
            response = {"action": "error", "message": "Нет доступа к папке"}
            ws.send(json.dumps(response))
        except FileNotFoundError:
            print("❌ Папка не найдена.")
            response = {"action": "error", "message": "Папка не найдена"}
            ws.send(json.dumps(response))

    def navigate(self, ws, path):
        """Навигация по папкам"""
        if path == "..":
            if self.history:
                self.current_path = self.history.pop()
            else:
                print("⚠ Уже находитесь на верхнем уровне.")
                response = {"action": "error", "message": "Вы уже находитесь на верхнем уровне."}
                ws.send(json.dumps(response))
                return
        else:
            self.history.append(self.current_path)
            self.current_path = path

        print(f"📂 Переход в папку: {self.current_path}")
        self.list_directory(ws, self.current_path)

    def run(self):
        self.ws.run_forever()



if __name__ == "__main__":
    ws_handler = WebSocketHandler("ws://192.168.0.108:8000/ws/listen/files_pc/123")
    ws_handler.run()
