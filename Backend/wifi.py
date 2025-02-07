import subprocess
def get_wifi():
    encoding = 'cp866'
    wifi = subprocess.check_output(f'netsh wlan show profiles', shell=True, text=True, encoding=encoding)
    return wifi

def get_wifi_password(ssid):
    try:
        encoding = 'cp866'

        password_data = subprocess.check_output(f'netsh wlan show profile name="{ssid}" key=clear', shell=True, text=True, encoding=encoding)
        for line in password_data.split("\n"):
            if "Содержимое ключа" in line:
                password = line.split(":")[1].strip()
                return f"Пароль от Wi-Fi '{ssid}': {password}"
        return f"Пароль для сети '{ssid}' не найден."
    except Exception as e:
        return f"Ошибка: {e}"
print(get_wifi())
ssid = input('введите название wifi сети:')  # Замени на имя своей сети
print(get_wifi_password(ssid))