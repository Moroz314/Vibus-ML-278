import os

def list_directory(path):
    try:
        contents = os.listdir(path)
        print(f"\n📂 Текущая папка: {path}")
        print("Содержимое:")
        for index, item in enumerate(contents):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                print(f"  [{index}] 📁 {item}/")
            else:
                print(f"  [{index}] 📄 {item}")
        return contents
    except PermissionError:
        print("⛔ Нет доступа к этой папке!")
        return []
    except FileNotFoundError:
        print("❌ Папка не найдена!")
        return []

def navigate(start_path):
    current_path = start_path
    history = []

    while True:
        contents = list_directory(current_path)
        print("\nДоступные команды:")
        print("  [номер] - открыть папку или файл")
        print("  [..] - вернуться назад")
        print("  [exit] - выйти из программы")
        
        choice = input("\nВведите команду: ").strip()
        
        if choice == "exit":
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



print("📂 Список дисков для сканирования:")
drives = get_drives()
for i, drive in enumerate(drives):
    print(f"[{i}] {drive}")
if not drives:
    print("⚠ Не удалось получить список дисков.")
    exit()

start_drive = input("\nВыберите диск для начала (номер): ").strip()
if start_drive.isdigit() and 0 <= int(start_drive) < len(drives):
    navigate(drives[int(start_drive)])

else:
    print("⚠ Неверный выбор.")