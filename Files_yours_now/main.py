import os
import aiohttp
import asyncio

FILE = "http://192.168.0.108:5050/file"
DISK = "http://192.168.0.108:5050/disk"
DIRS = "http://192.168.0.108:5050/dirs"
ZAPROS = "http://192.168.0.108:5050/zapr"


async def send_post_request(data, when):
    async with aiohttp.ClientSession() as session:
        try:
            url = {"file": FILE, "disk": DISK, "dirs": DIRS}.get(when)
            if url:
                async with session.post(url, json=data) as response:
                    if response.status == 200:
                        print(f"✅ Успешно отправлено: {await response.json()}")
                    else:
                        print(f"⚠ Ошибка отправки: {response.status}, {await response.text()}")
        except Exception as e:
            print(f"⚠ Ошибка при подключении: {e}")


async def get_command():
    while True:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(ZAPROS) as response:
                    if response.status == 200:
                        command = await response.text()
                        if command:  # Проверяем, что команда не пустая
                            return command.strip()
                        else:
                            print("⚠ Пустая команда. Повтор запроса...")
                    else:
                        print(f"⚠ Ошибка получения команды: {response.status}, {await response.text()}")
            except Exception as e:
                print(f"⚠ Ошибка при подключении: {e}")
        
        # Небольшая задержка перед повторной попыткой
        await asyncio.sleep(1)


async def list_directory(path):
    try:
        contents = os.listdir(path)
        print(f"\n📂 Текущая папка: {path}")
        print("Содержимое:")
        json_dirs = []
        for index, item in enumerate(contents):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                json_dirs.append({"index": index, "type": "folder", "name": item})
                print(f"  [{index}] 📁 {item}/")
            else:
                json_dirs.append({"index": index, "type": "file", "name": item})
                print(f"  [{index}] 📄 {item}")
        await send_post_request(json_dirs, 'dirs')  # Асинхронный вызов
        return contents
    except PermissionError:
        print("⛔ Нет доступа к этой папке!")
        return []
    except FileNotFoundError:
        print("❌ Папка не найдена!")
        return []


async def navigate(start_path):
    current_path = start_path
    history = []

    while True:
        contents = await list_directory(current_path)
        print("\nДоступные команды:")
        print("  [номер] - открыть папку или файл")
        print("  [..] - вернуться назад")
        print("  [exit] - выйти из программы")
        comm = '""'
        while comm == '""':
            comm = await get_command()
        print(comm)
        
        if comm:
            choice = comm.strip()
        else:
            print("⚠ Команда не получена.")
            continue

        if choice == '"exit"':
            print("👋 Выход из программы.")
            break
        elif choice == "..":
            if history:
                current_path = history.pop()
            else:
                print("⚠ Вы уже находитесь на верхнем уровне.")
        elif choice.isdigit():
            index = int(choice)
            if 0 <= index < len(contents):
                selected_item = contents[index]
                selected_path = os.path.join(current_path, selected_item)

                if os.path.isdir(selected_path):
                    history.append(current_path)
                    current_path = selected_path
                else:
                    print(f"\nОткрыт файл: {selected_item}")
                    try:
                        os.startfile(selected_path)
                    except Exception as e:
                        print(f"⚠ Не удалось открыть файл: {e}")
            else:
                print("⚠ Неверный номер.")
        else:
            print("⚠ Неизвестная команда.")


def get_drives():
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

        print("Диски найдены:", drives)
        return drives
    else:
        return ["/"]


async def main():
    print("📂 Список дисков для сканирования:")
    drives = get_drives()
    if not drives:
        print("⚠ Не удалось получить список дисков.")
        return

    await send_post_request({"disks": drives}, 'disk')

    for i, drive in enumerate(drives):
        print(f"[{i}] {drive}")

    start_drive = input("\nВыберите диск для начала (номер): ").strip()
    if start_drive.isdigit() and 0 <= int(start_drive) < len(drives):
        await navigate(drives[int(start_drive)])
    else:
        print("⚠ Неверный выбор.")


if __name__ == "__main__":
    asyncio.run(main())